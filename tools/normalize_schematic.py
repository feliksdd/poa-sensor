#!/usr/bin/env python3
"""
Normalize the one-time legacy -> KiCad 8 schematic conversion.

The legacy bootstrap schematic contained three project-local symbols. KiCad's first
conversion preserved placed symbol references but did not embed their native symbol
definitions/pins. This tool repairs that conversion deterministically and also fixes
known component metadata before the first PCB is generated.

It is intentionally narrow: only known references/library IDs are modified.
"""
from __future__ import annotations

import argparse
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARDWARE = ROOT / "hardware"
SCHEMATIC = HARDWARE / "poa-sensor.kicad_sch"
SYMBOL_LIBRARY = HARDWARE / "symbols" / "poa-sensor.kicad_sym"

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

CUSTOM = {
    "U1": {
        "old_lib_ids": {"poa-sensor-cache:E73-2G4M08S1C", "POA:E73-2G4M08S1C"},
        "lib_id": "POA:E73-2G4M08S1C",
        "symbol": "E73-2G4M08S1C",
        "pins": ["5", "11", "12", "13", "14", "19", "21", "22", "23", "24", "25", "26", "37", "39"],
    },
    "U2": {
        "old_lib_ids": {"poa-sensor-cache:ADS1115IDGSR", "POA:ADS1115IDGSR"},
        "lib_id": "POA:ADS1115IDGSR",
        "symbol": "ADS1115IDGSR",
        "pins": [str(i) for i in range(1, 11)],
    },
    "CELL1": {
        "old_lib_ids": {"poa-sensor-cache:KXOB25-14X1F", "POA:KXOB25-14X1F"},
        "lib_id": "POA:KXOB25-14X1F",
        "symbol": "KXOB25-14X1F",
        "pins": ["1", "2"],
    },
}

PIN_UUID_NAMESPACE = uuid.UUID("92242af3-a268-4fe6-a472-c96f445f6b15")


def find_balanced_block(text: str, start: int) -> tuple[int, int]:
    """Return [start,end) for an s-expression beginning at start."""
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


def placed_symbol_blocks(text: str):
    # Placed root-sheet symbols are indented with exactly one tab.
    # Library symbols are nested under lib_symbols and have two tabs.
    for m in re.finditer(r"(?m)^\t\(symbol\n", text):
        start = m.start() + 1
        start, end = find_balanced_block(text, start)
        block = text[start:end]
        ref_m = re.search(r'\(property "Reference" "([^"]+)"', block)
        if ref_m:
            yield ref_m.group(1), start, end, block


def replace_property(block: str, name: str, value: str) -> tuple[str, bool]:
    pattern = re.compile(rf'(\(property "{re.escape(name)}" ")[^"]*(")')
    new, n = pattern.subn(lambda m: m.group(1) + value + m.group(2), block, count=1)
    if n != 1:
        raise ValueError(f'property "{name}" not found exactly once')
    return new, new != block


def replace_on_board(block: str, value: str) -> tuple[str, bool]:
    new, n = re.subn(r"\(on_board (?:yes|no)\)", f"(on_board {value})", block, count=1)
    if n != 1:
        raise ValueError("on_board not found exactly once")
    return new, new != block


def repair_custom_placed_symbol(ref: str, block: str) -> tuple[str, list[str]]:
    cfg = CUSTOM[ref]
    changes: list[str] = []

    m = re.search(r'\(lib_id "([^"]+)"\)', block)
    if not m:
        raise ValueError(f"{ref}: lib_id missing")
    current = m.group(1)
    if current not in cfg["old_lib_ids"]:
        raise ValueError(f"{ref}: unexpected lib_id {current!r}")
    if current != cfg["lib_id"]:
        block = block[:m.start(1)] + cfg["lib_id"] + block[m.end(1):]
        changes.append(f"{ref}: lib_id -> {cfg['lib_id']}")

    expected_pins = list(cfg["pins"])
    existing_pins = re.findall(r'(?m)^\t\t\(pin "([^"]+)"', block)
    if existing_pins:
        if set(existing_pins) != set(expected_pins):
            raise ValueError(
                f"{ref}: unexpected placed-pin set {existing_pins}; expected {expected_pins}"
            )
    else:
        pin_text = ""
        for pin in expected_pins:
            puid = uuid.uuid5(PIN_UUID_NAMESPACE, f"{ref}:{pin}")
            pin_text += f'\t\t(pin "{pin}"\n\t\t\t(uuid "{puid}")\n\t\t)\n'
        marker = "\t\t(instances\n"
        idx = block.find(marker)
        if idx < 0:
            raise ValueError(f"{ref}: instances marker not found")
        block = block[:idx] + pin_text + block[idx:]
        changes.append(f"{ref}: embedded {len(expected_pins)} placed pin UUIDs")

    return block, changes


def extract_project_lib_symbols() -> dict[str, str]:
    text = SYMBOL_LIBRARY.read_text(encoding="utf-8")
    result: dict[str, str] = {}
    for m in re.finditer(r'(?m)^\t\(symbol "([^"]+)"', text):
        name = m.group(1)
        start = m.start() + 1
        start, end = find_balanced_block(text, start)
        result[name] = text[start:end]
    return result


def embed_project_lib_symbols(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    wanted = extract_project_lib_symbols()

    marker = "\t(lib_symbols\n"
    pos = text.find(marker)
    if pos < 0:
        raise ValueError("lib_symbols block missing")
    lib_start = pos + 1
    _, lib_end = find_balanced_block(text, lib_start)
    lib_block = text[lib_start:lib_end]

    additions: list[str] = []
    for cfg in CUSTOM.values():
        name = cfg["symbol"]
        embedded_name = f"POA:{name}"
        if re.search(rf'\(symbol "{re.escape(embedded_name)}"', lib_block):
            continue
        if name not in wanted:
            raise ValueError(f"project symbol {name!r} missing from {SYMBOL_LIBRARY}")
        block = wanted[name]
        block = block.replace(f'(symbol "{name}"', f'(symbol "{embedded_name}"', 1)
        # One additional tab because the schematic nests library symbols in lib_symbols.
        block = "\n".join("\t" + line for line in block.splitlines())
        additions.append(block)
        changes.append(f"lib_symbols: embedded {embedded_name}")

    if additions:
        # Insert before the closing parenthesis of (lib_symbols ...).
        insert_at = lib_end - 1
        payload = "\n" + "\n".join(additions) + "\n\t"
        text = text[:insert_at] + payload + text[insert_at:]

    return text, changes


def normalize(text: str) -> tuple[str, list[str]]:
    blocks = {ref: (start, end, block) for ref, start, end, block in placed_symbol_blocks(text)}
    required = set(EXPECTED) | set(ON_BOARD) | set(CUSTOM)
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

        if ref in CUSTOM:
            block, custom_changes = repair_custom_placed_symbol(ref, block)
            changes.extend(custom_changes)

        if block != original:
            edits.append((start, end, block))

    # Apply placed-symbol edits from end to start so offsets stay valid.
    for start, end, block in sorted(edits, reverse=True):
        text = text[:start] + block + text[end:]

    text, lib_changes = embed_project_lib_symbols(text)
    changes.extend(lib_changes)
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

    for ref, cfg in CUSTOM.items():
        block = blocks.get(ref)
        if block is None:
            issues.append(f"{ref}: symbol missing")
            continue
        m = re.search(r'\(lib_id "([^"]+)"\)', block)
        actual_lib = m.group(1) if m else None
        if actual_lib != cfg["lib_id"]:
            issues.append(f"{ref}: lib_id={actual_lib!r}, expected {cfg['lib_id']!r}")
        actual_pins = set(re.findall(r'(?m)^\t\t\(pin "([^"]+)"', block))
        if actual_pins != set(cfg["pins"]):
            issues.append(f"{ref}: pin set mismatch: {sorted(actual_pins)}")
        if f'(symbol "{cfg["lib_id"]}"' not in text:
            issues.append(f"{ref}: embedded lib symbol {cfg['lib_id']} missing")

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
            print("Schematic needs normalization:")
            for change in changes:
                print(f"  - {change}")
            return 1
        print("Schematic is normalized.")
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
