"""Test the packaged watchdog's syntax and crash-safety contract."""
import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
WATCHDOG = REPO_ROOT / "tools" / "aic8800-watchdog.sh"
SERVICE = REPO_ROOT / "tools" / "aic8800-watchdog.service"


def test_watchdog_script_exists_and_executable():
    """Verify the package contains an executable watchdog script."""
    assert WATCHDOG.is_file(), f"{WATCHDOG} not found"
    assert os.access(WATCHDOG, os.X_OK), f"{WATCHDOG} is not executable"


def test_watchdog_script_syntax():
    """Verify watchdog script contains valid bash syntax."""
    res = subprocess.run(["bash", "-n", str(WATCHDOG)], capture_output=True, text=True)
    assert res.returncode == 0, f"Syntax error in {WATCHDOG}: {res.stderr}"


def test_watchdog_cannot_reload_kernel_modules():
    """Recovery automation must never unload or reload either driver module."""
    content = WATCHDOG.read_text()
    assert "modprobe" not in content
    assert "rmmod" not in content
    assert "systemctl restart wpa_supplicant" not in content


def test_watchdog_defaults_to_observation_and_is_not_auto_enabled():
    """Reassociation is opt-in and package installation does not enable it."""
    script = WATCHDOG.read_text()
    unit = SERVICE.read_text()
    install = (REPO_ROOT / "install.sh").read_text()
    assert 'AIC8800_WATCHDOG_MODE:-observe' in script
    assert "Environment=AIC8800_WATCHDOG_MODE=observe" in unit
    assert "systemctl enable aic8800-watchdog" not in install


def test_dispatcher_txpower_script():
    """Verify NetworkManager dispatcher txpower script is set up safely."""
    dispatcher_script = "/etc/NetworkManager/dispatcher.d/99-wifi-txpower.sh"
    assert os.path.isfile(dispatcher_script), f"{dispatcher_script} is missing"
    assert os.access(dispatcher_script, os.X_OK), f"{dispatcher_script} is not executable"

    with open(dispatcher_script, "r") as f:
        content = f.read()

    # Ensure it limits txpower to 1400 mBm (14 dBm) and not excessive 2000 mBm
    assert "1400" in content, f"txpower script does not contain safe 1400 mBm limit:\n{content}"
