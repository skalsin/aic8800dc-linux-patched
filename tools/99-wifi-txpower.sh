#!/bin/bash
IFACE=$1
ACTION=$2
if [ "$IFACE" = "wlxb8fbb3681ee8" ] && [ "$ACTION" = "up" ]; then
    /usr/sbin/iw dev "$IFACE" set txpower limit 1400
    (sleep 3 && /usr/bin/nmcli device wifi rescan ifname "$IFACE" >/dev/null 2>&1) &
fi
