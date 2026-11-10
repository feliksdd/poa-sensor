#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
output_dir="${1:-hardware}"
mkdir -p "$output_dir"
kicad-cli sch export svg -o "$output_dir/" hardware/poa-sensor.kicad_sch
kicad-cli sch export pdf -o "$output_dir/poa-sensor.pdf" hardware/poa-sensor.kicad_sch
python3 - "$output_dir/poa-sensor.svg" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines()) + '\n')
PY
