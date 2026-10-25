# AIC8800DC Linux Driver (Patched)

Patched out-of-tree Linux kernel driver for the AIC8800DC USB Wi-Fi chipset.
Based on upstream version 6.4.3.0 with compatibility fixes.

The analysis and guarded validation procedure for the Linux 6.17 cfg80211
connection panic are documented in [docs/PANIC-RCA.md](docs/PANIC-RCA.md).

DKMS is supported. The driver rebuilds automatically after every kernel update.

---

## Installation

### 1. Install dependencies

**Ubuntu / Debian:**

```bash
sudo apt install dkms build-essential linux-headers-$(uname -r) linux-headers-generic
```

**Arch Linux:**

```bash
sudo pacman -S dkms linux-headers base-devel
```

**Fedora:**

```bash
sudo dnf install dkms kernel-devel kernel-headers
```

### 2. Clone and install

```bash
git clone https://github.com/Kiborgik/aic8800dc-linux-patched.git
cd aic8800dc-linux-patched

sudo chmod +x install.sh
sudo ./install.sh
```

### 3. Verify

```bash
sudo chmod +x test.sh
sudo ./test.sh
```

---

## Uninstall

```bash
sudo chmod +x uninstall.sh
sudo ./uninstall.sh
```

---

## Testing

`test.sh` checks everything without requiring a reboot:

```bash
sudo ./test.sh
```

It verifies:

- DKMS registration status
- `.ko` files installed for the running kernel
- Module metadata via `modinfo`
- Whether modules are currently loaded
- Firmware files in `/lib/firmware/aic8800DC/`
- udev rule and boot auto-load config
- DKMS AUTOINSTALL hook presence

For a read-only link, counter, USB, driver-parameter, and recent-log snapshot:

```bash
aic8800-diagnostics.sh
```

The diagnostics also report the installed and loaded module source versions,
watchdog/kdump state, previous-boot kernel failures, and the newest persisted
`/var/crash` dmesg files.  Each association now emits one unconditional kernel
record beginning with `connect completion:`; it includes the firmware status,
the status reported to cfg80211, and whether a retained BSS was supplied.

Do not run an automatic module-reload watchdog while investigating a kernel
panic.  A recovery loop can repeatedly exercise the same unsafe path and can
erase the useful timing around the first failure.

The packaged watchdog is therefore not enabled automatically.  If started, it
defaults to read-only `observe` mode and never unloads or reloads kernel
modules.  An opt-in `reconnect` mode may ask NetworkManager to reassociate, but
should only be used after the normal association path is proven stable.

The disconnect/reconnect and process fault-injection tests are intentionally
opt-in. Run them only from a local session:

```bash
sudo AIC8800_RUN_LIVE_E2E=1 ./run_tests.sh
```

On drivers whose scan path stalls active traffic, pin the NetworkManager
profile to the intended AP so it does not inject periodic roaming scans:

```bash
nmcli connection modify <profile> 802-11-wireless.bssid <AP-BSSID> \
    802-11-wireless.powersave 2
```

This intentionally disables roaming to another AP with the same SSID. Update
or clear the BSSID if the access point is replaced.

**Simulate a kernel upgrade rebuild** (no reboot needed):

```bash
# Install headers for another kernel version using your distro's package manager,
# then build for that kernel:
sudo dkms build -m aic8800 -v 1.0 -k <other-version>

# Confirm both kernels show as installed
dkms status
```

---

## Manual build (cross-compile / embedded targets)

For Rockchip, Allwinner, Amlogic, or other non-Ubuntu targets, set the platform
variables in `drivers/aic8800/Makefile` and build directly:

```bash
cd drivers/aic8800
make
sudo make install
sudo depmod -a
sudo modprobe aic_load_fw
sudo modprobe aic8800_fdrv
```

---

## Notes

- After a kernel update, DKMS rebuilds the driver automatically. No manual action needed.
- If the build fails on a new kernel, the driver may need patching for API changes introduced in that kernel. This is a limitation of all out-of-tree drivers.
- **Secure Boot users:** the kernel module must be signed to load under Secure Boot. See your distro's MOK (Machine Owner Key) documentation for signing instructions.
