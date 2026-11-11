#!/usr/bin/env python3
"""Check schematic/PCB agreement and reject DRC issues, including open connections."""
import argparse
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def parse_sexpr(path):
    stack, root = [], None
    for match in re.finditer(r'\(|\)|"(?:\\.|[^"\\])*"|[^\s()]+', path.read_text()):
        token = match.group()
        if token == '(':
            node = []
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
        elif token == ')':
            stack.pop()
        else:
            stack[-1].append(json.loads(token) if token.startswith('"') else token)
    assert not stack and root[0] == 'kicad_pcb', 'Invalid PCB file'
    return root


def children(node, name):
    return [x for x in node if isinstance(x, list) and x and x[0] == name]


def child(node, name):
    return next(iter(children(node, name)), [])


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('netlist', type=Path)
parser.add_argument('drc', type=Path)
parser.add_argument('--pcb', type=Path, default=Path('hardware/poa-sensor.kicad_pcb'))
args = parser.parse_args()
board = parse_sexpr(args.pcb)
netlist = ET.parse(args.netlist).getroot()
components = {c.get('ref'): c for c in netlist.findall('./components/comp')}
footprints = {}
for fp in children(board, 'footprint'):
    fields = {x[1]: x[2] for x in children(fp, 'property')}
    ref = fields['Reference']
    assert ref not in footprints, f'Duplicate footprint {ref}'
    footprints[ref] = (fp, fields)
assert set(footprints) == set(components) | {'H1', 'H2', 'H3', 'H4'}, 'PCB designators differ'

expected_pins = {}
for net in netlist.findall('./nets/net'):
    for node in net.findall('node'):
        expected_pins[(node.get('ref'), node.get('pin'))] = net.get('name')
actual_pins = {}
models = 0
for ref, comp in components.items():
    fp, fields = footprints[ref]
    assert fp[1] == comp.findtext('footprint'), f'{ref}: footprint differs'
    assert fields['Value'] == comp.findtext('value'), f'{ref}: value differs'
    for field in comp.findall('./fields/field'):
        if field.get('name') == 'Footprint':
            # Current KiCad PCB files carry this in the footprint identifier
            # (fp[1]) rather than duplicating it as a custom property.
            continue
        assert fields.get(field.get('name')) == (field.text or ''), f"{ref}: field {field.get('name')} differs"
    assert child(fp, 'path')[1].split('/')[-1] == comp.findtext('tstamps').strip(), f'{ref}: schematic link differs'
    dnp = any(p.get('name') == 'dnp' for p in comp.findall('property'))
    assert ('dnp' in child(fp, 'attr')) == dnp, f'{ref}: DNP state differs'
    for pad in children(fp, 'pad'):
        net = child(pad, 'net')
        if net:
            actual_pins[(ref, pad[1])] = net[-1]
    for model in children(fp, 'model'):
        path = Path(model[1].replace('${KIPRJMOD}', str(args.pcb.parent)))
        assert path.is_file(), f'{ref}: model missing: {path}'
        models += 1
assert actual_pins == expected_pins, 'PCB pad nets differ from schematic'

for ref, pos in {'H1': (124.5, 102.645), 'H2': (146.065, 124.5),
                 'H3': (124.5, 146.355), 'H4': (102.935, 124.5)}.items():
    fp = footprints[ref][0]
    at = child(fp, 'at')
    assert math.dist(tuple(map(float, at[1:3])), pos) < 0.001, f'{ref}: mount position differs'
    pad = child(fp, 'pad')
    assert pad[2] == 'np_thru_hole' and abs(float(child(pad, 'drill')[1]) - 2.6) < .001, f'{ref}: mount drill differs'
cell = child(footprints['CELL1'][0], 'at')
ntc = child(footprints['NTC1'][0], 'at')
cell_offset = math.dist(tuple(map(float, cell[1:3])), tuple(map(float, ntc[1:3])))
assert cell_offset <= 0.05, f'NTC is offset {cell_offset:.3f} mm from cell centre'

drc = json.loads(args.drc.read_text())
open_connections = drc['unconnected_items']
issues = drc['violations'] + drc['schematic_parity'] + open_connections
assert not issues, json.dumps(issues, indent=2)
print(json.dumps({'result': 'PASS', 'components': len(components), 'pads': len(actual_pins),
                  'mounts': 4, 'resolved_models': models,
                  'open_connections': len(open_connections)}, indent=2))
