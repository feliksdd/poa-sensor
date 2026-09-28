#!/usr/bin/env python3
"""
Normalize known POA-sensor schematic metadata after one-time legacy -> KiCad 8 conversion.

This script intentionally touches only placed top-level symbol blocks, identified by
their Reference property. It does not rewrite library symbol definitions.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMATIC = ROOT / "hardware" / "poa-sensor.kicad_sch"

EXPECTED = {
    "NTC1": {
        "Value": "NTCG063JF103FTBA",
        "Footprint": "Resistor_SMD:R_0201_0603Metric",
        "LCSC": "C29553871",
    },
    "J1": {
        "Footprint": "POA:SWD_Pogo_1x05_P2.00mm",
    },
    "J2": {
        "Footprint": "POA:WirePads_1x02_P2.54mm",
    },
    "BT1": {
        "Footprint": "POA:WirePads_1x02_P2.54mm",
    },
}

ON_BOARD = {
    "NTC2": "no",
}


def find_balanced_block(text: str, start: int) -> tuple[int, int]:
    """Return [start,end) for an s-expression beginning at start."""
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


def placed_symbol_blocks(text: str):
    # Placed root-sheet symbols are indented with exactly one tab.
    # Library symbols are nested under lib_symbols and have two tabs.
    for m in re.finditer(r"(?m)^\t\(symbol\n", text):
        start, end = find_balanced_block(text, m.start() + 1)
        block = text[start:end]
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block)
        if ref_m:
            yield ref_m.group(1), start, end, block


def replace_property(block: str, name: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(
        rf'(\(property "{re.escape(name)}" ")[^"]*(")',
        flags=re.MULTILINE,
    )
    new, n = pattern.subn(lambda m: m.group(1) + value + m.group(2), block, count=1)
    if n != 1:
        raise ValueError(f'property "{name}" not found exactly once')
    return new, new != block


def replace_on_board(block: str, value: str) -> tuple[str, bool]:
    new, n = re.subn(r"\(on_board (?:yes|no)\)", f"(on_board {value})", block, count=1)
    if n != 1:
        raise ValueError("on_board not found exactly once")
    return new, new != block


def normalize(text: str) -> tuple[str, list[str]]:
    blocks = {ref: (start, end, block) for ref, start, end, block in placed_symbol_blocks(text)}
    required = set(EXPECTED) | set(ON_BOARD)
    missing = required - blocks.keys()
    if missing:
        raise ValueError(f"missing placed symbols: {sorted(missing)}")

    edits: list[tuple[int, int, str]] = []
    changes: list[str] = []

    for ref in sorted(required):
        start, end, block = blocks[ref]
        original = block

        for prop, value in EXPECTED.get(ref, {}).items():
            block, changed = replace_property(block, prop, value)
            if changed:
                changes.append(f"{ref}: {prop} -> {value}")

        if ref in ON_BOARD:
            block, changed = replace_on_board(block, ON_BOARD[ref])
            if changed:
                changes.append(f"{ref}: on_board -> {ON_BOARD[ref]}")

        if block != original:
            edits.append((start, end, block))

    # Apply from end to start so offsets stay valid.
    for start, end, block in sorted(edits, reverse=True):
        text = text[:start] + block + text[end:]

    return text, changes


def verify(text: str) -> list[str]:
    issues: list[str] = []
    blocks = {ref: block for ref, _, _, block in placed_symbol_blocks(text)}

    for ref, props in EXPECTED.items():
        block = blocks.get(ref)
        if block is None:
            issues.append(f"{ref}: symbol missing")
            continue
        for name, expected in props.items():
            m = re.search(rf'\(property "{re.escape(name)}" "([^"]*)"', block)
            actual = m.group(1) if m else None
            if actual != expected:
                issues.append(f"{ref}: {name}={actual!r}, expected {expected!r}")

    for ref, expected in ON_BOARD.items():
        block = blocks.get(ref)
        if block is None:
            issues.append(f"{ref}: symbol missing")
            continue
        m = re.search(r"\(on_board (yes|no)\)", block)
        actual = m.group(1) if m else None
        if actual != expected:
            issues.append(f"{ref}: on_board={actual!r}, expected {expected!r}")

    # Sanity checks that must remain true.
    for ref, fp in {
        "U1": "POA:E73-2G4M08S1C",
        "CELL1": "POA:KXOB25-14X1F",
    }.items():
        block = blocks.get(ref)
        if block is None:
            issues.append(f"{ref}: symbol missing")
            continue
        m = re.search(r'\(property "Footprint" "([^"]*)"', block)
        actual = m.group(1) if m else None
        if actual != fp:
            issues.append(f"{ref}: Footprint={actual!r}, expected {fp!r}")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="do not write; fail if normalization is needed")
    ap.add_argument("--file", type=Path, default=SCHEMATIC)
    args = ap.parse_args()

    path = args.file
    text = path.read_text(encoding="utf-8")

    normalized, changes = normalize(text)
    issues = verify(normalized)
    if issues:
        print("Normalization result is inconsistent:")
        for issue in issues:
            print(f"  - {issue}")
        return 2

    if args.check:
        if changes:
            print("Schematic metadata needs normalization:")
            for change in changes:
                print(f"  - {change}")
            return 1
        print("Schematic metadata is normalized.")
        return 0

    if changes:
        path.write_text(normalized, encoding="utf-8", newline="\n")
        print(f"Updated {path}:")
        for change in changes:
            print(f"  - {change}")
    else:
        print(f"No changes needed: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
