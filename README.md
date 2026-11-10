# POA-Sensor

Kabelgebundener Einstrahlungssensor mit KXOB25-14X1F-Referenzzelle, Präzisionsshunt, Zelltemperaturmessung und ADS1115. Ein Sensor wird über maximal 3 m Kabel von einem [PanelLog](https://github.com/feliksdd/panellog) versorgt und per I²C ausgelesen. Der Sensor wird parallel zur PV-Modulebene und möglichst unverschattet montiert.

| Datei | Inhalt |
|---|---|
| [KiCad-Projekt](hardware/poa-sensor.kicad_pro) · [Schaltplan](hardware/poa-sensor.kicad_sch) | Elektrische Quelle |
| [PDF](hardware/poa-sensor.pdf) · [SVG](hardware/poa-sensor.svg) | Aktuelle Schaltplanansichten |
| [Stückliste](bom/bom.csv) | Bauteile, Bestellnummern und DNP-Bestückung |
| [Schaltung und Auslegung](docs/schaltung.md) | Messkanäle, Versorgung und I²C-Schnittstelle |
| [Mechanischer Aufbau](docs/aufbau.md) | Gehäusekontur, Zellkontakt und Montage |
| [Fertigung](docs/fertigung.md) | Bestückung und Fertigungsstand |

Das Schaltbild verwendet direkt gezeichnete Signalverbindungen, Spannungssymbole und zusammenhängende Funktionsgruppen. Das KiCad-Projekt verwendet KiCad 10. Die vorhandene PanelLog-Schnittstelle bleibt unverändert; eine eigene MCU oder Firmware ist nicht erforderlich.

**Für den kabelgebundenen Sensor ist noch kein geroutetes PCB vorhanden.** Die [Gehäusekontur](mechanical/poa-outline.kicad_pcb) enthält nur die mechanische Grundlage.

## Werkzeuge

`bash tools/check_hardware.sh` prüft ERC, Netzliste und Stückliste. Die Ausgaben liegen in `build/kicad/` und werden nicht versioniert. `bash tools/export_schematic.sh` aktualisiert die PDF-/SVG-Ansichten unter `hardware/`.

Die verbindlichen Regeln für weitere Arbeiten stehen in [AGENTS.md](AGENTS.md).
