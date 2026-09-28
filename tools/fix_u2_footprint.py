#!/usr/bin/env python3
"""Fix the ADS1115 footprint library alias after the legacy KiCad conversion.

The converted schematic used the invalid footprint path
`Package_TSSOP:VSSOP-10_3x3mm_P0.5mm`. KiCad's official ADS1115 VSSOP
footprint is in the `Package_SO` library.

This script is deliberately narrow and idempotent.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "hardware" / "poa-sensor.kicad_sch"

OLD = 'Package_TSSOP:VSSOP-10_3x3mm_P0.5mm'
NEW = 'Package_SO:VSSOP-10_3x3mm_P0.5mm'


def main() -> int:
    text = SCH.read_text(encoding="utf-8")
    old_count = text.count(OLD)
    new_count = text.count(NEW)

    if old_count == 1 and new_count == 0:
        SCH.write_text(text.replace(OLD, NEW, 1), encoding="utf-8", newline="\n")
        print(f"Updated U2 footprint: {OLD} -> {NEW}")
        return 0

    if old_count == 0 and new_count == 1:
        print(f"U2 footprint already correct: {NEW}")
        return 0

    print(
        "Unexpected schematic state: "
        f"old footprint count={old_count}, corrected footprint count={new_count}",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
