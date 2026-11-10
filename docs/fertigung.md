# Bestückung und Fertigung

## Stückliste

[bom/bom.csv](../bom/bom.csv) ist die maßgebliche elektrische Stückliste. `MPN`, `LCSC`, `Footprint` und `Assembly` beschreiben Bestellung und Bestückung. DNP-Positionen werden nicht bestückt. Die Daten sind keine aktuelle Preis- oder Lagerbestandszusage.

Standardbestückung ist **DIRECT**: R6/R7 sind 0-Ω-Brücken; U2, C5 und R8–R11 bleiben unbestückt. Die gepufferte Option und passende PanelLog-Bestückung stehen in [schaltung.md](schaltung.md).

CELL1, Verbindungskabel, Gehäuse, Kabeleinführung und optische Maske werden von Hand montiert. Der externe PV-Modultemperaturfühler gehört zu PanelLog.

## Platine

Ein geroutetes PCB und zugehörige Gerber-/CPL-Dateien liegen noch nicht vor. Grundlage sind der aktuelle Schaltplan und die [mechanische Kontur](../mechanical/poa-outline.kicad_pcb). Vorgesehen sind zwei Lagen, 1,6 mm FR-4 und einseitige SMD-Bestückung.

Vor Bestellung müssen Schaltplan und PCB übereinstimmen, ERC/DRC bestehen und Zell-/NTC-Aufbau, Gehäusepassung sowie Kabel-/ESD-Anordnung geprüft sein. Fertigungsdaten gemeinsam aus derselben aktuellen Konstruktion exportieren. Zwischenstände und Prüfberichte gehören nicht in das Repository.
