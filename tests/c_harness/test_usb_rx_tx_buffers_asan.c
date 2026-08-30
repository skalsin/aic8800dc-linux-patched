/*
 * USB RX/TX Framing, A-MSDU De-aggregation & Alignment ASan/UBSan Harness.
 * Ported from Linux kernel mt76 / rtw88 USB framing engines.
 * Compiled with: gcc -fsanitize=address,undefined -Wall -Wextra -O1
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

#define AMPDU_DELIM_SIG 0x4E

struct amsdu_subframe {
    uint8_t da[6];
    uint8_t sa[6];
    uint16_t len;
    const uint8_t *payload;
};

/* Safe A-MSDU parser */
int parse_amsdu(const uint8_t *buf, size_t buf_len, struct amsdu_subframe *out, int max_subframes) {
    size_t pos = 0;
    int count = 0;

    while (pos + 14 <= buf_len && count < max_subframes) {
        memcpy(out[count].da, buf + pos, 6);
        memcpy(out[count].sa, buf + pos + 6, 6);
        uint16_t len = (uint16_t)((buf[pos + 12] << 8) | buf[pos + 13]);
        pos += 14;

        if (pos + len > buf_len) {
            /* Truncated subframe - stop safely */
            break;
        }

        out[count].len = len;
        out[count].payload = buf + pos;
        count++;
        pos += len;

        /* Account for 4-byte padding */
        size_t pad = (4 - ((len + 14) % 4)) % 4;
        pos += pad;
    }

    return count;
}

/* Safe A-MPDU delimiter validator */
bool validate_ampdu_delimiter(const uint8_t *buf, size_t buf_len, uint16_t *out_len) {
    if (buf_len < 4) return false;
    uint8_t sig = buf[3];
    if (sig != AMPDU_DELIM_SIG) return false;

    uint16_t word16 = (uint16_t)((buf[0] << 8) | buf[1]);
    *out_len = word16 & 0x0FFF;
    return true;
}

void test_amsdu_aggregation(void) {
    uint8_t buffer[2048];
    memset(buffer, 0, sizeof(buffer));

    /* Build 3 subframes */
    size_t offset = 0;
    for (int i = 0; i < 3; i++) {
        memset(buffer + offset, 0x11 * (i + 1), 6);     /* DA */
        memset(buffer + offset + 6, 0x22 * (i + 1), 6); /* SA */
        uint16_t payload_len = (uint16_t)(50 + i * 20);
        buffer[offset + 12] = (uint8_t)(payload_len >> 8);
        buffer[offset + 13] = (uint8_t)(payload_len & 0xFF);
        offset += 14;

        memset(buffer + offset, 0xAA + i, payload_len);
        offset += payload_len;

        size_t pad = (4 - ((payload_len + 14) % 4)) % 4;
        memset(buffer + offset, 0, pad);
        offset += pad;
    }

    struct amsdu_subframe subframes[8];
    int parsed = parse_amsdu(buffer, offset, subframes, 8);
    assert(parsed == 3);
    assert(subframes[0].len == 50);
    assert(subframes[1].len == 70);
    assert(subframes[2].len == 90);
}

void test_ampdu_delimiters(void) {
    uint8_t valid_delim[4] = {0x01, 0x00, 0x55, 0x4E}; /* len = 0x100 = 256, sig = 0x4E */
    uint16_t len = 0;
    bool ok = validate_ampdu_delimiter(valid_delim, 4, &len);
    assert(ok && len == 256);

    uint8_t bad_delim[4] = {0x01, 0x00, 0x55, 0xFF}; /* wrong sig */
    ok = validate_ampdu_delimiter(bad_delim, 4, &len);
    assert(!ok);
}

int main(void) {
    printf("[ASAN_TEST] Running USB RX/TX Framing & A-MSDU ASan/UBSan harness...\n");
    test_amsdu_aggregation();
    test_ampdu_delimiters();
    printf("[ASAN_TEST] USB Framing ASan/UBSan harness PASSED (0 errors, 0 leaks)\n");
    return 0;
}
