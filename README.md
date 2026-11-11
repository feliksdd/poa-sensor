# POA-Sensor

Kabelgebundener Einstrahlungssensor mit KXOB25-14X1F-Referenzzelle, Präzisionsshunt, Zelltemperaturmessung und ADS1115. Ein Sensor wird über maximal 3 m Kabel von einem [PanelLog](https://github.com/feliksdd/panellog) versorgt und per I²C ausgelesen. Der Sensor wird parallel zur PV-Modulebene und möglichst unverschattet montiert.

| Datei | Inhalt |
|---|---|
| [KiCad-Projekt](hardware/poa-sensor.kicad_pro) · [Schaltplan](hardware/poa-sensor.kicad_sch) | Elektrische Quelle |
| [PCB](hardware/poa-sensor.kicad_pcb) | Layout mit Kradex-Kontur und integrierter Herstellerzeichnung |
| [PDF](hardware/poa-sensor.pdf) · [SVG](hardware/poa-sensor.svg) | Aktuelle Schaltplanansichten |
| [Stückliste](bom/bom.csv) | Bauteile, Bestellnummern und DNP-Bestückung |
| [Schaltung und Auslegung](docs/schaltung.md) | Messkanäle, Versorgung und I²C-Schnittstelle |
| [Mechanischer Aufbau](docs/aufbau.md) | Gehäusekontur, Zellkontakt und Montage |
| [Fertigung](docs/fertigung.md) | Bestückung und Fertigungsstand |

Das Schaltbild verwendet direkt gezeichnete Signalverbindungen, Spannungssymbole und zusammenhängende Funktionsgruppen. Das KiCad-Projekt verwendet KiCad 10. Die vorhandene PanelLog-Schnittstelle bleibt unverändert; eine eigene MCU oder Firmware ist nicht erforderlich.

Das PCB ist für **Kradex ZP60.60.40UJpH TM PC** mit transparentem Deckel angelegt. Das Layout enthält Leiterbahnen und konturgleiche GND-Flächen auf Ober- und Unterseite. Vor der Fertigung sind die offenen Punkte aus der Layoutprüfung zu klären. Herstellerzeichnungen, Freistellungen und Montagehöhe sind in [aufbau.md](docs/aufbau.md) beschrieben.

## Messprinzip und Umrechnung

Die KXOB25-14X1F arbeitet mit dem parallel geschalteten **1-Ω-Shunt RSH1** nahe am Kurzschluss. Auf diesem flachen Abschnitt der Zellkennlinie steigt der Strom näherungsweise proportional zur Einstrahlung in der Modulebene. Der ADS1115 misst die Shuntspannung differenziell an **AIN0–AIN1** mit getrennten Abgriffen an den beiden Shuntpads. Es gilt $I_\mathrm{Zelle} = U_\mathrm{SH}/R_\mathrm{SH}$. Bei einem PGA-Bereich von ±256 mV entspricht ein ADC-Count 7,8125 µV.

Bei 1.000 W/m², 25 °C und AM1.5 gibt ANYSOLAR typisch 58,6 mA Kurzschlussstrom an. Das entspricht am Shunt näherungsweise 58,6 mV bzw. 7.501 Counts. Aus dem typischen Temperaturkoeffizienten von +26,5 µA/K folgt die relative Korrektur $\alpha \approx 0{,}000452\,\mathrm{K}^{-1}$. [Datenblatt der KXOB25-14X1F](https://www.digikey.com/htmldatasheets/production/3648849/0/0/1/kxob25-14x1f-tr.pdf)

$$
G_\mathrm{POA} \approx 1000\,\frac{\mathrm W}{\mathrm{m^2}}\,
\frac{U_\mathrm{SH}-U_0}{58{,}6\,\mathrm{mV}}\,
\frac{1}{1+\alpha(T_\mathrm{Zelle}-25\,{}^\circ\mathrm C)}
$$

$U_0$ ist der bei lichtdicht abgedeckter Referenzzelle gemessene Offset. $T_\mathrm{Zelle}$ stammt vom NTC an der Zellrückseite. Eine offsetbereinigte Shuntspannung von 35,16 mV entspricht nominal 600 W/m² bei 25 °C bzw. 591 W/m² bei 60 °C.

Für absolute Werte den fertig montierten Sensor **mit Deckel** kalibrieren. Zuerst den Dunkeloffset $n_0$ in ADC-Counts erfassen. Dann bei stabiler Einstrahlung gleichzeitig den Sensorwert $n_\mathrm{ref}$, seine Zelltemperatur $T_\mathrm{ref}$ und die Einstrahlung $G_\mathrm{ref}$ einer kalibrierten Silizium-Referenzzelle messen. Beide Sensoren liegen in derselben Ebene. Die individuelle Empfindlichkeit ist

$$
S_{25} = \frac{n_\mathrm{ref}-n_0}{G_\mathrm{ref}\,[1+\alpha(T_\mathrm{ref}-25\,{}^\circ\mathrm C)]}
\quad \text{in Counts pro W/m².}
$$

Für die Auswertung in PanelLog gilt $G_\mathrm{POA}=(n-n_0)/(S_{25}[1+\alpha(T_\mathrm{Zelle}-25\,{}^\circ\mathrm C)])$. So gehen Zellstreuung, Shunt, ADC-Verstärkung und Deckeltransmission bei der Kalibriergeometrie in den Faktor ein. Den Einfluss des Deckels bei schrägem Lichteinfall separat durch Vergleichsmessungen prüfen. [Messkanäle und NTC-Auswertung](docs/schaltung.md)

## Werkzeuge

`bash tools/check_hardware.sh` prüft ERC, Netzliste und Stückliste. Die Ausgaben liegen in `build/kicad/` und werden nicht versioniert. `bash tools/export_schematic.sh` aktualisiert die PDF-/SVG-Ansichten unter `hardware/`.

Die verbindlichen Regeln für weitere Arbeiten stehen in [AGENTS.md](AGENTS.md).
