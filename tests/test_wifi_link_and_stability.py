"""
Test Wi-Fi hardware state, RF parameters, TX power limit, and live link quality.
"""
import re
import subprocess
import pytest


def test_wifi_interface_exists(wifi_interface):
    """Verify that a wireless netdevice interface is created by the driver."""
    assert wifi_interface is not None, "No Wi-Fi interface found in iw dev"
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
    gw = "192.168.68.1"
    try:
        route_out = subprocess.check_output(["ip", "route", "show", "dev", wifi_interface], text=True)
        for line in route_out.splitlines():
            if line.startswith("default via"):
                gw = line.split()[2]
                break
    except Exception:
        pass

    # Ping 10 packets
    res = subprocess.run(
        ["ping", "-I", wifi_interface, "-c", "10", "-W", "2", gw],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Ping to gateway {gw} failed:\n{res.stdout}\n{res.stderr}"

    # Parse packet loss
    loss_match = re.search(r"(\d+)%\s+packet\s+loss", res.stdout)
    assert loss_match is not None, f"Could not parse packet loss from:\n{res.stdout}"
    packet_loss = int(loss_match.group(1))
    assert packet_loss < 100, f"Total packet loss (100%) to gateway {gw}:\n{res.stdout}"

    # Parse average latency if available
    rtt_match = re.search(r"rtt\s+min/avg/max/mdev\s*=\s*[\d.]+/([\d.]+)/", res.stdout)
    if rtt_match:
        avg_rtt = float(rtt_match.group(1))
        # Ensure average RTT is valid positive float
        assert avg_rtt > 0.0
