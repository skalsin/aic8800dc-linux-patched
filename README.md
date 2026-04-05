# AIC8800DC Linux Driver (Patched)

Patched out-of-tree Linux kernel driver for the AIC8800DC USB Wi-Fi chipset.
Based on upstream version 6.4.3.0 with compatibility fixes.

DKMS is supported. The driver rebuilds automatically after every kernel update.

---

## Installation

### 1. Install dependencies

**Ubuntu / Debian:**

```bash
sudo apt install dkms build-essential linux-headers-$(uname -r)
```

If that fails because the package is not found (HWE or non-generic kernel), use the metapackage instead (Ubuntu/Debian only):

```bash
sudo apt install dkms build-essential linux-headers-generic
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

**Simulate a kernel upgrade rebuild** (no reboot needed):

```bash
# Install headers for another kernel version
sudo apt install linux-headers-<other-version>

# Build for that kernel
sudo dkms build -m aic8800dc -v 6.4.3.0-patched.1 -k <other-version>

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

- After `apt upgrade` installs a new kernel, DKMS rebuilds the driver automatically. No manual action needed.
- If the build fails on a new kernel, the driver may need patching for API changes introduced in that kernel. This is a limitation of all out-of-tree drivers.
- **Secure Boot users:** the kernel module must be signed to load under Secure Boot. See your distro's MOK (Machine Owner Key) documentation for signing instructions.
