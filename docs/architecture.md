# Elektrische Architektur — POA Revision 0.3

Festgelegt am 2026-11-10: maximal ein POA pro PanelLog, maximal 3 m Kabel, drei verdrillte Aderpaare, Lötanschlüsse. Das optische Konzept bleibt eine zur PV-Ebene parallele, unverschattete Silizium-Referenzzelle; kein meteorologisches Referenzpyranometer.

## Funktion und Messkanäle

| Element | Funktion |
|---|---|
| CELL1 KXOB25-14X1F | Lokale Referenzzelle, nahe Kurzschluss betrieben |
| RSH1 RT0805BRD071RL, C865286 | 1 Ω, 0,1 %, 25 ppm/K, 0805; getrennte Force-/Kelvin-Anschlüsse |
| U1 ADS1115IDGSR, C37593 | I²C-ADC; ADDR an GND, Adresse 0x48 |
| AIN0–AIN1 | Differenziell über R4/R5 (100 Ω) und C3 (100 nF) am Shunt |
| AIN2 | NTC1 NTCG063JF103FTBA, 0201, thermisch an der Referenzzelle |
| AIN3 | Lokale analoge Versorgung / 2 über R2/R3, je 47 kΩ / 0,1 %; C7=100 nF |

ALERT/RDY bleibt unbeschaltet; PanelLog pollt die Wandlungen. Kein MCU und keine Firmware auf dem POA-Board. Kein zweiter Temperaturfühler für das PV-Modul.

58,6 mA bei 1000 W/m² ergeben ideal 58,6 mV und 3,43 mW am Shunt. Bei PGA ±0,256 V beträgt die Quantisierung 7,8125 µV bzw. rechnerisch 0,133 W/m² je LSB. Das ist Auflösung, keine Messgenauigkeit. Zellkennlinie, Fenstertransmission, Winkel und Temperatur erfordern Kalibrierung. 100 Ω + 100 Ω / 100 nF ergeben ungefähr 7,96 kHz analoge Grenzfrequenz.

## Kabel und Host-Pins

| PanelLog J8 | POA J1 | Signal | Paar |
|---|---|---|---|
| 1 | 1 | POA_VDD_CABLE, 3,3 V nominal über PanelLog R36 | mit 2 |
| 2 | 2 | GND | Versorgung |
| 3 | 3 | SDA | mit 4 |
| 4 | 4 | GND | SDA-Rückleiter |
| 5 | 5 | SCL | mit 6 |
| 6 | 6 | GND | SCL-Rückleiter |

Aktueller PanelLog-C6-WROOM-Schaltplan: SDA = **GPIO22 / Modulpad 20**, SCL = **GPIO23 / Modulpad 21**. Die früheren MINI-Angaben GPIO21/22 sind überholt. Der vorhandene INA237-Bus bleibt auf GPIO6/GPIO7. Adresse 0x48 kann daher unabhängig verwendet werden. Spätere Host-Firmware muss GPIO22/23 verwenden; diese Revision entwickelt oder ändert keine Firmware.

UV-/außentaugliches Kabel verwenden; Paarung bei der Montage erhalten. Kein Verbinden des Schirms mit PV-Rahmen oder PE. Schirm am Sensor isolieren; eine optionale einseitige Verbindung zu PanelLog-GND erst nach EMV-/Massekonzeptprüfung. Die drei GND-Adern sind Rückleiter und werden an beiden Boards verbunden. Zugentlastung und abgedichtete Kabeleinführung vorsehen. Es ist ein fest verdrahteter, nicht galvanisch isolierter Anschluss; nur spannungsfrei montieren.

## Versorgung

Die Versorgung erfolgt aus der vorhandenen PanelLog-3V3-Schiene über R36=0 Ω und J8.1. Maßgeblich ist PanelLog-Commit `26c2335`; PanelLog wird für diesen POA-Entwurf nicht geändert.

Am POA-Kabeleingang C6=1 µF. R12=10 Ω plus C1=100 nF/C2=1 µF filtern die analoge Versorgung von ADC und Temperaturteilern. Der optionale P82B715 bleibt am ungefilterten Kabel-VDD und erhält C5=100 nF (DNP zusammen mit U2). Kein zusätzlicher Spannungsregler nötig. Die lokale Versorgung wird über AIN3 mitgemessen. Ein Betrieb bei ausgefallener PanelLog-3V3-Versorgung ist nicht vorgesehen; insbesondere ist keine unabhängige Nachtversorgung enthalten.

## DIRECT — Standardbestückung

| Ort | Bestückt | Unbestückt |
|---|---|---|
| POA | R6/R7=0 Ω; D1; ADC/Analogteil | U2, R8–R11, C5 |
| PanelLog | R30/R31=2,2 kΩ; R32/R33=0 Ω; R36=0 Ω; D3 | U4, R34/R35, C26 |

Die beiden 2,2-kΩ-Pull-ups R30/R31 liegen nur bei PanelLog an dessen bestehender +3V3-Schiene. MCU-Pins ausschließlich Open-Drain/hochohmig betreiben; interne Pull-ups aus. Kein aktiv getriebener High-Pegel. Die getrennten Netznamen vor und hinter den 0-Ω-Widerständen sind absichtlich erhalten.

Startwert 25 kHz; Gesamtlast je Leitung einschließlich Kabel, Schutz und Platinen ≤400 pF anstreben. Bei 2,2 kΩ/400 pF beträgt die rechnerische 30–70-%-Anstiegszeit 0,746 µs. Die zulässige Anstiegszeit wird durch niedrigeren Takt nicht automatisch aufgehoben. Am realen Kabel Anstiegszeit ≤1 µs, VOL und Störfestigkeit prüfen.

D1/D3 = TPD2E2U06DRLR (C1972959), SOT-553: Pin 3 SDA, Pin 4 GND, Pin 5 SCL; Pin 1/2 NC. Schutz nahe Kabeleinführung mit kurzem Massepfad. ESD-Bauteile ersetzen keine Messung der Restspannung und keine vollständige Prüfung von Störungen auf der Versorgung.

## BUFFERED — vorbereitete DNP-Option

An **beiden** Enden die direkten Bypässe entfernen: POA R6/R7 und PanelLog R32/R33. POA U2/C5 und PanelLog U4/C26 bestücken. Lokale S-seitige Pull-ups: POA R10/R11=2,2 kΩ und PanelLog R30/R31=2,2 kΩ. L-seitige Pull-ups: POA R8/R9=1 kΩ; PanelLog R34/R35=1 kΩ bestücken. R30/R31 bleiben bestückt. Zusammen etwa 500 Ω / 6,6 mA pro Low-Leitung bei 3,3 V. Das ist ein Ausgangspunkt für Messungen, keine qualifizierte Bestückungsfreigabe.

P82B715: 2=Lx, 3=Sx, 4=GND, 6=Sy, 7=Ly, 8=VCC, 1/5 NC. Betriebsspannung an beiden Enden mindestens 3,0 V und Temperaturbereich bis 85 °C beachten. Spannungsabfall, VOL, Parallel-Pull-ups und Versorgungsausfallverhalten prüfen. Die Defaultbestückung ist ausdrücklich DIRECT.

## Temperaturauswertung und Grenzen

NTC1 liegt unter/an der Referenzzelle und wird über R1=47 kΩ an POA_VDD_ANALOG gespeist. Bei 25 °C / 10 kΩ: ungefähr 0,579 V, 57,9 µA, 33,5 µW im NTC. Keine GPIO-Erregung und kein zusätzlicher Schalter erforderlich.

Bei nominell gleichen R2/R3 gilt: VDD_local = 2 × U_AIN3; R_NTC = 47 kΩ × U_AIN2 / (VDD_local − U_AIN2). Für AIN2 und AIN3 die gleiche PGA-Spanne verwenden, z.B. ±4,096 V, und nach MUX-/PGA-Wechsel eine vollständige frische Wandlung abwarten. R/T-Kennlinie des exakten TDK-Teils statt einer über den ganzen Bereich vereinfachten Beta-Kurve verwenden.

Die Versorgungskorrektur ist keine vollständige Fehlerkompensation: ADC-Eingangsimpedanz ist endlich und PGA-/kanalabhängig; der 47k/47k-Teiler hat 23,5 kΩ Quellimpedanz. ADC-Loading, Widerstandstoleranz, NTC-Toleranz und thermische Kopplung müssen im Fehlerbudget berücksichtigt bzw. am montierten Sensor kalibriert werden. C4/C7 filtern die Messknoten; beim Kaltstart mindestens 100 ms Einschwingzeit vorsehen und anschließend gültige ADC-Wandlungen abwarten. Das ist ein Integrationshinweis, keine Firmwareimplementierung.

## Quellen

- TI ADS1115: https://www.ti.com/lit/ds/symlink/ads1115.pdf
- TI P82B715: https://www.ti.com/lit/ds/symlink/p82b715.pdf
- TI TPD2E2U06: https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf
- ESP32-C6-WROOM-1: https://www.espressif.com/sites/default/files/documentation/esp32-c6-wroom-1_wroom-1u_datasheet_en.pdf
