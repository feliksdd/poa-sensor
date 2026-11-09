# Wired POA prototype option (2026-11-09)

Current baseline: `main` source at `0970a7abca613ca047073c4c38a08328d09aa023`. The existing `hardware/poa-sensor.kicad_sch` and `hardware/poa-sensor.kicad_pcb` remain the historical battery/Zigbee revision, **not** the intended new wired board.

A new native KiCad draft schematic has been created in `hardware/poa-sensor-wired.kicad_sch`. It contains the reference cell KXOB25-14X1F, ADS1115IDGSR C37593, true Kelvin shunt 1.000R C865286, 0201 TDK NTC C29553871, 47k NTC divider and 1:2 supply monitor, 6 cable pads, optional P82B715DR C2649394 **DNP**, and direct 0R bypasses. P82B715 pin function is verified against the TI datasheet (Sx pin3, Sy pin6, Lx pin2, Ly pin7). Independent matched cable footprints are under `hardware/footprints/poa-sensor.pretty/POA_Cable_6pad.kicad_mod`.

The intended mating cable pinout is:
1 +3V3, 2 GND, 3 SDA, 4 GND, 5 SCL, 6 GND. Twist each logic or supply wire with its own adjacent return. Use at most 3m outdoor cable.

### Direct mode / default

R6 and R7 = zero-ohm **fitted**; P82B715 U2 and R8/R9 cable pull-ups **DNP**. The 2.2k pull-ups are at PanelLog only. Single-ended ADS1115 AIN2 reads NTC; AIN3 reads half VDD. AIN0/AIN1 read a true 1Ω Kelvin sense. All analog signal routing stays in a compact, quiet analog island over continuous local ground; keep I2C and cable pads away from the cell/shunt voltage sense pair.

### Buffered option (not ready to populate)

Remove POA R6/R7 and PanelLog R32/R33; fit POA U2 and PanelLog U4, plus properly dimensioned L-side pullups. Both S sides need local pullups. **POA S-side pullups not yet added** to this draft: P82B715 remains an intentionally unqualified DNP option. Buffer does not improve common-mode isolation, and its digital traces should not run under the cell.

### Blockers

- No matching wired PCB layout yet; the existing `poa-sensor.kicad_pcb` is for the standalone RF sensor. The new schematic has not undergone native KiCad 10 ERC, parity or physical placement review.
- PCB revision must remove RF/battery/extra NTC, shrink geometry, retain the 0201 cell NTC contact mechanics, and place ADC plus Kelvin network locally. Cable mechanical strain relief, ESD array and supply protection are unqualified and require explicit parts before release.
- Environmental optical seal/window/transmission and thermal calibration must be confirmed in the final enclosure.
- Firmware reader is implemented as an untested component in the PanelLog repository; system integration is outstanding.

The draft is for engineering development only, not fabrication. The original KiCad files were deliberately left unchanged to protect the last existing source until full native KiCad 10 validation is possible.
