"""Projeção de leitura da seção 2 do cronograma; nunca reordena a fonte."""
import hashlib
import json
import posixpath
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = '05_Orcamento_e_cronograma/Cronograma_obra_e_compras.md'
PLAN = '01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md'
REVIEW = '05_Orcamento_e_cronograma/README.md'
# Somente destinos documentais, sem datas, duração ou dependências paralelas.
AREAS = [
    ('Impermeabilização', 'Banheiro', '03_Ambientes/Banheiro/README.md'),
    ('Revestimentos', 'Acabamentos', '03_Ambientes/Acabamentos/README.md'),
    ('Pintura', 'Obra e pintura', '05_Orcamento_e_cronograma/Orcamento/Obra_e_pintura/Analise_obra.md'),
    ('Piso', 'Acabamentos', '03_Ambientes/Acabamentos/README.md'),
    ('Box,', 'Box e pedras', '05_Orcamento_e_cronograma/Orcamento/Pedras_e_box/Analise_pedras_box.md'),
    ('Box,', 'Equipamentos', '03_Ambientes/Equipamentos/README.md'),
    ('Box,', 'Iluminação', '03_Ambientes/Iluminacao/README.md'),
    ('Marcenaria', 'Móveis', '04_Moveis/README.md'),
    ('Marcenaria', 'Box e pedras', '05_Orcamento_e_cronograma/Orcamento/Pedras_e_box/Analise_pedras_box.md'),
    ('Retoques', 'Obra e pintura', '05_Orcamento_e_cronograma/Orcamento/Obra_e_pintura/Analise_obra.md'),
]
LINK = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def display(text):
    return re.sub(r'laminado', 'vinílico Olmo', LINK.sub(r'\1', text).replace('**', ''), flags=re.I)


def parse(text):
    section = re.search(r'^## 2\. [^\n]+\n(.*?)(?=^## |\Z)', text, re.M | re.S)
    if not section:
        raise ValueError('Seção 2 do cronograma ausente')
    lines = [s.strip() for s in section[1].splitlines() if s.strip().startswith('|')]
    if not lines or lines[0] != '| Semana | Serviço | Depende de | Observação |':
        raise ValueError('Cabeçalho da sequência mudou; conferir o parser')
    result = []
    for line in lines[2:]:
        cells = [s.strip() for s in line.strip('|').split('|')]
        if len(cells) != 4:
            raise ValueError('Linha de cronograma sem quatro colunas')
        week, service, dependency, note = cells
        match = re.fullmatch(r'(\d+)(?:[–-](\d+))?', week)
        if not match or not service:
            raise ValueError('Semana ou serviço não reconhecido: ' + line)
        start, end = int(match[1]), int(match[2] or match[1])
        if not 0 <= start <= end <= 104:
            raise ValueError('Faixa semanal inválida: ' + week)
        docs = []
        for label, target in LINK.findall(' '.join(cells)):
            target = posixpath.normpath(posixpath.join(posixpath.dirname(SOURCE), target))
            docs.append(dict(titulo=label, caminho=target))
        docs.extend(dict(titulo=label, caminho=path) for token, label, path in AREAS if service.startswith(token))
        if not docs:
            docs.append(dict(titulo='Cronograma da obra', caminho=SOURCE))
        result.append(dict(id='etapa-' + hashlib.sha256('\x1f'.join(cells).encode()).hexdigest()[:16],
                           semana=week, inicio=start, fim=end, servico=display(service),
                           depende_de=display(dependency), observacao=display(note), documentos=docs))
    if not result or len({r['id'] for r in result}) != len(result):
        raise ValueError('Sequência vazia ou etapas idênticas')
    return result


def document_paths():
    """Lista explícita para a biblioteca web, sem varrer diretórios."""
    return list(dict.fromkeys([SOURCE, PLAN, REVIEW] + [p for _, _, p in AREAS] + [
        '07_Imovel/Roteiro_dia_das_chaves_R01.md', '03_Ambientes/Planta_pontos/README.md']))


def data(root=ROOT):
    text = (root / SOURCE).read_text(encoding='utf-8')
    stages = parse(text)
    for path in document_paths():
        if not (root / path).is_file():
            raise FileNotFoundError(path)
    for stage in stages:
        for doc in stage['documentos']:
            if doc['caminho'] not in document_paths():
                raise ValueError('Novo destino documental requer seleção explícita: ' + doc['caminho'])
    return dict(fonte=SOURCE, plano=PLAN, revisao=REVIEW,
                sha256=hashlib.sha256(text.encode()).hexdigest(), etapas=stages)


def build(root=ROOT):
    payload = data(root)
    output = '// Gerado de Cronograma_obra_e_compras.md, seção 2.\n' + 'globalThis.GUEDALA_WORK_PLAN=' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + ';\n'
    path = root / 'ferramentas/site/src/work-data.js'
    if not path.exists() or path.read_text(encoding='utf-8') != output:
        path.write_text(output, encoding='utf-8')
    return payload


if __name__ == '__main__':
    build()
