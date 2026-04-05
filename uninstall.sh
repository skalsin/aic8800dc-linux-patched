#!/bin/bash

set -e

PACKAGE_NAME="aic8800dc"
PACKAGE_VERSION="6.4.3.0-patched.1"
SRC_DIR="/usr/src/${PACKAGE_NAME}-${PACKAGE_VERSION}"

echo "##################################################"
echo "AIC8800DC Wi-Fi driver uninstaller"
echo "##################################################"

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: this script must be run as root (use sudo)" >&2
    exit 1
fi

# --- Unload modules ---
echo "[1/4] Unloading modules..."
modprobe -r aic8800_fdrv 2>/dev/null || true
modprobe -r aic_load_fw 2>/dev/null || true

# --- Remove DKMS registration ---
echo "[2/4] Removing DKMS registration..."
if command -v dkms &>/dev/null && dkms status -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" 2>/dev/null | grep -q .; then
    dkms remove -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" --all
else
    echo "  No DKMS registration found, skipping."
fi

# --- Remove DKMS source tree ---
echo "[3/4] Removing DKMS source tree..."
rm -rf "${SRC_DIR}"

# --- Remove firmware, udev rule, auto-load config ---
echo "[4/4] Removing firmware and udev rules..."
rm -rf /lib/firmware/aic8800DC/
rm -f /etc/udev/rules.d/aic.rules
rm -f /etc/modules-load.d/aic8800.conf
udevadm control --reload

echo ""
echo "##################################################"
echo "Uninstallation complete."
echo "##################################################"
