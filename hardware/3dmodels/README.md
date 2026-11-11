# 3D-Modelle

`KXOB25-14X1F.step` ist ein vereinfachtes Hüllmodell der Referenzzelle, 23 × 8 × 1,8 mm. Der Montageabstand von 0,7 mm wird im Footprint und PCB als Z-Offset angewendet.

`TDK_NTCG103JF103FT1.step` basiert auf dem [TDK-Herstellermodell NTCG1005](https://product.tdk.com/system/files/dam/doc/product/protection/voltage/varistor_ctvs/3doutline_step/tdk_ntcg1005.step), das auf der [Produktseite](https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG103JF103FT1) angeboten wird. Für KiCad wurde das Modell um die Z-Achse um +90° gedreht und anschließend um (+0,5; −0,25; 0) mm verschoben. Die Geometrie ist unverändert: drei Volumenkörper, Gesamthülle 1,0 × 0,5 × 0,5 mm. Die Längsachse liegt jetzt auf X, die Unterseite bei Z=0 und der XY-Mittelpunkt im Footprint-Ursprung. Das Modell ist eine Herstellerreferenz, kein Bestandteil der KiCad-Bibliothekslizenz.

Die Modelle unter `standard/` stammen aus den KiCad-Bibliotheken; deren Lizenz und Quellenhinweise stehen in [standard/LICENSE.md](standard/LICENSE.md). Der 0402-Footprint wird in diesem Projekt ausschließlich für NTC1 verwendet und verweist deshalb auf das TDK-Modell.
