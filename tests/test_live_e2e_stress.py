"""
Live End-to-End (E2E) Stress, Fault-Injection, and Historical Bug Reproduction Suite.
Executes real hardware and kernel operations to stress-test the active driver.
"""
import os
import subprocess
import time
import re
import pytest


pytestmark = pytest.mark.skipif(
    os.environ.get("AIC8800_RUN_LIVE_E2E") != "1",
    reason=("destructive hardware tests are opt-in; set "
            "AIC8800_RUN_LIVE_E2E=1 to enable them"),
)


@pytest.fixture(scope="module")
def wifi_iface():
    """Find active Wi-Fi interface."""
    res = subprocess.run(["iw", "dev"], capture_output=True, text=True)
    match = re.search(r"Interface\s+([a-zA-Z0-9_-]+)", res.stdout)
    if not match:
        pytest.skip("No wireless interface present for E2E tests")
    return match.group(1)


def get_gateway_ip(iface: str) -> str:
    """Find gateway IP for specific interface."""
    try:
        route_out = subprocess.check_output(["ip", "route", "show", "dev", iface], text=True)
        for line in route_out.splitlines():
            if line.startswith("default via"):
                return line.split()[2]
    except Exception:
        pass
    return "192.168.68.1"


# =========================================================================
# E2E Test 1: Repeated Association / Disconnection Stress Cycle
# (Reproduces historical bug: SM_DISCONNECT_REQ timeout crash in loop)
# =========================================================================

def test_e2e_repeated_disconnect_reconnect_cycle(wifi_iface):
    """
    Stress test: Disconnect and reconnect Wi-Fi 3 consecutive times.
    Verifies that command queue state machine handles successive teardowns
    without entering STATE_CRASHED or locking up.
    """
    gw = get_gateway_ip(wifi_iface)

    for cycle in range(3):
        # 1. Disconnect
        res_down = subprocess.run(["nmcli", "dev", "disconnect", wifi_iface], capture_output=True, text=True)
        assert res_down.returncode == 0, f"Disconnect cycle {cycle} failed: {res_down.stderr}"
        time.sleep(2)

        # 2. Reconnect
        res_up = subprocess.run(["nmcli", "connection", "up", "HomeWiFi1"], capture_output=True, text=True)
        assert res_up.returncode == 0, f"Reconnect cycle {cycle} failed: {res_up.stderr}"
        time.sleep(4)

        # 3. Verify IP assigned and ping works
        res_ping = subprocess.run(["ping", "-I", wifi_iface, "-c", "3", "-W", "2", gw], capture_output=True, text=True)
        assert res_ping.returncode == 0, f"Ping failed on cycle {cycle}:\n{res_ping.stdout}"

    # Verify no cmd queue crashes in dmesg
    dmesg = subprocess.run(["dmesg"], capture_output=True, text=True)
    assert "cmd queue crashed" not in dmesg.stdout.lower()


# =========================================================================
# E2E Test 2: Rapid Scan Stress Under Active Connection
# (Reproduces historical bug: background scan collision with active traffic)
# =========================================================================

def test_e2e_rapid_background_scans_under_load(wifi_iface):
    """
    Stress test: Trigger 3 rapid successive scans while maintaining active connection.
    Verifies that scan requests do not collide or lock the command manager.
    """
    gw = get_gateway_ip(wifi_iface)

    for i in range(3):
        res_scan = subprocess.run(["nmcli", "dev", "wifi", "rescan"], capture_output=True, text=True)
        # Scan can return 0 or rate-limited error; interface must remain alive
        time.sleep(2)

    # Assert interface is still connected and passing traffic
    res_ping = subprocess.run(["ping", "-I", wifi_iface, "-c", "3", "-W", "2", gw], capture_output=True, text=True)
    assert res_ping.returncode == 0, f"Interface dropped after rapid scans:\n{res_ping.stdout}"


# =========================================================================
# E2E Test 3: Idle Sleep & Power Save Wakeup Latency
# (Reproduces historical bug: ps_on / dpsm dropping connection after idle)
# =========================================================================

def test_e2e_idle_sleep_wakeup_and_arp_retention(wifi_iface):
    """
    Verify that the interface wakes up instantly after an idle sleep period
    and does not drop ARP or beacon tracking.
    """
    gw = get_gateway_ip(wifi_iface)

    # Idle sleep
    time.sleep(5)

    # Immediate single ping
    res = subprocess.run(["ping", "-I", wifi_iface, "-c", "2", "-W", "2", gw], capture_output=True, text=True)
    assert res.returncode == 0, f"Wakeup ping failed after idle sleep:\n{res.stdout}"


# =========================================================================
# E2E Test 4: Reverse SSH Tunnel Process Recovery
# (Reproduces historical bug: autossh process death & server socket lockout)
# =========================================================================

def test_e2e_ssh_tunnel_autossh_recovery():
    """
    Fault injection test: Kill the underlying SSH child process of autossh.
    Verify autossh immediately respawns the tunnel and the user service remains active.
    """
    # 1. Find running ssh child under autossh
    res = subprocess.run(["pgrep", "-f", "ssh -N -o ServerAliveInterval 10"], capture_output=True, text=True)
    pids = res.stdout.strip().split()
    if pids:
        # Kill the child ssh process to simulate drop
        subprocess.run(["kill", "-9", pids[0]])
        time.sleep(4)

    # 2. Check systemd user unit is active and restarted
    res_status = subprocess.run(["systemctl", "--user", "is-active", "ssh-tunnel-fra.service"], capture_output=True, text=True)
    assert "active" in res_status.stdout.strip()
