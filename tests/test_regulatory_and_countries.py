"""
Comprehensive Regulatory Domain & Country Code Test Matrix.
Ported from Linux kernel regulatory.db / crda / cfg80211 test suites.
"""
import pytest


# Comprehensive regulatory rules database
REGULATORY_DB = {
    "US": {"name": "United States", "max_ch_2g": 11, "max_txpower_dbm": 30, "allow_ch12_13": False, "allow_ch14": False},
    "CA": {"name": "Canada", "max_ch_2g": 11, "max_txpower_dbm": 30, "allow_ch12_13": False, "allow_ch14": False},
    "DE": {"name": "Germany", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "CH": {"name": "Switzerland", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "FR": {"name": "France", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "GB": {"name": "United Kingdom", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "IT": {"name": "Italy", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "ES": {"name": "Spain", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "NL": {"name": "Netherlands", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "SE": {"name": "Sweden", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "NO": {"name": "Norway", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "FI": {"name": "Finland", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "PL": {"name": "Poland", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "AT": {"name": "Austria", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "BE": {"name": "Belgium", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "DK": {"name": "Denmark", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "IE": {"name": "Ireland", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "PT": {"name": "Portugal", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "GR": {"name": "Greece", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "CZ": {"name": "Czechia", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "HU": {"name": "Hungary", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "RO": {"name": "Romania", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "BG": {"name": "Bulgaria", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "JP": {"name": "Japan", "max_ch_2g": 14, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": True},
    "CN": {"name": "China", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "KR": {"name": "South Korea", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "AU": {"name": "Australia", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "NZ": {"name": "New Zealand", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "BR": {"name": "Brazil", "max_ch_2g": 13, "max_txpower_dbm": 30, "allow_ch12_13": True, "allow_ch14": False},
    "IN": {"name": "India", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "SG": {"name": "Singapore", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "IL": {"name": "Israel", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "ZA": {"name": "South Africa", "max_ch_2g": 13, "max_txpower_dbm": 20, "allow_ch12_13": True, "allow_ch14": False},
    "00": {"name": "World Regulatory Default", "max_ch_2g": 11, "max_txpower_dbm": 20, "allow_ch12_13": False, "allow_ch14": False},
}


def validate_country_code_param(country_code: str) -> str:
    """Sanitize and validate country code string input for module parameter."""
    if not country_code:
        return "00"  # Worldwide fallback to avoid 'Error, wrong country = '
    cc = country_code.strip().upper()
    if len(cc) != 2 or not cc.isalpha():
        if cc != "00":
            return "00"
    return cc


def is_channel_legal_in_country(channel: int, country_code: str) -> bool:
    """Check if a 2.4 GHz channel is legal in the given regulatory domain."""
    cc = validate_country_code_param(country_code)
    reg = REGULATORY_DB.get(cc, REGULATORY_DB["00"])
    if channel < 1 or channel > 14:
        return False
    if channel > reg["max_ch_2g"]:
        return False
    if channel in (12, 13) and not reg["allow_ch12_13"]:
        return False
    if channel == 14 and not reg["allow_ch14"]:
        return False
    return True


# =========================================================================
# Country Code Validation Matrix
# =========================================================================

@pytest.mark.parametrize("cc,data", list(REGULATORY_DB.items()))
def test_all_country_codes_valid_in_regdb(cc, data):
    """Verify all country codes in the database validate properly."""
    assert validate_country_code_param(cc) == cc
    assert data["max_ch_2g"] in (11, 13, 14)
    assert data["max_txpower_dbm"] in (20, 30)


@pytest.mark.parametrize("invalid_cc", ["", "   ", "USA", "1", "DEU", "XYZ123", "\x00\x00"])
def test_invalid_country_codes_fallback_safely_to_world(invalid_cc):
    """Verify invalid country code inputs safely fall back to '00' without crashing."""
    assert validate_country_code_param(invalid_cc) == "00"


# =========================================================================
# Channel Legality Matrix Across Countries
# =========================================================================

@pytest.mark.parametrize("ch", range(1, 12))
@pytest.mark.parametrize("cc", ["US", "DE", "CH", "JP", "CN", "00"])
def test_channels_1_to_11_legal_globally(ch, cc):
    """Channels 1-11 are universally legal across all major regulatory domains."""
    assert is_channel_legal_in_country(ch, cc) is True


@pytest.mark.parametrize("ch", [12, 13])
def test_channels_12_13_forbidden_in_us_allowed_in_eu_jp(ch):
    """Channels 12-13 are illegal in US/CA/00 but allowed in EU (DE, CH) and JP."""
    assert is_channel_legal_in_country(ch, "US") is False
    assert is_channel_legal_in_country(ch, "CA") is False
    assert is_channel_legal_in_country(ch, "00") is False
    assert is_channel_legal_in_country(ch, "DE") is True
    assert is_channel_legal_in_country(ch, "CH") is True
    assert is_channel_legal_in_country(ch, "JP") is True


@pytest.mark.parametrize("cc", ["US", "DE", "CH", "FR", "GB", "CN", "00"])
def test_channel_14_strictly_forbidden_everywhere_except_jp(cc):
    """Channel 14 is strictly reserved for Japan (DSSS/CCK 11b)."""
    assert is_channel_legal_in_country(14, cc) is False
    assert is_channel_legal_in_country(14, "JP") is True
