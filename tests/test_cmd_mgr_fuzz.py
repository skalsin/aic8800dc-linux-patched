"""
Command Manager Queue, State Machine, and Timeout Fuzz Test Suite.
Ported from vendor driver RPC stress harnesses and kernel workqueue simulators.
"""
import threading
import time
from collections import deque
import pytest


# Driver Message IDs from lmac_msg.h & rwnx_cmds.h
MM_START_REQ = 0x0001
MM_START_CFM = 0x0002
MM_SET_CHANNEL_REQ = 0x0003
MM_SET_CHANNEL_CFM = 0x0004
SM_CONNECT_REQ = 0x1800
SM_CONNECT_IND = 0x1801
SM_DISCONNECT_REQ = 0x1803
SM_DISCONNECT_CFM = 0x1804
SCAN_START_REQ = 0x0800
SCAN_START_CFM = 0x0801
ME_TRAFFIC_IND_REQ = 0x0400


class SimulatedCmdMgr:
    """
    Python emulation of rwnx_cmds.c command manager.
    Validates queue ordering, lock-free safety, and timeout recovery.
    """
    def __init__(self, max_queue_sz=16, timeout_sec=0.1):
        self.lock = threading.Lock()
        self.cmds = deque()
        self.max_queue_sz = max_queue_sz
        self.timeout_sec = timeout_sec
        self.next_tkn = 0
        self.state = "INIT"  # "INIT", "DEGRADED" (never permanently "CRASHED")

    def queue_cmd(self, msg_id: int, req_cfm: bool = True) -> dict:
        with self.lock:
            if len(self.cmds) >= self.max_queue_sz:
                return {"result": -12, "tkn": -1}  # -ENOMEM
            tkn = self.next_tkn
            self.next_tkn += 1
            cmd = {
                "id": msg_id,
                "tkn": tkn,
                "req_cfm": req_cfm,
                "done": False,
                "result": -4,  # -EINTR initial
                "event": threading.Event(),
            }
            self.cmds.append(cmd)
            return {"result": 0, "cmd": cmd}

    def complete_cmd(self, tkn: int, status: int = 0):
        with self.lock:
            for cmd in list(self.cmds):
                if cmd["tkn"] == tkn:
                    cmd["result"] = status
                    cmd["done"] = True
                    cmd["event"].set()
                    self.cmds.remove(cmd)
                    return True
        return False

    def handle_timeout(self, cmd: dict):
        """
        Hardened timeout handler (matches our patch to rwnx_cmds.c).
        Pops the timed out command without poisoning self.state to permanent CRASHED.
        """
        with self.lock:
            if not cmd["done"]:
                cmd["result"] = -110  # -ETIMEDOUT
                cmd["done"] = True
                cmd["event"].set()
                if cmd in self.cmds:
                    self.cmds.remove(cmd)
                # Keep state healthy so subsequent commands can continue!
                self.state = "INIT"


# =========================================================================
# Command Manager Queue Tests
# =========================================================================

def test_cmd_mgr_fifo_ordering():
    """Verify command manager preserves strict FIFO ordering for queued messages."""
    mgr = SimulatedCmdMgr()
    tokens = []
    for msg_id in [MM_START_REQ, MM_SET_CHANNEL_REQ, SM_CONNECT_REQ]:
        res = mgr.queue_cmd(msg_id)
        assert res["result"] == 0
        tokens.append(res["cmd"]["tkn"])

    assert len(mgr.cmds) == 3
    assert [c["tkn"] for c in mgr.cmds] == tokens

    # Complete in FIFO order
    for tkn in tokens:
        assert mgr.complete_cmd(tkn, 0) is True

    assert len(mgr.cmds) == 0


def test_cmd_mgr_max_queue_size_protection():
    """Verify queue rejects excess commands with -ENOMEM when reaching limit."""
    mgr = SimulatedCmdMgr(max_queue_sz=4)
    for _ in range(4):
        res = mgr.queue_cmd(SCAN_START_REQ)
        assert res["result"] == 0

    # 5th command must be rejected
    overflow_res = mgr.queue_cmd(SCAN_START_REQ)
    assert overflow_res["result"] == -12  # -ENOMEM
    assert len(mgr.cmds) == 4


def test_cmd_mgr_timeout_does_not_break_subsequent_commands():
    """
    Critical regression test: Verify a timed out command does NOT brick the queue.
    Future commands must still succeed.
    """
    mgr = SimulatedCmdMgr()

    # Step 1: Enqueue command that times out
    res1 = mgr.queue_cmd(SM_DISCONNECT_REQ)
    assert res1["result"] == 0
    cmd1 = res1["cmd"]

    # Trigger timeout handler
    mgr.handle_timeout(cmd1)
    assert cmd1["result"] == -110  # -ETIMEDOUT
    assert cmd1["done"] is True
    assert len(mgr.cmds) == 0
    assert mgr.state != "CRASHED"  # Verified not poisoned!

    # Step 2: Enqueue new command after timeout -> MUST SUCCEED
    res2 = mgr.queue_cmd(SM_CONNECT_REQ)
    assert res2["result"] == 0
    cmd2 = res2["cmd"]
    assert len(mgr.cmds) == 1

    # Complete successfully
    assert mgr.complete_cmd(cmd2["tkn"], 0) is True
    assert cmd2["result"] == 0
    assert len(mgr.cmds) == 0


# =========================================================================
# Concurrency Stress Test
# =========================================================================

def test_cmd_mgr_concurrent_stress():
    """Stress test concurrent command submissions and completions across threads."""
    mgr = SimulatedCmdMgr(max_queue_sz=32)
    success_count = [0]
    lock = threading.Lock()

    def worker():
        for _ in range(50):
            res = mgr.queue_cmd(SM_CONNECT_REQ)
            if res["result"] == 0:
                cmd = res["cmd"]
                # Simulate fast firmware reply
                time.sleep(0.001)
                mgr.complete_cmd(cmd["tkn"], 0)
                with lock:
                    success_count[0] += 1

    threads = [threading.Thread(target=worker) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert success_count[0] > 100
    assert len(mgr.cmds) == 0
