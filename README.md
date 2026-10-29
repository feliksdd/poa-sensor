# POA Sensor

Low-cost wireless, battery-powered plane-of-array (POA) irradiance sensor.

The project measures reproducible, silicon-equivalent irradiance in W/m² using a small monocrystalline reference cell. It is intentionally independent of the PV-module electrical measurement so it can be mounted at the **optically best, unshaded location** while remaining parallel to the measured PV array plane. It is not intended to be a meteorological reference-class pyranometer.

## Project split

PV module voltage/current/power/energy, module backsheet temperature and per-module curtailment are handled by the separate [PanelLog](https://github.com/feliksdd/panellog) project.

The separation is intentional:

- **POA Sensor:** optical reference; battery powered; placement optimized for representative unshaded irradiance.
- **PanelLog:** one inline node per PV module; PV powered; placement optimized for short DC wiring and module-temperature measurement.

For a system with two different array orientations, the intended deployment is one POA sensor per orientation plus one PanelLog node per PV module.

## Design goals

- POA irradiance measurement with silicon reference cell
- reference-cell temperature compensation
- battery-powered low-duty-cycle operation
- Zigbee sleepy end device based on nRF52840
- freedom to place the sensor at the best unshaded point in the module plane
- outdoor enclosure, target IP67/IP68
- PCB/PCBA optimized for JLCPCB and LCSC sourcing
- target hardware cost: approximately EUR 20-30 per sensor at small quantity

## Repository layout

- `hardware/` - KiCad project and project-local libraries
- `bom/` - design BOM and component-selection notes
- `manufacturing/jlcpcb/` - JLCPCB assembly/export notes and release outputs
- `mechanical/` - enclosure, optical window and mounting
- `docs/` - electrical architecture, calibration and measurement principle
- `firmware/` - firmware source (planned)

## Current design baseline

- Ebyte E73-2G4M08S1C / nRF52840 module
- ADS1115 precision ADC
- ANYSOLAR KXOB25-14X1F reference cell
- 1.000 ohm precision shunt
- one reference-cell 10 kohm NTC
- Li-SOCl2 1/2-AA cell
- 32.768 kHz crystal for low-power operation

## Hardware-revision note

The existing v0.1 KiCad design still contains the former external PV-module-temperature channel (NTC2/J2). That channel predates the repository split and is now **legacy**. It must be removed in the next electrical schematic/PCB revision; until that change is made, the KiCad files remain the source of truth for what is physically present in v0.1.

No new POA design work should add module-voltage, module-current, module-temperature or PV-curtailment functions here; those belong in PanelLog.

The KiCad project remains the source of truth for schematic, PCB, footprints and component metadata.
