"""Entrada de consulta: fontes documentais existentes; somente biblioteca padrão."""
import json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def plain(text):
    return re.sub(r'[*`]', '',re.sub(r'\[([^]]+)\]\([^)]+\)',r'\1',text)).strip()


def build():
    state=(ROOT/'ESTADO_ATUAL.md').read_text(encoding='utf-8')
    release=json.loads((HERE/'current_release.json').read_text(encoding='utf-8'))
    source=json.loads((HERE/'architect-source.json').read_text(encoding='utf-8'))
    table=state.split('## Onde estamos',1)[1].split('## Decisões',1)[0]
    progress=[]
    for line in table.splitlines():
        cells=[plain(c) for c in line.strip('|').split('|')]
        if len(cells)==3 and re.match(r'\d',cells[1]) and '%' in cells[1]:progress.append(dict(stage=cells[0],percent=cells[1],reading=cells[2].split(';')[0],source='ESTADO_ATUAL.md'))
    assert len(progress)==9,'Tabela de etapas mudou: revisar o extrator'
    def bullet(label):return plain(re.search(r'- \*\*'+label+r':\*\* (.+)',state)[1])
    overview=dict(project=plain(state.split('## O projeto',1)[1].split('\n\n')[1]),objective=bullet('Objetivo'),budget=bullet('Verba'),model=release['cadRevision'],notice='Tudo nominal até o levantamento real',source='ESTADO_ATUAL.md')
    for d in source['disciplines']:
        assert (ROOT/d['path']).exists(),d['path']
        if d['ownerSource']:assert d['ownerQuote'].lower() in (ROOT/d['ownerSource']).read_text(encoding='utf-8').lower(),d['id']
    data=dict(overview=overview,progress=progress,**source)
    (HERE/'src/architect-data.js').write_text('// Gerado por build_architect_data.py; fontes documentais.\nglobalThis.GUEDALA_ARCHITECT='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
    return data


if __name__=='__main__':build()
