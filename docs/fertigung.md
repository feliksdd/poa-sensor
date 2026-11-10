# Bestückung und Fertigung

## Stückliste

[bom/bom.csv](../bom/bom.csv) ist die maßgebliche elektrische Stückliste. `MPN`, `LCSC`, `Footprint` und `Assembly` beschreiben Bestellung und Bestückung. DNP-Positionen werden nicht bestückt. Die Daten sind keine aktuelle Preis- oder Lagerbestandszusage.

Standardbestückung ist **DIRECT**: R6/R7 sind 0-Ω-Brücken; U2, C5 und R8–R11 bleiben unbestückt. Die gepufferte Option und passende PanelLog-Bestückung stehen in [schaltung.md](schaltung.md).

Die mit LCSC-Nummer versehenen SMD-Positionen sind für den LCSC-Einkauf spezifiziert. Bestellmengen und Staffelpreise pro Typ prüfen; mehrere Positionen mit gleicher MPN gemeinsam bestellen. R8/R9 verwenden Yageo RC0603FR-071KL (C22548), bleiben in DIRECT aber DNP und gehören nicht in die Standardbestellung.

CELL1 wird separat als ANYSOLAR KXOB25-14X1F-TR beschafft, z. B. bei DigiKey als Gurtabschnitt KXOB25-14X1FCT-ND. Für diese Zelle ist kein passender LCSC-Ersatz freigegeben. Andere Solarzellen sind wegen Kennlinie, Abmessungen und thermischem Aufbau keine pauschalen Ersatztypen.

CELL1, Verbindungskabel, Gehäuse, Kabeleinführung und optische Maske werden von Hand montiert. Der externe PV-Modultemperaturfühler gehört zu PanelLog.

## Platine

Das [PCB](../hardware/poa-sensor.kicad_pcb) enthält die Gehäusekontur, vier NPTH-Befestigungen, Freistellungen für die Deckeldome und alle 26 elektrischen Positionen. Die Bestückung liegt auf der Oberseite; vorgesehen sind zwei Lagen und 1,6 mm FR-4. Die DNP-Positionen sind ebenfalls platziert.

**Routing und Fertigungsdaten sind offen.** Die Luftlinien bleiben sichtbar; Gerber-/CPL-Dateien werden erst nach dem Routing erzeugt. Die Gehäusehöhe, Abstandshalter, Kabeleinführung und der Zellkontakt müssen am Muster abgeglichen werden.

Die normalen Leiterbahnabstände betragen 0,20 mm. Innerhalb der Standard-Footprints von U1, D1 und NTC1 sind 0,15 mm erlaubt. Nur für NTC1 unter CELL1 ist die beabsichtigte Überlappung der mechanischen Courtyards zugelassen; elektrische Abstände bleiben geprüft.

Vor Bestellung müssen Schaltplan und PCB übereinstimmen, ERC/DRC bestehen und Zell-/NTC-Aufbau, Gehäusepassung sowie Kabel-/ESD-Anordnung geprüft sein. Fertigungsdaten gemeinsam aus derselben aktuellen Konstruktion exportieren. Zwischenstände und Prüfberichte gehören nicht in das Repository.
