# POA Sensor — kabelgebundene Referenzzelle

Aktuelle elektrische Revision: **0.3, 2026-11-10**. Ein POA-Sensor wird über maximal 3 m Kabel von genau einem [PanelLog](https://github.com/feliksdd/panellog) versorgt und per I²C ausgelesen. Das Kabel wird an beiden Enden direkt angelötet und mechanisch zugentlastet.

Der Sensor enthält eine KXOB25-14X1F-Referenzzelle, einen Präzisionsshunt, einen NTC an der Referenzzelle und einen ADS1115. Eigene Batterie, Mikrocontroller und Funk entfallen. PV-Modulspannung, Strom, Abschaltung und Modulrückseitentemperatur bleiben bei PanelLog.

- **Aktueller Schaltplan:** [hardware/poa-sensor.kicad_sch](hardware/poa-sensor.kicad_sch)
- **Ansicht:** [SVG](hardware/review_2026-11-10/poa-sensor.svg) · [PDF](hardware/review_2026-11-10/poa-sensor.pdf)
- **Verbindliche Schnittstelle und Auslegung:** [docs/architecture.md](docs/architecture.md)
- **Aktuelle elektrische Stückliste:** [bom/bom.csv](bom/bom.csv); DNP-Teile separat gekennzeichnet. Keine neue pauschale Lager-/Preiszusage.
- **Prüfung und Grenzen:** [docs/wired_revision_2026-11-10.md](docs/wired_revision_2026-11-10.md)

Die bisherige Funkversion liegt unter `hardware/poa-sensor-wireless-legacy.*`; ihre Platine gehört ausschließlich zu dieser historischen Schaltung. **Für die kabelgebundene Revision gibt es noch keine passende Platine.** Diese Änderung ist eine Schaltplanrevision, keine Fertigungsfreigabe. Die zugehörigen Änderungen im PanelLog-Schaltplan müssen ebenfalls erst ins Layout übernommen werden.

`bash tools/review_hardware.sh` führt native ERC, Netlist-Abgleich und Zeichnungsexport aus. Die Schaltung ist im nativen KiCad-9-Dateiformat gespeichert und lässt sich auch mit KiCad 10 öffnen; die PanelLog-Datei bleibt unverändert im KiCad-10-Format. Historische Berichte und Beschaffungslisten mit Datum 2026-11-09 gelten nur für ihre damaligen Quellen.
