#!/usr/bin/env bash
# Cycle the system power profile: power-saver -> balanced -> performance -> ...
#
# This does NOT control fan speed. This laptop exposes no fan interface to
# Linux at all -- no PWM channels and no tachometers in any hwmon, no ACPI
# fan device, no platform_profile. Changing the power profile changes how
# hard the CPU is allowed to work, and the embedded controller spins the
# fans according to the resulting temperature. That is an indirect effect,
# not fan control. Real fan behaviour can only be changed in the BIOS.
#
# Runs entirely as your user -- power-profiles-daemon handles the privileged
# part over D-Bus, so no sudo and no sudoers entry is needed.
#
# Deliberately no `set -e`: every failure path has to reach a notification
# rather than dying silently, which is exactly how the old fan script failed.

set -uo pipefail

notify() {
    command -v notify-send >/dev/null && notify-send -t "$1" "Power profile" "$2"
}

fail() {
    command -v notify-send >/dev/null && \
        notify-send -u critical -t 4000 "Power profile failed" "$1"
    printf 'power-profile-toggle: %s\n' "$1" >&2
    exit 1
}

command -v powerprofilesctl >/dev/null \
    || fail "powerprofilesctl not found (install power-profiles-daemon)"

systemctl is-active --quiet power-profiles-daemon \
    || fail "power-profiles-daemon is not running"

current=$(powerprofilesctl get 2>&1) \
    || fail "could not read current profile: $current"

# Only cycle profiles this machine actually offers; `performance` disappears
# on some systems when the firmware reports the platform as degraded.
mapfile -t available < <(powerprofilesctl list 2>/dev/null |
    sed -n 's/^[ *]*\([a-z-]\+\):$/\1/p')

[ "${#available[@]}" -gt 0 ] || fail "powerprofilesctl listed no profiles"

# Walk them in a sensible order rather than whatever order they were listed.
ordered=()
for want in power-saver balanced performance; do
    for have in "${available[@]}"; do
        [ "$want" = "$have" ] && ordered+=("$want")
    done
done
[ "${#ordered[@]}" -gt 0 ] || ordered=("${available[@]}")

next="${ordered[0]}"
for i in "${!ordered[@]}"; do
    if [ "${ordered[$i]}" = "$current" ]; then
        next="${ordered[$(((i + 1) % ${#ordered[@]}))]}"
        break
    fi
done

if ! result=$(powerprofilesctl set "$next" 2>&1); then
    fail "could not switch to $next: $result"
fi

# Confirm it actually took, rather than trusting the exit code.
now=$(powerprofilesctl get 2>&1) || fail "could not confirm profile: $now"
[ "$now" = "$next" ] || fail "asked for $next but the profile is $now"

case "$now" in
    power-saver) label="Power saver" ;;
    balanced)    label="Balanced" ;;
    performance) label="Performance" ;;
    *)           label="$now" ;;
esac

# Also move the CPU package power limit. On this machine that is the only
# lever big enough to change how hard the fans have to work -- EPP alone
# barely shifts temperature, so the EC never changes fan speed for it.
#
# Optional on purpose: if the helper or its sudoers rule is not installed,
# the profile switch above still stands and we simply say so, rather than
# turning a working keypress into an error.
RAPL=/usr/local/bin/power-profile-rapl
detail=""
if [ -x "$RAPL" ]; then
    if watts=$(sudo -n "$RAPL" "$now" 2>&1); then
        detail="  -  CPU limit ${watts}"
    else
        detail="  -  CPU limit unchanged"
        printf 'power-profile-toggle: RAPL helper failed: %s\n' "$watts" >&2
    fi
fi

notify 1500 "${label}${detail}"
