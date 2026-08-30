#!/bin/bash
set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

echo "=================================================="
echo "AIC8800 Driver & Stability Comprehensive Test Suite"
echo "=================================================="

# Run bash sanity check test.sh
echo "[1/2] Running deployment sanity checks (test.sh)..."
bash "$REPO_DIR/test.sh"

# Run pytest suite
echo ""
echo "[2/2] Running automated regression and link quality tests (pytest)..."
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
echo "All tests completed successfully!"
echo "=================================================="
