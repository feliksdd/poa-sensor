# Electrical architecture

## Functional blocks

1. Li-SOCl2 battery supply
2. nRF52840 Zigbee sleepy-end-device module
3. 32.768 kHz low-frequency crystal
4. ADS1115 precision ADC
5. silicon reference cell and Kelvin-connected precision shunt
6. reference-cell NTC
7. external PV-module NTC
8. battery-voltage measurement
9. SWD programming/test pads

## ADC allocation

The baseline allocates the ADS1115 to the precision analog measurements:

- AIN0/AIN1 differential: reference-cell shunt voltage
- AIN2: reference-cell NTC divider
- AIN3: module-temperature NTC divider

This keeps irradiance and both calibrated temperature channels on one ADC. The nRF52840 SAADC remains available for battery voltage and diagnostic measurements.

## Irradiance channel

The KXOB25-14X1F reference cell is operated close to short circuit through a nominal 1.000 ohm precision shunt. At approximately 58.6 mA at 1000 W/m², the expected shunt voltage is approximately 58.6 mV.

Routing requirements:

- RSH1 placed close to U2
- Kelvin sense from the two shunt terminals to ADS1115 differential inputs
- symmetric RC input filtering if filtering is used
- no radio/clock traces through the analog island
- keep the reference-cell current path separate from sensitive sense traces

## Temperature channels

Both temperature channels use the same 10 kohm TDK NTC type. Each divider uses a stable reference resistor and is energized only for measurement if practical, to reduce self-heating and standby current.

NTC1 is thermally bonded to the reference-cell rear surface.

NTC2 is connected over a two-wire UV-resistant cable and bonded to the rear of the monitored PV module beneath a cell region rather than the frame or junction box.

## Power strategy

Battery: 3.6 V Li-SOCl2 1/2-AA.

The exact U1 high-voltage-supply connection and REGOUT0 configuration must be checked against the E73-2G4M08S1C manufacturer pinout before schematic freeze. The target is to avoid an external regulator if the module exposes the nRF52840 high-voltage supply path as expected.

The ADC and analog network should run from a defined logic/analog rail compatible with ADS1115 limits. Large low-leakage local capacitance near the radio is required to absorb transmit pulses and reduce battery voltage sag.

## Low-power clock

Use a 32.768 kHz crystal for low-power sleep timing. Final crystal and load capacitor values must be selected as a set from the crystal CL, nRF52840 input capacitance and estimated PCB stray capacitance.

## Programming

Provide exposed SWDIO, SWCLK, GND, VREF/VDD and reset/test access as PCB pads. Avoid a fitted connector unless prototype handling proves it necessary.

## RF placement

Place U1 at a PCB edge with the antenna facing away from copper, battery and enclosure metal. Implement the Ebyte keep-out area on all copper layers and keep tall components out of the antenna near field.
