/*
 * 802.11 Frame & Information Element Parsing ASan/UBSan Test Harness.
 * Ported from mac80211 / hostap frame parser test suites.
 * Compiled with: gcc -fsanitize=address,undefined -Wall -Wextra -O1
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

#define WLAN_EID_SSID 0
#define WLAN_EID_SUPP_RATES 1
#define WLAN_EID_DS_PARAMS 3
#define WLAN_EID_TIM 5
#define WLAN_EID_COUNTRY 7
#define WLAN_EID_HT_CAP 45
#define WLAN_EID_HT_OPERATION 61
#define WLAN_EID_VHT_CAP 191
#define WLAN_EID_VENDOR_SPECIFIC 221
#define WLAN_EID_EXTENSION 255

struct parsed_ie {
    uint8_t eid;
    uint8_t len;
    const uint8_t *data;
};

/* Safe IE parser with strict buffer boundary checks */
int parse_80211_ies(const uint8_t *data, size_t data_len, struct parsed_ie *out_ies, size_t max_ies) {
    size_t pos = 0;
    size_t count = 0;

    while (pos + 2 <= data_len && count < max_ies) {
        uint8_t eid = data[pos];
        uint8_t len = data[pos + 1];
        pos += 2;

        if (pos + len > data_len) {
            /* Truncated IE - stop safely without reading out of bounds */
            break;
        }

        out_ies[count].eid = eid;
        out_ies[count].len = len;
        out_ies[count].data = &data[pos];
        count++;
        pos += len;
    }

    return (int)count;
}

/* Parse 802.11 Beacon fixed fields */
struct beacon_fixed {
    uint64_t timestamp;
    uint16_t beacon_int;
    uint16_t cap_info;
};

int parse_beacon_hdr(const uint8_t *buf, size_t len, struct beacon_fixed *out) {
    if (len < 12) return -1;
    memcpy(&out->timestamp, buf, 8);
    memcpy(&out->beacon_int, buf + 8, 2);
    memcpy(&out->cap_info, buf + 10, 2);
    return 0;
}

/* Fuzz test with truncated and crafted malformed buffers */
void test_ie_fuzzing(void) {
    uint8_t fuzzed_buf[512];
    struct parsed_ie ies[32];

    for (size_t len = 0; len < sizeof(fuzzed_buf); len++) {
        memset(fuzzed_buf, (int)len, len);
        int parsed = parse_80211_ies(fuzzed_buf, len, ies, 32);
        assert(parsed >= 0 && parsed <= 32);
    }

    /* Pattern test with repeating headers */
    for (int i = 0; i < 256; i += 2) {
        fuzzed_buf[i] = (uint8_t)(i / 2);
        fuzzed_buf[i + 1] = (uint8_t)(255 - i);
    }
    int parsed = parse_80211_ies(fuzzed_buf, 256, ies, 32);
    assert(parsed >= 0);
}

/* Test structured multi-IE frame */
void test_structured_beacon(void) {
    uint8_t beacon[128];
    memset(beacon, 0, sizeof(beacon));

    struct beacon_fixed bfix;
    bfix.timestamp = 0x0102030405060708ULL;
    bfix.beacon_int = 100;
    bfix.cap_info = 0x0011;
    memcpy(beacon, &bfix.timestamp, 8);
    memcpy(beacon + 8, &bfix.beacon_int, 2);
    memcpy(beacon + 10, &bfix.cap_info, 2);

    /* Append SSID IE: "HomeWiFi1" */
    beacon[12] = WLAN_EID_SSID;
    beacon[13] = 9;
    memcpy(beacon + 14, "HomeWiFi1", 9);

    /* Append DS Parameter IE: Ch 4 */
    beacon[23] = WLAN_EID_DS_PARAMS;
    beacon[24] = 1;
    beacon[25] = 4;

    struct beacon_fixed parsed_fix;
    int res = parse_beacon_hdr(beacon, 12, &parsed_fix);
    assert(res == 0);
    assert(parsed_fix.timestamp == 0x0102030405060708ULL);
    assert(parsed_fix.beacon_int == 100);

    struct parsed_ie ies[16];
    int count = parse_80211_ies(beacon + 12, 14, ies, 16);
    assert(count == 2);
    assert(ies[0].eid == WLAN_EID_SSID && ies[0].len == 9);
    assert(memcmp(ies[0].data, "HomeWiFi1", 9) == 0);
    assert(ies[1].eid == WLAN_EID_DS_PARAMS && ies[1].len == 1 && ies[1].data[0] == 4);
}

int main(void) {
    printf("[ASAN_TEST] Running 802.11 Frame & IE Parser ASan/UBSan harness...\n");
    test_ie_fuzzing();
    test_structured_beacon();
    printf("[ASAN_TEST] 802.11 Frame & IE Parser ASan/UBSan harness PASSED (0 errors, 0 leaks)\n");
    return 0;
}
