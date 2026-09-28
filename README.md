# POA Sensor

Low-cost wireless plane-of-array (POA) irradiance and PV module temperature sensor.

The project is intended to measure reproducible, silicon-equivalent irradiance in W/m² using a small monocrystalline reference cell. It is not intended to be a meteorological reference-class pyranometer.

## Design goals

- POA irradiance measurement with silicon reference cell
- reference-cell temperature compensation
- external PV module backsheet temperature sensor
- battery-powered low-duty-cycle operation
- Zigbee sleepy end device based on nRF52840
- outdoor enclosure, target IP67/IP68
- PCB/PCBA optimized for JLCPCB and LCSC sourcing
- target hardware cost: approximately EUR 20–30 per sensor at small quantity

## Repository layout

- `hardware/` – KiCad project and project-local libraries
- `bom/` – design BOM and component-selection notes
- `manufacturing/jlcpcb/` – JLCPCB assembly/export notes and release outputs
- `mechanical/` – enclosure, mounting and external temperature probe
- `docs/` – electrical architecture, calibration and measurement principle
- `firmware/` – firmware source (planned)

## Current design baseline

- Ebyte E73-2G4M08S1C / nRF52840 module
- ADS1115 precision ADC
- ANYSOLAR KXOB25-14X1F reference cell
- 1.000 ohm precision shunt
- two 10 kohm NTCs: reference cell + PV module
- Li-SOCl2 1/2-AA cell
- 32.768 kHz crystal for low-power operation

The KiCad project will be the source of truth for schematic, PCB, footprints and component metadata.
