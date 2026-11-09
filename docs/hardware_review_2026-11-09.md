# Hardware review — 2026-11-09

Basis: PanelLog main `0b9faa9a3c6ec9b03f33cb80663329b57e3553f1`, POA main `69b763a1dfef06ae69d4aa692752678bc46e127b`.

## Result and limits

Engineering revision, **not a manufacturing release**. PanelLog copper was corrected and checked with native KiCad 10.0.8 during this session: final local DRC before the connector-cache cleanup and model-link cleanup reported **0 violations, 0 unconnected items, 0 schematic parity issues**. The wired POA schematic reported **0 ERC violations**. These are observed intermediate results, not a substitute for the final CI checks. Temporary native reports/runtime were lost after the runtime transition. A subsequent tooling installation was rejected because it used an unverified/trusted PPA; this route was stopped. No recreated reports are presented as native evidence.

The final connector-cache correction preserves pin geometry and removes the stale `lib_name` alias that selected the old modified connector despite an apparently correct `lib_id`. The last exact source files need the added CI run; see `hardware/review_2026-11-09/source_hashes.json`.

## Corrections

- PanelLog P82B715 SOIC-8 and TPD2E2U06 SOT-553 replaced provisional pad geometry with official KiCad 10 library geometry. SOIC adjacent copper spacing was only 0.07 mm in the input. Local optional-buffer routes were reworked to accommodate the real lands.
- R30–R36 use official 0603 footprints; direct mode and buffered mode are mutually exclusive. U4 is DNP, R32/R33 fitted, R34/R35 DNP.
- All new PCB symbol paths, values, MPN fields and no-connect nets synchronized. No blanket severity suppression was added.
- TI DRL-5 official lands use 0.5 mm pitch / 0.35 mm pad width. Only **intra-D3 pad-to-pad spacing** has a documented 0.15 mm exception in `panellog.kicad_dru`; all unrelated board spacing remains unchanged.
- The ESP32 antenna-side silkscreen was trimmed at the board edge; copper, antenna keepout and module placement retained.
- POA RSH1 was erroneously assigned 0603 although C865286 is 0805: fixed. ADS1115 DGS10 mapped to the actual KiCad `MSOP-10_3x3mm_P0.5mm` footprint, rather than a nonexistent library identifier. Cached standard R/C symbols refreshed; POA-specific symbols exported to the project library. No-connect pins and off-grid endpoints corrected.
- Incorrect absolute model links to the old BVB 0.7mΩ shunt and a CDRH127 47µH body removed. No guessed 3D bodies substituted. Exact HoVB and Sumida LD models remain unavailable; holes/pogo/solder pads require no purchased component model.

## Electrical calculations and datasheet cross-check

### POA local current measurement

KXOB25-14X1F nominal Isc=58.6mA at 1000W/m² and 25°C. With RSH1=1Ω: 58.6mV and 3.434mW. At 1500W/m² assuming linearity: 87.9mV and 7.726mW. ADS1115 ±0.256V range has 7.8125µV/LSB, corresponding to 7.8125µA or **0.1333W/m²/LSB**. This is resolution, not accuracy. At nominal sensitivity full scale is ~4369W/m². Cell short-circuit linearity, window transmission, angle and thermal contact still require reference calibration.

The 100Ω+100Ω/100nF differential input filter has fc≈7.96kHz; it suppresses RF/switching pickup but does not provide mains rejection. ADS1115 has a switched-capacitor input; its typical 710kΩ differential impedance at this gain creates ~0.028% attenuation with the 200Ω series network. Calibrate the assembled chain. The typical impedance is not a guaranteed precision resistor.

47kΩ NTC excitation at 3.3V/10kΩ gives ~0.579V, 57.9µA and 33.5µW NTC dissipation. The 47k/47k rail divider gives 1.65V and 23.5kΩ Thevenin impedance. Include ADC loading and NTC R/T tolerance in the temperature budget; the supply divider does not cancel the ADC's channel-dependent input loading. Use exact TDK R/T data in release firmware rather than relying on a single beta over the full outdoor range.

### Cable and P82B715

GPIO21=module pad27 SDA, GPIO22=pad28 SCL. Separate software bus, no electrical sharing with INA237 GPIO6/7. Direct mode total 2.2k pullups at 3.3V draw 1.5mA per low line; 400pF yields tr(30–70%)≈746ns. Maximum capacitance for a 1µs rise is ~536pF by the RC model, but retain the Standard-Mode 400pF design limit including cable, ESD and pads. 25kHz does not waive rise-time limits. Use SDA/GND, SCL/GND, 3V3/GND twisted pairs and test actual 3m cable.

P82B715 supply minimum is 3.0V, maximum operating temperature 85°C. If fitted at both ends: remove all direct bypasses; populate local S-side pullups and line pullups; qualify VOL, sink current, remote supply drop and hot enclosure temperature. The two 1k line pullups appear in parallel (500Ω), about 6.6mA per low line at 3.3V; account for current at both ends. Add local buffer bypass capacitors before releasing the optional buffered assembly. Buffered mode is reserved/DNP and not qualified by the direct-mode checks.

### PanelLog existing power and measurement

INA237 1mΩ shunt: 15A → 15mV / 225mW; 20A → 20mV / 400mW. ±40.96mV range has margin, but does not increase the PCB current rating. At 50ppm/K and ΔT=50K the shunt contribution is 0.25%. Retain four-terminal routing and calibrate offset/gain. Sensor ground must not use the load-current return as its Kelvin sense conductor.

LM5163: FB=1.2V, 174k/100k gives 3.288V nominal; RON=27.4k gives ~300kHz in CCM. At 60V and L=68µH, ripple is ~0.152App; 0.5A load gives ~0.576A peak ideal, subject to actual current limit/transients. 3×4.7µF input MLCC nominal does not establish effective capacitance at 60V: require the exact bias curve. Output 2×22µF must likewise be checked with bias/tolerance and Zigbee burst load.

R8=47k gate feed at 60V: upper-bound dissipation ~76.6mW when pulled low; approximately 1.06mA remains if the bias node is 10V. Verify hot derating of the selected 1206 resistor, actual zener knee/leakage, turn-on time and fail-ON under supply and Q2 fault conditions. A 100V MOSFET/buck and 85V INA237 require a measured PV cold-Voc/transient envelope; the unselected DNP TVS is not protection.

## EMC / signal integrity review

The new digital routes remain in the controller/POA corner, well away from the INA237/shunt Kelvin network and PV switching path. Local layer transitions avoid the pre-existing PGOOD route and maintain clearance. No new power-path neck or new Kelvin branch is introduced. Continuous ground reference must be confirmed on the final filled layers; DRC proves connectivity/spacing, not return-current quality or radiated immunity.

The D3 ESD path terminates near J8 with short ground return; the TI part's 12.4V catalogue clamp figure is not a guaranteed MCU pin voltage. Scope/ESD testing must establish residual voltage and whether additional series impedance/clamping is required. No certification claim follows from fitting a TVS.

Keep cable shield insulated at remote POA. Any one-end connection is to defined PanelLog local ground only after system grounding review; do not introduce a PV−/module frame/PE loop. Do not put shield current through Kelvin traces. Measure samples away from radio bursts where possible and inspect inverter switching noise on actual analog channels.

## Unresolved release blockers

1. R36 is still a **0Ω unprotected 3.3V cable supply**. A cable short can reset PanelLog. Add a qualified low-quiescent current limiter/load switch or a separately justified fuse; TPS2553DBVR (C55266) is a candidate, not yet integrated. Do not call the present cable interface fault tolerant.
2. The wired POA has no matching routed PCB. The historical `poa-sensor.kicad_pcb` is the RF/battery board and must not be fabricated for this wired schematic. A full mechanical/optical sensor PCB review remains impossible until that board exists.
3. R18 C1721340 is zero stock; two checked KOA 0603 0.05%/10ppm alternatives also zero stock. Preserve the precision specification; do not substitute a 25ppm resistor silently. C45783 stock is low; the checked newer Samsung candidate C3836327 is zero stock.
4. Exact HoVB/LD 3D bodies missing. Package-only models do not prove enclosure collision freedom or heat clearance.
5. Hot-enclosure buck/shunt/gate thermal behavior, DC bias, surge envelope and 3m EMI need bench verification. Final native CI status must be checked after the source push.

## BOM

`bom/reviewed_selection_2026-11-09.csv` covers each actual schematic component with LCSC number, live stock, MOQ and full price ladder where verified. The raw retrieval is stored separately. PCB features are explicitly non-purchased; the reference cell has no verified LCSC listing. Unselected DNP snubber/TVS positions remain explicitly unresolved: a random cheap part is not a valid tuned design. Costs are USD excluding tax/shipping/PCBA. These are verified economical existing candidates, not a proof of the cheapest part across LCSC's entire catalogue.

## Sources

- https://www.ti.com/lit/ds/symlink/ads1115.pdf
- https://www.ti.com/lit/ds/symlink/p82b715.pdf
- https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf
- https://www.ti.com/lit/ds/symlink/lm5163.pdf
- https://www.ti.com/lit/ds/symlink/ina237.pdf
- https://product.tdk.com/en/search/sensor/ntc/chip-ntc-thermistor/info?part_no=NTCG063JF103FTBA
- Exact LCSC product URLs and retrieval data in `bom/lcsc_audit_2026-11-09.json`.
