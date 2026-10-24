"""Group equivalent listed panels without discarding their individual CAD identities."""
import hashlib
import json
import re


def stable(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def geometry_key(panel, part):
    if panel['rectangular']:
        return 'rectangular'
    if not part or not part.get('v') or not part.get('t'):
        return 'unverified:' + panel['id']
    # Translation is irrelevant; rotations/reflections remain distinct for special pieces.
    vertices = part['v']
    origin = [min(v[i] for v in vertices) for i in range(3)]
    points = [tuple(round((v[i] - origin[i]) * 100000) for i in range(3)) for v in vertices]
    triangles = sorted(tuple(sorted(points[i] for i in triangle)) for triangle in part['t'])
    return hashlib.sha256(stable(triangles).encode()).hexdigest()


def technical_key(panel, module):
    identifier = panel['id']
    def clean(value):
        if isinstance(value, dict):
            return {k: clean(v) for k, v in value.items() if k not in ('id', 'item', 'partId', 'partIds', 'sourceObject', 'sources', 'sourceSHA256', 'module')}
        if isinstance(value, list):
            return [clean(v) for v in value]
        if isinstance(value, str):
            return value.replace(identifier, '{piece}')
        return value
    operations = [clean(r) for r in module.get('drilling', []) if identifier in r.get('partIds', [])]
    drawings = [clean(r) for r in module.get('drawings', []) if r.get('partId') == identifier]
    return [sorted(stable(r) for r in operations), sorted(stable(r) for r in drawings)]


def group_panels(module, parts):
    groups = {}
    for p in module['panels']:
        # Do not use names or IDs as equivalence criteria. Do not round nominal dimensions.
        key = stable([p['dimensions'], p['thickness'], p['cadMaterial'], p.get('specifiedMaterial'),
                      p.get('finishComplete'), p.get('remainingFinish'),
                      {k: p.get(k) for k in ('grain', 'edges', 'machining')},
                      geometry_key(p, parts.get(p['id'])), technical_key(p, module)])
        if key not in groups:
            groups[key] = {**p, 'quantity': 0, 'ids': [], 'members': []}
        g = groups[key]
        g['quantity'] += p.get('quantity', 1)
        g['ids'].append(p['id'])
        g['members'].append({'id': p['id'], 'name': p['name']})
    for g in groups.values():
        names = list(dict.fromkeys(p['name'] for p in g['members']))
        joined = ' / '.join(names)
        roles = list(dict.fromkeys(re.split(r'\s+[—–-]\s+', n, maxsplit=1)[0] for n in names))
        if len(roles) == 1 and all('porta' in n.lower() for n in names) and 'porta' not in roles[0].lower():
            roles[0] += ' · portas'
        g['name'] = joined if len(joined) <= 85 or len(names) == 1 else roles[0] if len(roles) == 1 else 'Peças equivalentes'
    return list(groups.values())
