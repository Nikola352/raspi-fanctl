#!/bin/bash
# fanctl - Control or check Raspberry Pi fan speed

OVERRIDE_FILE="/tmp/fan_override"
STATUS_FILE="/tmp/fan_status"

case "$1" in
    auto|on|off|[0-9]*)
        echo "$1" > "$OVERRIDE_FILE"
        echo "Fan override set to '$1'"
        ;;
    status|"")
        if [[ -f "$STATUS_FILE" ]]; then
            cat "$STATUS_FILE"
        else
            echo "No status available."
        fi
        ;;
    *)
        echo "Usage: $0 [auto|on|off|<0-100>|status]"
        ;;
esac
