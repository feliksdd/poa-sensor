# Mechanischer Aufbau

## Gehäuse und Herstellerdaten

Verwendet wird **Kradex ZP60.60.40UJpH TM PC**: hellgraues Polycarbonat-Unterteil, transparenter PC-Deckel, Dichtung, Messinggewinde für den Deckel und äußere Befestigungslaschen. Die ähnlich bezeichnete ABS-PC-Ausführung hat ein ABS-Unterteil. Schutzart des unveränderten Gehäuses: IP65; Öffnungen passend abdichten.

- [Hersteller und Bestellvariante](https://www.kradex.de/product/gehaeuse_hermetisch_aus_polykarbonat/zp60_60_40ujph_tm_pc)
- [Originalzeichnung: Zusammenbau, Unterteil, Deckel](../mechanical/manufacturer/Kradex_ZP60_60_40.pdf)
- [Datenblatt mit empfohlener Platinenkontur](../mechanical/manufacturer/Kradex_ZP60_60_40_datasheet.pdf)

Die Unterteilzeichnung ist als editierbare Liniengrafik auf **Dwgs.User** rechts neben dem PCB integriert. Sie ist verkleinert; die eingetragenen Zahlenmaße gelten. **User.1** zeigt am PCB den inneren Deckelraum und die vier Deckeldome im Maßstab 1:1. Diese Dokumentationslagen gehören nicht in die Fertigungs-Gerber.

## Platinenkontur und Befestigung

[hardware/poa-sensor.kicad_pcb](../hardware/poa-sensor.kicad_pcb) ist die einzige Platinenquelle. Die Hersteller-Platinenkontur mit 51,16 mm Außenmaß und abgestuften Ecken bildet die Grundlage. Für die Montage nahe dem optischen Fenster ist sie umlaufend um 1,08 mm eingezogen: Der Deckel hat nur 50,2 mm freien Innenraum. Vier zusätzliche, zu den äußeren Eckausschnitten offene Kreisfreistellungen lassen die inneren Deckeldome passieren. Die Kontur besteht aus echten Geraden und Kreisbögen.

| Größe | Wert |
|---|---|
| Gehäusekörper | 61,3 × 61,1 × 40,1 mm |
| Länge einschließlich Laschen | 91,3 mm |
| PCB | 49,00 × 49,00 mm; 1,6 mm FR-4; 2 Lagen |
| PCB-Begrenzung in KiCad | X/Y = 100,00 bis 149,00 mm |
| PCB-/Zellmittelpunkt | X/Y = 124,50 mm |
| H1–H4 | 4 × Ø 2,60 mm NPTH, gemäß Hersteller-Platinenzeichnung |
| H1 relativ zur PCB-Begrenzung | (24,500; 2,645) mm |
| H2 | (46,065; 24,500) mm |
| H3 | (24,500; 46,355) mm |
| H4 | (2,935; 24,500) mm |
| Befestigungsraster | 43,13 mm horizontal / 43,71 mm vertikal |
| Deckeldome | Raster 30,95 × 30,95 mm; Freistellungen Ø 9,00 mm |
| Mitten der Deckelfreistellungen relativ zur PCB-Begrenzung | X/Y jeweils 9,025 oder 39,975 mm |

Die PCB-Orientierung entspricht der empfohlenen Platinenzeichnung; gegenüber der Unterteil-Draufsicht liegt sie um 90° gedreht. Die Original-Unterteilzeichnung nennt für die Dome 43,7 / 43,15 mm; die Differenz zur PCB-Zeichnung beträgt höchstens 0,02 mm. Kunststoff- und Zeichnungstoleranzen am Muster prüfen. Die 2,6-mm-Bohrungen sind keine M3-Durchgangsbohrungen. Befestigungsmittel passend zu den tatsächlichen Kunststoffdomen auswählen, nicht die M3-Deckelschrauben verwenden.

## Montagehöhe und Zellkontakt

Die Platine wird auf zusätzlichen isolierenden Abstandshaltern über den Bodendomen angeordnet. **Etwa 22 mm zusätzliche Höhe** ist ein Startwert für den Musteraufbau, keine freigegebene Abstandshalterlänge. Vor Festlegung die Deckelinnenfläche, Dome, Schraubenköpfe und die Bauhöhe von Platine, Lötung und Zelle vermessen. Ziel: Zelloberseite etwa 1–2 mm unter der inneren Deckelfläche. Die vollständige Höhenpassung ist am realen Gehäuse abzugleichen.

CELL1 und NTC1 liegen exakt übereinander. Die Zellunterseite soll nominal **0,7 mm über der Platinenoberseite** liegen und den **0,50 ±0,05 mm hohen 0402-NTC** freistellen. Nominell bleiben 0,2 mm für Lötung, Toleranzen und thermische Kopplung; der NTC darf die Zelle nicht mechanisch tragen. Eine kleine Menge thermisch leitfähiger, elektrisch isolierender Kleber oder Silikon koppelt den NTC an die Zellrückseite, ohne Druck auszuüben. Bei 1,8 mm nominaler Zellhöhe liegt die Zelloberseite 2,5 mm über dem PCB. Den Abstand der Platine zum Deckel darauf abstimmen und am Muster prüfen. Die Zelle nach der SMD-Bestückung von Hand montieren. Eine gezielte Courtyard-Regel erlaubt ausschließlich diese beabsichtigte Überlappung.

Eine außen aufgebrachte weiße, wetterfeste Deckelmaske reduziert die solare Erwärmung. Das Fenster größer als die Zelle ausführen und bei schrägem Lichteinfall auf Abschattung prüfen. Zelle und Deckel gemeinsam kalibrieren.

## Platzierung, Kabel und Dachmontage

- Zelle und NTC liegen mittig unter dem Fenster. Die Kelvin-Leitungen zu R4 und R5 zweigen direkt an den beiden Shuntpads vom Zellstrompfad ab. Eine lokale Sperrfläche auf F.Cu hält den GND-Guss und Vias vom Sense-Zweig zwischen R5.1 und RSH1.2 fern. Der Zweig trifft am Shuntpad auf die Massefläche. Die durchgehende Bottom-Fläche ist außerhalb der Sperrfläche über GND-Vias mit Top verbunden.
- Temperaturteiler, Referenzteiler, Filter und ADC-Abblockung lokal gruppiert. I²C-Brücken und optionale DNP-Pufferung liegen rechts, getrennt vom analogen Messbereich.
- J1 liegt am unteren Rand. Pinreihenfolge links nach rechts: **1 +3V3, 2 GND, 3 SDA, 4 GND, 5 SCL, 6 GND**. D1 liegt unmittelbar davor; den ESD-Massepfad beim Routing kurz halten.
- Das Kabel mit drei verdrillten Paaren direkt anlöten und unter der erhöhten Platine zugentlasten. Die Kabeleinführung hangabwärts im Unterteil vorsehen. Mutter und Gewindelänge müssen unter der Platine bleiben und Abstand zu den Bodendomen halten. Die Markierung auf User.1 ist ein Bauraumhinweis, kein freigegebenes Bohrbild für eine bestimmte Verschraubung.
- Gehäuse über die äußeren Laschen an einem kurzen Alu-Halter auf der PV-Montageschiene befestigen. Die vier Ø5-mm-Löcher haben ein Raster von 32 × 76,3 mm. M4-Schrauben mit großen Unterlegscheiben verwenden und die Kunststofflaschen nicht verspannen.
- Sensor neben dem Modul, parallel zur PV-Ebene und möglichst auf Höhe der Glasoberfläche anordnen. Rahmen und Halter dürfen die Referenzzelle nicht abschatten. Die Schienenbefestigung benötigt keine zusätzliche Dachdurchdringung.

## Bibliotheken und 3D-Modelle

Die Projektbibliothek `POA` enthält Zelle, Kabelpads und die Kradex-Befestigungsbohrung. Die benötigten [KiCad-Standardfootprints](https://github.com/KiCad/kicad-footprints) liegen ebenfalls unter `hardware/footprints`; die projektspezifische Bibliothekstabelle verwendet diese festgelegten Versionen. Die benötigten Standard-Bauteilmodelle sind unter [hardware/3dmodels/standard](../hardware/3dmodels/standard) mit relativen PCB-Verweisen eingebunden. Quelle: [KiCad packages3D](https://github.com/KiCad/kicad-packages3D); Lizenz und Quellenhinweise liegen bei den Bibliotheksdateien. Das vorhandene Zellmodell ist ein vereinfachtes Hüllmodell mit 0,7 mm Montageabstand, kein Herstellermodell. Für NTC1 ist im lokalen 0402-Footprint das [TDK-Herstellermodell](../hardware/3dmodels/TDK_NTCG103JF103FT1.step) eingebunden; Ausrichtung und Quelle sind in [3dmodels/README.md](../hardware/3dmodels/README.md) beschrieben.

Ein verwendbares Hersteller-STEP des Gehäuses ist nicht eingebunden: Die im Kradex-Datenblatt verlinkte Datei ist nicht abrufbar; das vollständige Herstellerpaket enthält nur 2D-Daten. Die Gehäusepassung beruht auf den Originalzeichnungen und benötigt den Musterabgleich.
