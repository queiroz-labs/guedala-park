"""Teste integrado em cópia descartável fora do repositório.

python ferramentas/pranchas/testar.py --temporarios CAMINHO_FORA_DO_REPOSITORIO
"""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import xml.etree.ElementTree as ET

sys.dont_write_bytecode = True
from medidas import numero, resolver

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def testar(parent):
    compound={'DIM-01':dict(valor_nominal_atual='2,45 × 2,95 m',valor_medido='2400 × 2900 mm')}
    assert resolver(compound,'DIM-01/0').mm==2400
    assert resolver(compound,'DIM-01/1').mm==2900
    assert resolver(compound,'DIM-01/1').origem=='medido'
    parent=parent.resolve()
    if parent==ROOT or ROOT in parent.parents:
        raise ValueError('Teste deve ficar fora do repositório')
    target=parent/('gp-pranchas-teste-'+uuid.uuid4().hex)
    target.mkdir(parents=True)
    source_files=['07_Imovel/Medidas_e_impactos.csv','06_Entregas/Planta_cotada/Cotas.json',
                  '06_Entregas/Caderno_pranchas/Geometria.json',
                  '02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd','ferramentas/fatos.json']
    before={name:sha(ROOT/name) for name in source_files}
    try:
        for name in source_files:
            dest=target/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
        shutil.copytree(ROOT/'ferramentas/pranchas',target/'ferramentas/pranchas')
        out=target/'06_Entregas/Caderno_pranchas'
        def run():
            subprocess.run([sys.executable,'-B',str(target/'ferramentas/pranchas/gerar.py')],cwd=target,check=True)
        run()
        baseline=json.loads((out/'Ultima_geracao.json').read_text(encoding='utf-8'))['cotas']
        elevation_before={p.name:sha(p) for p in out.glob('E*.svg')}
        detail_before=sha(out/'DT1.svg')
        measure=target/'07_Imovel/Medidas_e_impactos.csv'
        with measure.open(encoding='utf-8',newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
        codes=[]
        for row in rows:
            if row['codigo_medida'].startswith('PD-'):
                assert numero(row['valor_nominal_atual'],nominal=True)==2600
                row['valor_medido']='2470 mm'
                row['evidencia_campo']='TESTE TEMPORARIO; não representa medição real'
                codes.append(row['codigo_medida'])
        assert len(codes)==6
        with measure.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        run()
        impact=json.loads((out/'Impacto.json').read_text(encoding='utf-8'))
        current=json.loads((out/'Ultima_geracao.json').read_text(encoding='utf-8'))['cotas']
        changed_elevations=[name for name,h in elevation_before.items() if sha(out/name)!=h]
        assert len(changed_elevations)==12
        assert sha(out/'DT1.svg')!=detail_before
        changed_values=[a for a in impact['alteracoes'] if a['antes'] and a['depois'] and a['antes']['mm']!=a['depois']['mm']]
        conflicts=[a for a in impact['avisos'] if 'ultrapassa o teto' in a['mensagem']]
        assert conflicts and all(a['depois']['prancha'] and a['depois']['movel'] for a in changed_values)
        for name in ('P09','P10','P11','P12'):
            assert current['E01:'+name+'-folga']['mm']==-80
            assert current['E01:'+name+'-altura-parametrica']['mm']==baseline['E01:'+name+'-altura-parametrica']['mm']-130
        assert current['E01:pe-direito']['origem']=='medido'
        assert current['E01:P09-folga']['origem']=='nominal'
        assert current['DT1:fechamento']['mm']==30
        svg=ET.fromstring((out/'E01.svg').read_text(encoding='utf-8'))
        assert svg.attrib['width']=='420mm' and svg.attrib['height']=='297mm'
        assert svg.attrib['viewBox']=='0 0 420 297'
        lines=svg.findall('{http://www.w3.org/2000/svg}line')
        assert any(l.get('x1')==l.get('x2')=='17' and
                   math.isclose(abs(float(l.get('y2'))-float(l.get('y1'))),2470/25) for l in lines)
        stable_pdf=sha(out/'Guedala_Park_Pranchas_R02.pdf')
        run()
        assert not json.loads((out/'Impacto.json').read_text(encoding='utf-8'))['alteracoes']
        assert sha(out/'Guedala_Park_Pranchas_R02.pdf')==stable_pdf
        assert len(list(out.glob('*.svg')))==20
        try:numero('2470')
        except ValueError:pass
        else:raise AssertionError('Medida sem unidade foi aceita')
        assert numero('2,47 m')==numero('247 cm')==2470
        assert numero('0 mm')==0 and numero('') is None
        snapshot_hash=sha(out/'Ultima_geracao.json')
        for row in rows:
            if row['codigo_medida']=='PD-QUA':row['valor_medido']='-1 mm'
        with measure.open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
        failed=subprocess.run([sys.executable,'-B',str(target/'ferramentas/pranchas/gerar.py')],cwd=target,capture_output=True)
        assert failed.returncode!=0 and sha(out/'Ultima_geracao.json')==snapshot_hash
        assert sha(out/'Guedala_Park_Pranchas_R02.pdf')==stable_pdf
        assert all(sha(ROOT/name)==before[name] for name in source_files)
        result=dict(pe_direito='2600 -> 2470 mm',ambientes=len(codes),elevacoes_alteradas=len(changed_elevations),
                    cotas_alteradas=len(changed_values),conflitos=conflicts,fechamento_P03='160 -> 30 mm',
                    repeticao_sem_mudancas=0,originais_preservados=True,folhas=20,
                    escala_vetorial_1_25=True,pdf_deterministico=True,entrada_invalida_preserva_saida=True)
        print(json.dumps(result,ensure_ascii=True,indent=2))
        return result
    finally:
        # Alvo fixo desta execução, validado como filho do diretório externo informado.
        assert target.resolve().parent==parent and target.name.startswith('gp-pranchas-teste-')
        shutil.rmtree(target)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--temporarios',type=Path,required=True)
    testar(parser.parse_args().temporarios)
