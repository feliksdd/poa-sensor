#!/usr/bin/env python3
"""Normalize ADS1115 U2 footprint to the project-local POA library.

KiCad 8 stores the footprint string twice in this project: once in the embedded
symbol definition and once in the placed U2 symbol. This script deliberately
normalizes both occurrences and is idempotent.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "hardware" / "poa-sensor.kicad_sch"

OLD_VALUES = (
    "Package_TSSOP:VSSOP-10_3x3mm_P0.5mm",
    "Package_SO:VSSOP-10_3x3mm_P0.5mm",
)
TARGET = "POA:ADS1115IDGSR_VSSOP-10"
EXPECTED_TARGET_COUNT = 2


def main() -> int:
    text = SCH.read_text(encoding="utf-8")
    changes = 0
    for old in OLD_VALUES:
        count = text.count(old)
        if count:
            text = text.replace(old, TARGET)
            changes += count

    target_count = text.count(TARGET)
    if target_count != EXPECTED_TARGET_COUNT:
        print(
            "Unexpected schematic state after normalization: "
            f"target count={target_count}, expected={EXPECTED_TARGET_COUNT}",
            file=sys.stderr,
        )
        return 1

    if changes:
        SCH.write_text(text, encoding="utf-8", newline="\n")
        print(f"Updated {changes} U2/ADS1115 footprint entries -> {TARGET}")
    else:
        print(f"U2 footprint already correct: {TARGET} ({target_count} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
