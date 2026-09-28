# Electrical architecture

## Functional blocks

1. 3.6 V Li-SOCl2 battery on nRF52840 VDDH
2. nRF52840 high-voltage REG0 configured to 2.4 V
3. optional/high-efficiency REG0 DC/DC path using 10 uH from DCCH to VDD
4. E73-2G4M08S1C Zigbee sleepy-end-device module
5. 32.768 kHz low-frequency crystal
6. ADS1115 precision ADC on the regulated 2.4 V rail
7. silicon reference cell and Kelvin-connected precision shunt
8. switched reference-cell NTC divider
9. switched external PV-module NTC divider
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
- AIN3 single-ended: module-temperature NTC divider
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

Both temperature sensors use TDK NTCG163JF103FT1S, nominal 10 kohm at 25 °C.

Each divider uses a 10 kohm 1 % reference resistor. The two reference resistors are fed from GPIO `SENS_PWR`, not directly from VDD_2V4. During sleep SENS_PWR is driven low. Before temperature conversion firmware drives SENS_PWR high, waits for RC/ADC settling, performs both ADC readings and then drives it low again.

This removes essentially all divider standby current and keeps NTC self-heating negligible.

Topology for each channel:

`SENS_PWR -> 10k reference resistor -> ADC node -> 10k NTC -> GND`

C10/C11 = 100 nF from each ADC node to GND provide local filtering. Because the NTC node can approach the 2.4 V rail at the extremes, firmware uses an ADS1115 range large enough for the full node voltage (normally ±4.096 V for the temperature channels).

NTC1 is thermally bonded to the rear surface of the reference cell.

NTC2 is connected through J2 over a two-wire UV-resistant cable and bonded to the rear of the monitored PV module beneath a cell region, not to the frame or junction box.

## Battery measurement

No external resistor divider is fitted. nRF52840 SAADC selects the internal VDDH/5 source. This is only valid because the battery is connected directly to VDDH.

Battery measurement should preferably be sampled during or directly after a representative radio load if firmware later wants to estimate battery internal resistance/sag in addition to open-circuit state.

## Low-power clock

Y1 baseline is Epson Q13FC13500004, 32.768 kHz, ±20 ppm, CL = 12.5 pF, SMD3215.

C7/C8 start at 22 pF C0G each. This is a practical initial value for a 12.5 pF crystal with PCB/pin parasitics; the final value can be tuned after PCB layout or prototype frequency measurement if necessary.

## Programming

J1 is a connectorless five-pad pogo/SWD pattern:

1. VDD_2V4 / VTref
2. SWDIO
3. SWDCLK
4. RESET_N
5. GND

The first programming/provisioning flow must set UICR REGOUT0 to 2.4 V and reset the device before normal application operation.

## RF placement

U1 is placed at a PCB edge with the ceramic antenna facing outwards. No copper, traces, battery, metal mounting hardware or tall components are allowed in the antenna keep-out/near-field region. The analog measurement island is placed at the opposite side of the board where practical.

## Schematic revision

This document describes electrical schematic baseline **v0.1**. PCB placement/routing has not yet been frozen.
