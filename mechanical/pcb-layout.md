# PCB and enclosure layout baseline

This document defines the initial mechanical layout for the first POA-sensor PCB. It is a placement baseline, not a frozen production drawing.

## Enclosure

Baseline enclosure: **Hammond 1554B2GYCL**.

Nominal enclosure size is approximately 66 x 66 x 41 mm. Hammond publishes a maximum PCB envelope of roughly 55.45 x 55.96 mm for this enclosure family/size.

To preserve assembly tolerance, cable-gland clearance and wall clearance, the first PCB uses a conservative **52.0 x 52.0 mm** outline.

Recommended board:

- 52.0 x 52.0 mm
- 2 layers
- 1.6 mm FR-4
- 1 oz copper
- all JLCPCB-assembled parts on the top side
- battery below the PCB

Do not add mounting holes until the exact enclosure boss locations are verified against the physical enclosure or Hammond mechanical drawing. Corner radii are also deferred until that check.

## Coordinate convention

The native placement template uses absolute KiCad coordinates:

- board: X = 100...152 mm, Y = 100...152 mm
- right edge = RF/antenna edge
- bottom edge = cable-gland / module-NTC edge

For relative reasoning the board centre is (0,0), with X positive toward the RF/right edge and Y positive toward the bottom/cable edge.

## Functional placement zones

### 1. RF zone — right edge

Place U1 (E73-2G4M08S1C) at the **upper-right edge**, unrotated, with the ceramic-antenna end of the custom footprint facing the right enclosure wall.

Template target:

- U1 body guide: X = 133.5...151.5 mm
- Y = 105.5...118.5 mm
- antenna/right-side keepout: X = 147.5...152.0 mm
- Y = 104.5...119.5 mm

Rules:

- no copper pour, traces or vias in the antenna keepout on either copper layer
- no battery, cable, mounting hardware or tall components in front of the antenna
- keep the ceramic antenna close to the board/enclosure edge
- the clear polycarbonate enclosure does not create a metal RF shield

The placement template contains a **real KiCad rule-area keepout**, not only a drawing marker. The custom E73 footprint also contains a visible reference marker for review.

### 2. Optical / reference-cell zone — upper-left

Place CELL1 (KXOB25-14X1F) at approximately:

- centre X = 115 mm
- centre Y = 114 mm
- long axis horizontal

The cell body is approximately 23 x 8 mm. The placement template also marks a larger optical-clear region. The lid mask/window should remain larger than the cell to avoid artificial shading at oblique incidence; final lid target remains roughly 40 x 25 mm to 45 x 30 mm.

### 3. Reference-cell NTC

NTC1 is intentionally placed **directly underneath the centre of CELL1** on the same PCB side.

Target:

- NTC1 centre coincident with CELL1 centre
- TDK NTCG063JF103FTBA
- 0201 package, about 0.3 mm high

CELL1 is manually soldered after JLCPCB assembly. A controlled solder stand-off at the two SolarBIT terminals must leave enough clearance for NTC1. A very small thermally conductive but electrically insulating adhesive/silicone dot may couple the NTC body to the rear surface of CELL1.

This footprint/courtyard overlap is intentional and must be documented as a DRC exception.

Prototype checks:

1. verify JLCPCB 0201 placement and solder fillet
2. verify SolarBIT terminal stand-off
3. ensure CELL1 does not mechanically load NTC1
4. compare thermal response against a temporary thin rear-surface reference sensor

### 4. Precision analog island

Place RSH1 and U2 close to CELL1 but outside the SolarBIT body. The template reserves roughly X = 124...137 mm and Y = 116...133 mm for this block.

Current path:

`CELL1+ -> RSH1 -> CELL1- / local current return`

The important layout detail is the low-side star connection: the shunt low terminal, CELL1 negative return and ADC low-side Kelvin sense meet locally. Do **not** let the ~59 mA cell current flow through a narrow shared ground trace used by the ADC sense path before it reaches that point.

Routing priorities:

- high-current cell/shunt loop short and direct
- Kelvin sense leaves both shunt pads independently
- R7/R8 and C9 adjacent to U2 AIN0/AIN1
- Kelvin traces routed as a close, symmetric pair
- no digital clock/SWD/I2C trace through the Kelvin region
- solid ground plane elsewhere, but controlled local current return at the shunt

The ADS1115 does not require a separate isolated analog ground plane.

### 5. NTC divider / sensor-power zone

R1, R2, C10 and C11 sit close to U2/associated sensor node. Keep the cell-NTC connection extremely short. The external module-NTC path runs toward J2 without entering the RF keepout.

### 6. Module-temperature cable connection

Place J2 at the **bottom-left edge**, near the planned M8 cable gland.

Template area:

- X = 102...111 mm
- Y = 143...149 mm

The two-wire cable is soldered directly to the board. Mechanical strain relief is provided by the gland/enclosure, not the solder pads.

Pin baseline:

- J2.1 = NTC_MODULE ADC/divider node
- J2.2 = GND

Optional protection footprints can be added later if outdoor-cable EMC tests show a need; v0.1 avoids unnecessary leakage/cost.

### 7. Battery

The 1/2-AA Li-SOCl2 battery is **not top-side PCB mounted**.

Baseline:

- factory-tabbed or factory-wired ER14250/LS14250
- battery below PCB
- wires connect to BT1 solder pads (VBAT/GND)
- insulating foam/adhesive or enclosure retention prevents motion
- battery kept outside the E73 antenna projection

The placement template reserves the lower-centre region for the battery wire exit/under-board volume.

### 8. SWD programming pads

J1 is at the bottom-right, accessible with the lid removed and outside optical/RF zones.

Template area:

- X = 136...148 mm
- Y = 143...149 mm

Pin order:

1. VDD_2V4 / VTref
2. SWDIO
3. SWCLK
4. RESET_N
5. GND

The footprint uses exposed circular pogo pads on 2.00 mm pitch and no paste apertures.

## Initial placement map

Approximate top view, not to scale:

```text
   +--------------------------------------+
   | optical clear area         [ E73 ]>>|  -> RF/right wall
   |                                      |
   | [      KXOB CELL1      ]              |
   | [      NTC1 below      ] RSH1/U2      |
   |                           analog      |
   |                                      |
   | J2 / cable       battery       J1 SWD|
   +--------------------------------------+
                      bottom / gland side
```

Battery: below PCB and outside antenna projection.

## Optical height

The design goal remains to place the active reference cell as close to the clear lid as practical, preferably around 1–2 mm below the inner lid surface.

Do not determine PCB spacer height from nominal enclosure depth alone. Measure the actual enclosure and lid after receipt because gasket compression, lid geometry, SolarBIT thickness and solder stand-off all contribute.

## Lid mask

Use white outdoor cast vinyl on the **outside** of the clear lid. Keep only the optical window open. This reflects visible/IR solar energy, reduces enclosure heating, leaves the enclosure mechanically unmodified and remains replaceable.

The KXOB, clear lid and mask are treated as one optical measurement assembly and calibrated together.

## Native PCB template

`hardware/poa-sensor-layout-template.kicad_pcb` is the current mechanical source for the first board. It contains:

- 52 x 52 mm Edge.Cuts
- placement guides on User.1
- optical-clear-area drawing on Dwgs.User
- all-layer E73 antenna rule-area keepout

After schematic normalization, copy it to `poa-sensor.kicad_pcb`, run **Update PCB from Schematic (F8)** and place imported footprints into the marked zones.

## Release gates before routing/fabrication

Do not release the PCB until these are checked:

- E73 footprint and antenna orientation against the actual module
- KXOB contact geometry against a physical sample/manufacturer drawing
- NTC1-under-cell mechanical clearance
- Hammond internal bosses and actual lid geometry
- PCB-to-lid reference-cell clearance
- M8 gland drill/nut clearance
- battery clearance under PCB
- JLCPCB availability for selected LCSC parts
- ERC clean except intentional documented exclusions
- DRC and schematic-parity clean
