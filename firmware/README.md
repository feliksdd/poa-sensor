# Firmware

Der kabelgebundene POA-Sensor besitzt keinen Mikrocontroller und benötigt keine eigene Firmware. PanelLog liest den ADS1115 auf einem separaten I²C-Bus aus. Aktuelle Host-Pins: GPIO22 SDA, GPIO23 SCL (C6-WROOM).

Diese Schaltplanrevision entwickelt oder ändert keine Firmware. Der vorhandene PanelLog-Prototyp muss vor Betrieb auf diese Pins, Open-Drain ohne interne Pull-ups und die aktuelle Messkanalbelegung abgestimmt werden. Auslegung und Einschwinghinweise stehen in `../docs/architecture.md`.
