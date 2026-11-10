#!/usr/bin/env python3
"""Check the electrical interface in a native KiCad XML netlist, using stdlib only."""
import argparse, csv, json
from pathlib import Path
import xml.etree.ElementTree as ET

parser=argparse.ArgumentParser()
parser.add_argument('netlist',type=Path)
parser.add_argument('--host',action='store_true')
parser.add_argument('--bom',type=Path)
args=parser.parse_args()
root=ET.parse(args.netlist).getroot()
components={c.get('ref'):c for c in root.findall('./components/comp')}
nets={}
for net in root.findall('./nets/net'):
    name=net.get('name').lstrip('/')
    for n in net.findall('node'):
        nets[(n.get('ref'),n.get('pin'))]=name

def expect(ref,pin,name):
    actual=nets.get((ref,str(pin)))
    if actual!=name:
        raise SystemExit(f'{ref}.{pin}: expected {name}, got {actual}')

def populated(ref,yes):
    c=components[ref]
    dnp=any(p.get('name')=='dnp' for p in c.findall('property'))
    if dnp==yes:raise SystemExit(f'{ref}: incorrect DNP state')

if args.host:
    for pin,name in {1:'POA_VDD_CABLE',2:'GND',3:'POA_SDA_CABLE',4:'GND',5:'POA_SCL_CABLE',6:'GND'}.items():expect('J8',pin,name)
    for pin,name in {1:'+3V3',2:'GND',3:'+3V3',5:'+3V3',6:'POA_VDD_CABLE'}.items():expect('U5',pin,name)
    expect('C26',1,'POA_VDD_CABLE');expect('U4',8,'POA_VDD_CABLE')
    expect('U3',20,'POA_SDA_MCU');expect('U3',21,'POA_SCL_MCU')
    for ref,name in [('R34','POA_SDA_CABLE'),('R35','POA_SCL_CABLE')]:
        expect(ref,1,'POA_VDD_CABLE');expect(ref,2,name);populated(ref,True)
        if components[ref].findtext('value')!='2.2k':raise SystemExit(f'{ref}: expected 2.2k')
    for ref in ['R30','R31','U4','C26']:populated(ref,False)
    for ref in ['R32','R33','U5','C27','C28']:populated(ref,True)
    if 'R36' in components:raise SystemExit('Unsafe supply bypass R36 still present')
    expect('D3',3,'POA_SDA_CABLE');expect('D3',4,'GND');expect('D3',5,'POA_SCL_CABLE')
else:
    for pin,name in {1:'POA_VDD_CABLE',2:'GND',3:'POA_SDA_CABLE',4:'GND',5:'POA_SCL_CABLE',6:'GND'}.items():expect('J1',pin,name)
    for pin,name in {1:'GND',3:'GND',4:'POA_ADC_P',5:'POA_ADC_N',6:'POA_NTC_ADC',7:'POA_VDD_HALF',8:'POA_VDD_ANALOG',9:'POA_SDA_LOCAL',10:'POA_SCL_LOCAL'}.items():expect('U1',pin,name)
    expect('D1',3,'POA_SDA_CABLE');expect('D1',4,'GND');expect('D1',5,'POA_SCL_CABLE')
    expect('R12',1,'POA_VDD_CABLE');expect('R12',2,'POA_VDD_ANALOG')
    expect('CELL1',1,'CELL_P');expect('CELL1',2,'GND')
    expect('RSH1',1,'CELL_P');expect('RSH1',2,'GND')
    for ref,n in [('R4','POA_ADC_P'),('R5','POA_ADC_N')]:expect(ref,2,n)
    expect('R1',1,'POA_VDD_ANALOG');expect('R1',2,'POA_NTC_ADC')
    expect('NTC1',1,'POA_NTC_ADC');expect('NTC1',2,'GND')
    for ref in ['U2','R8','R9','R10','R11','C5']:populated(ref,False)
    for ref in ['R6','R7','U1','D1','NTC1','RSH1']:populated(ref,True)
    if '0805' not in components['RSH1'].findtext('footprint'):raise SystemExit('Shunt package must be 0805')
    if any(r in components for r in ['BT1','Y1','NTC2']):raise SystemExit('Legacy battery/radio/remote temperature remains')
if args.bom:
    with args.bom.open() as f:rows=list(csv.DictReader(f))
    by_ref={r['Ref']:r for r in rows}
    if set(by_ref)!=set(components):raise SystemExit('BOM designators differ from schematic')
    for ref,c in components.items():
        fields={f.get('name'):f.text or '' for f in c.findall('./fields/field')}
        if by_ref[ref]['LCSC']!=fields.get('LCSC',''):raise SystemExit(f'{ref}: BOM LCSC mismatch')
print(json.dumps({'kind':'PanelLog host' if args.host else 'POA','components':len(components),'checked':'connector, ADC, supply, ESD, default assembly and optional BOM','result':'PASS'},indent=2))
