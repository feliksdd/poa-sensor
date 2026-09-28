#!/usr/bin/env python3
"""Deterministically place POA-sensor footprints after KiCad F8 schematic sync.

Workflow:
  1. Normalize/save the schematic.
  2. Open hardware/poa-sensor.kicad_pcb and run Update PCB from Schematic (F8).
  3. Save the board.
  4. Run: python3 tools/place_pcb.py
  5. Re-open/save the board in KiCad and review placement.

The script only changes the top-level `(at ...)` field of known footprint
references. It deliberately does not route, change nets, footprints, zones or pads.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware" / "poa-sensor.kicad_pcb"

# KiCad board coordinates in mm. Board outline: (100,100) .. (152,152).
# U1 footprint antenna is on +X, therefore rotation 0 points it at right board edge.
PLACEMENT: dict[str, tuple[float, float, float]] = {
    # RF / MCU
    "U1": (142.5, 112.0, 0.0),
    "L1": (131.7, 114.6, 90.0),
    "C2": (133.0, 116.2, 0.0),
    "C3": (132.0, 109.2, 0.0),
    "C4": (134.5, 116.2, 0.0),
    "Y1": (130.6, 106.8, 0.0),
    "C7": (128.6, 106.0, 90.0),
    "C8": (128.6, 108.0, 90.0),

    # Optical head / irradiance analog island
    "CELL1": (115.0, 114.0, 0.0),
    "NTC1": (115.0, 114.0, 0.0),  # intentional physical overlap, NTC below cell
    "RSH1": (123.0, 121.0, 0.0),
    "R7": (126.0, 119.7, 0.0),
    "R8": (126.0, 122.3, 0.0),
    "C9": (128.1, 121.0, 90.0),
    "U2": (131.5, 123.0, 0.0),
    "C5": (131.5, 127.0, 0.0),
    "C6": (133.3, 127.0, 0.0),
    "R3": (136.0, 124.5, 90.0),
    "R4": (136.0, 127.0, 90.0),

    # Temperature-divider components
    "R1": (109.0, 127.5, 0.0),
    "C10": (112.0, 127.5, 0.0),
    "R2": (117.5, 132.0, 0.0),
    "C11": (120.5, 132.0, 0.0),

    # Battery and service interfaces
    "C1": (132.0, 134.5, 0.0),
    "BT1": (122.0, 145.5, 0.0),
    "J2": (106.5, 146.0, 0.0),
    "J1": (142.0, 146.0, 0.0),
}


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
    raise ValueError(f"unterminated s-expression at byte {start}")


def footprint_blocks(text: str):
    for m in re.finditer(r"(?m)^\t\(footprint\s", text):
        start = m.start() + 1
        start, end = find_balanced_block(text, start)
        block = text[start:end]
        ref = None
        # KiCad 8 footprints normally carry a Reference property.
        pm = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        if pm:
            ref = pm.group(1)
        else:
            # Fallback for older footprint text.
            tm = re.search(r'\(fp_text\s+reference\s+"?([^"\s\)]+)', block)
            if tm:
                ref = tm.group(1)
        if ref:
            yield ref, start, end, block


def replace_top_level_at(block: str, x: float, y: float, rot: float) -> str:
    # Footprint's own at-expression is indented two tabs in KiCad 8. Pad/text
    # at-expressions are nested more deeply, so this avoids touching them.
    patt = re.compile(r"(?m)^\t\t\(at\s+[-+0-9.eE]+\s+[-+0-9.eE]+(?:\s+[-+0-9.eE]+)?\)\s*$")
    replacement = f"\t\t(at {x:.3f} {y:.3f} {rot:.3f})"
    new, n = patt.subn(replacement, block, count=1)
    if n != 1:
        raise ValueError("footprint top-level (at ...) not found exactly once")
    return new


def place(text: str) -> tuple[str, list[str], list[str]]:
    edits: list[tuple[int, int, str]] = []
    changed: list[str] = []
    present: set[str] = set()

    for ref, start, end, block in footprint_blocks(text):
        present.add(ref)
        if ref not in PLACEMENT:
            continue
        x, y, rot = PLACEMENT[ref]
        new = replace_top_level_at(block, x, y, rot)
        if new != block:
            edits.append((start, end, new))
            changed.append(f"{ref} -> ({x:.1f}, {y:.1f}) rot {rot:.0f}")

    # NTC2 is intentionally off-board after schematic normalization.
    expected = set(PLACEMENT)
    missing = sorted(expected - present)

    for start, end, block in sorted(edits, reverse=True):
        text = text[:start] + block + text[end:]
    return text, changed, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--file", type=Path, default=BOARD)
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8")
    updated, changes, missing = place(text)

    if missing:
        print("Board is missing expected footprints (run KiCad F8 first):")
        for ref in missing:
            print(f"  - {ref}")
        return 2

    if args.check:
        if changes:
            print("PCB placement differs from canonical placement:")
            for change in changes:
                print(f"  - {change}")
            return 1
        print("PCB placement matches canonical placement.")
        return 0

    if changes:
        args.file.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Updated {args.file}:")
        for change in changes:
            print(f"  - {change}")
    else:
        print(f"No placement changes needed: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
