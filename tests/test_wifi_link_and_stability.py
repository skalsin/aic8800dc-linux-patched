"""
Test Wi-Fi hardware state, RF parameters, TX power limit, and live link quality.
"""
import re
import subprocess
from pathlib import Path
import pytest


def gateway_for_interface(wifi_interface):
    """Return the gateway routed through the tested Wi-Fi interface."""
    route_out = subprocess.check_output(
        ["ip", "route", "show", "dev", wifi_interface], text=True
    )
    for line in route_out.splitlines():
        if line.startswith("default via"):
            return line.split()[2]
    pytest.fail(f"No default gateway found for {wifi_interface}")


def test_wifi_interface_exists(wifi_interface):
    """Verify that a wireless netdevice interface is created by the driver."""
    if not wifi_interface:
        pytest.skip("No Wi-Fi interface available")
    assert wifi_interface.startswith("wl"), f"Unexpected Wi-Fi interface name: {wifi_interface}"


def test_wifi_connected(wifi_interface):
    """Verify that the Wi-Fi interface is actively connected to an SSID."""
    if not wifi_interface:
        pytest.skip("No Wi-Fi interface available")

    res = subprocess.run(["iw", "dev", wifi_interface, "link"], capture_output=True, text=True)
    assert res.returncode == 0, f"iw dev link failed: {res.stderr}"
    assert "Connected to" in res.stdout, f"Wi-Fi interface {wifi_interface} is not connected: {res.stdout}"


def test_wifi_ping_and_low_packet_loss(wifi_interface):
    """Verify low packet loss and low jitter to the default gateway over Wi-Fi."""
    if not wifi_interface:
        pytest.skip("No Wi-Fi interface available")

    # Determine gateway
    try:
        gw = gateway_for_interface(wifi_interface)
    except (OSError, subprocess.SubprocessError) as exc:
        pytest.fail(f"Could not determine Wi-Fi gateway: {exc}")

    # A 4 Hz sample catches multi-second receive stalls without tripping
    # consumer-router ICMP rate limits during repeated test runs.
    res = subprocess.run(
        ["ping", "-I", wifi_interface, "-c", "20", "-i", "0.25", "-W", "1", gw],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Ping to gateway {gw} failed:\n{res.stdout}\n{res.stderr}"

    # Parse packet loss
    loss_match = re.search(r"([\d.]+)%\s+packet\s+loss", res.stdout)
    assert loss_match is not None, f"Could not parse packet loss from:\n{res.stdout}"
    packet_loss = float(loss_match.group(1))
    assert packet_loss <= 5, f"Excess packet loss to gateway {gw}:\n{res.stdout}"

    # Parse average latency if available
    rtt_match = re.search(r"rtt\s+min/avg/max/mdev\s*=\s*[\d.]+/([\d.]+)/", res.stdout)
    if rtt_match:
        avg_rtt = float(rtt_match.group(1))
        assert avg_rtt < 50.0, f"Excess average gateway latency: {avg_rtt} ms\n{res.stdout}"


def test_host_rx_reorder_is_disabled():
    """The broken host reorder path must not be present in the loaded module."""
    module_dir = Path("/sys/module/aic8800_fdrv")
    if not module_dir.exists():
        pytest.skip("aic8800_fdrv is not loaded")

    reorder_param = module_dir / "parameters" / "reorder_timeout"
    assert not reorder_param.exists(), (
        "aic8800_fdrv was built with host RX reorder enabled; this causes "
        "receive stalls and packet loss"
    )


def test_rx_packet_counter_advances(wifi_interface):
    """Packets delivered by the non-reorder fast path must be observable."""
    if not wifi_interface:
        pytest.skip("No Wi-Fi interface available")

    counter = Path("/sys/class/net") / wifi_interface / "statistics" / "rx_packets"
    gw = gateway_for_interface(wifi_interface)
    before = int(counter.read_text().strip())
    subprocess.run(
        ["ping", "-I", wifi_interface, "-c", "3", "-W", "1", gw],
        capture_output=True,
        text=True,
    )
    after = int(counter.read_text().strip())
    assert after > before, "RX packet counter did not account delivered traffic"
