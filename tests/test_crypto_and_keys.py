"""
802.11 Security, Cipher Suites, and Key Negotiation Test Suite.
Ported from hostap/tests/hwsim and IEEE 802.11i / WPA3 security specifications.
"""
import struct
import pytest


# 802.11 Cipher Suite Selectors (OUI:Type)
CIPHER_SUITE_WEP40 = bytes([0x00, 0x0F, 0xAC, 1])
CIPHER_SUITE_TKIP = bytes([0x00, 0x0F, 0xAC, 2])
CIPHER_SUITE_CCMP_128 = bytes([0x00, 0x0F, 0xAC, 4])
CIPHER_SUITE_WEP104 = bytes([0x00, 0x0F, 0xAC, 5])
CIPHER_SUITE_BIP_CMAC_128 = bytes([0x00, 0x0F, 0xAC, 6])
CIPHER_SUITE_GCMP_128 = bytes([0x00, 0x0F, 0xAC, 8])
CIPHER_SUITE_GCMP_256 = bytes([0x00, 0x0F, 0xAC, 9])
CIPHER_SUITE_CCMP_256 = bytes([0x00, 0x0F, 0xAC, 10])

# Key Types
KEY_TYPE_PAIRWISE = "pairwise"
KEY_TYPE_GROUP = "group"
KEY_TYPE_IGTK = "igtk"  # Management Frame Protection


def validate_key_installation(key_idx: int, key_type: str, cipher: bytes, key_data: bytes) -> dict:
    """
    Validate key parameters before installing into driver hardware registers.
    Emulates driver rwnx_set_key boundary checks.
    """
    # Key index validation
    if key_type == KEY_TYPE_PAIRWISE:
        if key_idx not in (0, 1, 2, 3):
            raise ValueError(f"Invalid pairwise key index: {key_idx}")
    elif key_type == KEY_TYPE_GROUP:
        if key_idx not in (1, 2, 3, 4):
            raise ValueError(f"Invalid group key index: {key_idx}")
    elif key_type == KEY_TYPE_IGTK:
        if key_idx not in (4, 5):
            raise ValueError(f"Invalid IGTK key index: {key_idx}")

    # Cipher key length validation
    expected_len = {
        CIPHER_SUITE_WEP40: 5,
        CIPHER_SUITE_WEP104: 13,
        CIPHER_SUITE_TKIP: 32,
        CIPHER_SUITE_CCMP_128: 16,
        CIPHER_SUITE_BIP_CMAC_128: 16,
        CIPHER_SUITE_GCMP_128: 16,
        CIPHER_SUITE_GCMP_256: 32,
        CIPHER_SUITE_CCMP_256: 32,
    }.get(cipher)

    if expected_len is None:
        raise ValueError("Unsupported cipher suite")

    if len(key_data) != expected_len:
        raise ValueError(f"Key length mismatch: expected {expected_len}, got {len(key_data)}")

    return {"key_idx": key_idx, "key_type": key_type, "cipher": cipher, "valid": True}


def parse_eapol_key_frame(data: bytes) -> dict:
    """Parse an 802.1X EAPOL-Key frame (WPA 4-way handshake)."""
    if len(data) < 95:
        raise ValueError("EAPOL frame under minimum 95 bytes")

    # IEEE 802.1X header (4B)
    proto_ver, eapol_type, eapol_len = struct.unpack_from(">BBH", data, 0)
    if eapol_type != 3:  # Key descriptor
        raise ValueError(f"Invalid EAPOL type: {eapol_type} (expected 3 for Key)")

    # EAPOL-Key descriptor
    desc_type, key_info, key_len, replay_cnt = struct.unpack_from(">BHHQ", data, 4)

    return {
        "proto_ver": proto_ver,
        "desc_type": desc_type,
        "key_info": key_info,
        "key_len": key_len,
        "replay_counter": replay_cnt,
        "is_pairwise": bool(key_info & 0x0008),
        "is_install": bool(key_info & 0x0040),
        "is_ack": bool(key_info & 0x0080),
        "is_mic": bool(key_info & 0x0100),
        "is_secure": bool(key_info & 0x0200),
    }


# =========================================================================
# Key Validation Matrix Tests
# =========================================================================

@pytest.mark.parametrize("cipher,expected_len", [
    (CIPHER_SUITE_CCMP_128, 16),
    (CIPHER_SUITE_TKIP, 32),
    (CIPHER_SUITE_WEP40, 5),
    (CIPHER_SUITE_WEP104, 13),
    (CIPHER_SUITE_BIP_CMAC_128, 16),
])
def test_valid_pairwise_keys(cipher, expected_len):
    """Test valid pairwise key installations for all supported ciphers."""
    key_data = b"\xAA" * expected_len
    res = validate_key_installation(0, KEY_TYPE_PAIRWISE, cipher, key_data)
    assert res["valid"] is True


@pytest.mark.parametrize("invalid_len", [0, 4, 15, 17, 31, 64])
def test_invalid_key_length_rejected(invalid_len):
    """Verify keys with invalid lengths are rejected."""
    key_data = b"\x00" * invalid_len
    with pytest.raises(ValueError):
        validate_key_installation(0, KEY_TYPE_PAIRWISE, CIPHER_SUITE_CCMP_128, key_data)


@pytest.mark.parametrize("invalid_idx", [-1, 4, 5, 10])
def test_invalid_pairwise_key_indices_rejected(invalid_idx):
    """Pairwise keys only allow indices 0-3."""
    with pytest.raises(ValueError):
        validate_key_installation(invalid_idx, KEY_TYPE_PAIRWISE, CIPHER_SUITE_CCMP_128, b"\x00" * 16)


# =========================================================================
# EAPOL 4-Way Handshake Frame Parsing Tests
# =========================================================================

def test_parse_eapol_m1_frame():
    """Verify parsing Message 1 of 4-Way Handshake (Pairwise, Ack=1, MIC=0)."""
    # Build a simulated 95-byte EAPOL M1 packet
    # Key info: Pairwise (bit 3), Ack (bit 7) -> 0x0088
    eapol_hdr = struct.pack(">BBH", 2, 3, 91)
    key_desc = struct.pack(">BHHQ", 2, 0x0088, 16, 1)  # Desc Type 2 (RSN), Replay 1
    nonce = b"\x11" * 32
    iv = b"\x00" * 16
    rsc = b"\x00" * 8
    resvd = b"\x00" * 8
    mic = b"\x00" * 16
    data_len = struct.pack(">H", 0)

    packet = eapol_hdr + key_desc + nonce + iv + rsc + resvd + mic + data_len
    parsed = parse_eapol_key_frame(packet)

    assert parsed["is_pairwise"] is True
    assert parsed["is_ack"] is True
    assert parsed["is_mic"] is False
    assert parsed["replay_counter"] == 1
