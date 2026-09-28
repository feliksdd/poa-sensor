# Hardware

KiCad is the single source of truth for the electrical and PCB design.

## Current project state

Native KiCad 8 project files now exist:

- `poa-sensor.kicad_pro`
- `poa-sensor.kicad_sch`
- `poa-sensor.kicad_pcb`

The PCB currently contains the **mechanical baseline only**: board outline, optical window guide and the RF antenna keepout. Electrical footprints are intentionally imported from the schematic in KiCad using F8 so KiCad creates the correct symbol/footprint UUID and net relationships.

The legacy bootstrap files (`poa-sensor.sch` and `poa-sensor-cache.lib`) are retained temporarily until the native project passes the first complete ERC/PCB parity review. They can then be removed.

## Normalize the converted schematic before first PCB sync

The legacy conversion retained a few obsolete metadata values (old NTC1 package and pre-library custom footprint names). Normalize them once with:

```bash
python3 tools/normalize_schematic.py
python3 tools/normalize_geometry.py
```

The normalization changes only known/audited items, including:

- NTC1 -> TDK `NTCG063JF103FTBA`, 0201, LCSC `C29553871`
- NTC2 -> off-board (`on_board no`)
- J1 -> `POA:SWD_Pogo_1x05_P2.00mm`
- J2 -> `POA:WirePads_1x02_P2.54mm`
- BT1 -> `POA:WirePads_1x02_P2.54mm`
- native custom symbol IDs/pins for U1, U2 and CELL1
- known harmless geometry artifacts from the legacy conversion

After running both scripts, open/save `poa-sensor.kicad_sch` once in KiCad and commit it.

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

`poa-sensor.kicad_pcb` is now the real board file and contains:

- 52 x 52 mm board outline
- optical/reference-cell zone
- E73 placement guide at the right board edge
- real all-layer E73 antenna rule-area keepout
- analog-island placement guide
- J1/J2/battery placement guides

`poa-sensor-layout-template.kicad_pcb` remains only as the historical/mechanical template and may later be removed.

### First electrical PCB synchronization

1. Run both schematic normalization scripts above.
2. Open/save the schematic in KiCad.
3. Open `poa-sensor.kicad_pcb` in PCB Editor.
4. Run **Tools -> Update PCB from Schematic (F8)**.
5. Save the board. Do not manually route yet.
6. Run:

```bash
python3 tools/place_pcb.py
```

7. Re-open/save the PCB in KiCad and visually review the placement.
8. Commit the resulting `.kicad_sch` and `.kicad_pcb`.

`place_pcb.py` only changes the top-level position/rotation of known footprints. It deliberately does not alter nets, pads, footprints, zones or routing.

## Placement baseline

The canonical placement currently targets:

- U1 E73 at the upper-right edge, antenna facing +X/right
- CELL1 KXOB in the optical area at upper-left/center
- NTC1 directly underneath CELL1 (intentional courtyard overlap)
- RSH1, R7/R8, C9 and U2 as a tight analog island immediately beside CELL1
- LF crystal and its capacitors close to U1 XL1/XL2
- REG0 inductor/decoupling close to U1 power pins
- J2 at the lower-left cable-entry edge
- J1 SWD pogo pads at lower-right
- battery wire pads near the lower center; the 1/2-AA battery sits below the PCB

The exact coordinates are version-controlled in `../tools/place_pcb.py`.

## Routing constraints

Do not route before the F8 import/placement review is complete.

Important constraints:

- the irradiance shunt must use **true Kelvin routing**; the reference-cell current path and ADS1115 sense pair must not share copper segments
- keep the RSH1 -> R7/R8 -> U2 differential pair short and symmetric
- keep radio/clock currents out of the analog island
- use a mostly continuous GND plane on B.Cu
- no copper, traces, vias or parts inside the E73 antenna keepout on either copper layer
- avoid battery, cable and metal mounting hardware in front of the antenna
- NTC1 is intentionally mounted below CELL1; verify physical clearance on the first assembled prototype

## CI / ERC / DRC

GitHub Actions runs KiCad ERC on the native schematic. PCB DRC with schematic parity activates automatically once the board actually contains imported schematic footprints. The mechanical-only PCB baseline intentionally skips parity DRC.
