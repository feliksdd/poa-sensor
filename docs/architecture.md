# Electrical architecture

## Scope after the PanelLog split

This repository is now restricted to the battery-powered optical POA reference. PV-module voltage/current/power/energy, module backsheet temperature and per-module curtailment belong to [PanelLog](https://github.com/feliksdd/panellog).

The existing schematic **v0.1** still contains NTC2/J2 from the former combined concept. Those items are legacy and must be removed in the next electrical revision. The descriptions below distinguish the physical v0.1 state from the target post-split architecture.

## Functional blocks

1. 3.6 V Li-SOCl2 battery on nRF52840 VDDH
2. nRF52840 high-voltage REG0 configured to 2.4 V
3. optional/high-efficiency REG0 DC/DC path using 10 uH from DCCH to VDD
4. E73-2G4M08S1C Zigbee sleepy-end-device module
5. 32.768 kHz low-frequency crystal
6. ADS1115 precision ADC on the regulated 2.4 V rail
7. silicon reference cell and Kelvin-connected precision shunt
8. switched reference-cell NTC divider
9. **legacy v0.1 only:** switched external PV-module NTC divider
10. internal VDDH/5 battery-voltage measurement with nRF52840 SAADC
11. SWD programming/test pads

## Power strategy

Battery nominal voltage is 3.6 V and is connected to U1 VDDH, not VDD. This avoids relying on the 3.6 V maximum normal-voltage-mode supply limit and uses the nRF52840 high-voltage supply path.

U1 VDD is used as the REG0 output and is the system logic/analog rail `VDD_2V4`. Firmware/provisioning must program UICR REGOUT0 to 2.4 V. A fully erased nRF52840 defaults REGOUT0 to 1.8 V, so the provisioning sequence must set REGOUT0 before normal sensor operation. The ADS1115 is specified from 2.0 V and therefore is intentionally not expected to operate before that first REGOUT0 configuration/reset.

L1 = 10 uH connects U1 DCCH to U1 VDD so REG0 can operate in DC/DC mode. Firmware enables DCDCEN0. The circuit remains conceptually usable in REG0 LDO mode during early bring-up, but the production configuration is DC/DC for battery efficiency.

Decoupling baseline:

- C1 47 uF from VBAT/VDDH to GND for battery/radio pulse buffering
- C2 4.7 uF from VDD_2V4 to GND at U1
- 100 nF local bypass at VDDH, VDD and ADS1115 VDD
- 1 uF additional bulk at ADS1115 VDD

## MCU pin allocation

E73-2G4M08S1C module pins used by schematic v0.1:

| Function | nRF pin | E73 pad | Net |
| --- | --- | ---: | --- |
| LFCLK XL1 | P0.00/XL1 | 11 | XL1 |
| I2C SDA | P0.26 | 12 | I2C_SDA |
| LFCLK XL2 | P0.01/XL2 | 13 | XL2 |
| I2C SCL | P0.06 | 14 | I2C_SCL |
| VDD / REG0 output | VDD | 19 | VDD_2V4 |
| NTC excitation | P0.07 | 22 | SENS_PWR |
| battery input | VDDH | 23 | VBAT |
| REG0 DC/DC | DCCH | 25 | DCCH |
| reset | P0.18/RESET | 26 | RESET_N |
| SWDIO | SWDIO | 37 | SWDIO |
| SWDCLK | SWDCLK | 39 | SWDCLK |
| ground | GND | 5,21,24 | GND |

All unused GPIOs remain uncommitted in v0.1.

## ADC allocation

ADS1115 address pin is tied to GND, giving address 0x48.

- AIN0/AIN1 differential: reference-cell shunt voltage
- AIN2 single-ended: reference-cell NTC divider
- AIN3 single-ended: **legacy v0.1** module-temperature NTC divider; unused after NTC2/J2 removal
- ALERT/RDY: not connected in v0.1; conversions are polled in single-shot mode

The nRF52840 SAADC uses its internal `VDDH/5` input for battery voltage. The former external 1 Mohm / 330 kohm battery divider has therefore been removed, eliminating both parts and continuous divider leakage.

## Irradiance channel

KXOB25-14X1F is operated close to short circuit through RSH1 = 1.000 ohm, 0.1 %, 25 ppm/K. The reference-cell negative terminal is connected to GND. The positive terminal connects to the high side of RSH1; the low side of RSH1 returns to GND.

At approximately 58.6 mA at 1000 W/m², expected shunt voltage is approximately 58.6 mV and shunt dissipation is only about 3.4 mW.

ADS1115 measures this voltage differentially using true Kelvin sense traces from the two shunt terminals:

- R7 = 100 ohm in the AIN0 sense path
- R8 = 100 ohm in the AIN1 sense path
- C9 = 100 nF directly across AIN0 and AIN1 after R7/R8

The high-current cell/shunt loop must not share trace segments with the Kelvin sense pair.

Firmware baseline for irradiance: ADS1115 PGA ±0.256 V, single-shot conversion, several samples per measurement event.

## Temperature channels

The target POA architecture has **one temperature sensor only: NTC1 on the reference cell**. Schematic v0.1 still contains the former remote module sensor NTC2; that channel is legacy and moves functionally to PanelLog.

v0.1 parts:

- NTC1: TDK NTCG063JF103FTBA, 0201, 10 kohm ±1 %, B25/50 = 3380 K, approximately 0.3 mm high
- NTC2: TDK NTCG163JF103FT1S, 0603, 10 kohm ±1 %, B25/50 = 3380 K

Each divider uses a 10 kohm 1 % reference resistor. The two reference resistors are fed from GPIO `SENS_PWR`, not directly from VDD_2V4. During sleep SENS_PWR is driven low. Before temperature conversion firmware drives SENS_PWR high, waits for RC/ADC settling, performs both ADC readings and then drives it low again.

This removes essentially all divider standby current and keeps NTC self-heating negligible. A 1 % reference resistor is sufficient: its contribution to temperature error is small compared with the sensor/mechanical thermal uncertainty, and calibration remains available.

Topology for each channel:

`SENS_PWR -> 10k reference resistor -> ADC node -> 10k NTC -> GND`

C10/C11 = 100 nF from each ADC node to GND provide local filtering. Because the NTC node can approach the 2.4 V rail at the extremes, firmware uses an ADS1115 range large enough for the full node voltage (normally ±4.096 V for the temperature channels).

### Reference-cell NTC mechanics

NTC1 is placed on the top side of the PCB directly beneath the center region of CELL1. The 0201 package is only about 0.3 mm high. CELL1 is manually assembled after JLCPCB PCBA, with a small controlled stand-off/solder height at its two rear terminal pads. A very small thermally conductive, electrically insulating silicone/epoxy dot may be used between the NTC body and the SolarBIT rear surface.

This arrangement preserves a single main PCB while measuring temperature close to the rear of the actual reference cell. It intentionally creates a known mechanical overlap between the KXOB and NTC1 footprints; this overlap is a documented DRC/mechanical exception.

NTC2/J2 describe the former combined concept only. They are not part of the post-split POA sensor and must be removed in the next schematic/PCB revision. Module backsheet temperature is measured by the corresponding PanelLog node.

## Battery measurement

No external resistor divider is fitted. nRF52840 SAADC selects the internal VDDH/5 source. This is only valid because the battery is connected directly to VDDH.

Battery measurement should preferably be sampled during or directly after a representative radio load if firmware later wants to estimate battery internal resistance/sag in addition to open-circuit state.

## Low-power clock

Y1 baseline is Epson Q13FC13500004, 32.768 kHz, ±20 ppm, CL = 12.5 pF, SMD3215.

C7/C8 start at 22 pF C0G each. This is a practical initial value for a 12.5 pF crystal with PCB/pin parasitics; the final value can be tuned after PCB layout or prototype frequency measurement if necessary.

## Programming

J1 is a connectorless five-pad pogo/SWD pattern, 2.00 mm pitch:

1. VDD_2V4 / VTref
2. SWDIO
3. SWDCLK
4. RESET_N
5. GND

The first programming/provisioning flow must set UICR REGOUT0 to 2.4 V and reset the device before normal application operation.

## RF placement

U1 is placed at a PCB edge with the ceramic antenna facing outwards. No copper, traces, battery, metal mounting hardware or tall components are allowed in the antenna keep-out/near-field region. The custom footprint marks a conservative antenna area on `Dwgs.User`; the PCB itself must additionally contain an enforced copper keep-out/rule area on both copper layers before routing is frozen.

The analog measurement island is placed at the opposite side of the board where practical.

## PCB baseline

- 2-layer FR-4, 1.6 mm
- all JLCPCB-assembled components on the top side to avoid double-sided assembly cost
- provisional outline: 52 x 52 mm with rounded corners, to fit inside Hammond 1554B2GYCL while retaining margin against the published maximum PCB envelope
- CELL1 on top side below the optical window
- NTC1 underneath CELL1 on the same PCB side
- U1 at an outer PCB edge, antenna directed toward the enclosure wall and away from CELL1/analog section
- battery below the raised PCB, connected by factory-tabbed leads
- **legacy v0.1:** J2 near the former cable-gland edge; remove with NTC2
- J1 accessible with the lid removed

Mechanical details are tracked in `../mechanical/pcb-layout.md`.

## Schematic revision

This document describes electrical schematic baseline **v0.1** plus the initial PCB/mechanical baseline. v0.1 still contains the legacy NTC2/J2 channel. The next electrical revision removes it so the POA sensor is optically independent of any particular PV module. Placement/routing has not yet been frozen.
