"""
Test DKMS registration, installed module files, and sysfs module parameters.
"""
import os
import subprocess
import pytest


def test_dkms_installed_for_running_kernel(running_kernel):
    """Verify DKMS shows aic8800 as installed for the active kernel."""
    res = subprocess.run(["dkms", "status"], capture_output=True, text=True)
    assert res.returncode == 0, f"dkms status failed: {res.stderr}"
    assert "installed" in res.stdout, f"No installed DKMS module found in: {res.stdout}"
    assert running_kernel in res.stdout, f"Running kernel {running_kernel} not registered in DKMS status: {res.stdout}"


def test_kernel_modules_on_disk(running_kernel):
    """Verify both .ko files exist on disk for the running kernel."""
    base_dir = f"/lib/modules/{running_kernel}"
    for mod in ["aic_load_fw", "aic8800_fdrv"]:
        found = False
        for root, _, files in os.walk(base_dir):
            for f in files:
                if f.startswith(mod) and (f.endswith(".ko") or f.endswith(".ko.zst") or f.endswith(".ko.gz")):
                    found = True
                    break
            if found:
                break
        assert found, f"Module {mod} not found under {base_dir}"


def test_modules_loaded_in_kernel():
    """Verify both aic_load_fw and aic8800_fdrv are loaded in lsmod."""
    res = subprocess.run(["lsmod"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "aic_load_fw" in res.stdout, "aic_load_fw is not loaded in kernel"
    assert "aic8800_fdrv" in res.stdout, "aic8800_fdrv is not loaded in kernel"


def test_power_save_disabled_in_sysfs():
    """Verify power saving parameters are set to 0 (ps_on=0, dpsm=0) to prevent jitter."""
    ps_on_path = "/sys/module/aic8800_fdrv/parameters/ps_on"
    dpsm_path = "/sys/module/aic8800_fdrv/parameters/dpsm"

    if os.path.exists(ps_on_path):
        with open(ps_on_path, "r") as f:
            val = f.read().strip()
            assert val in ("0", "N", "n", "false"), f"ps_on should be disabled, got {val}"

    if os.path.exists(dpsm_path):
        with open(dpsm_path, "r") as f:
            val = f.read().strip()
            assert val in ("0", "N", "n", "false"), f"dpsm should be disabled, got {val}"


def test_firmware_files_present():
    """Verify firmware files exist in /lib/firmware/aic8800DC/."""
    fw_dir = "/lib/firmware/aic8800DC"
    assert os.path.isdir(fw_dir), f"Firmware directory {fw_dir} missing"
    bins = [f for f in os.listdir(fw_dir) if f.endswith(".bin")]
    assert len(bins) >= 2, f"Expected at least 2 .bin firmware files, found {len(bins)}: {bins}"
