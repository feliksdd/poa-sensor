# Arbeitsregeln

## Schaltpläne

- Signale direkt mit Leitungen verbinden. Netzlabels benennen Netze und ersetzen keine übersichtlich darstellbare Verbindung.
- Versorgung und GND mit Spannungssymbolen darstellen. Gefilterte oder getrennte Versorgungsschienen elektrisch getrennt halten.
- Bauteile nach Funktion gruppieren; die Leitungsführung kurz, nachvollziehbar und kreuzungsarm gestalten.
- Symbol-Pins dürfen für die Darstellung umgeordnet werden; elektrische Pinnummern, Footprints und Anschlussbelegung müssen erhalten bleiben.
- Nach Darstellungsänderungen ERC und Netzliste prüfen. Ansichten mit `bash tools/export_schematic.sh` aktualisieren.

## Repository

- Nur den aktuellen Stand pflegen: eine maßgebliche Schaltung, eine Stückliste und aktuelle Dokumentation.
- Keine Legacy-Entwürfe, Backups, Review-Dokumente, Verlaufsbeschreibungen oder datierten Prüf-/Beschaffungssnapshots hinzufügen.
- Prüfberichte und temporäre Exporte ausschließlich in `build/` oder außerhalb des Repositorys erzeugen und nicht versionieren.
- Aktuelle PDF-/SVG-Schaltplanansichten unter `hardware/` müssen zur KiCad-Quelle passen.
- Nur benötigte Symbole, Footprints, Modelle und Hilfsskripte behalten. Relative Verweise nach Bereinigungen prüfen.
- Die vorhandene PanelLog-Schnittstelle verwenden. PanelLog und dessen Versorgungsschaltung nicht im Rahmen von POA-Arbeiten ändern.
