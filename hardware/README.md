# Hardware

KiCad is the single source of truth for the electrical and PCB design.

## Repository split

The target POA sensor is now **irradiance + reference-cell temperature only**. Module voltage/current/power/energy, module backsheet temperature and PV curtailment are implemented in [PanelLog](https://github.com/feliksdd/panellog).

The current v0.1 KiCad files predate this split and still contain NTC2/J2. They remain documented here so source and documentation agree, but NTC2/J2 are scheduled for removal in the next electrical revision.

## Current project state

Native KiCad 8 project files now exist:

- `poa-sensor.kicad_pro`
- `poa-sensor.kicad_sch`
- `poa-sensor.kicad_pcb`

The PCB contains the electrical footprints imported so far. Mechanical geometry is synchronized from the dedicated Hammond 1554BPL template so the enclosure outline is not maintained independently in two places.

The ADS1115 U2 may be absent in boards synchronized before the footprint-library correction below.

The legacy bootstrap files (`poa-sensor.sch` and `poa-sensor-cache.lib`) are retained temporarily until the native project passes the first complete ERC/PCB parity review. They can then be removed.

## Normalize the converted schematic before PCB sync

The legacy conversion retained a few obsolete metadata values. Run:

```bash
python3 tools/normalize_schematic.py
python3 tools/normalize_geometry.py
python3 tools/fix_u2_footprint.py
```

The normalization/fix steps change only known/audited items, including:

- NTC1 -> TDK `NTCG063JF103FTBA`, 0201, LCSC `C29553871`
- NTC2 -> off-board (`on_board no`)
- J1 -> `POA:SWD_Pogo_1x05_P2.00mm`
- J2 -> `POA:WirePads_1x02_P2.54mm`
- BT1 -> `POA:WirePads_1x02_P2.54mm`
- native custom symbol IDs/pins for U1, U2 and CELL1
- known harmless geometry artifacts from the legacy conversion
- U2 ADS1115 footprint -> `Package_SO:VSSOP-10_3x3mm_P0.5mm`

The last correction is important: the earlier path `Package_TSSOP:VSSOP-10_3x3mm_P0.5mm` is invalid, so KiCad F8 silently/explicitly leaves U2 out of the PCB when that old value is present.

After running the scripts, open/save `poa-sensor.kicad_sch` once in KiCad and commit it.

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
- **legacy v0.1:** switched external module-temperature NTC divider (remove next revision)
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

## PCB mechanical baseline

The former 52 x 52 mm rectangular outline is obsolete.

`poa-sensor-layout-template.kicad_pcb` is now the **mechanical source of truth** and contains:

- `Edge.Cuts` matching the Hammond **1554BPL steel-panel profile**
- H1/H2 mounting holes matching the Hammond panel drawing
- revised optical/reference-cell placement guides
- revised E73 placement zone and all-layer antenna keepout
- revised analog/J1/J2/battery placement guides (J2 is legacy after the PanelLog split)

`tools/sync_pcb_mechanics.py` copies only the mechanical source-of-truth items into the production board:

- Edge.Cuts
- H1/H2
- E73 antenna keepout

This prevents the Hammond contour from diverging between template and production PCB.

### Electrical PCB synchronization

1. Run all three normalization/fix scripts above.
2. Open/save the schematic in KiCad.
3. Open `poa-sensor.kicad_pcb` in PCB Editor.
4. Run **Tools -> Update PCB from Schematic (F8)**.
5. Verify that **U2 is present** and uses `Package_SO:VSSOP-10_3x3mm_P0.5mm`.
6. Save the board. Do not manually route yet.
7. Synchronize the enclosure mechanics:

```bash
python3 tools/sync_pcb_mechanics.py
```

8. Apply the canonical component placement:

```bash
python3 tools/place_pcb.py
```

9. Re-open/save the PCB in KiCad and visually review:
   - steel-panel outline
   - H1/H2 screw clearance
   - E73 antenna clearance
   - CELL1/window alignment
   - analog island clearance
   - J1/J2 edge clearance
   - battery volume below PCB
10. Commit the resulting `.kicad_sch` and `.kicad_pcb`.

Checks can be run without modifying files:

```bash
python3 tools/sync_pcb_mechanics.py --check
python3 tools/place_pcb.py --check
```

## Placement baseline

The canonical placement now targets the Hammond 1554BPL geometry:

- U1 E73 shifted down along the right edge, antenna facing +X/right, clear of the top-right radius
- CELL1 KXOB rotated 90 degrees in the large unobstructed left-hand optical area
- NTC1 directly underneath CELL1 (intentional courtyard overlap)
- RSH1, R7/R8, C9 and U2 in a compact analog island clear of H1/H2
- LF crystal and its capacitors close to U1 XL1/XL2
- REG0 inductor/decoupling close to U1 power pins
- **legacy v0.1:** J2 in the lower-left usable panel area; remove with NTC2 in the next electrical revision
- J1 SWD pogo pads in the lower-right usable area
- battery wire pads near the lower centre; the 1/2-AA battery sits below the PCB and must clear both enclosure mounting bosses/screws

The exact electrical-footprint coordinates are version-controlled in `../tools/place_pcb.py`.
The exact board mechanics are version-controlled in `poa-sensor-layout-template.kicad_pcb`.

## Routing constraints

Do not route before the F8 import/mechanical-sync/placement review is complete.

Important constraints:

- the irradiance shunt must use **true Kelvin routing**; the reference-cell current path and ADS1115 sense pair must not share copper segments
- keep the RSH1 -> R7/R8 -> U2 differential pair short and symmetric
- keep radio/clock currents out of the analog island
- use a mostly continuous GND plane on B.Cu
- no copper, traces, vias or parts inside the E73 antenna keepout on either copper layer
- avoid battery, cable and metal mounting hardware in front of the antenna
- maintain copper/component clearance around H1/H2 and the eventual screw/washer/spacer stack
- NTC1 is intentionally mounted below CELL1; verify physical clearance on the first assembled prototype

## CI / ERC / DRC

GitHub Actions runs KiCad ERC on the native schematic. PCB DRC with schematic parity activates automatically once the board actually contains imported schematic footprints. Mechanical fit still requires a physical first-prototype check in a real Hammond 1554B2GYCL enclosure before fabrication is treated as production-ready.
