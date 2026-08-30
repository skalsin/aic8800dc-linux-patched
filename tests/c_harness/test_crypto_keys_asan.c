/*
 * 802.11 Security, Cipher Suites & Key Management ASan/UBSan Harness.
 * Ported from IEEE 802.11i / hostap crypto suites.
 * Compiled with: gcc -fsanitize=address,undefined -Wall -Wextra -O1
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <stdbool.h>

enum cipher_type {
    CIPHER_WEP40 = 1,
    CIPHER_TKIP = 2,
    CIPHER_CCMP_128 = 4,
    CIPHER_WEP104 = 5,
    CIPHER_BIP_CMAC = 6,
    CIPHER_GCMP_128 = 8,
    CIPHER_GCMP_256 = 9,
    CIPHER_CCMP_256 = 10,
};

struct sec_key {
    int key_idx;
    enum cipher_type cipher;
    uint8_t key_data[32];
    size_t key_len;
    uint64_t rx_pn;
    bool in_use;
};

int install_sec_key(struct sec_key *table, int table_size, int key_idx, enum cipher_type cipher, const uint8_t *key, size_t key_len) {
    if (key_idx < 0 || key_idx >= table_size) return -1;

    size_t req_len = 0;
    switch (cipher) {
        case CIPHER_WEP40: req_len = 5; break;
        case CIPHER_WEP104: req_len = 13; break;
        case CIPHER_CCMP_128:
        case CIPHER_BIP_CMAC:
        case CIPHER_GCMP_128: req_len = 16; break;
        case CIPHER_TKIP:
        case CIPHER_GCMP_256:
        case CIPHER_CCMP_256: req_len = 32; break;
        default: return -2;
    }

    if (key_len != req_len) return -3;

    table[key_idx].key_idx = key_idx;
    table[key_idx].cipher = cipher;
    table[key_idx].key_len = key_len;
    memcpy(table[key_idx].key_data, key, key_len);
    table[key_idx].rx_pn = 0;
    table[key_idx].in_use = true;
    return 0;
}

/* Validate Packet Number (PN) replay counter protection */
bool check_and_update_pn(struct sec_key *key, uint64_t incoming_pn) {
    if (!key->in_use) return false;
    if (incoming_pn <= key->rx_pn && key->rx_pn != 0) {
        /* Replay attack detected! */
        return false;
    }
    key->rx_pn = incoming_pn;
    return true;
}

void test_key_installation_and_pn(void) {
    struct sec_key key_table[6];
    memset(key_table, 0, sizeof(key_table));

    uint8_t ccmp_key[16] = {0xAA};
    memset(ccmp_key, 0xAA, 16);

    int res = install_sec_key(key_table, 6, 0, CIPHER_CCMP_128, ccmp_key, 16);
    assert(res == 0);
    assert(key_table[0].in_use);

    /* Test PN monotonic sequence */
    assert(check_and_update_pn(&key_table[0], 1) == true);
    assert(check_and_update_pn(&key_table[0], 2) == true);
    assert(check_and_update_pn(&key_table[0], 5) == true);

    /* Replay attempt (PN 2 <= 5) MUST FAIL */
    assert(check_and_update_pn(&key_table[0], 2) == false);
    assert(check_and_update_pn(&key_table[0], 5) == false);

    /* Subsequent valid PN */
    assert(check_and_update_pn(&key_table[0], 6) == true);
}

int main(void) {
    printf("[ASAN_TEST] Running 802.11 Security & Replay Counter ASan/UBSan harness...\n");
    test_key_installation_and_pn();
    printf("[ASAN_TEST] 802.11 Security ASan/UBSan harness PASSED (0 errors, 0 leaks)\n");
    return 0;
}
