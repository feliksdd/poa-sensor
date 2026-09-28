# JLCPCB manufacturing notes

## Source of truth

KiCad is the source of truth. JLCPCB fabrication and assembly files are generated from the tagged KiCad revision.

## Component policy

- Prefer JLCPCB Basic parts for generic resistors and capacitors.
- Use Extended parts only when their electrical/mechanical function justifies them.
- Store the JLCPCB/LCSC code in the KiCad symbol field `LCSC`.
- Also store `Manufacturer`, `MPN`, `Assembly` and `DNP` fields.
- Do not silently substitute the irradiance shunt, ADC, NTC type, radio module or LF crystal without an engineering review.

## Expected manual assembly after PCBA

The following are currently expected to be assembled outside JLCPCB:

- ANYSOLAR KXOB25-14X1F reference cell
- external module-temperature NTC and cable
- Li-SOCl2 battery with factory tabs/leads
- cable gland
- enclosure and reflective optical mask

## Release contents

For a hardware release, generate:

- Gerbers
- drill files
- BOM CSV
- component placement/CPL CSV
- schematic PDF
- assembly drawing
- PCB render/screenshots
- released `*.kicad_pro`, `*.kicad_sch`, `*.kicad_pcb`

Generated Gerber/assembly directories are ignored on normal development commits and should be attached to tagged releases or explicitly committed only when useful for traceability.
