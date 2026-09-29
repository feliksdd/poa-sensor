#!/usr/bin/env python3
"""Deterministically place POA-sensor footprints after KiCad F8 schematic sync.

Workflow:
  1. Normalize/save the schematic.
  2. Open hardware/poa-sensor.kicad_pcb and run Update PCB from Schematic (F8).
  3. Save the board.
  4. Run: python3 tools/sync_pcb_mechanics.py
  5. Run: python3 tools/place_pcb.py
  6. Re-open/save the board in KiCad and review placement.

This script only changes the top-level `(at ...)` field of known electrical
footprints. Mechanical outline and mounting-hole synchronization is handled by
`sync_pcb_mechanics.py`.

`--allow-missing` is intended only for mechanical bring-up of a partially
synchronized PCB. It applies canonical placement to all footprints that are
present while still reporting the missing references. Normal release checks
must run without this option.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware" / "poa-sensor.kicad_pcb"

# KiCad board coordinates in mm.
# Mechanical datum/bounding box follows the Hammond 1554BPL steel panel:
#   X = 100.00 ... 155.96 mm
#   Y = 100.00 ... 155.96 mm
# The profile is asymmetric because of the enclosure corner/boss clearances.
# H1 = (127.98, 116.47), H2 = (127.98, 137.99).
# U1 footprint antenna is on +X, therefore rotation 0 points it at the right wall.
PLACEMENT: dict[str, tuple[float, float, float]] = {
    # RF / MCU — shifted down from the former upper-right corner so the E73
    # clears the 1554BPL top-right radius while keeping the antenna near +X wall.
    "U1": (144.0, 117.5, 0.0),
    "L1": (133.8, 116.5, 90.0),
    "C2": (135.2, 118.2, 0.0),
    "C3": (133.8, 113.5, 0.0),
    "C4": (136.8, 118.2, 0.0),
    "Y1": (133.0, 111.0, 0.0),
    "C7": (130.8, 110.5, 90.0),
    "C8": (130.8, 112.5, 90.0),

    # Optical head — KXOB long axis rotated 90 degrees to occupy the large
    # unobstructed left-hand area of the Hammond steel-panel profile.
    "CELL1": (115.0, 114.5, 90.0),
    "NTC1": (115.0, 114.5, 90.0),  # intentional physical overlap below cell

    # Irradiance analog island. Keep clear of H1/H2 screw/washer volumes.
    "RSH1": (132.0, 126.5, 0.0),
    "R7": (134.7, 125.5, 0.0),
    "R8": (134.7, 128.0, 0.0),
    "C9": (136.8, 126.8, 90.0),
    "U2": (139.7, 129.5, 0.0),
    "C5": (139.0, 133.2, 0.0),
    "C6": (141.0, 133.2, 0.0),
    "R3": (144.0, 128.2, 90.0),
    "R4": (144.0, 131.0, 90.0),

    # Temperature-divider components — left/mid-lower area, away from H1/H2.
    "R1": (113.0, 131.0, 0.0),
    "C10": (116.0, 131.0, 0.0),
    "R2": (113.0, 135.0, 0.0),
    "C11": (116.0, 135.0, 0.0),

    # Battery and service interfaces. Battery itself is below the PCB and must
    # clear both enclosure mounting bosses/screws.
    "C1": (140.5, 141.5, 0.0),
    "BT1": (129.5, 148.5, 0.0),
    "J2": (116.0, 150.0, 0.0),
    "J1": (137.5, 150.0, 0.0),
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
        pm = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
        if pm:
            ref = pm.group(1)
        else:
            tm = re.search(r'\(fp_text\s+reference\s+"?([^"\s\)]+)', block)
            if tm:
                ref = tm.group(1)
        if ref:
            yield ref, start, end, block


def replace_top_level_at(block: str, x: float, y: float, rot: float) -> str:
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

    expected = set(PLACEMENT)
    missing = sorted(expected - present)

    for start, end, block in sorted(edits, reverse=True):
        text = text[:start] + block + text[end:]
    return text, changed, missing


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument(
        "--allow-missing",
        action="store_true",
        help="apply placement to present footprints but do not fail on missing refs",
    )
    ap.add_argument("--file", type=Path, default=BOARD)
    args = ap.parse_args()

    text = args.file.read_text(encoding="utf-8")
    updated, changes, missing = place(text)

    if missing:
        print("Board is missing expected footprints (run KiCad F8 first):")
        for ref in missing:
            print(f"  - {ref}")
        if not args.allow_missing:
            return 2
        print("Continuing because --allow-missing was requested; release check remains open.")

    if args.check:
        if changes:
            print("PCB placement differs from canonical 1554BPL placement:")
            for change in changes:
                print(f"  - {change}")
            return 1
        print("PCB placement matches canonical 1554BPL placement for all present footprints.")
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
