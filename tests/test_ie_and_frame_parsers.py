"""
802.11 Management Frame, Information Element (IE), and Beacon Parsing Test Suite.
Ported from hostap/tests/hwsim and Linux kernel net/mac80211 IE parsers.
"""
import struct
import pytest


# 802.11 Information Element Element IDs
WLAN_EID_SSID = 0
WLAN_EID_SUPP_RATES = 1
WLAN_EID_DS_PARAMS = 3
WLAN_EID_TIM = 5
WLAN_EID_COUNTRY = 7
WLAN_EID_HT_CAP = 45
WLAN_EID_EXT_SUPP_RATES = 50
WLAN_EID_HT_OPERATION = 61
WLAN_EID_VHT_CAP = 191
WLAN_EID_VHT_OPERATION = 192
WLAN_EID_VENDOR_SPECIFIC = 221
WLAN_EID_EXTENSION = 255


def build_ie(eid: int, payload: bytes) -> bytes:
    """Build a standard TLV (Type-Length-Value) Information Element."""
    return struct.pack("BB", eid, len(payload)) + payload


def parse_ies(data: bytes) -> dict:
    """
    Parse a sequence of Information Elements with full bounds checking.
    Returns a dict mapping EID to list of raw payloads.
    Guarantees buffer overflow protection against malformed frames.
    """
    ies = {}
    pos = 0
    total_len = len(data)

    while pos + 2 <= total_len:
        eid, length = struct.unpack_from("BB", data, pos)
        pos += 2
        if pos + length > total_len:
            # Truncated IE detected (fuzz/malformed input) -> break safely
            break
        payload = data[pos:pos + length]
        pos += length
        if eid not in ies:
            ies[eid] = []
        ies[eid].append(payload)

    return ies


def parse_beacon_fixed_fields(data: bytes) -> dict:
    """Parse 802.11 Beacon fixed fields: Timestamp (8B), Beacon Interval (2B), Capability Info (2B)."""
    if len(data) < 12:
        raise ValueError("Beacon frame truncated (under 12 bytes fixed header)")
    timestamp, interval, cap_info = struct.unpack_from("<QHH", data, 0)
    return {
        "timestamp": timestamp,
        "interval_tu": interval,
        "cap_info": cap_info,
        "ess": bool(cap_info & 0x0001),
        "ibss": bool(cap_info & 0x0002),
        "privacy": bool(cap_info & 0x0010),
        "short_preamble": bool(cap_info & 0x0020),
        "short_slot_time": bool(cap_info & 0x0400),
    }


# =========================================================================
# IE Construction and Parsing Tests
# =========================================================================

@pytest.mark.parametrize("ssid_name", ["HomeWiFi1", "Test-5G", "", "A" * 32, "Spaces In Name", "Special_!@#$%^&*()"])
def test_parse_ssid_ie(ssid_name):
    """Test parsing SSID Information Elements with various lengths up to 32 bytes."""
    ssid_bytes = ssid_name.encode("utf-8")
    ie_buf = build_ie(WLAN_EID_SSID, ssid_bytes)
    res = parse_ies(ie_buf)
    assert WLAN_EID_SSID in res
    assert res[WLAN_EID_SSID][0] == ssid_bytes
    assert res[WLAN_EID_SSID][0].decode("utf-8") == ssid_name


@pytest.mark.parametrize("ch", range(1, 14))
def test_parse_ds_parameter_ie(ch):
    """Test DS Parameter IE (Channel indicator)."""
    ds_payload = struct.pack("B", ch)
    ie_buf = build_ie(WLAN_EID_DS_PARAMS, ds_payload)
    res = parse_ies(ie_buf)
    assert WLAN_EID_DS_PARAMS in res
    parsed_ch = struct.unpack("B", res[WLAN_EID_DS_PARAMS][0])[0]
    assert parsed_ch == ch


def test_parse_multi_ie_stream():
    """Test parsing a full multi-IE stream as found in 802.11 Beacons."""
    ssid_ie = build_ie(WLAN_EID_SSID, b"HomeWiFi1")
    rates_ie = build_ie(WLAN_EID_SUPP_RATES, bytes([0x82, 0x84, 0x8B, 0x96]))  # 1, 2, 5.5, 11 Mbps basic
    ds_ie = build_ie(WLAN_EID_DS_PARAMS, bytes([4]))  # Channel 4
    ht_cap_ie = build_ie(WLAN_EID_HT_CAP, b"\x00" * 26)  # 26 bytes HT Cap
    vendor_ie = build_ie(WLAN_EID_VENDOR_SPECIFIC, b"\x00\x50\xF2\x01\x01\x00")  # WPA OUI

    stream = ssid_ie + rates_ie + ds_ie + ht_cap_ie + vendor_ie
    res = parse_ies(stream)

    assert len(res) == 5
    assert res[WLAN_EID_SSID][0] == b"HomeWiFi1"
    assert res[WLAN_EID_DS_PARAMS][0] == bytes([4])
    assert len(res[WLAN_EID_HT_CAP][0]) == 26
    assert len(res[WLAN_EID_VENDOR_SPECIFIC][0]) == 6


# =========================================================================
# Fuzzing & Malformed Frame Buffer Safety Tests
# =========================================================================

@pytest.mark.parametrize("malformed_data", [
    b"",
    b"\x00",  # EID only, missing length byte
    b"\x00\x10",  # EID 0, Length 16, but 0 payload bytes (truncated)
    b"\x00\x20" + b"A" * 10,  # EID 0, Length 32, but only 10 bytes provided
    b"\xFF\xFF" + b"\x00" * 200,  # Huge length exceeding buffer
    b"\x00\x00",  # Empty SSID (valid zero-length)
])
def test_fuzzed_malformed_ie_handling_does_not_crash(malformed_data):
    """Verify parsing malformed or truncated IE streams never raises index/unpack errors."""
    res = parse_ies(malformed_data)
    assert isinstance(res, dict)


@pytest.mark.parametrize("cap_flags,is_privacy,is_ess", [
    (0x0001, False, True),
    (0x0011, True, True),
    (0x0002, False, False),
    (0x0000, False, False),
])
def test_beacon_fixed_field_parser(cap_flags, is_privacy, is_ess):
    """Test Beacon capability bits extraction."""
    hdr = struct.pack("<QHH", 123456789, 100, cap_flags)
    fields = parse_beacon_fixed_fields(hdr)
    assert fields["timestamp"] == 123456789
    assert fields["interval_tu"] == 100
    assert fields["privacy"] is is_privacy
    assert fields["ess"] is is_ess
