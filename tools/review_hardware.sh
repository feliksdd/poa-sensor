#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
out=hardware/review_2026-11-10
mkdir -p "$out"
kicad-cli version
kicad-cli sch erc --format json --severity-all --exit-code-violations -o "$out/ERC.json" hardware/poa-sensor.kicad_sch
kicad-cli sch export netlist --format kicadxml -o "$out/netlist.xml" hardware/poa-sensor.kicad_sch
python3 tools/check_wired_netlist.py "$out/netlist.xml" --bom bom/bom.csv > "$out/interface_check.json"
kicad-cli sch export svg -o "$out/" hardware/poa-sensor.kicad_sch
kicad-cli sch export pdf -o "$out/poa-sensor.pdf" hardware/poa-sensor.kicad_sch
python3 - <<'PY'
from pathlib import Path
import hashlib,json
p=Path('hardware/review_2026-11-10')
inputs=['hardware/poa-sensor.kicad_sch','hardware/poa-sensor.kicad_pro','hardware/symbols/poa-sensor.kicad_sym','bom/bom.csv']
(p/'source_hashes.json').write_text(json.dumps({s:hashlib.sha256(Path(s).read_bytes()).hexdigest() for s in inputs},indent=2)+'\n')
PY
# No wired PCB exists: do not run parity against the explicitly archived RF board.
