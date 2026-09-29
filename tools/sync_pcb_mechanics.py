#!/usr/bin/env python3
"""Synchronize production-board mechanics from the Hammond 1554BPL template.

The mechanical template is the single dimensional source for:
- Edge.Cuts profile
- H1/H2 enclosure mounting holes
- E73 antenna keepout
- mechanical placement/optical guides

This lets KiCad F8 update electrical footprints without creating a second,
independently maintained copy of the enclosure geometry.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "hardware" / "poa-sensor.kicad_pcb"
TEMPLATE = ROOT / "hardware" / "poa-sensor-layout-template.kicad_pcb"

# Stable UUIDs of the User.1/Dwgs.User placement and optical guides owned by the
# mechanical template. Keeping an explicit list avoids deleting unrelated user
# annotations that may be added to the production board later.
MECHANICAL_GUIDE_UUIDS = {
    "f0df077f-bc0c-4e19-bbbd-7506dd57b0a1",  # U1 guide
    "b6dcc158-666d-4932-9a6c-a1ffde0b1472",  # U1 label
    "2a90a70a-b40e-4069-b2f8-c7c8805190ad",  # CELL1 guide
    "0fbe4585-a5d2-4a7d-ad2b-a92fce6973ca",  # CELL1 label
    "d770d0ab-dfe6-4162-aa69-813340e27c1f",  # analog guide
    "eca07e67-6809-485d-9043-4db2d6a890fe",  # analog label
    "a478853f-7633-4554-8fc9-15f81a02b488",  # J1 guide
    "f6697070-e247-4cd3-b754-ffe072c1d1ee",  # J1 label
    "a197c6d3-9d17-43a8-8208-be5e8b4d601c",  # J2 guide
    "134da89b-78af-4926-ab1b-ae684fb586bc",  # J2 label
    "b747f5e8-4707-44db-aa68-7ea65193e075",  # battery guide
    "ad57220d-38a2-462f-a9e6-c5312e73fc8b",  # battery label
    "0a225cb4-54e7-4877-94ef-982612546352",  # optical clear area
    "cb454324-bcda-4c37-b21a-6408fd38a2b5",  # optical label
    "33079fba-4ab9-48ce-bd47-b45bda0803fc",  # H1/H2 note
    "7e944d37-f1f2-4f54-b6a3-d5606be8243a",  # Edge.Cuts source note
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


def top_level_blocks(text: str):
    """Yield root-child s-expression blocks from a KiCad board file."""
    for m in re.finditer(r"(?m)^\t\(", text):
        start = m.start() + 1
        try:
            start, end = find_balanced_block(text, start)
        except ValueError:
            continue
        yield start, end, text[start:end]


def reference_of(block: str) -> str | None:
    m = re.search(r'\(property\s+"Reference"\s+"([^"]+)"', block)
    if m:
        return m.group(1)
    m = re.search(r'\(fp_text\s+reference\s+"?([^"\s\)]+)', block)
    return m.group(1) if m else None


def uuid_of(block: str) -> str | None:
    m = re.search(r'\(uuid\s+"?([0-9a-fA-F-]{36})"?\)', block)
    return m.group(1).lower() if m else None


def is_edge_block(block: str) -> bool:
    return (
        (block.startswith("(gr_line") or block.startswith("(gr_arc"))
        and '(layer "Edge.Cuts")' in block
    )


def is_mount_block(block: str) -> bool:
    return block.startswith("(footprint") and reference_of(block) in {"H1", "H2"}


def is_rf_keepout(block: str) -> bool:
    return block.startswith("(zone") and '(name "E73 antenna keepout")' in block


def is_mechanical_guide(block: str) -> bool:
    uid = uuid_of(block)
    return uid in MECHANICAL_GUIDE_UUIDS if uid else False


def is_mechanical_block(block: str) -> bool:
    return (
        is_mount_block(block)
        or is_edge_block(block)
        or is_rf_keepout(block)
        or is_mechanical_guide(block)
    )


def select_mechanics(text: str) -> list[str]:
    selected: list[str] = []
    for _, _, block in top_level_blocks(text):
        if is_mechanical_block(block):
            selected.append(block)
    return selected


def strip_mechanics(text: str) -> str:
    edits: list[tuple[int, int]] = []
    for start, end, block in top_level_blocks(text):
        if is_mechanical_block(block):
            edits.append((start, end))

    for start, end in sorted(edits, reverse=True):
        # Include one preceding tab/newline pair where practical so repeated runs
        # do not accumulate blank lines.
        left = start
        if left >= 1 and text[left - 1] == "\t":
            left -= 1
        if left >= 1 and text[left - 1] == "\n":
            left -= 1
        text = text[:left] + text[end:]
    return text


def synchronize(board_text: str, template_text: str) -> str:
    mechanics = select_mechanics(template_text)
    edge_count = sum(is_edge_block(block) for block in mechanics)
    mount_refs = {reference_of(block) for block in mechanics if is_mount_block(block)}
    rf_count = sum(is_rf_keepout(block) for block in mechanics)
    guide_uuids = {
        uuid_of(block) for block in mechanics if is_mechanical_guide(block)
    }

    if edge_count != 10:
        raise ValueError(f"expected 10 1554BPL Edge.Cuts primitives, found {edge_count}")
    if mount_refs != {"H1", "H2"}:
        raise ValueError(f"expected H1/H2 mounting holes, found {sorted(mount_refs)}")
    if rf_count != 1:
        raise ValueError(f"expected one E73 antenna keepout, found {rf_count}")
    if guide_uuids != MECHANICAL_GUIDE_UUIDS:
        missing = sorted(MECHANICAL_GUIDE_UUIDS - guide_uuids)
        extra = sorted(guide_uuids - MECHANICAL_GUIDE_UUIDS)
        raise ValueError(f"mechanical guide UUID mismatch; missing={missing}, extra={extra}")

    clean = strip_mechanics(board_text).rstrip()
    if not clean.endswith(")"):
        raise ValueError("production board does not end with root ')' s-expression")

    # Insert mechanics as root children immediately before the final root ')'.
    body = clean[:-1].rstrip()
    injected = "\n\n".join("\t" + block.replace("\n", "\n\t") for block in mechanics)
    return body + "\n\n" + injected + "\n)\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--file", type=Path, default=BOARD)
    ap.add_argument("--template", type=Path, default=TEMPLATE)
    args = ap.parse_args()

    board_text = args.file.read_text(encoding="utf-8")
    template_text = args.template.read_text(encoding="utf-8")
    updated = synchronize(board_text, template_text)

    if args.check:
        if updated != board_text:
            print("PCB mechanics differ from canonical Hammond 1554BPL template.")
            return 1
        print("PCB mechanics match canonical Hammond 1554BPL template.")
        return 0

    if updated != board_text:
        args.file.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Synchronized 1554BPL mechanics into {args.file}")
    else:
        print(f"No mechanical changes needed: {args.file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
