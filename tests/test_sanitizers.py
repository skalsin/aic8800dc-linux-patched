"""
Pytest integration for AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan),
and ThreadSanitizer (TSan) C Harness Suites.
"""
import subprocess
from pathlib import Path
import pytest


@pytest.fixture(scope="module")
def charness_dir():
    d = Path(__file__).parent / "c_harness"
    assert d.exists(), f"C harness directory missing at {d}"
    return d


def test_asan_and_ubsan_c_harness(charness_dir):
    """
    Compile and run 802.11 frame parsers, USB buffers, and security keys
    with AddressSanitizer + UndefinedBehaviorSanitizer.
    Asserts zero buffer overflows, zero memory leaks, and zero undefined behavior.
    """
    # Compile ASan targets
    res_build = subprocess.run(["make", "clean", "asan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_build.returncode == 0, f"ASan compilation failed:\n{res_build.stdout}\n{res_build.stderr}"

    # Run frame parser ASan
    res_parser = subprocess.run(["./test_frame_parser_asan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_parser.returncode == 0, f"Frame parser ASan failed:\n{res_parser.stdout}\n{res_parser.stderr}"
    assert "PASSED" in res_parser.stdout

    # Run USB buffer ASan
    res_usb = subprocess.run(["./test_usb_rx_tx_buffers_asan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_usb.returncode == 0, f"USB buffer ASan failed:\n{res_usb.stdout}\n{res_usb.stderr}"
    assert "PASSED" in res_usb.stdout

    # Run crypto keys ASan
    res_crypto = subprocess.run(["./test_crypto_keys_asan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_crypto.returncode == 0, f"Crypto keys ASan failed:\n{res_crypto.stdout}\n{res_crypto.stderr}"
    assert "PASSED" in res_crypto.stdout


def test_tsan_thread_concurrency_c_harness(charness_dir):
    """
    Compile and run command manager queue concurrency harness with ThreadSanitizer (TSan).
    Asserts zero data races under 10,000 rapid concurrent enqueue/dequeue operations.
    """
    # Compile TSan target
    res_build = subprocess.run(["make", "tsan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_build.returncode == 0, f"TSan compilation failed:\n{res_build.stdout}\n{res_build.stderr}"

    # Run TSan binary
    res_run = subprocess.run(["./test_cmd_mgr_tsan"], cwd=str(charness_dir), capture_output=True, text=True)
    assert res_run.returncode == 0, f"TSan detected data race or failure:\n{res_run.stdout}\n{res_run.stderr}"
    assert "0 data races" in res_run.stdout
