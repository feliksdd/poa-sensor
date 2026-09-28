# PCB and enclosure layout baseline

This document defines the initial mechanical layout for the first POA-sensor PCB. It is a placement baseline, not a frozen production drawing.

## Enclosure

Baseline enclosure: **Hammond 1554B2GYCL**.

Nominal enclosure size is approximately 66 x 66 x 41 mm. Hammond publishes a maximum PCB envelope of roughly 55.45 x 55.96 mm for this enclosure family/size.

To preserve assembly tolerance, cable-gland clearance and wall clearance, the first PCB should use a conservative **52.0 x 52.0 mm** outline.

Recommended board:

- 52.0 x 52.0 mm
- 2 layers
- 1.6 mm FR-4
- 1 oz copper
- rounded corners, provisional radius 3.0 mm
- all JLCPCB-assembled parts on the top side
- battery below the PCB

Do not add mounting holes until the exact enclosure boss locations are verified against the physical enclosure or Hammond mechanical drawing. The first PCB can be supported by the enclosure's internal features or small removable spacers if required.

## Coordinate convention

For the first placement proposal, use PCB center as (0,0), with:

- X increasing to the right
- Y increasing upward
- top edge = RF/antenna edge
- bottom edge = cable-gland / module-NTC edge

Board edges are therefore approximately X = +/-26 mm and Y = +/-26 mm.

## Functional placement zones

### 1. RF zone — top edge

Place U1 (E73-2G4M08S1C) at the **top-right edge** with the ceramic antenna end pointing toward/outside the board edge.

Initial module center target:

- U1 center: approximately **(+16 mm, +18 mm)**
- rotate so the antenna is closest to the +Y board edge

Rules:

- module antenna region must face the enclosure wall, not the battery or analog section
- no copper pour, traces or vias beneath the antenna keep-out on either copper layer
- no battery, cable, mounting hardware or tall components in front of the antenna
- keep at least several millimetres of free volume between antenna and enclosure wall where possible
- the clear polycarbonate enclosure is beneficial because it does not create a metal RF shield

The custom E73 footprint contains a visible `Dwgs.User` RF marker, but this is **not** sufficient protection by itself. Add a real KiCad keep-out/rule area on the PCB before routing.

### 2. Optical / reference-cell zone — upper-left / center-left

Place CELL1 (KXOB25-14X1F) approximately at:

- CELL1 center: **(-10 mm, +8 mm)**
- long axis horizontal

This leaves room around the cell for the optical aperture and keeps it away from the E73 antenna.

The cell body is approximately 23 x 8 mm. The lid mask/window should remain larger than the cell to prevent artificial shading at oblique incidence. Mechanical target remains approximately 40 x 25 mm to 45 x 30 mm clear optical window.

### 3. Reference-cell NTC

NTC1 is intentionally placed **directly underneath the centre of CELL1** on the same PCB side.

Target:

- NTC1 center coincident with CELL1 center
- 0201 package, about 0.3 mm high

CELL1 is manually soldered after JLCPCB assembly. A controlled solder stand-off at the two SolarBIT terminals must leave enough clearance for NTC1. A tiny thermally conductive but electrically insulating adhesive/silicone dot may couple the NTC body to the rear surface of CELL1.

This footprint/courtyard overlap is intentional and must be documented as a DRC exception.

Prototype check before production release:

1. verify JLCPCB 0201 placement height and solder fillet
2. verify SolarBIT terminal stand-off
3. check that no mechanical force from CELL1 is transferred into NTC1
4. confirm thermal response versus a temporary rear-surface thermocouple or thin reference sensor

### 4. Precision analog island

Place RSH1 and U2 close to CELL1 but outside the physical SolarBIT body.

Recommended order:

`CELL1 positive -> RSH1 -> GND current return`

with independent Kelvin sense from both RSH1 terminals to R7/R8 and then U2 AIN0/AIN1.

Suggested placement area:

- RSH1: just below/right of CELL1
- R7/R8 and C9: immediately adjacent to U2
- U2: around **(+1 mm, -2 mm)**

Routing priorities:

- high-current cell/shunt loop short and direct
- Kelvin sense leaves the shunt pads independently
- Kelvin traces run as a close, symmetric pair
- no digital clock/SWD/I2C trace through the Kelvin region
- ground return from the cell/shunt does not share a narrow trace segment with ADC ground
- C9 directly at ADS1115 differential inputs after R7/R8

The ADS1115 does not require a separate isolated analog ground. Use a solid ground plane while controlling current paths by placement.

### 5. NTC divider / sensor-power zone

R1, R2, C10 and C11 can sit close to U2.

Keep the reference-cell NTC trace very short. The external module-NTC path can be longer and should approach J2 without running through the RF keep-out.

### 6. Module-temperature cable connection

Place J2 at the **bottom edge**, near the planned M8 cable gland.

Suggested target:

- J2 center: approximately **(-15 mm, -22 mm)**

The two-wire cable is soldered directly to the board. Use mechanical strain relief in the enclosure/cable gland; do not rely on the PCB solder joints for cable pull strength.

Pin baseline:

- J2.1 = NTC2 ADC/divider node
- J2.2 = GND

Optional future EMC footprint pads can be added near J2 if outdoor cable susceptibility proves problematic, but no unnecessary protection components are fitted in v0.1.

### 7. Battery

The 1/2-AA Li-SOCl2 battery is **not PCB-mounted on the top side**.

Baseline:

- factory-tabbed or factory-wired ER14250/LS14250
- battery lies below the PCB, roughly parallel to one board edge
- wires connect directly to VBAT and GND solder pads
- insulating foam/adhesive or enclosure retention prevents motion

Keep the battery away from the E73 antenna projection.

Before PCB freeze, check the real enclosure/PCB stack height so the battery, PCB, KXOB and clear lid do not mechanically conflict.

### 8. SWD programming pads

Place J1 where pogo access is easy with the lid removed but outside the optical/RF zones.

Suggested target:

- J1 center: approximately **(+14 mm, -19 mm)**

Pin order:

1. VDD_2V4 / VTref
2. SWDIO
3. SWCLK
4. RESET_N
5. GND

The footprint uses exposed 1.5 mm circular pads on 2.00 mm pitch and no paste apertures.

## Initial placement map

Approximate top view, not to scale:

```text
        +Y / RF edge
   +--------------------------------+
   |                    [ E73 ]>>>> |
   |                                |
   |  +----------------------+      |
   |  |      KXOB CELL1      |      |
   |  |      NTC1 below      |      |
   |  +----------------------+      |
   |           RSH1   U2 ADS1115    |
   |                  filters       |
   |                                |
   | J2 / cable             J1 SWD  |
   +--------------------------------+
        -Y / cable-gland edge

Battery: below PCB, outside antenna projection.
```

## Optical height

The design goal remains to place the active reference cell as close to the clear lid as practical, preferably around 1–2 mm below the inner lid surface.

Do not determine PCB spacer height from nominal enclosure depth alone. Measure the actual enclosure and lid after receipt because gasket compression, lid geometry, SolarBIT thickness and solder stand-off all contribute.

The PCB support height can then be selected so that CELL1 is close to the lid without touching it under tolerance/thermal expansion.

## Lid mask

Use white outdoor cast vinyl on the **outside** of the clear lid. Keep only the optical window open.

Reasons:

- reflects visible and IR solar energy rather than merely blocking UV
- reduces enclosure heating
- leaves the enclosure mechanically unmodified
- easy to replace if weathered or scratched

The KXOB plus clear lid and mask are treated as one optical measurement assembly and calibrated together.

## Release gates before routing/fabrication

The PCB should not be released until all of these are checked:

- E73 footprint against the currently ordered module
- antenna orientation and real copper keep-out
- KXOB terminal geometry against sample/datasheet
- NTC1-under-cell mechanical clearance
- Hammond internal boss and lid dimensions
- PCB-to-lid reference-cell clearance
- M8 gland drill location and nut clearance
- battery clearance under PCB
- JLCPCB availability for the selected LCSC parts

After the legacy schematic is converted and committed as `.kicad_sch`, create `poa-sensor.kicad_pcb`, import footprints/nets from schematic, set the 52 x 52 mm provisional outline, place the blocks above, and only then begin routing.
