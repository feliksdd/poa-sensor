#!/usr/bin/env python3
"""Generate project-local mechanical-envelope STEP models.

These models are intentionally simple collision/clearance envelopes, not
photorealistic component models. Dimensions come from the manufacturers:

- E73-2G4M08S1C: 18.0 x 13.0 x 0.8 mm
- KXOB25-14X1F: 23.0 x 8.0 x 1.8 mm

The footprint origins are at the body centres in X/Y; model Z=0 is the PCB
surface so the solids extend upward from the board.
"""
from __future__ import annotations

import re
from pathlib import Path

import cadquery as cq
from cadquery import exporters

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "hardware" / "3dmodels"

MODELS = {
    "E73-2G4M08S1C.step": (18.0, 13.0, 0.8),
    "KXOB25-14X1F.step": (23.0, 8.0, 1.8),
}


def export_box(path: Path, x: float, y: float, z: float) -> None:
    solid = cq.Workplane("XY").box(x, y, z, centered=(True, True, False))
    exporters.export(solid, str(path))

    # CadQuery/OpenCascade writes the current time into FILE_NAME. Normalize it
    # so regenerated STEP files stay deterministic in git.
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"('Open CASCADE Shape Model',)'[^']+'",
        r"\1'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (x, y, z) in MODELS.items():
        path = OUT / name
        export_box(path, x, y, z)
        print(f"generated {path.relative_to(ROOT)}: {x} x {y} x {z} mm")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
