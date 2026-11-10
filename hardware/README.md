# Aktuelle Hardware: kabelgebundener POA, Revision 0.3

`poa-sensor.kicad_pro` / `poa-sensor.kicad_sch` sind das aktive Projekt: Referenzzelle, Shunt, Zell-NTC und I²C-ADC. Kabel und Versorgung sind in [architecture.md](../docs/architecture.md) festgelegt. Projektlokale Symbole einschließlich der festgelegten R/C-Kopien vermeiden unterschiedliche Symbolbibliotheken zwischen KiCad 9 und 10; Footprints verweisen auf Standardbibliotheken bzw. `POA`.

Die früheren Dateien `poa-sensor-wired.*` wurden als Hauptprojekt übernommen. Die alte Batterie-/Funkversion heißt jetzt `poa-sensor-wireless-legacy.*`; auch ihre PCB-Datei trägt diesen Namen, damit sie nicht versehentlich mit dem neuen Hauptschaltplan zusammen bestellt wird. Frühere `.sch`-Bootstrap-Dateien und Normalisierungsskripte gehören ebenfalls zur Funkversion.

**Es existiert noch kein passendes kabelgebundenes PCB-Layout.** Das bestehende Layout-Template ist nur eine historische mechanische Vorlage. Für ein neues Layout Kelvin-Abgriffe, NTC-Zellkontakt, ruhige analoge Masse, Kabel-/ESD-Platzierung, Zugentlastung und optisches Fenster neu prüfen. Keine Fertigungsfreigabe aus einem ERC-Ergebnis ableiten.

Prüfen: `bash tools/review_hardware.sh`. Die Ausgabe liegt in `review_2026-11-10/`; der Netlist-Check prüft ADC-Pins, Kabelbelegung, ESD-Pins und Versorgungsdomänen. Für Montage-/Messhinweise siehe [Schaltplanrevision](../docs/wired_revision_2026-11-10.md).
