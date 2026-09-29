# PCB and enclosure layout baseline

This document defines the mechanical baseline for the first POA-sensor PCB.

## Enclosure

Baseline enclosure: **Hammond 1554B2GYCL**.

The PCB outline is no longer a generic square. It now follows the **Hammond 1554BPL steel-panel profile**, which is the mechanical reference part intended for this enclosure size. This gives the PCB the same corner/boss clearance geometry as the manufacturer's panel instead of relying on an approximate rectangular envelope.

### 1554BPL reference geometry

The KiCad mechanical template uses these manufacturer dimensions:

- overall width: **55.45 mm**
- overall height: **55.96 mm**
- corner relief radius: **R9.525 mm** (3/8 in)
- stepped straight section: **10.16 mm**
- two mounting holes: **Ø3.73 mm**
- mounting-hole centre line: **27.98 mm** from the left datum
- upper mounting-hole centre: **16.46 mm** from the top datum
- lower mounting-hole centre: **37.98 mm** from the top datum
- mounting-hole pitch: **21.52 mm**

The exact steel-panel contour is treated as the source of truth. Do **not** replace it with a 52 x 52 mm rectangle or simplified corner cut-outs.

Reference: Hammond 1554BPL manufacturer drawing.

Recommended board stack:

- 2 layers
- 1.6 mm FR-4
- 1 oz copper
- all JLCPCB-assembled parts on the top side
- battery below the PCB

## Coordinate convention

The native mechanical template is anchored with the steel-panel bounding box at:

- left datum: X = 100.00 mm
- top datum: Y = 100.00 mm
- maximum right extent: X = 155.45 mm
- maximum bottom extent: Y = 155.96 mm

The panel is intentionally asymmetric because of the Hammond corner/boss clearance profile.

Mounting-hole centres in template coordinates:

- H1 = (127.98, 116.46) mm
- H2 = (127.98, 137.98) mm

## Mounting holes

The PCB uses the same two-hole geometry as the 1554BPL panel:

- H1/H2 are NPTH
- nominal drill/finished hole diameter: **3.73 mm**
- keep copper, vias and components clear around the screw/washer volume
- final screw/washer stack must be checked against the real enclosure and chosen spacers before release

The two holes sit relatively close to the centre of the usable PCB area and therefore constrain component placement. The precision analog section and battery retention must not overlap the screw volumes.

## Functional placement zones

The old 52 x 52 mm placement map is obsolete. The following zones are the new mechanical starting point and may still be optimized during routing.

### 1. RF zone — right edge

Place U1 (E73-2G4M08S1C) along the **right-hand enclosure wall**, shifted down from the former upper-right corner so the module does not collide with the steel-panel corner relief.

Template target:

- U1 body guide: approximately X = 135...153 mm
- Y = 111...124 mm
- antenna/right-side keepout: approximately X = 149...155.45 mm
- Y = 110...125 mm

Rules:

- no copper pour, traces or vias in the antenna keepout on either copper layer
- no battery, cable, mounting hardware or tall components in front of the antenna
- keep the ceramic antenna close to the board/enclosure edge
- the clear polycarbonate enclosure does not create a metal RF shield

The placement template contains a real KiCad rule-area keepout, not only a drawing marker.

### 2. Optical / reference-cell zone

The KXOB25-14X1F remains under the clear lid window, but the long axis is rotated approximately 90 degrees relative to the former square-board placement so it fits cleanly in the large unobstructed left-hand area of the steel-panel outline.

Template target:

- CELL1 body guide: approximately X = 111...119 mm
- Y = 103...126 mm
- cell body: approximately 23 x 8 mm

The lid mask/window remains larger than the cell to avoid artificial shading at oblique incidence; final lid target remains roughly **40 x 25 mm to 45 x 30 mm**.

### 3. Reference-cell NTC

NTC1 remains intentionally placed **directly underneath the centre of CELL1** on the same PCB side.

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

Place RSH1 and U2 close to CELL1 but outside the SolarBIT body and outside the H1/H2 mounting keepouts. The new template reserves approximately X = 132...144 mm and Y = 124.5...135 mm for this block.

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

Place J2 near the lower-left portion of the PCB, close to the planned M8 cable gland but clear of the lower-left corner relief.

Template area:

- approximately X = 111...121 mm
- Y = 147...153 mm

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
- battery must also clear both enclosure mounting bosses/screws

The final below-PCB battery position is dependent on spacer height and the real screw stack and therefore remains a prototype fit check.

### 8. SWD programming pads

J1 remains accessible with the lid removed and outside optical/RF zones.

Template area:

- approximately X = 132...143 mm
- Y = 147...153 mm

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
        ┌────────────────────────────╮
        │ optical             E73 >> │
   ┌────┘                            │
   │  KXOB                           │
   │                 H1 ○            │
   │                         analog  │
   │                 H2 ○            │
   │                                 │
   │ J2          battery       SWD   │
   ╰────────────────────────────┐    │
                                └────┘
```

The actual `Edge.Cuts` profile in KiCad is authoritative; the ASCII drawing is only explanatory.

## Optical height

The design goal remains to place the active reference cell as close to the clear lid as practical, preferably around **1–2 mm below the inner lid surface**.

Do not determine PCB spacer height from nominal enclosure depth alone. Measure the actual enclosure and lid after receipt because gasket compression, lid geometry, SolarBIT thickness, screw stack and solder stand-off all contribute.

## Lid mask

Use white outdoor cast vinyl on the **outside** of the clear lid. Keep only the optical window open. This reflects visible/IR solar energy, reduces enclosure heating, leaves the enclosure mechanically unmodified and remains replaceable.

The KXOB, clear lid and mask are treated as one optical measurement assembly and calibrated together.

## Native PCB template

`hardware/poa-sensor-layout-template.kicad_pcb` is the current mechanical source for the board. It contains:

- exact Hammond 1554BPL-derived `Edge.Cuts`
- H1/H2 mounting holes at the manufacturer positions
- revised placement guides on User.1
- optical-clear-area drawing on Dwgs.User
- all-layer E73 antenna rule-area keepout

Do not independently redraw the outline in the production board. Copy/synchronize the template geometry so there is a single dimensional source.

## Release gates before routing/fabrication

Do not release the PCB until these are checked:

- compare the KiCad Edge.Cuts against the latest Hammond 1554BPL drawing/DXF
- physical fit check with a real 1554B2GYCL enclosure
- mounting-hole/screw/washer/spacer stack
- E73 footprint and antenna orientation against the actual module
- KXOB contact geometry against a physical sample/manufacturer drawing
- NTC1-under-cell mechanical clearance
- PCB-to-lid reference-cell clearance
- M8 gland drill/nut clearance
- battery clearance under PCB and around both mounting bosses
- JLCPCB availability for selected LCSC parts
- ERC clean except intentional documented exclusions
- DRC and schematic-parity clean
