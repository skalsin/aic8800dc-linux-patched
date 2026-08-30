"""
Test the auto-recovery watchdog service, syntax, and configuration.
"""
import os
import subprocess
import pytest


def test_watchdog_script_exists_and_executable():
    """Verify watchdog script is present and marked executable."""
    script = "/usr/local/bin/aic8800-watchdog.sh"
    assert os.path.isfile(script), f"{script} not found"
    assert os.access(script, os.X_OK), f"{script} is not executable"


def test_watchdog_script_syntax():
    """Verify watchdog script contains valid bash syntax."""
    script = "/usr/local/bin/aic8800-watchdog.sh"
    res = subprocess.run(["bash", "-n", script], capture_output=True, text=True)
    assert res.returncode == 0, f"Syntax error in {script}: {res.stderr}"


def test_watchdog_systemd_service_active():
    """Verify aic8800-watchdog.service is active and enabled."""
    res = subprocess.run(["systemctl", "is-active", "aic8800-watchdog.service"], capture_output=True, text=True)
    assert res.stdout.strip() == "active", f"aic8800-watchdog service is not active: {res.stdout.strip()}"


def test_dispatcher_txpower_script():
    """Verify NetworkManager dispatcher txpower script is set up safely."""
    dispatcher_script = "/etc/NetworkManager/dispatcher.d/99-wifi-txpower.sh"
    assert os.path.isfile(dispatcher_script), f"{dispatcher_script} is missing"
    assert os.access(dispatcher_script, os.X_OK), f"{dispatcher_script} is not executable"

    with open(dispatcher_script, "r") as f:
        content = f.read()

    # Ensure it limits txpower to 1400 mBm (14 dBm) and not excessive 2000 mBm
    assert "1400" in content, f"txpower script does not contain safe 1400 mBm limit:\n{content}"
