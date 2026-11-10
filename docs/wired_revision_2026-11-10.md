# Schaltplanrevision 0.3 — 2026-11-10

## Umsetzung

Ein POA pro PanelLog, maximal 3 m, drei verdrillte Aderpaare, direkte Lötanschlüsse. Der aktive Hauptschaltplan enthält ausschließlich Referenzzelle mit Shunt, Zelltemperaturmessung, ADS1115 und Versorgung-/Schnittstellenbeschaltung. Keine Batterie, kein MCU, kein Funk, kein PV-Modul-Temperaturkanal.

Der bestehende Wired-Entwurf ist zum Hauptprojekt geworden. Die alte Funkversion und ihre Platine sind als `poa-sensor-wireless-legacy.*` erhalten. Eine aktive PCB-Datei mit irreführend passendem Hauptnamen gibt es nicht mehr. Der alte KiCad-9-CI-Job, der die Funkversion normalisierte, ist entfernt; der vorhandene KiCad-10-Prüfjob prüft jetzt den neuen Hauptschaltplan. Historische Normalisierungs-/Layoutskripte zielen ausdrücklich auf Legacy-Dateien.

I²C-Standardbestückung ist DIRECT: P82B715 samt lokalen und zusätzlichen Kabel-Pull-ups unbestückt. Abblockkondensator C5 für die spätere Buffer-Option ergänzt. Kabelversorgung am POA-Eingang gepuffert und über R12=10 Ω zur Analogversorgung gefiltert. C7 filtert die lokale VDD/2-Messung. Kabelbelegung und GPIO22/23 stimmen mit dem aktuellen C6-WROOM-PanelLog-Schaltplan überein. ADC AIN0/AIN1 messen den Shunt, AIN2 den NTC, AIN3 die lokale Versorgung / 2.

PanelLog bleibt auf Commit `26c2335` unverändert. Versorgung über vorhandenes R36/J8; R30/R31 sind die bestückten 2,2-kΩ-Pull-ups. R34/R35, U4 und C26 bleiben im Direktbetrieb unbestückt.

## Nachgewiesene Prüfungen

- Exakter POA-Hauptschaltplan mit lokalem KiCad **9.0.2** geladen, SVG/PDF exportiert und visuell geprüft; natives ERC: **0 Meldungen** bei `--severity-all --exit-code-violations`.
- Native XML-Netzliste: ADC-/Kabel-/ESD-Pins, Versorgungsdomänen, DNP-Standardbestückung und Stücklistenreferenzen/LCSC-Felder geprüft.
- Die J8-/GPIO-Zuordnung und Standardbestückung sind gegen die unveränderte PanelLog-Netzliste zu Commit `26c2335` geprüft; die temporäre KiCad-9-Kopie normalisiert ausschließlich die Dateisyntax.
- `hardware/review_2026-11-10/source_hashes.json` benennt die lokal geprüften POA-Quellen. Der KiCad-10-GitHub-Workflow prüft den gepushten Hauptschaltplan nochmals; sein Ergebnis ist separat zu betrachten.

## Verbleibende Arbeiten

**Keine Fertigungsfreigabe:** Für den Wired-POA fehlt die zugehörige Platine. Vor Bestellung sind Layout, Zonenfüllung, DRC und Schaltplan-Parität erforderlich für den POA.

Danach am Aufbau prüfen: reale 3-m-Kabellast und Flanken, VOL/EMV bei Wechselrichterbetrieb, ESD-Restspannungen einschließlich Versorgung, Spannungsreserve der Buffer-Option, Zell-/NTC-Kopplung, optische Abdichtung und Kalibrierung. Keine Genauigkeits- oder Resetfestigkeitszusage allein aus dem ERC. Die Grundlagen und Bestückungsvarianten stehen in [architecture.md](architecture.md).
