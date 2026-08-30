"""
Test configuration and fixtures for AIC8800 driver test suite.
"""
import subprocess
import pytest


@pytest.fixture(scope="session")
def running_kernel():
    """Return the currently running kernel version string."""
    return subprocess.check_output(["uname", "-r"], text=True).strip()


@pytest.fixture(scope="session")
def wifi_interface():
    """Return the active AIC8800 Wi-Fi interface name or None."""
    try:
        out = subprocess.check_output(["iw", "dev"], text=True)
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Interface"):
                return line.split()[1]
    except Exception:
        pass
    return None
