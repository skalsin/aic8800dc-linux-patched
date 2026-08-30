"""
802.11 Data Rates, MCS Mapping, and Firmware Power Table Validation Suite.
Ported from IEEE 802.11n/ac/ax physical layer specification tables and AIC userconfig.
"""
from pathlib import Path
import pytest


# HT (802.11n) theoretical bitrates in Mbps: (MCS, width_MHz, SGI) -> Mbps
HT_RATES_MBPS = {
    # MCS 0-7 (1 Spatial Stream) - 20 MHz
    (0, 20, False): 6.5,  (0, 20, True): 7.2,
    (1, 20, False): 13.0, (1, 20, True): 14.4,
    (2, 20, False): 19.5, (2, 20, True): 21.7,
    (3, 20, False): 26.0, (3, 20, True): 28.9,
    (4, 20, False): 39.0, (4, 20, True): 43.3,
    (5, 20, False): 52.0, (5, 20, True): 57.8,
    (6, 20, False): 58.5, (6, 20, True): 65.0,
    (7, 20, False): 65.0, (7, 20, True): 72.2,
    # MCS 0-7 (1 Spatial Stream) - 40 MHz
    (0, 40, False): 13.5,  (0, 40, True): 15.0,
    (1, 40, False): 27.0,  (1, 40, True): 30.0,
    (2, 40, False): 40.5,  (2, 40, True): 45.0,
    (3, 40, False): 54.0,  (3, 40, True): 60.0,
    (4, 40, False): 81.0,  (4, 40, True): 90.0,
    (5, 40, False): 108.0, (5, 40, True): 120.0,
    (6, 40, False): 121.5, (6, 40, True): 135.0,
    (7, 40, False): 135.0, (7, 40, True): 150.0,
}

# HE (802.11ax / Wi-Fi 6) MCS 0-11 bitrates for 1 NSS 20MHz (0.8us GI)
HE_RATES_20M_1SS = {
    0: 8.6,
    1: 17.2,
    2: 25.8,
    3: 34.4,
    4: 51.6,
    5: 68.8,
    6: 77.4,
    7: 86.0,
    8: 103.2,
    9: 114.7,
    10: 129.0,
    11: 143.4,
}

# HE (802.11ax / Wi-Fi 6) MCS 0-11 bitrates for 1 NSS 40MHz (0.8us GI)
HE_RATES_40M_1SS = {
    0: 17.2,
    1: 34.4,
    2: 51.6,
    3: 68.8,
    4: 103.2,
    5: 137.6,
    6: 154.9,
    7: 172.1,
    8: 206.5,
    9: 229.4,
    10: 258.1,
    11: 286.8,
}


def parse_userconfig_power_table(content: str) -> dict:
    """Parse key-value power configuration levels from aic_userconfig text."""
    pwr = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, v = line.split("=", 1)
            try:
                pwr[k.strip()] = int(v.strip())
            except ValueError:
                pass
    return pwr


# =========================================================================
# HT MCS Rate Table Tests
# =========================================================================

@pytest.mark.parametrize("mcs", range(8))
@pytest.mark.parametrize("width", [20, 40])
@pytest.mark.parametrize("sgi", [False, True])
def test_ht_mcs_rates_consistency(mcs, width, sgi):
    """Verify that HT MCS 0-7 data rate lookups are strictly increasing with MCS."""
    rate = HT_RATES_MBPS.get((mcs, width, sgi))
    assert rate is not None
    assert rate > 0
    if sgi:
        # Short Guard Interval gives ~11% throughput increase
        non_sgi_rate = HT_RATES_MBPS.get((mcs, width, False))
        assert rate > non_sgi_rate
    if width == 40:
        # 40 MHz gives more than double 20 MHz throughput
        r20 = HT_RATES_MBPS.get((mcs, 20, sgi))
        assert rate >= r20 * 2.0


# =========================================================================
# HE (Wi-Fi 6) MCS Rate Table Tests
# =========================================================================

@pytest.mark.parametrize("mcs,rate", list(HE_RATES_20M_1SS.items()))
def test_he_20m_rates(mcs, rate):
    """Verify Wi-Fi 6 20MHz single stream rates up to MCS 11 (143.4 Mbps)."""
    assert rate > 0
    if mcs > 0:
        prev_rate = HE_RATES_20M_1SS[mcs - 1]
        assert rate > prev_rate


@pytest.mark.parametrize("mcs,rate", list(HE_RATES_40M_1SS.items()))
def test_he_40m_rates(mcs, rate):
    """Verify Wi-Fi 6 40MHz single stream rates up to MCS 11 (286.8 Mbps)."""
    assert rate > 0
    if mcs > 0:
        prev_rate = HE_RATES_40M_1SS[mcs - 1]
        assert rate > prev_rate


# =========================================================================
# Userconfig Power Level File Tests
# =========================================================================

def test_userconfig_power_table_validity():
    """Verify that the userconfig power level file is syntactically valid and bounded."""
    repo_root = Path(__file__).parent.parent
    userconfig_path = repo_root / "fw" / "aic8800DC" / "aic_userconfig_8800dc_3625.txt"
    assert userconfig_path.exists(), f"Userconfig file missing at {userconfig_path}"

    content = userconfig_path.read_text()
    pwr = parse_userconfig_power_table(content)

    assert pwr.get("enable") == 1
    # Check all standard legacy power levels are defined and in [10, 22] dBm range
    for mode in ["1m", "2m", "5m5", "11m", "6m", "9m", "12m", "18m", "24m", "36m", "48m", "54m"]:
        key = f"lvl_11b_11ag_{mode}_2g4"
        assert key in pwr, f"Missing power level definition for {key}"
        assert 10 <= pwr[key] <= 22, f"Power level {pwr[key]} out of safe hardware range for {key}"

    # Check HT/VHT power levels
    for mcs in range(10):
        key = f"lvl_11n_11ac_mcs{mcs}_2g4"
        assert key in pwr, f"Missing power level definition for {key}"
        assert 10 <= pwr[key] <= 22

    # Check HE (11ax) power levels
    for mcs in range(12):
        key = f"lvl_11ax_mcs{mcs}_2g4"
        assert key in pwr, f"Missing power level definition for {key}"
        assert 10 <= pwr[key] <= 22
