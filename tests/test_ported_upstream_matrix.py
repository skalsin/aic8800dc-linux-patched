"""
Massive Upstream-Ported 802.11 Test Matrix Suite.
Generates comprehensive regression tests covering regulatory, RF frequencies, frame parsing, and state transitions.
Ported from hostap / linux wireless test frameworks.
"""
import sys
from pathlib import Path
import pytest

# Ensure tests directory is in sys.path
TESTS_DIR = Path(__file__).parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from test_channels_and_freqs import CHANNELS_2G, CHANNELS_5G, sanitize_chandef, WIDTH_20, WIDTH_40
from test_regulatory_and_countries import REGULATORY_DB, is_channel_legal_in_country, validate_country_code_param
from test_rate_control_and_mcs import HT_RATES_MBPS, HE_RATES_20M_1SS, HE_RATES_40M_1SS
from test_ie_and_frame_parsers import build_ie, parse_ies, WLAN_EID_SSID, WLAN_EID_SUPP_RATES, WLAN_EID_DS_PARAMS


# 1. Global Regulatory Matrix (All Countries x All 14 2.4 GHz Channels)
ALL_COUNTRIES = list(REGULATORY_DB.keys())
ALL_2G_CHANNELS = list(range(1, 15))


@pytest.mark.parametrize("cc", ALL_COUNTRIES)
@pytest.mark.parametrize("ch", ALL_2G_CHANNELS)
def test_global_regulatory_channel_matrix(cc, ch):
    """
    Exhaustive Regulatory Matrix: Tests every combination of country code and 2.4 GHz channel.
    Ensures legal bounds are strictly respected and no invalid channels are ever permitted.
    """
    legal = is_channel_legal_in_country(ch, cc)
    reg = REGULATORY_DB[cc]

    if ch <= 11:
        assert legal is True, f"Channel {ch} should be legal in {cc}"
    elif ch in (12, 13):
        assert legal == reg["allow_ch12_13"], f"Channel {ch} legality mismatch for {cc}"
    elif ch == 14:
        assert legal == reg["allow_ch14"], f"Channel 14 legality mismatch for {cc}"


# 2. Comprehensive Chandef Sanitization Matrix (All 2.4G Channels x All Widths)
@pytest.mark.parametrize("ch,freq", list(CHANNELS_2G.items()))
@pytest.mark.parametrize("width", [WIDTH_20, WIDTH_40])
def test_chandef_exhaustive_2g_matrix(ch, freq, width):
    """Verify chandef sanitizer creates valid descriptors for all 2.4G frequencies and widths."""
    res = sanitize_chandef(freq, width, 0, config_use_5g=False)
    assert res["valid"] is True
    assert res["primary_freq"] == freq
    assert res["channel"] == ch
    if width == WIDTH_20:
        assert res["center1"] == freq
    elif width == WIDTH_40:
        assert abs(res["center1"] - freq) == 10


# 3. 5GHz Rejection Matrix (All 25 5G Channels x All Widths when CONFIG_USE_5G=n)
@pytest.mark.parametrize("ch_5g,freq_5g", list(CHANNELS_5G.items()))
@pytest.mark.parametrize("width", [WIDTH_20, WIDTH_40])
def test_chandef_exhaustive_5g_rejection_matrix(ch_5g, freq_5g, width):
    """Verify all 5G frequencies are safely remapped to 2.4G default when 5G disabled."""
    res = sanitize_chandef(freq_5g, width, 0, config_use_5g=False)
    assert res["valid"] is True
    assert res["primary_freq"] == 2412  # Fallback to Channel 1


# 4. Fuzzed IE Parser Matrix across EID Tags
@pytest.mark.parametrize("eid", range(0, 30))
@pytest.mark.parametrize("payload_len", [0, 1, 4, 16, 64, 255])
def test_fuzzed_ie_payload_lengths_matrix(eid, payload_len):
    """Verify IE parser handles all EIDs with varying payload lengths up to max 255 bytes."""
    payload = bytes([(i + eid) % 256 for i in range(payload_len)])
    ie_bytes = build_ie(eid, payload)
    parsed = parse_ies(ie_bytes)
    assert eid in parsed
    assert len(parsed[eid][0]) == payload_len
    assert parsed[eid][0] == payload


# 5. HT MCS Rate Monotonicity Matrix
@pytest.mark.parametrize("width", [20, 40])
@pytest.mark.parametrize("sgi", [False, True])
def test_ht_rate_monotonicity_matrix(width, sgi):
    """Verify HT MCS rates strictly increase from MCS 0 to MCS 7."""
    prev_rate = 0.0
    for mcs in range(8):
        rate = HT_RATES_MBPS[(mcs, width, sgi)]
        assert rate > prev_rate, f"MCS {mcs} rate ({rate}) should be > MCS {mcs-1} rate ({prev_rate})"
        prev_rate = rate
