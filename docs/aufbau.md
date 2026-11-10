# Mechanischer Aufbau

## Gehäuse und Kontur

Vorgesehen ist das Hammond-Gehäuse **1554B2GYCL** mit transparentem Deckel. [mechanical/poa-outline.kicad_pcb](../mechanical/poa-outline.kicad_pcb) enthält die vom 1554BPL-Profil abgeleitete Kontur und die Befestigungsbohrungen. Sie enthält keine bestückte oder geroutete Sensorplatine.

| Größe | Wert |
|---|---|
| Maximale Konturabmessungen | 55,45 × 55,96 mm |
| Eckradius | 9,525 mm |
| Befestigungsbohrungen | 2 × Ø 3,73 mm, NPTH |
| Lochmitten ab linkem/oberem Konturdatum | (27,98; 16,46) mm und (27,98; 37,98) mm |
| Lochabstand | 21,52 mm |
| Konturdatum in der KiCad-Datei | X=100,00 mm; Y=100,00 mm |

Die Kontur ist wegen der Gehäusefreistellungen asymmetrisch. Beim Platinenentwurf die vorhandenen Edge.Cuts übernehmen und Platz für Schraubenköpfe, Unterlegscheiben und Abstandshalter lassen. Die zugehörige Lochgeometrie ist als projektlokaler Footprint hinterlegt.

## Referenzzelle und Temperaturkontakt

CELL1 wird unter dem optischen Fenster montiert. NTC1 liegt auf derselben Platinenseite unmittelbar unter der Zellenmitte. Die Montagehöhe der Zelle muss das etwa 0,3 mm hohe 0201-Bauteil freistellen. Eine kleine Menge thermisch leitfähiger, elektrisch isolierender Kleber oder Silikon koppelt den NTC an die Zellrückseite, ohne mechanischen Druck auszuüben.

Die Zelle wird nach der SMD-Bestückung von Hand montiert. Gehäuse, Fenster und Zelle bilden die gemeinsam zu kalibrierende optische Baugruppe. Eine außen aufgebrachte weiße, wetterfeste Deckelmaske lässt das optische Fenster frei und reduziert die solare Erwärmung. Das Fenster benötigt auch bei schrägem Lichteinfall ausreichend Randabstand zur Zelle.

Zielabstand zur inneren Deckelfläche: etwa 1–2 mm. Die Abstandshalterhöhe anhand des realen Gehäuses, Deckels und Zellaufbaus bestimmen.

## Platzierung und Leitungen

- Zell-/Shunt-Stromschleife kurz halten; beide ADC-Kelvin-Leitungen separat von den Shuntanschlüssen abführen.
- ADC, Eingangsfilter und Temperaturteiler lokal gruppieren. Digitale Leitungen nicht durch den Kelvin-Bereich führen.
- Kabelpads und ESD-Beschaltung nahe der Kabeleinführung anordnen; den ESD-Massepfad kurz halten.
- Das Kabel mit drei verdrillten Paaren direkt anlöten, zugentlasten und die Gehäuseeinführung abdichten.
- Den Sensor parallel zur PV-Ebene an einer repräsentativen, unverschatteten Stelle befestigen.

## Bibliotheken und Modelle

Die KiCad-Tabellen registrieren die projektlokale Bibliothek als `POA`. Referenzzelle und Kabelpads verwenden eigene Footprints, Standard-SMD-Bauteile die KiCad-Standardbibliotheken. Das STEP-Modell der KXOB-Zelle ist ein vereinfachtes Hüllmodell zur Platzkontrolle, kein Herstellermodell. Es ersetzt keinen Abgleich der Kontaktgeometrie und Passung am realen Bauteil.
