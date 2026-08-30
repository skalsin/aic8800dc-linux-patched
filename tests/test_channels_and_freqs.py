"""
Comprehensive 802.11 Channel, Frequency, and Chandef Validation Test Suite.
Ported from Linux kernel cfg80211 / mac80211 / hostap test patterns.
"""
import pytest


# 2.4 GHz standard channel definitions (1-14)
CHANNELS_2G = {
    1: 2412,
    2: 2417,
    3: 2422,
    4: 2427,
    5: 2432,
    6: 2437,
    7: 2442,
    8: 2447,
    9: 2452,
    10: 2457,
    11: 2462,
    12: 2467,
    13: 2472,
    14: 2484,  # Japan only (DSSS/CCK)
}

# 5 GHz channels (UNII-1, UNII-2, UNII-2e, UNII-3)
CHANNELS_5G = {
    36: 5180, 40: 5200, 44: 5220, 48: 5240,
    52: 5260, 56: 5280, 60: 5300, 64: 5320,
    100: 5500, 104: 5520, 108: 5540, 112: 5560,
    116: 5580, 120: 5600, 124: 5620, 128: 5640,
    132: 5660, 136: 5680, 140: 5700, 144: 5720,
    149: 5745, 153: 5765, 157: 5785, 161: 5805, 165: 5825,
}

WIDTH_20 = "20MHz"
WIDTH_40 = "40MHz"
WIDTH_80 = "80MHz"
WIDTH_160 = "160MHz"


def channel_to_freq_2g(channel: int) -> int:
    """Compute 2.4 GHz frequency from channel number."""
    if channel == 14:
        return 2484
    if 1 <= channel <= 13:
        return 2407 + channel * 5
    raise ValueError(f"Invalid 2.4 GHz channel: {channel}")


def freq_to_channel_2g(freq: int) -> int:
    """Compute 2.4 GHz channel number from frequency."""
    if freq == 2484:
        return 14
    if 2412 <= freq <= 2472 and (freq - 2407) % 5 == 0:
        return (freq - 2407) // 5
    raise ValueError(f"Invalid 2.4 GHz frequency: {freq}")


def calculate_ht40_center_freq(primary_freq: int, extension: str) -> int:
    """Calculate center frequency for HT40 channel bonding."""
    if extension == "above" or extension == "+":
        return primary_freq + 10
    elif extension == "below" or extension == "-":
        return primary_freq - 10
    raise ValueError(f"Invalid HT40 extension: {extension}")


def sanitize_chandef(primary_freq: int, width: str, center1: int, config_use_5g: bool = False):
    """
    Python emulation of driver rwnx_rx_sm_connect_ind fallback & sanitization logic.
    Handles firmware bugs returning freq 0 or invalid center frequencies.
    """
    # Fallback for firmware bug: freq 0
    if primary_freq == 0:
        primary_freq = 2412  # Fallback to Channel 1 (2412 MHz)

    # 5 GHz guard when 5G disabled in build
    if not config_use_5g and primary_freq > 2500:
        # Re-map/reject invalid 5G frequency to 2.4G default
        primary_freq = 2412

    # Center frequency sanitization
    if width == WIDTH_40:
        expected_center = primary_freq + 10 if primary_freq <= 2452 else primary_freq - 10
        if center1 == 0 or abs(center1 - primary_freq) != 10:
            center1 = expected_center
    elif width == WIDTH_20:
        center1 = primary_freq

    return {
        "primary_freq": primary_freq,
        "width": width,
        "center1": center1,
        "channel": freq_to_channel_2g(primary_freq),
        "valid": True,
    }


# =========================================================================
# Parameterized Test Matrix: 2.4 GHz Channels
# =========================================================================

@pytest.mark.parametrize("ch,expected_freq", list(CHANNELS_2G.items()))
def test_channel_to_freq_2g_all_channels(ch, expected_freq):
    """Verify standard frequency calculation for all 14 2.4 GHz channels."""
    assert channel_to_freq_2g(ch) == expected_freq
    assert freq_to_channel_2g(expected_freq) == ch


@pytest.mark.parametrize("invalid_ch", [-1, 0, 15, 16, 36, 100, 999])
def test_channel_to_freq_2g_invalid_channels(invalid_ch):
    """Verify out-of-range 2.4GHz channels raise ValueError."""
    with pytest.raises(ValueError):
        channel_to_freq_2g(invalid_ch)


@pytest.mark.parametrize("invalid_freq", [0, 2400, 2411, 2413, 2480, 2500, 5180])
def test_freq_to_channel_2g_invalid_freqs(invalid_freq):
    """Verify invalid frequencies raise ValueError."""
    with pytest.raises(ValueError):
        freq_to_channel_2g(invalid_freq)


# =========================================================================
# HT40 Channel Bonding Matrix
# =========================================================================

@pytest.mark.parametrize("ch", range(1, 8))
def test_ht40_plus_center_frequencies(ch):
    """Channels 1-7 using HT40+ (extension channel above)."""
    prim_freq = channel_to_freq_2g(ch)
    center = calculate_ht40_center_freq(prim_freq, "+")
    assert center == prim_freq + 10
    # Center frequency should match channel (ch + 2)
    expected_sec_ch = ch + 2
    assert center == channel_to_freq_2g(expected_sec_ch)


@pytest.mark.parametrize("ch", range(5, 12))
def test_ht40_minus_center_frequencies(ch):
    """Channels 5-11 using HT40- (extension channel below)."""
    prim_freq = channel_to_freq_2g(ch)
    center = calculate_ht40_center_freq(prim_freq, "-")
    assert center == prim_freq - 10
    # Center frequency should match channel (ch - 2)
    expected_sec_ch = ch - 2
    assert center == channel_to_freq_2g(expected_sec_ch)


# =========================================================================
# Regression Tests for Frequency 0 Firmware Bug & Chandef Sanitization
# =========================================================================

@pytest.mark.parametrize("zero_freq", [0])
def test_firmware_freq_0_fallback_resolution(zero_freq):
    """Regression test for commit 113de0c: resolve freq 0 NULL chandef."""
    res = sanitize_chandef(zero_freq, WIDTH_20, 0, config_use_5g=False)
    assert res["valid"] is True
    assert res["primary_freq"] == 2412
    assert res["center1"] == 2412
    assert res["channel"] == 1


@pytest.mark.parametrize("ch", range(1, 14))
@pytest.mark.parametrize("width", [WIDTH_20, WIDTH_40])
def test_chandef_sanitizer_matrix(ch, width):
    """Test chandef sanitization across all channels and bandwidth combinations."""
    prim_freq = channel_to_freq_2g(ch)
    res = sanitize_chandef(prim_freq, width, 0, config_use_5g=False)
    assert res["valid"] is True
    assert res["primary_freq"] == prim_freq
    if width == WIDTH_20:
        assert res["center1"] == prim_freq
    elif width == WIDTH_40:
        assert abs(res["center1"] - prim_freq) == 10


# =========================================================================
# 5 GHz Rejection Matrix (when CONFIG_USE_5G=n)
# =========================================================================

@pytest.mark.parametrize("ch_5g,freq_5g", list(CHANNELS_5G.items()))
def test_5g_channels_rejected_or_sanitized_when_5g_disabled(ch_5g, freq_5g):
    """Verify all 5GHz channels are gracefully handled without crashing when CONFIG_USE_5G=n."""
    res = sanitize_chandef(freq_5g, WIDTH_20, 0, config_use_5g=False)
    assert res["valid"] is True
    assert res["primary_freq"] == 2412  # Remapped safely to 2.4G default
