"""
Regression tests verifying critical driver source invariants that prevent crash loops:
1. Command timeout must be >= 10000ms.
2. Command manager must not permanently enter STATE_CRASHED on command timeouts.
3. Queue wait loops in msg_tx must be bounded to prevent softirq hangs.
"""
import re
from pathlib import Path


def test_command_timeout_invariant():
    """Verify RWNX_80211_CMD_TIMEOUT_MS default is at least 10000ms."""
    repo_root = Path(__file__).parent.parent
    hdr = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_cmds.h"
    assert hdr.exists(), f"{hdr} not found"

    content = hdr.read_text()
    matches = re.findall(r"#define\s+RWNX_80211_CMD_TIMEOUT_MS\s+\(?([^\)\n]+)\)?", content)
    assert len(matches) > 0, "Could not find RWNX_80211_CMD_TIMEOUT_MS definition"
    # Check the default #else branch (the last definition)
    last_def = matches[-1].strip()
    timeout_val = eval(last_def, {"__builtins__": None}, {})
    assert timeout_val >= 10000, f"Timeout too small ({timeout_val}ms < 10000ms), can cause false crash loops"


def test_cmd_mgr_timeout_does_not_poison_state():
    """Verify timeout handlers in rwnx_cmds.c do not permanently set STATE_CRASHED."""
    repo_root = Path(__file__).parent.parent
    src = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_cmds.c"
    assert src.exists(), f"{src} not found"

    content = src.read_text()
    # Check wait_for_completion_killable_timeout block in cmd_mgr_queue
    # It must not contain cmd_mgr->state = RWNX_CMD_MGR_STATE_CRASHED
    lines = content.splitlines()
    in_timeout_block = False
    for i, line in enumerate(lines):
        if "wait_for_completion_killable_timeout" in line:
            in_timeout_block = True
        if in_timeout_block:
            if "RWNX_CMD_MGR_STATE_CRASHED" in line and not line.strip().startswith("//"):
                assert False, f"Found STATE_CRASHED in timeout block at line {i+1}: {line}"
            if "rwnx_cmd_free" in line or "spin_unlock_bh" in line:
                in_timeout_block = False


def test_msg_tx_wait_loop_is_bounded():
    """Verify rwnx_msg_tx.c cmdqueue drain loop has a break counter."""
    repo_root = Path(__file__).parent.parent
    src = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_msg_tx.c"
    assert src.exists(), f"{src} not found"

    content = src.read_text()
    assert "wait_count >" in content, "Missing bounded iteration counter in rwnx_msg_tx.c cmdqueue wait loop"
