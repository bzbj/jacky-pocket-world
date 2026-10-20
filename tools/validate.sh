#!/usr/bin/env bash
# Scoped from the upstream gate: only modules present in this static edition.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
mode="${1:---all}"
static_checks() (
    python3 tools/check_public.py
    test_dir="$(mktemp -d /tmp/pocket-static-tests.XXXXXX)"
    [[ "$test_dir" == /tmp/pocket-static-tests.* ]] || exit 1
    trap 'case "$test_dir" in /tmp/pocket-static-tests.*) rm -rf -- "$test_dir" ;; esac' EXIT
    "${CC:-cc}" -std=c11 -Wall -Wextra -Werror -Imain \
        tests/test_navigation.c main/navigation.c -o "$test_dir/navigation"
    "$test_dir/navigation"
    "${CC:-cc}" -std=c11 -Wall -Wextra -Werror -Icomponents/bsp/src \
        tests/test_bsp_display_rounding.c components/bsp/src/bsp_display_rounding.c \
        -o "$test_dir/rounding"
    "$test_dir/rounding"
    PYTHONDONTWRITEBYTECODE=1 python3 tests/test_verify_firmware.py
    PYTHONDONTWRITEBYTECODE=1 python3 tests/test_archive_firmware.py
    echo "Host tests: PASS"
)
firmware_checks() (
    repo_root="$(pwd)"
    validation_build_dir="$(mktemp -d /tmp/pocket-static-firmware.XXXXXX)"
    [[ "$validation_build_dir" == /tmp/pocket-static-firmware.* ]] || exit 1
    trap 'case "$validation_build_dir" in /tmp/pocket-static-firmware.*) rm -rf -- "$validation_build_dir" ;; esac' EXIT
    SDKCONFIG_DEFAULTS="$repo_root/sdkconfig.defaults" \
        idf.py -B "$validation_build_dir" -D "SDKCONFIG=$validation_build_dir/sdkconfig" build
    idf.py -B "$validation_build_dir" merge-bin -o "$validation_build_dir/FoloToy-AI-Passport-full.bin"
    python3 tools/verify_firmware.py "$validation_build_dir"
    PYTHONDONTWRITEBYTECODE=1 python3 tools/archive_firmware.py create \
        "$validation_build_dir" --archive-root "$repo_root/build/firmware"
    mkdir -p build
    cp "$validation_build_dir/FoloToy-AI-Passport-full.bin" build/FoloToy-AI-Passport-full.bin
    echo "Firmware build: PASS"
)
case "$mode" in
    --all) static_checks; firmware_checks ;;
    --static) static_checks ;;
    --firmware) firmware_checks ;;
    *) echo 'Usage: tools/validate.sh [--all|--static|--firmware]' >&2; exit 2 ;;
esac
