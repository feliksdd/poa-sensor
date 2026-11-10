> Historischer Stand: Die aktuelle kabelgebundene Schaltplanrevision 0.3 ist in [README](../README.md) und `docs/architecture.md` beschrieben. Alte Funk-PCB-/BOM-Angaben gelten nicht für die aktuelle Schaltung.

# Component selection

## Selection philosophy

The design is optimized for JLCPCB assembly with LCSC/JLCPCB parts wherever that materially reduces total cost. Ordinary R/C passives should use Basic parts when practical. Specialized measurement/RF parts may remain Extended where their function justifies the feeder/loading cost.

## Locked / preferred parts

### U1 — nRF52840 radio module
- **Ebyte E73-2G4M08S1C**
- JLCPCB/LCSC: **C356849**
- 18 x 13 mm SMD module
- selected because it combines the nRF52840, 2.4 GHz RF matching/antenna and 32 MHz clock in a low-cost module
- use manufacturer antenna keep-out exactly as specified

### U2 — precision ADC
- **TI ADS1115IDGSR**
- LCSC: **C37593**
- VSSOP-10
- keep for irradiance measurement; its cost is small compared with the gain in reproducibility versus relying only on the nRF SAADC
- irradiance channel should be measured differentially across the shunt

### NTC1 — reference-cell temperature sensor

The post-split POA sensor keeps only NTC1, thermally coupled to the KXOB reference cell. The current native schematic uses **TDK NTCG063JF103FTBA** (0201). The exact production sourcing entry should follow the native KiCad metadata at schematic freeze.

### NTC2 — legacy v0.1

The former external PV-module-temperature NTC and J2 cable interface are no longer part of the POA architecture. They remain in schematic v0.1 only and must be removed in the next electrical revision. Module backsheet temperature belongs to [PanelLog](https://github.com/feliksdd/panellog).

### R1 / R2 — NTC reference resistors
- **RESI PTFR0603B47K0N9**
- JLCPCB/LCSC: **C394548**
- 47 kohm, ±0.1 %, ±10 ppm/K

This is intentionally more accurate than a standard 1 % thick-film part. It may later be relaxed after the complete temperature error budget is calculated; for the first revision it removes the divider resistor as a meaningful error source.

### Cx — 100 nF decoupling
- **Yageo CC0603KRX7R9BB104**
- JLCPCB/LCSC: **C14663**
- 0603, 100 nF, X7R, 50 V, ±10 %
- JLCPCB Basic part

### Y1 — LF crystal
Current baseline:
- **NDK NX3215SA-32.768K-STD-MUA-8**
- JLCPCB/LCSC: **C156245**
- 32.768 kHz, ±20 ppm, CL = 12.5 pF, ESR 70 kohm

Before schematic freeze, compare the effective JLCPCB cost with stocked 9 pF / 6 pF alternatives. The actual load capacitors must be calculated from the selected CL plus PCB/input parasitics.

### RSH1 — irradiance shunt
Preferred electrical part:
- **Yageo RT0805BRD071RL**
- 1.000 ohm, ±0.1 %, ≤25 ppm/K

The exact current JLCPCB/LCSC stocking code still needs to be confirmed before schematic freeze. Do not substitute a generic 1 % thick-film resistor without re-running the irradiance gain/temperature error budget.

## Manually assembled / non-JLCPCB parts

### CELL1 — reference cell
- **ANYSOLAR KXOB25-14X1F-TR**
- roughly 23 x 8 mm
- approximately 58.6 mA short-circuit current at 1000 W/m² (datasheet starting calibration)
- assembled manually after PCBA

### BT1 — battery
- 1/2-AA Li-SOCl2, 3.6 V
- preferred low-cost: EVE ER14250 with factory tabs/leads
- premium alternative: Saft LS14250
- never solder directly to a bare lithium cell

### Enclosure
- current baseline: **Hammond 1554B2GYCL**
- transparent lid, compact outdoor enclosure
- optical area masked externally with white outdoor cast vinyl except for the reference-cell window

## Cost-sensitive items still to lock

Before the first KiCad schematic is frozen, select current JLCPCB Basic/preferred parts for:
- 1 uF local bulk capacitor
- 47 uF radio/battery pulse-buffer capacitor(s)
- LF crystal load capacitors
- 4.7 kohm I2C pull-ups
- battery-divider resistors
- ADC input-filter components

These parts should be chosen based on the current JLCPCB stock at ordering time because they are electrically non-critical and availability/Basic status changes more often than the design requirements.
