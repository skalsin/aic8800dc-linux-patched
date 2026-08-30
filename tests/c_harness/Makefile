CC ?= gcc
CFLAGS_ASAN = -fsanitize=address,undefined -Wall -Wextra -O1 -g -fno-omit-frame-pointer
CFLAGS_TSAN = -fsanitize=thread -Wall -Wextra -O1 -g -pthread

TARGETS_ASAN = test_frame_parser_asan test_usb_rx_tx_buffers_asan test_crypto_keys_asan
TARGETS_TSAN = test_cmd_mgr_tsan

all: asan tsan

asan: $(TARGETS_ASAN)

tsan: $(TARGETS_TSAN)

test_frame_parser_asan: test_frame_parser_asan.c
	$(CC) $(CFLAGS_ASAN) $< -o $@

test_usb_rx_tx_buffers_asan: test_usb_rx_tx_buffers_asan.c
	$(CC) $(CFLAGS_ASAN) $< -o $@

test_crypto_keys_asan: test_crypto_keys_asan.c
	$(CC) $(CFLAGS_ASAN) $< -o $@

test_cmd_mgr_tsan: test_cmd_mgr_tsan.c
	$(CC) $(CFLAGS_TSAN) $< -o $@

run: all
	@echo "=================================================="
	@echo "Executing AddressSanitizer & UndefinedBehaviorSanitizer Suites"
	@echo "=================================================="
	./test_frame_parser_asan
	./test_usb_rx_tx_buffers_asan
	./test_crypto_keys_asan
	@echo "=================================================="
	@echo "Executing ThreadSanitizer Concurrency Suites"
	@echo "=================================================="
	./test_cmd_mgr_tsan
	@echo "=================================================="
	@echo "All Sanitizers PASSED cleanly (0 leaks, 0 races)"
	@echo "=================================================="

clean:
	rm -f $(TARGETS_ASAN) $(TARGETS_TSAN) *.o
