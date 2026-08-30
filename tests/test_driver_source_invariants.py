"""
Regression tests verifying critical driver source invariants that prevent crash loops:
1. Command timeout must be >= 10000ms.
2. Command manager must not permanently enter STATE_CRASHED on command timeouts.
3. Queue wait loops in msg_tx must be bounded to prevent softirq hangs.
4. Broken host RX reorder must remain disabled by default.
5. Broken firmware ARP offload must remain disabled by default.
6. The direct RX path must expose packet counters without bridge support.
7. Firmware-owned flag bytes must not be represented as C _Bool values.
8. Async connect completion must retain and return an exact cfg80211 BSS.
9. Pending BSS ownership must be single-consumer and validated before STA setup.
"""
import re
from pathlib import Path


def test_command_timeout_invariant():
    """Verify RWNX_80211_CMD_TIMEOUT_MS default is at least 10000ms."""
    repo_root = Path(__file__).parent.parent
    hdr = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_cmds.h"
    assert hdr.exists(), f"{hdr} not found"

    content = hdr.read_text()
    matches = re.findall(r"#define\s+RWNX_80211_CMD_TIMEOUT_MS\s+\(?([^\)\n]+)\)?", content)
    assert len(matches) > 0, "Could not find RWNX_80211_CMD_TIMEOUT_MS definition"
    # Check the default #else branch (the last definition)
    last_def = matches[-1].strip()
    timeout_val = eval(last_def, {"__builtins__": None}, {})
    assert timeout_val >= 10000, f"Timeout too small ({timeout_val}ms < 10000ms), can cause false crash loops"


def test_cmd_mgr_timeout_does_not_poison_state():
    """Verify timeout handlers in rwnx_cmds.c do not permanently set STATE_CRASHED."""
    repo_root = Path(__file__).parent.parent
    src = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_cmds.c"
    assert src.exists(), f"{src} not found"

    content = src.read_text()
    # Check wait_for_completion_killable_timeout block in cmd_mgr_queue
    # It must not contain cmd_mgr->state = RWNX_CMD_MGR_STATE_CRASHED
    lines = content.splitlines()
    in_timeout_block = False
    for i, line in enumerate(lines):
        if "wait_for_completion_killable_timeout" in line:
            in_timeout_block = True
        if in_timeout_block:
            if "RWNX_CMD_MGR_STATE_CRASHED" in line and not line.strip().startswith("//"):
                assert False, f"Found STATE_CRASHED in timeout block at line {i+1}: {line}"
            if "rwnx_cmd_free" in line or "spin_unlock_bh" in line:
                in_timeout_block = False


def test_msg_tx_wait_loop_is_bounded():
    """Verify rwnx_msg_tx.c cmdqueue drain loop has a break counter."""
    repo_root = Path(__file__).parent.parent
    src = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_msg_tx.c"
    assert src.exists(), f"{src} not found"

    content = src.read_text()
    assert "wait_count >" in content, "Missing bounded iteration counter in rwnx_msg_tx.c cmdqueue wait loop"


def test_host_rx_reorder_disabled_by_default():
    """Prevent reintroduction of the RX batching/loss regression."""
    repo_root = Path(__file__).parent.parent
    makefile = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "Makefile"
    content = makefile.read_text()
    assert re.search(r"^CONFIG_RX_REORDER\s*\?=\s*n\s*$", content, re.MULTILINE), (
        "CONFIG_RX_REORDER must default to n"
    )


def test_firmware_arp_offload_disabled_by_default():
    """Prevent fresh-neighbor packet loss and multi-second RX stalls."""
    repo_root = Path(__file__).parent.parent
    makefile = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "Makefile"
    content = makefile.read_text()
    assert re.search(r"^CONFIG_ARP_OFFLOAD\s*=\s*n\s*$", content, re.MULTILINE), (
        "CONFIG_ARP_OFFLOAD must be n"
    )


def test_direct_rx_stats_are_not_bridge_conditional():
    """RX counters must advance in the default CONFIG_BR_SUPPORT=n build."""
    repo_root = Path(__file__).parent.parent
    src = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_rx.c"
    content = src.read_text()
    direct_rx = content[content.index("static bool rwnx_rx_data_skb("):]
    forward = direct_rx[direct_rx.index("if (forward) {"):]
    stats_pos = forward.index("net_stats.rx_packets++")
    bridge_pos = forward.index("#ifdef CONFIG_BR_SUPPORT")
    assert stats_pos < bridge_pos, "RX statistics are hidden behind CONFIG_BR_SUPPORT"


def test_connect_indication_flags_use_integer_abi_types():
    """Raw firmware bytes cannot safely populate C _Bool fields."""
    repo_root = Path(__file__).parent.parent
    hdr = repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "lmac_msg.h"
    content = hdr.read_text()
    connect_ind = content[content.index("struct sm_connect_ind"):]
    connect_ind = connect_ind[:connect_ind.index("};")]
    assert re.search(r"\bu8_l\s+roamed\s*;", connect_ind)
    assert re.search(r"\bu8_l\s+qos\s*;", connect_ind)
    disconnect_ind = content[content.index("struct sm_disconnect_ind"):]
    disconnect_ind = disconnect_ind[:disconnect_ind.index("};")]
    assert re.search(r"\bu8_l\s+ft_over_ds\s*;", disconnect_ind)


def test_connect_completion_retains_exact_bss():
    """Always retain a BSS and never report successful connect with NULL."""
    repo_root = Path(__file__).parent.parent
    defs = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_defs.h").read_text()
    main = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_main.c").read_text()
    rx = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_msg_rx.c").read_text()
    assert "struct cfg80211_bss *connect_bss" in defs
    assert "connect_bss = cfg80211_get_bss" in main
    assert "xchg(&rwnx_vif->sta.connect_bss, connect_bss)" in main
    assert "if (sme->bssid)" not in main[main.index("/* cfg80211 requires a live BSS"):main.index("/* Forward the information to the LMAC */")]
    assert "cfg80211_connect_bss(dev" in rx
    assert "connect_bss ? NULL : (const u8 *)ind->bssid.array" not in rx
    assert "cfg80211_connect_bss(dev,\n                             (const u8 *)ind->bssid.array,\n                             connect_bss" in rx
    assert "ind->status_code == WLAN_STATUS_SUCCESS && !connect_bss" in rx
    assert "connect_status = WLAN_STATUS_UNSPECIFIED_FAILURE" in rx


def test_connect_bss_has_single_consumer_and_pre_setup_validation():
    """Every async consumer atomically takes the reference before using it."""
    repo_root = Path(__file__).parent.parent
    main = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_main.c").read_text()
    rx = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_msg_rx.c").read_text()
    assert "xchg(&rwnx_vif->sta.connect_bss, NULL)" in main
    assert "connect_bss = xchg(&rwnx_vif->sta.connect_bss, NULL)" in rx
    setup_pos = rx.index("if (connect_status == WLAN_STATUS_SUCCESS)")
    validate_pos = rx.index("connected BSS is missing from scan cache")
    assert validate_pos < setup_pos, "BSS validation must happen before station setup"
    invalid_ie = rx[rx.index("if (ind->assoc_req_ie_len > SM_ASSOC_IE_LEN"):]
    invalid_ie = invalid_ie[:invalid_ie.index("roamed = ind->roamed != 0")]
    assert "cfg80211_connect_bss" in invalid_ie
    assert "WLAN_STATUS_UNSPECIFIED_FAILURE" in invalid_ie
    assert "ind->ch_idx >= NX_CHAN_CTXT_CNT" in rx
    assert "ind->band >= PHY_BAND_MAX" in rx
    assert "ind->width >= PHY_CHNL_BW_OTHER" in rx
    assert '"connect completion: bssid=%pM fw_status=%u reported_status=%u retained_bss=%u' in rx
    assert "had_pending_bss = connect_bss != NULL" in rx
    assert "if (!roamed && !had_pending_bss)" in rx
    assert "dropping stale connect indication" in rx
    disconnect = main[main.index("static int rwnx_cfg80211_disconnect"):]
    assert "if (connect_bss)\n            cfg80211_connect_bss" in disconnect
    assert "cfg80211_connect_bss(dev, connect_bss->bssid, connect_bss" in disconnect
    assert "reason_code ? reason_code" not in disconnect[:disconnect.index("return 0;")]


def test_disconnect_ind_guards_sta_ap_null():
    """Disconnect indication cleanup must guard against NULL sta.ap."""
    repo_root = Path(__file__).parent.parent
    rx = (repo_root / "drivers" / "aic8800" / "aic8800_fdrv" / "rwnx_msg_rx.c").read_text()
    disconnect_func = rx[rx.index("int rwnx_rx_sm_disconnect_ind("):]
    disconnect_func = disconnect_func[:disconnect_func.index("int rwnx_rx_sm_external_auth_required_ind(")]
    assert "if (rwnx_vif->sta.ap) {" in disconnect_func
    assert "rwnx_vif->sta.ap->valid = false;" in disconnect_func
    # Ensure sta.ap is checked before dereference
    check_pos = disconnect_func.index("if (rwnx_vif->sta.ap) {")
    deref_pos = disconnect_func.index("rwnx_vif->sta.ap->valid = false;")
    assert check_pos < deref_pos, "rwnx_vif->sta.ap accessed without NULL guard in disconnect ind"

