#!/bin/bash
# Conservative AIC8800 link monitor.  It never reloads kernel modules.

set -u

MODE="${AIC8800_WATCHDOG_MODE:-observe}"
INTERVAL="${AIC8800_WATCHDOG_INTERVAL:-25}"
FAIL_LIMIT="${AIC8800_WATCHDOG_FAIL_LIMIT:-6}"
RECONNECT_COOLDOWN="${AIC8800_WATCHDOG_RECONNECT_COOLDOWN:-300}"

case "$MODE" in
    observe|reconnect) ;;
    *)
        printf 'Invalid AIC8800_WATCHDOG_MODE=%s (expected observe or reconnect)\n' "$MODE" >&2
        exit 2
        ;;
esac

log() {
    logger -t aic8800-watchdog -- "$*"
}

monitor_kernel_events() {
    journalctl -k -f -n 0 --output=cat 2>/dev/null | while IFS= read -r line; do
        case "$line" in
            *"cmd queue crashed"*|*"aicwf_rwnx_usb_platform_init err -110"*|*"__cfg80211_connect_result"*|*"BUG: kernel NULL pointer dereference"*)
                log "Observed kernel failure; automatic driver reload is disabled: $line"
                ;;
        esac
    done
}

monitor_kernel_events &
LOG_PID=$!
trap 'kill "$LOG_PID" 2>/dev/null || true; wait "$LOG_PID" 2>/dev/null || true' EXIT INT TERM

consecutive_fails=0
last_reconnect=0
log "Started in $MODE mode; kernel module reload is permanently disabled"

while sleep "$INTERVAL"; do
    wlan_if="$(iw dev 2>/dev/null | awk '$1 == "Interface" { print $2; exit }')"
    if [ -z "$wlan_if" ]; then
        consecutive_fails=0
        continue
    fi

    gateway="$(ip -4 route show dev "$wlan_if" 2>/dev/null | awk '$1 == "default" && $2 == "via" { print $3; exit }')"
    if [ -z "$gateway" ]; then
        consecutive_fails=0
        continue
    fi

    if ping -c 3 -W 2 -I "$wlan_if" "$gateway" >/dev/null 2>&1; then
        consecutive_fails=0
        continue
    fi

    consecutive_fails=$((consecutive_fails + 1))
    log "Gateway $gateway unreachable on $wlan_if ($consecutive_fails/$FAIL_LIMIT)"

    # Flush stale ARP/neighbor entries and settle firmware channel state after 2 consecutive fails
    if [ "$consecutive_fails" -ge 2 ]; then
        ip neigh flush dev "$wlan_if" >/dev/null 2>&1 || true
        nmcli device wifi rescan ifname "$wlan_if" >/dev/null 2>&1 || true
    fi

    if [ "$MODE" != reconnect ] || [ "$consecutive_fails" -lt "$FAIL_LIMIT" ]; then
        continue
    fi

    now="$(date +%s)"
    if [ $((now - last_reconnect)) -lt "$RECONNECT_COOLDOWN" ]; then
        log "Reconnect suppressed by ${RECONNECT_COOLDOWN}s cooldown"
        continue
    fi

    # Reassociation is opt-in because it exercises driver connection paths.
    # Even in reconnect mode, never unload or reload either kernel module.
    log "Opt-in reconnect: asking NetworkManager to reconnect $wlan_if"
    nmcli device connect "$wlan_if" >/dev/null 2>&1 || true
    last_reconnect="$now"
    consecutive_fails=0
done
