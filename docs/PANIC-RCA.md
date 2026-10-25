# AIC8800 connection panic RCA (2026-08-30)

## Incident

Three guarded association attempts on Linux `6.17.0-41-generic` produced the
same kernel panic:

| Crash dump | Connect indication | NULL dereference |
| --- | ---: | ---: |
| `/var/crash/202608301628/dmesg.202608301628` | uptime `19003.612571` | `19003.721209` |
| `/var/crash/202608301635/dmesg.202608301635` | uptime `379.084442` | `379.140506` |
| `/var/crash/202608301644/dmesg.202608301644` | uptime `360.387735` | `360.446695` |

All three faults have the same signature:

- `BUG: kernel NULL pointer dereference, address: 0000000000000000`
- workqueue `cfg80211_event_work`
- `RIP: __cfg80211_connect_result+0x433/0xc10 [cfg80211]`
- faulting instruction `41 8b 06`
- `R14 = 0`

The first panic followed the driver log `connect mac e4 fa c4 64 5b 72` by
109 ms. The next two followed it by 56 ms and 59 ms. This reproducibility and
the cfg80211 workqueue stack rule out RF congestion as a cause of the panic.

## Root cause

The crashing driver revision retained a `struct cfg80211_bss` but reported a
successful connection with a NULL explicit BSSID. Conceptually, its completion
was equivalent to:

```c
cfg80211_connect_bss(dev, NULL, connect_bss, ...,
                     WLAN_STATUS_SUCCESS, ...);
```

Linux 6.17's [`__cfg80211_connect_result()`](https://github.com/torvalds/linux/blob/v6.17/net/wireless/sme.c#L760-L875)
sets `connected_addr` from `cr->links[0].bssid` for a non-MLO connection. After
adopting the supplied BSS, the success path unconditionally copies
`connected_addr` into `wdev->u.client.connected_addr`. The crash instruction
dereferenced the NULL address held in R14.

The cfg80211 header says either BSSID or BSS may be supplied, but that general
API statement is insufficient for this Linux 6.17 success path. Supplying both
the exact retained BSS and its explicit BSSID is the safe contract for this
driver.

## Corrections

The driver now:

1. Retains a scan-cache BSS before sending the asynchronous firmware connect
   request.
2. Passes both the firmware-selected BSSID and exact retained BSS to
   `cfg80211_connect_bss()` on success.
3. Downgrades firmware success to `WLAN_STATUS_UNSPECIFIED_FAILURE` if the exact
   BSS cannot be supplied, before allocating or marking a station connected.
4. Atomically transfers the retained reference so only one path can consume it.
5. Drops non-roaming firmware indications that no longer own the original
   pending-request token, preventing late success after cancellation.
6. Bounds-checks firmware-provided VIF, AP, channel-context, band, width, and IE
   lengths before indexing host tables.
7. Uses the retained BSSID and a real status code—not a disconnect reason—when
   cancelling a pending connection.
8. Emits an unconditional `connect completion:` kernel record with firmware
   status, reported status, BSS presence, BSSID, channel metadata, and driver
   state.

The automatic recovery watchdog was also found active with code that could
unload and reload both kernel modules. It is not the cause of the NULL
dereference, but it can repeatedly exercise a fatal path and obscure the first
failure. The packaged replacement defaults to observation, cannot reload
modules, and is not enabled automatically.

## Other Wi-Fi failures established during this investigation

These are separate from the cfg80211 panic:

- Host RX reorder caused delayed batches, sequence gaps, packet loss, and low
  throughput. It is disabled by default with `CONFIG_RX_REORDER ?= n`.
- Firmware ARP offload caused loss for fresh neighbor entries. It is disabled
  with `CONFIG_ARP_OFFLOAD = n`.
- NetworkManager background scans stalled this firmware's RX path for several
  seconds. The affected profile was pinned to its intended BSSID and power save
  disabled. BSSID pinning intentionally disables roaming and must be updated if
  the AP changes.

These mechanisms explain the observed throughput and packet-loss regression;
none explains the kernel NULL dereference.

## Offline verification

- The combined `aic_load_fw` and `aic8800_fdrv` module build completes for
  `6.17.0-41-generic`.
- Source invariants cover explicit BSSID plus BSS, missing-BSS downgrade,
  single-consumer ownership, stale indication rejection, metadata bounds, RX
  reorder, and ARP-offload defaults.
- The complete non-destructive pytest run passed 1,150 tests and skipped 7.
- LeakSanitizer cannot execute under the ptrace-based test sandbox; this is an
  environment limitation, not a sanitizer finding.
- Runtime association remains deliberately unverified until explicitly
  authorized.

## Guarded live verification

Do not automate or loop this procedure.

1. Use a local console and confirm kdump is active.
2. Confirm `aic8800-watchdog.service` is inactive and disabled.
3. Record the installed and loaded `aic8800_fdrv` source versions and the
   current `/var/crash` directory list.
4. Install the signed DKMS build while the AIC8800 USB adapter is absent.
5. Confirm the installed and loaded source versions match the tested build.
6. Start a live kernel journal capture, attach the adapter once, and request one
   association.
7. Require a `connect completion:` record with `reported_status=0` and
   `retained_bss=1` before considering association successful.
8. Confirm there is no cfg80211 warning, oops, new crash dump, command-manager
   timeout, or automatic module reload.
9. Only then run gateway loss, fresh-neighbor/ARP, sustained traffic, and
   throughput checks.

If association fails or logs inconsistent metadata, unplug the adapter and
preserve the journal. Do not reload the module repeatedly.
