#!/usr/bin/env python3
"""Remove known harmless geometry artifacts from the legacy -> KiCad 8 conversion.

The legacy bootstrap schematic often drew a wire past a net-label anchor. KiCad 9
correctly reports the unused tail as an unconnected wire endpoint. In addition, the
modern Device:Battery_Cell symbol moved its negative pin by 1.27 mm relative to the
legacy symbol. This script performs only the audited coordinate changes below.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMATIC = ROOT / "hardware" / "poa-sensor-wireless-legacy.kicad_sch"

# Exact native-KiCad coordinate rewrites, old -> canonical.
REPLACEMENTS = [
    # Battery negative: adapt to current Battery_Cell pin geometry and stop at label.
    (
        "\t\t\t(xy 29.21 45.72) (xy 39.37 45.72)",
        "\t\t\t(xy 29.21 44.45) (xy 31.75 44.45)",
        "BT1 negative wire -> native pin and GND-label anchor",
    ),
    (
        '\t(label "GND"\n\t\t(at 31.75 45.72 0)',
        '\t(label "GND"\n\t\t(at 31.75 44.45 0)',
        "BT1 GND label -> native pin Y",
    ),
    # LF crystal: stop the two horizontal wires at their XL1/XL2 label anchors.
    (
        "\t\t\t(xy 38.1 87.63) (xy 45.72 87.63)",
        "\t\t\t(xy 38.1 87.63) (xy 39.37 87.63)",
        "Y1 XL1 wire -> label anchor",
    ),
    (
        "\t\t\t(xy 38.1 95.25) (xy 45.72 95.25)",
        "\t\t\t(xy 38.1 95.25) (xy 39.37 95.25)",
        "Y1 XL2 wire -> label anchor",
    ),
    # E73 pins whose old wires extended beyond a label and ended in free space.
    (
        "\t\t\t(xy 99.06 36.83) (xy 109.22 36.83)",
        "\t\t\t(xy 99.06 36.83) (xy 101.6 36.83)",
        "U1 VDDH wire -> VBAT label anchor",
    ),
    (
        "\t\t\t(xy 99.06 71.12) (xy 109.22 71.12)",
        "\t\t\t(xy 99.06 71.12) (xy 102.87 71.12)",
        "U1 GND24 wire -> GND label anchor",
    ),
    (
        "\t\t\t(xy 99.06 73.66) (xy 109.22 73.66)",
        "\t\t\t(xy 99.06 73.66) (xy 102.87 73.66)",
        "U1 GND21 wire -> GND label anchor",
    ),
    # Shunt low side: stop at GND label anchor instead of extending to free space.
    (
        "\t\t\t(xy 162.56 138.43) (xy 172.72 138.43)",
        "\t\t\t(xy 162.56 138.43) (xy 166.37 138.43)",
        "RSH1 low-side wire -> GND label anchor",
    ),
]


def find_balanced_block(text: str, start: int) -> tuple[int, int]:
    if text[start] != "(":
        raise ValueError(f"expected '(' at byte {start}")
    depth = 0
    in_string = False
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return start, i + 1
    raise ValueError("unterminated s-expression")


def replace_idempotent(text: str, old: str, new: str, description: str) -> tuple[str, str | None]:
    old_count = text.count(old)
    new_count = text.count(new)
    if old_count == 1 and new_count == 0:
        return text.replace(old, new, 1), description
    if old_count == 0 and new_count == 1:
        return text, None
    raise ValueError(
        f"{description}: expected exactly one old or one canonical form; "
        f"found old={old_count}, canonical={new_count}"
    )


def remove_cell_negative_tail(text: str) -> tuple[str, str | None]:
    """CELL1- has its GND label directly on the pin; remove the redundant tail."""
    needle = "\t\t\t(xy 172.72 127) (xy 177.8 127)"
    if needle not in text:
        # Canonical state: no such wire. The label itself remains at the CELL1 pin.
        return text, None

    hit = text.index(needle)
    wire_marker = "\t(wire\n"
    wire_line = text.rfind(wire_marker, 0, hit)
    if wire_line < 0:
        raise ValueError("CELL1 negative tail: containing wire block not found")
    start = wire_line + 1
    start, end = find_balanced_block(text, start)
    block = text[start:end]
    if needle not in block:
        raise ValueError("CELL1 negative tail: wrong containing wire block")

    # Remove the leading tab together with the expression; retain one newline.
    return text[:wire_line] + text[end:] , "CELL1 negative redundant GND wire removed"


def normalize(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    for old, new, description in REPLACEMENTS:
        text, changed = replace_idempotent(text, old, new, description)
        if changed:
            changes.append(changed)
    text, changed = remove_cell_negative_tail(text)
    if changed:
        changes.append(changed)
    return text, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--file", type=Path, default=SCHEMATIC)
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8")
    normalized, changes = normalize(text)

    if args.check:
        if changes:
            print("Schematic geometry needs normalization:")
            for change in changes:
                print(f"  - {change}")
            return 1
        print("Schematic geometry is normalized.")
        return 0

    if changes:
        args.file.write_text(normalized, encoding="utf-8", newline="\n")
        print(f"Updated {args.file}:")
        for change in changes:
            print(f"  - {change}")
    else:
        print(f"No geometry changes needed: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
