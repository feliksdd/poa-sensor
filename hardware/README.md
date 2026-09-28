# Hardware

KiCad is the single source of truth for the electrical and PCB design.

## Current schematic v0.1

The first complete electrical schematic is committed as:

- `poa-sensor.sch`
- `poa-sensor-cache.lib`

These two files use the legacy Eeschema text format as a one-time bootstrap because the automated design environment does not have a KiCad executable available. KiCad 8/9 can import/open this format and convert it to the current `.kicad_sch` format.

### One-time conversion

1. Open `poa-sensor.sch` in KiCad / Eeschema.
2. Let KiCad rescue/import the cached project symbols if prompted.
3. Save the schematic as `poa-sensor.kicad_sch`.
4. Create/save the project as `poa-sensor.kicad_pro` if KiCad has not done so automatically.
5. Commit the converted `.kicad_sch` and `.kicad_pro` files.
6. After the converted project has been checked, the legacy `.sch` and `-cache.lib` files can be removed.

From that point onward the project should stay in the current KiCad format only.

## Schematic scope

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

## Next hardware files

After conversion/review:

- `poa-sensor.kicad_pro`
- `poa-sensor.kicad_sch`
- `poa-sensor.kicad_pcb`
- `symbols/poa-sensor.kicad_sym`
- `footprints/poa-sensor.pretty/`

Project-local libraries should contain only custom parts/footprints that are not safely covered by the official KiCad libraries, especially the E73 module, reference-cell mechanics, SWD pogo pads and wire pads.

## Important before PCB routing

Do not route until the custom E73 and KXOB footprints have been checked dimension-by-dimension against manufacturer drawings. The irradiance shunt must use true Kelvin routing, and the E73 antenna keep-out applies to all copper layers and nearby components.
