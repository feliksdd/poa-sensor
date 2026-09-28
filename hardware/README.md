# Hardware

KiCad is the single source of truth for the electrical and PCB design.

## Current project state

The schematic has been converted to the native KiCad 8 format:

- `poa-sensor.kicad_pro`
- `poa-sensor.kicad_sch`

The legacy bootstrap files (`poa-sensor.sch` and `poa-sensor-cache.lib`) are retained temporarily until the native project passes the first complete ERC/PCB parity review. They can then be removed.

## One-time schematic normalization after conversion

The legacy conversion retained a few obsolete metadata values (old NTC1 package and pre-library custom footprint names). Normalize them once with:

```bash
python3 tools/normalize_schematic.py
```

The tool changes only known placed-symbol metadata:

- NTC1 -> TDK `NTCG063JF103FTBA`, 0201, LCSC `C29553871`
- NTC2 -> off-board (`on_board no`)
- J1 -> `POA:SWD_Pogo_1x05_P2.00mm`
- J2 -> `POA:WirePads_1x02_P2.54mm`
- BT1 -> `POA:WirePads_1x02_P2.54mm`

After running it, open/save the schematic once in KiCad and commit the resulting `.kicad_sch`.

## Schematic scope v0.1

Revision 0.1 contains:

- Ebyte E73-2G4M08S1C / nRF52840
- Li-SOCl2 battery connected to VDDH
- REG0 2.4 V output and 10 uH DC/DC path
- 32.768 kHz LF crystal
- ADS1115 on I2C
- KXOB25-14X1F reference cell
- 1.000 ohm Kelvin-sensed shunt
- differential ADC input filter
- switched reference-cell NTC divider
- switched external module-temperature NTC divider
- connectorless SWD/pogo interface
- battery measurement via internal nRF52840 VDDH/5 SAADC source

Electrical rationale and firmware requirements are in `../docs/architecture.md`.

## Footprint library

Project-local custom footprints are in:

`footprints/poa-sensor.pretty/`

Current custom parts:

- `E73-2G4M08S1C`
- `KXOB25-14X1F`
- `SWD_Pogo_1x05_P2.00mm`
- `WirePads_1x02_P2.54mm`

The project library alias is `POA` via `fp-lib-table`.

## PCB baseline

`poa-sensor-layout-template.kicad_pcb` contains the mechanical baseline before schematic footprints are imported:

- 52 x 52 mm board outline
- optical/reference-cell zone
- E73 placement guide at the right board edge
- real all-layer E73 antenna rule-area keepout
- analog-island placement guide
- J1/J2/battery placement guides

To create the first electrical PCB:

1. Normalize and save `poa-sensor.kicad_sch`.
2. Copy/rename `poa-sensor-layout-template.kicad_pcb` to `poa-sensor.kicad_pcb`.
3. Open the project in KiCad PCB Editor.
4. Run **Tools -> Update PCB from Schematic (F8)**.
5. Place components according to the User.1 guides; keep U1 unrotated with its antenna end at the right board edge.
6. Save and commit `poa-sensor.kicad_pcb`.

After that point routing can be done directly on the native board file.

## Routing constraints

Do not route until the custom E73 and KXOB footprints have been checked dimension-by-dimension against manufacturer drawings. The irradiance shunt must use true Kelvin routing: the reference-cell current path and ADC sense pair must not share copper segments. The E73 antenna keepout applies on both copper layers and to nearby components/metalwork.

The intended layer strategy is a mostly continuous GND plane on B.Cu, signals/components on F.Cu, with the RF keepout removed from both layers.
