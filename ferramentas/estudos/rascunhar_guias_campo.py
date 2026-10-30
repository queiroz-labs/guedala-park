"""Gera rascunho externo para revisão manual; não substitui guias_campo.json."""
import argparse
import csv
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'ferramentas/site'))
from build_field_data import rows


def draft():
    with (ROOT/'04_Moveis/Dependencias/Descricao_fisica.csv').open(encoding='utf-8-sig',newline='') as f:
        descriptions={r['codigo_medida']:r for r in csv.DictReader(f,delimiter=';')}
    result=[]
    for row in rows():
        description=descriptions.get(row['codigo'],{})
        for part in row['partes']:
            pending='pendente' in description.get('situacao','')
            result.append(dict(codigo=part['codigo'],titulo_simples=row['descricao'],
                onde=dict(comodo=row['ambiente'],alvo=None,orientacao='só cômodo; marco físico a identificar'),
                como=['ver protocolo de datum' if pending else description.get('descricao_fisica',row['descricao']),
                      'Rascunho: revisar o texto e a associação física antes de usar.'],
                instrumento=description.get('instrumento','a definir'),altura_ref_mm=1000,foto=None))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--saida',type=Path,required=True)
    args=parser.parse_args();target=args.saida.resolve()
    if target==ROOT or ROOT in target.parents:parser.error('Rascunho deve ficar fora do repositório')
    target.write_text(json.dumps(draft(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
