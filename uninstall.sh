#!/bin/bash


PACKAGE_NAME="aic8800"
PACKAGE_VERSION="1.0"
SRC_DIR="/usr/src/${PACKAGE_NAME}-${PACKAGE_VERSION}"

echo "##################################################"
echo "AIC8800DC Wi-Fi driver uninstaller"
echo "##################################################"

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: this script must be run as root (use sudo)" >&2
    exit 1
fi

# --- Stop packaged monitor before unloading anything ---
echo "[1/5] Stopping link monitor..."
systemctl disable --now aic8800-watchdog.service 2>/dev/null || true

# --- Unload modules ---
echo "[2/5] Unloading modules..."
modprobe -r aic8800_fdrv 2>/dev/null || true
modprobe -r aic_load_fw 2>/dev/null || true

# --- Remove DKMS registration ---
echo "[3/5] Removing DKMS registration..."
if command -v dkms &>/dev/null && dkms status -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" 2>/dev/null | grep -q .; then
    dkms remove -m "${PACKAGE_NAME}" -v "${PACKAGE_VERSION}" --all
else
    echo "  No DKMS registration found, skipping."
fi

# --- Remove DKMS source tree ---
echo "[4/5] Removing DKMS source tree..."
rm -rf "${SRC_DIR}"

# --- Remove firmware, udev rule, auto-load config ---
echo "[5/5] Removing firmware and udev rules..."
rm -rf /lib/firmware/aic8800DC/
rm -f /etc/udev/rules.d/aic.rules
rm -f /etc/modules-load.d/aic8800.conf
rm -f /usr/local/bin/aic8800-diagnostics.sh
rm -f /usr/local/bin/aic8800-watchdog.sh
rm -f /etc/systemd/system/aic8800-watchdog.service
systemctl daemon-reload
udevadm control --reload

echo ""
echo "##################################################"
echo "Uninstallation complete."
echo "##################################################"
