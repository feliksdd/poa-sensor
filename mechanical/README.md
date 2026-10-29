# Mechanical

This directory contains enclosure, optical-window and mounting information for the **standalone battery-powered POA sensor**.

Current baseline:

- Hammond **1554B2GYCL** enclosure
- PCB `Edge.Cuts` follows the **Hammond 1554BPL steel-panel profile** rather than a generic rectangular board
- two PCB mounting holes follow the 1554BPL manufacturer hole pattern
- reference cell directly below a small clear optical window
- white outdoor cast-vinyl mask over the remaining transparent lid
- mounting bracket keeps the sensor plane parallel to the corresponding PV-module plane
- placement is chosen for representative **unshaded POA irradiance**, independently of PanelLog/module wiring

The old v0.1 concept includes an M8-class cable gland for an external PV-module NTC. That probe/gland requirement is **legacy after the PanelLog split** and should be removed from the next POA enclosure/PCB revision. Module temperature is measured locally by [PanelLog](https://github.com/feliksdd/panellog).

Mechanical source of truth for the PCB outline is `hardware/poa-sensor-layout-template.kicad_pcb`. See `mechanical/pcb-layout.md` for dimensions, placement constraints and release checks.
