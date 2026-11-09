#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p hardware/review_2026-11-09
kicad-cli version
kicad-cli sch erc --format json --severity-all --exit-code-violations -o hardware/review_2026-11-09/ERC.json hardware/poa-sensor-wired.kicad_sch
