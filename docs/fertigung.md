# Bestückung und Fertigung

## Stückliste

[bom/bom.csv](../bom/bom.csv) ist die maßgebliche elektrische Stückliste. `MPN`, `LCSC`, `Footprint` und `Assembly` beschreiben Bestellung und Bestückung. DNP-Positionen werden nicht bestückt. Die Daten sind keine aktuelle Preis- oder Lagerbestandszusage.

Standardbestückung ist **DIRECT**: R6/R7 sind 0-Ω-Brücken; U2, C5 und R8–R11 bleiben unbestückt. Die gepufferte Option und passende PanelLog-Bestückung stehen in [schaltung.md](schaltung.md).

Die LCSC-Nummern identifizieren die Teile auch im JLCPCB-Bestückungskatalog. Die Lagerbestände von LCSC und JLCPCB sind getrennt; für eine bestückte Platine zählt der JLCPCB-Bestand. Bestellmengen, Bestückungsverluste und Staffelpreise pro Typ prüfen; mehrere Positionen mit gleicher MPN gemeinsam zusammenfassen. R8/R9 verwenden Uniroyal 0603WAF1001T5E (C21190), bleiben in DIRECT aber DNP und gehören nicht in die Standardbestellung.

## JLCPCB-Bestückung

Die Baugrößen sind für **Economic PCBA** ausgelegt: NTC1 ist 0402, die übrigen SMD-Bauteile sind größer oder haben mindestens 0,5 mm Pinabstand. Eine Bestellfreigabe setzt weiterhin das fertige Routing und die Prüfung der übrigen Fertigungsoptionen voraus. Vor Bestellung die aktuelle Katalogklasse und Verfügbarkeit kontrollieren.

| Klasse | DIRECT-Positionen | Unterschiedliche Typen |
|---|---|---|
| Basic | R4/R5 C22775; R6/R7 C21189; R12 C22859; C1/C3/C4/C7 C14663; C2/C6 C28323 | 5 |
| Extended | RSH1 C865286; R1–R3 C2828645; U1 C37593; D1 C1972959; NTC1 C209959 | 5 |

Bei Economic PCBA fällt die Zuführungsgebühr je unterschiedlichem Extended-Typ und Auftrag an, nicht je Position oder Platine. Basic und Preferred/Promotional Extended sind dort von dieser Gebühr befreit. Bei Standard PCBA werden auch Basic-Typen mit einer Zuführungsgebühr belastet. R1–R3 zählen gemeinsam als ein Typ; ihre 0,1-%-Toleranz und 25 ppm/K bleiben ebenso erhalten wie die des Shunts. Die DNP-Option erzeugt in DIRECT keine Bestückungsgebühren.

C2/C6 sind Basic-Typen in 0805 mit 1 µF, 50 V, X7R und ±10 %. Ein 0603-X5R-Ersatz mit nur 85 °C Dielektrikbereich ist für diesen Aufbau nicht vorgesehen. NTC1 bleibt Extended; seine 0402-Baugröße vermeidet die 0201-bedingte Einschränkung auf Standard PCBA.

Quellen: [JLCPCB-Kapazitäten](https://jlcpcb.com/capabilities/pcb-assembly-capabilities), [Gebühren](https://jlcpcb.com/help/article/pcb-assembly-price), [Basic/Preferred](https://jlcpcb.com/help/article/pcb-assembly-faqs).

CELL1 wird separat als ANYSOLAR KXOB25-14X1F-TR beschafft, z. B. bei DigiKey als Gurtabschnitt KXOB25-14X1FCT-ND. Für diese Zelle ist kein passender LCSC-Ersatz freigegeben. Andere Solarzellen sind wegen Kennlinie, Abmessungen und thermischem Aufbau keine pauschalen Ersatztypen.

CELL1, Verbindungskabel, Gehäuse, Kabeleinführung und optische Maske werden von Hand montiert. Der externe PV-Modultemperaturfühler gehört zu PanelLog.

## Platine

Das [PCB](../hardware/poa-sensor.kicad_pcb) enthält die Gehäusekontur, vier NPTH-Befestigungen, Freistellungen für die Deckeldome und alle 26 elektrischen Positionen. Die Bestückung liegt auf der Oberseite; vorgesehen sind zwei Lagen und 1,6 mm FR-4. Die DNP-Positionen sind ebenfalls platziert.

**Routing und Fertigungsdaten sind offen.** Die Luftlinien bleiben sichtbar; Gerber-/CPL-Dateien werden erst nach dem Routing erzeugt. Die Gehäusehöhe, Abstandshalter, Kabeleinführung und der Zellkontakt müssen am Muster abgeglichen werden.

Die normalen Leiterbahnabstände betragen 0,20 mm. Innerhalb der Standard-Footprints von U1, D1 und NTC1 sind 0,15 mm erlaubt. Nur für NTC1 unter CELL1 ist die beabsichtigte Überlappung der mechanischen Courtyards zugelassen; elektrische Abstände bleiben geprüft.

Vor Bestellung müssen Schaltplan und PCB übereinstimmen, ERC/DRC bestehen und Zell-/NTC-Aufbau, Gehäusepassung sowie Kabel-/ESD-Anordnung geprüft sein. Fertigungsdaten gemeinsam aus derselben aktuellen Konstruktion exportieren. Zwischenstände und Prüfberichte gehören nicht in das Repository.
