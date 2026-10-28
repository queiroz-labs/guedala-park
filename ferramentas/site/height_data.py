"""Pé-direito do site usa a mesma fonte e precedência das pranchas."""
from collections import Counter
from html import escape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'ferramentas/pranchas'))
from medidas import carregar, resolver


def heights(root=ROOT):
    config = json.loads((root / '06_Entregas/Planta_cotada/Cotas.json').read_text(encoding='utf8'))
    rows = carregar(root)
    result = {}
    for room, code in config['pranchas']['ceiling'].items():
        value = resolver(rows, code)
        if value.mm is None or value.mm <= 0:
            raise ValueError('Pé-direito inválido: ' + code)
        result[room] = dict(mm=value.mm, origem=value.origem, codigo=code)
    return result


def summary(values):
    """Uma frase curta: valor comum aos cômodos e exceções por ambiente."""
    labels = {'quarto': 'no quarto', 'cozinha': 'na cozinha', 'lavanderia': 'na lavanderia',
              'escritorio': 'no escritório', 'banho': 'no banheiro', 'sala': 'na sala',
              'circulacao': 'na circulação'}
    metres = lambda mm: f"{mm / 1000:.2f}".replace('.', ',') + ' m'
    common = Counter(v['mm'] for v in values.values()).most_common(1)[0][0]
    others = [f"{metres(v['mm'])} {labels[room]}" for room, v in values.items() if v['mm'] != common]
    text = 'Pé-direito: ' + metres(common) + (' nos cômodos e ' + ' e '.join(others) if others else ' em todos os ambientes')
    measured = all(v['origem'] == 'medido' for v in values.values())
    return text + (', medido no imóvel.' if measured else ', medida a confirmar no imóvel.') + ' Valores para estudo, não fabricação.'


def build():
    values = heights()
    path = ROOT / 'ferramentas/site/src/data.js'
    text = path.read_text(encoding='utf8')
    match = re.search(r'const PROJECT\s*=\s*(\{.*?\});', text, re.S)
    project = json.loads(match[1])
    project.pop('officeCeilingStudy', None)
    project['ceiling'] = max(v['mm'] for v in values.values()) / 10
    project['ceilingByRoom'] = {room: v['mm'] / 10 for room, v in values.items()}
    project['heightStudy'] = summary(values)
    content = text[:match.start(1)] + json.dumps(project, ensure_ascii=False, indent=2) + text[match.end(1):]
    if content != text:
        path.write_text(content, encoding='utf8')
    return escape(summary(values))
