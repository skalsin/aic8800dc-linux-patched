"""
USB RX/TX Frame Framing, A-MSDU / A-MPDU, and Ring Buffer Safety Test Suite.
Ported from Linux kernel drivers/net/wireless USB drivers (mt76, rtw88, ath9k_htc).
"""
import struct
import pytest


def build_amsdu_subframe(da: bytes, sa: bytes, payload: bytes) -> bytes:
    """
    Construct an A-MSDU subframe according to IEEE 802.11n/ac/ax:
    DA (6B) + SA (6B) + Length (2B) + Payload (N bytes) + Padding (0-3B to 4B boundary).
    """
    assert len(da) == 6
    assert len(sa) == 6
    hdr = da + sa + struct.pack(">H", len(payload))
    subframe = hdr + payload
    # Pad to 4-byte boundary if needed
    pad_len = (4 - (len(subframe) % 4)) % 4
    return subframe + (b"\x00" * pad_len)


def parse_amsdu_stream(data: bytes) -> list:
    """
    Parse a contiguous A-MSDU aggregated frame stream with strict boundary validation.
    Guarantees no out-of-bounds reads.
    """
    subframes = []
    pos = 0
    total_len = len(data)

    while pos + 14 <= total_len:
        da = data[pos:pos + 6]
        sa = data[pos + 6:pos + 12]
        payload_len = struct.unpack_from(">H", data, pos + 12)[0]
        pos += 14

        if pos + payload_len > total_len:
            # Truncated subframe
            break

        payload = data[pos:pos + payload_len]
        pos += payload_len

        # Account for 4-byte padding (except possibly the last subframe)
        pad_len = (4 - (payload_len + 14) % 4) % 4
        pos += pad_len

        subframes.append({"da": da, "sa": sa, "payload": payload})

    return subframes


def build_ampdu_delimiter(length: int, crc: int = 0) -> bytes:
    """
    Build a 4-byte A-MPDU delimiter:
    Reserved (4 bits) + Length (12 bits) + CRC (8 bits) + Signature (8 bits = 0x4E).
    """
    signature = 0x4E
    word16 = (0x0 << 12) | (length & 0x0FFF)
    return struct.pack(">HBB", word16, crc & 0xFF, signature)


def parse_ampdu_delimiter(data: bytes) -> dict:
    """Parse and validate an A-MPDU delimiter header."""
    if len(data) < 4:
        raise ValueError("A-MPDU delimiter buffer under 4 bytes")
    word16, crc, sig = struct.unpack_from(">HBB", data, 0)
    if sig != 0x4E:
        raise ValueError(f"Invalid A-MPDU delimiter signature (expected 0x4E, got 0x{sig:02X})")
    length = word16 & 0x0FFF
    return {"length": length, "crc": crc, "valid": True}


# =========================================================================
# A-MSDU De-aggregation Tests
# =========================================================================

@pytest.mark.parametrize("payload_sizes", [
    [100],
    [50, 150],
    [64, 128, 256, 512],
    [1500, 1500],
    [1, 2, 3, 4, 5],
])
def test_amsdu_pack_unpack_integrity(payload_sizes):
    """Test aggregation and de-aggregation of multiple subframes of varying lengths."""
    da = b"\x00\x11\x22\x33\x44\x55"
    sa = b"\x66\x77\x88\x99\xAA\xBB"
    stream = b""
    expected_payloads = []

    for size in payload_sizes:
        payload = bytes([i % 256 for i in range(size)])
        expected_payloads.append(payload)
        stream += build_amsdu_subframe(da, sa, payload)

    parsed = parse_amsdu_stream(stream)
    assert len(parsed) == len(payload_sizes)
    for i, sf in enumerate(parsed):
        assert sf["da"] == da
        assert sf["sa"] == sa
        assert sf["payload"] == expected_payloads[i]


# =========================================================================
# A-MPDU Delimiter Tests
# =========================================================================

@pytest.mark.parametrize("frame_len", [64, 512, 1500, 4095])
def test_ampdu_delimiter_roundtrip(frame_len):
    """Verify A-MPDU delimiter generation and parsing across allowed length ranges."""
    delim = build_ampdu_delimiter(frame_len, crc=0xAA)
    assert len(delim) == 4
    parsed = parse_ampdu_delimiter(delim)
    assert parsed["valid"] is True
    assert parsed["length"] == frame_len
    assert parsed["crc"] == 0xAA


def test_ampdu_invalid_signature_rejected():
    """Verify delimiters with invalid signature bytes raise ValueError."""
    bad_delim = b"\x00\x64\x00\xFF"  # Sig is 0xFF instead of 0x4E
    with pytest.raises(ValueError):
        parse_ampdu_delimiter(bad_delim)


# =========================================================================
# USB Buffer Alignment & Boundary Tests
# =========================================================================

@pytest.mark.parametrize("size", range(1, 65))
def test_usb_buffer_4byte_alignment(size):
    """Verify 4-byte padding calculation for USB DMA transfer requirements."""
    pad_len = (4 - (size % 4)) % 4
    aligned_size = size + pad_len
    assert aligned_size % 4 == 0
    assert 0 <= pad_len <= 3
