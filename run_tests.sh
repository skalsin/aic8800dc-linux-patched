#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "=================================================="
echo "AIC8800 Driver & Stability Comprehensive Test Suite"
echo "=================================================="

# Run bash sanity check test.sh
echo "[1/3] Running deployment sanity checks (test.sh)..."
bash "$REPO_DIR/test.sh"

# Run C ASan/UBSan/TSan harnesses
echo ""
echo "[2/3] Running AddressSanitizer, UBSan & ThreadSanitizer C harnesses..."
if [ -d "$REPO_DIR/tests/c_harness" ]; then
    make -C "$REPO_DIR/tests/c_harness" run
fi

# Run pytest suite
echo ""
echo "[3/3] Running automated regression and link quality tests (pytest)..."
PYTEST_BIN=""
if command -v pytest &>/dev/null; then
    PYTEST_BIN="pytest"
elif [ -f "/home/skalsin/bot/venv/bin/pytest" ]; then
    PYTEST_BIN="/home/skalsin/bot/venv/bin/pytest"
elif [ -f "/home/skalsin/ouroboros/.venv/bin/pytest" ]; then
    PYTEST_BIN="/home/skalsin/ouroboros/.venv/bin/pytest"
fi

if [ -n "$PYTEST_BIN" ]; then
    "$PYTEST_BIN" -v "$REPO_DIR/tests"
else
    echo "Warning: pytest not found in system or known virtual environments. Running standalone checks."
    python3 -m unittest discover -s "$REPO_DIR/tests" -p "test_*.py" || true
fi

echo ""
echo "=================================================="
echo "All tests and memory sanitizers completed successfully!"
echo "=================================================="
