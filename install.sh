#!/bin/bash

set -e

PACKAGE_NAME="aic8800dc"
PACKAGE_VERSION="6.4.3.0-patched.1"
SRC_DIR="/usr/src/${PACKAGE_NAME}-${PACKAGE_VERSION}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "##################################################"
echo "AIC8800DC Wi-Fi driver installer"
echo "Version: ${PACKAGE_VERSION}"
echo "##################################################"

# Check for root
if [ "$(id -u)" -ne 0 ]; then
    echo "Error: this script must be run as root (use sudo)" >&2
    exit 1
fi

# Check dependencies
for cmd in dkms make depmod; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "Error: '$cmd' is not installed." >&2
        echo ""
        echo "Install dependencies first:"
        echo "  Ubuntu/Debian: sudo apt install dkms build-essential linux-headers-\$(uname -r)"
        echo "  (if not found): sudo apt install dkms build-essential linux-headers-generic"
        echo "  Arch:          sudo pacman -S dkms linux-headers base-devel"
        echo "  Fedora:        sudo dnf install dkms kernel-devel kernel-headers"
        exit 1
    fi
done

# Check kernel headers are present for the running kernel
if [ ! -d "/lib/modules/$(uname -r)/build" ]; then
    echo "Error: kernel headers not found for $(uname -r)" >&2
    echo "  Ubuntu/Debian: sudo apt install linux-headers-\$(uname -r)" >&2
    echo "  (if not found): sudo apt install linux-headers-generic" >&2
    echo "  Fedora:        sudo dnf install kernel-devel-\$(uname -r)" >&2
    echo "  Arch:          sudo pacman -S linux-headers" >&2
    exit 1
fi

# --- Firmware and udev rules ---
echo "[1/5] Installing firmware and udev rules..."
cp -rf "${SCRIPT_DIR}/fw/aic8800DC" /lib/firmware/
cp "${SCRIPT_DIR}/tools/aic.rules" /etc/udev/rules.d/
udevadm trigger
udevadm control --reload
if [ -L /dev/aicudisk ]; then
    eject /dev/aicudisk || true
fi

# --- Prepare DKMS source tree ---
echo "[2/5] Preparing DKMS source tree..."
if dkms status -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" 2>/dev/null | grep -q .; then
    echo "  Removing existing DKMS registration..."
    dkms remove -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" --all || true
fi
rm -rf "${SRC_DIR}"
mkdir -p "${SRC_DIR}"
cp -rp "${SCRIPT_DIR}/." "${SRC_DIR}/"

# --- DKMS add / build / install ---
echo "[3/5] Registering with DKMS..."
dkms add -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}"

echo "[4/5] Building kernel modules (this may take a minute)..."
dkms build -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}"

echo "[5/5] Installing kernel modules..."
dkms install -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}"

# --- Auto-load on boot ---
tee /etc/modules-load.d/aic8800.conf > /dev/null <<EOF
aic_load_fw
aic8800_fdrv
EOF

# --- Load now ---
echo ""
echo "Loading modules..."
modprobe aic_load_fw || echo "  Note: aic_load_fw not loaded (plug in the device and run: sudo modprobe aic_load_fw)"
modprobe aic8800_fdrv || echo "  Note: aic8800_fdrv not loaded (plug in the device and run: sudo modprobe aic8800_fdrv)"

echo ""
echo "##################################################"
echo "Installation complete!"
echo ""
echo "To verify:  sudo ./test.sh"
echo "To remove:  sudo ./uninstall.sh"
echo "##################################################"
