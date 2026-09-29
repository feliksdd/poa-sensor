# Mechanical

This directory contains enclosure, mounting and external temperature-probe design information.

Current baseline:

- Hammond **1554B2GYCL** enclosure
- PCB `Edge.Cuts` follows the **Hammond 1554BPL steel-panel profile** rather than a generic rectangular board
- two PCB mounting holes follow the 1554BPL manufacturer hole pattern
- reference cell directly below a small clear optical window
- white outdoor cast-vinyl mask over the remaining transparent lid
- external two-wire PV-module NTC probe
- M8-class IP68 cable gland
- mounting bracket keeps sensor plane parallel to PV module plane

Mechanical source of truth for the PCB outline is `hardware/poa-sensor-layout-template.kicad_pcb`. See `mechanical/pcb-layout.md` for dimensions, placement constraints and release checks.
