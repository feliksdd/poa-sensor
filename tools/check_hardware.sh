#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
output_dir="${1:-build/kicad}"
mkdir -p "$output_dir"
kicad-cli version
kicad-cli sch erc --format json --severity-all --exit-code-violations -o "$output_dir/ERC.json" hardware/poa-sensor.kicad_sch
kicad-cli sch export netlist --format kicadxml -o "$output_dir/netlist.xml" hardware/poa-sensor.kicad_sch
python3 tools/check_wired_netlist.py "$output_dir/netlist.xml" --bom bom/bom.csv > "$output_dir/interface_check.json"
bash tools/export_schematic.sh "$output_dir"
kicad-cli pcb drc --format json --schematic-parity -o "$output_dir/DRC.json" hardware/poa-sensor.kicad_pcb
python3 tools/check_pcb.py "$output_dir/netlist.xml" "$output_dir/DRC.json" > "$output_dir/placement_check.json"
kicad-cli pcb export svg --mode-single --layers F.Cu,F.SilkS,Edge.Cuts -o "$output_dir/poa-placement.svg" hardware/poa-sensor.kicad_pcb
kicad-cli pcb export svg --mode-single --layers Dwgs.User,User.1,Edge.Cuts -o "$output_dir/poa-mechanics.svg" hardware/poa-sensor.kicad_pcb
