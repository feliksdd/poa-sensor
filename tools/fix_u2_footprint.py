#!/usr/bin/env python3
"""Fix the ADS1115 footprint library alias after the legacy KiCad conversion.

The converted KiCad 8 schematic contains the ADS1115 footprint string twice:

1. in the embedded library-symbol definition, and
2. in the placed U2 symbol instance.

Both must use KiCad's official `Package_SO` library.  This script intentionally
expects exactly those two occurrences and is idempotent.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "hardware" / "poa-sensor.kicad_sch"

OLD = 'Package_TSSOP:VSSOP-10_3x3mm_P0.5mm'
NEW = 'Package_SO:VSSOP-10_3x3mm_P0.5mm'
EXPECTED_TOTAL = 2


def main() -> int:
    text = SCH.read_text(encoding="utf-8")
    old_count = text.count(OLD)
    new_count = text.count(NEW)

    if old_count + new_count != EXPECTED_TOTAL:
        print(
            "Unexpected schematic state: expected exactly two ADS1115 footprint "
            f"entries, found old={old_count}, corrected={new_count}",
            file=sys.stderr,
        )
        return 1

    if old_count == 0 and new_count == EXPECTED_TOTAL:
        print(f"U2 footprint already correct in both KiCad entries: {NEW}")
        return 0

    updated = text.replace(OLD, NEW)

    # Defensive postcondition: after replacement there must be no stale alias and
    # exactly two corrected entries (embedded library symbol + placed U2).
    if updated.count(OLD) != 0 or updated.count(NEW) != EXPECTED_TOTAL:
        print("Internal error while normalizing U2 footprint entries.", file=sys.stderr)
        return 1

    SCH.write_text(updated, encoding="utf-8", newline="\n")
    print(
        f"Updated {old_count} U2/ADS1115 footprint entr"
        f"{'y' if old_count == 1 else 'ies'}: {OLD} -> {NEW}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
