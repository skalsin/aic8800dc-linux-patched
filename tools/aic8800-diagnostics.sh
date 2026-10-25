#!/bin/bash
# Read-only AIC8800 health snapshot.  Safe to run while the link carries traffic.

set -u

section() {
    printf '\n== %s ==\n' "$1"
}

run() {
    printf '$'
    printf ' %q' "$@"
    printf '\n'
    "$@" 2>&1 || true
}

WIFI_IFACE="${1:-}"
if [ -z "$WIFI_IFACE" ] && command -v iw >/dev/null 2>&1; then
    WIFI_IFACE="$(iw dev 2>/dev/null | awk '$1 == "Interface" { print $2; exit }')"
fi

section "host"
run date --iso-8601=seconds
run uname -a
run uptime

section "driver"
run modinfo aic8800_fdrv
run modinfo -F srcversion aic8800_fdrv
if [ -r /sys/module/aic8800_fdrv/srcversion ]; then
    printf 'loaded_srcversion=%s\n' "$(</sys/module/aic8800_fdrv/srcversion)"
fi
run lsmod
PARAM_DIR=/sys/module/aic8800_fdrv/parameters
if [ -d "$PARAM_DIR" ]; then
    for param in aicwf_dbg_level ps_on dpsm use_2040 ant_div reorder_timeout; do
        if [ -r "$PARAM_DIR/$param" ]; then
            printf '%s=%s\n' "$param" "$(<"$PARAM_DIR/$param")"
        elif sudo -n test -r "$PARAM_DIR/$param" 2>/dev/null; then
            printf '%s=' "$param"
            sudo -n cat "$PARAM_DIR/$param" 2>/dev/null || true
        fi
    done
fi

section "recovery safety"
run systemctl is-active aic8800-watchdog.service
run systemctl is-enabled aic8800-watchdog.service
if systemctl is-active --quiet aic8800-watchdog.service 2>/dev/null; then
    printf 'WARNING: aic8800-watchdog may reload kernel modules automatically; stop it before reproducing a crash.\n'
fi
run systemctl is-active kdump-tools.service
if [ -e "$PARAM_DIR/reorder_timeout" ]; then
    printf 'WARNING: host RX reorder is compiled in; this configuration is known to stall AIC8800DC RX.\n'
else
    printf 'host_rx_reorder=disabled\n'
fi

section "USB"
run lsusb
run lsusb -t

if [ -z "$WIFI_IFACE" ]; then
    printf '\nNo wireless interface found. Driver and kernel logs are still included below.\n'
else
    section "link: $WIFI_IFACE"
    run iw dev "$WIFI_IFACE" info
    run iw dev "$WIFI_IFACE" link
    run ip -details -statistics link show dev "$WIFI_IFACE"
    run ip -4 address show dev "$WIFI_IFACE"
    run ip -4 route show dev "$WIFI_IFACE"

    if command -v nmcli >/dev/null 2>&1; then
        section "NetworkManager profile"
        ACTIVE_CONNECTION="$(nmcli -g GENERAL.CONNECTION device show "$WIFI_IFACE" 2>/dev/null)"
        if [ -n "$ACTIVE_CONNECTION" ] && [ "$ACTIVE_CONNECTION" != "--" ]; then
            run nmcli --fields 802-11-wireless.bssid,802-11-wireless.powersave \
                connection show "$ACTIVE_CONNECTION"
            PROFILE_BSSID="$(nmcli -g 802-11-wireless.bssid connection show "$ACTIVE_CONNECTION" 2>/dev/null)"
            if [ -z "$PROFILE_BSSID" ]; then
                printf 'WARNING: profile is not pinned to a BSSID; NetworkManager may enable periodic bgscan.\n'
            fi
        fi
    fi

    GATEWAY="$(ip -4 route show dev "$WIFI_IFACE" 2>/dev/null | awk '$1 == "default" && $2 == "via" { print $3; exit }')"
    if [ -n "$GATEWAY" ]; then
        section "gateway latency: $GATEWAY"
        run ping -I "$WIFI_IFACE" -c 20 -i 0.25 -W 1 "$GATEWAY"
    fi
fi

section "recent kernel/network logs"
if journalctl -k -n 1 --no-pager >/dev/null 2>&1; then
    journalctl -k --since "15 minutes ago" --no-pager 2>&1 \
        | grep -Ei 'aic|rwnx|wlan|wifi|cfg80211|usb|firmware|ubsan|bug:|warning:|timeout|disconnect|connect completion' \
        || true
elif sudo -n journalctl -k -n 1 --no-pager >/dev/null 2>&1; then
    sudo -n journalctl -k --since "15 minutes ago" --no-pager 2>&1 \
        | grep -Ei 'aic|rwnx|wlan|wifi|cfg80211|usb|firmware|ubsan|bug:|warning:|timeout|disconnect|connect completion' \
        || true
else
    run dmesg
fi

section "previous-boot kernel failures"
if journalctl -k -b -1 -n 1 --no-pager >/dev/null 2>&1; then
    journalctl -k -b -1 --no-pager 2>&1 \
        | grep -Ei 'aic|rwnx|cfg80211|connect completion|BUG:|WARNING:|NULL pointer|general protection|Call Trace|RIP:' \
        || true
elif sudo -n journalctl -k -b -1 -n 1 --no-pager >/dev/null 2>&1; then
    sudo -n journalctl -k -b -1 --no-pager 2>&1 \
        | grep -Ei 'aic|rwnx|cfg80211|connect completion|BUG:|WARNING:|NULL pointer|general protection|Call Trace|RIP:' \
        || true
else
    printf 'Previous-boot kernel journal is unavailable.\n'
fi

section "persisted crash dumps"
CRASH_ROOT=/var/crash
if [ -d "$CRASH_ROOT" ]; then
    FOUND_DUMP=0
    while IFS= read -r dump; do
        FOUND_DUMP=1
        printf '\n-- %s --\n' "$dump"
        if [ -r "$dump" ]; then
            grep -Ei 'aic|rwnx|cfg80211|connect completion|BUG:|WARNING:|NULL pointer|general protection|Call Trace|RIP:' "$dump" \
                | tail -n 100 || true
        elif sudo -n test -r "$dump" 2>/dev/null; then
            sudo -n grep -Ei 'aic|rwnx|cfg80211|connect completion|BUG:|WARNING:|NULL pointer|general protection|Call Trace|RIP:' "$dump" \
                | tail -n 100 || true
        else
            printf 'Crash dump is not readable; rerun diagnostics with sudo.\n'
        fi
    done < <(find "$CRASH_ROOT" -maxdepth 3 -type f -name 'dmesg*' -printf '%T@ %p\n' 2>/dev/null \
        | sort -rn | head -n 5 | cut -d' ' -f2-)
    if [ "$FOUND_DUMP" -eq 0 ]; then
        printf 'No persisted dmesg crash dump found.\n'
    fi
else
    printf '%s is absent.\n' "$CRASH_ROOT"
fi
