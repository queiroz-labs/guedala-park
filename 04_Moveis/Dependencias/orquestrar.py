"""Cadeia nominal em saída externa; não abre FCStd nem grava medidas nas fontes.

python -B 04_Moveis/Dependencias/orquestrar.py --medidas C:/Temp/campo.csv
"""
import argparse
import contextlib
import copy
import csv
import hashlib
import importlib.util
import io
import json
import math
from pathlib import Path
import shutil
import sys
import tempfile
import time
from types import SimpleNamespace

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'ferramentas/estudos'))
sys.path.insert(0,str(ROOT/'ferramentas/medidas'))
import recalcular as dimensional
import gerar_furacao as furacao
import conferir_furacao as conflitos
import quantificar_furacao as quantidades


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result)
    return result


corte=module('corte_cadeia',ROOT/'04_Moveis/Proximas_decisoes/Corte_e_formatos/analisar.py')
ROOMS={'QUA':'quarto','COZ':'cozinha','LAV':'lavanderia','ESC':'escritorio','BAN':'banho','SAL':'sala','CIR':'circulacao'}
AUX={f'CAMPO-{code}-{kind}':dict(room=room,kind=kind) for code,room in ROOMS.items() for kind in ['ESQUADRO','PISO']}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_out(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def outside(path):
    return dimensional.saida_segura(path)


def source_paths():
    return [HERE/'regras.json',ROOT/'07_Imovel/Medidas_e_impactos.csv',ROOT/furacao.GEO,
            ROOT/furacao.TECH,ROOT/furacao.HINGES,corte.HERE/'Parametros.json',Path(__file__),
            Path(dimensional.__file__),Path(furacao.__file__),Path(conflitos.__file__),Path(quantidades.__file__),
            *sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')),
            *sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-furacao.csv')),
            *sorted(furacao.OUT.glob('P??-coordenadas.csv')),furacao.OUT/'Quantitativos.json']


def document():
    doc=dimensional.ler_json(HERE/'regras.json')
    geo=dimensional.ler_json(ROOT/doc['exportacao'])
    if doc['cad_sha256']!=geo['cad_sha256']:
        raise ValueError('Regras/exportação pertencem a fontes diferentes')
    # Validate the exported metadata, without reading the FCStd.
    return doc


def parse_aux(code,text):
    if AUX[code]['kind']=='PISO':
        value=dimensional.resolver({code:dict(valor_medido=text,valor_nominal_atual='')},code).mm
    else:
        import re
        match=re.fullmatch(r'\s*(\d+(?:[.,]\d+)?)\s*(deg|grau|graus|°)\s*',text)
        if not match:raise ValueError(code+': informar ângulo com unidade deg/grau/°')
        value=float(match[1].replace(',','.'))
    if value is None or value<0 or not math.isfinite(value):raise ValueError('Valor auxiliar inválido: '+code)
    if AUX[code]['kind']=='ESQUADRO' and value>=45:raise ValueError('Ângulo fora da representação de triagem')
    return value


def inputs(path,output):
    known=dimensional.entradas();normal=[];aux={};seen=set()
    with path.open(encoding='utf-8-sig',newline='') as stream:
        reader=csv.DictReader(stream)
        if not {'codigo_medida','valor_medido'}<=set(reader.fieldnames or []):raise ValueError('CSV exige codigo_medida,valor_medido')
        for r in reader:
            code=r['codigo_medida']
            if code in seen:raise ValueError('Código repetido: '+code)
            seen.add(code)
            if code.startswith('PAREDE-'):
                from sensibilidade import model
                wall,_,kind=code.rpartition('-')
                if wall not in model()['walls'] or kind not in ['DESLOCAMENTO','ANGULO']:raise ValueError('Pano/parâmetro desconhecido: '+code)
                if kind=='DESLOCAMENTO':aux[code]=dimensional.resolver({code:dict(valor_medido=r['valor_medido'],valor_nominal_atual='')},code).mm
                else:
                    import re
                    match=re.fullmatch(r'\s*(-?\d+(?:[.,]\d+)?)\s*(deg|grau|graus|°)\s*',r['valor_medido'])
                    if not match:raise ValueError('Ângulo com unidade inválida: '+code)
                    aux[code]=float(match[1].replace(',','.'))
                if aux[code] is None or not math.isfinite(aux[code]):raise ValueError('Parâmetro de parede inválido')
            elif code in AUX:aux[code]=parse_aux(code,r['valor_medido'])
            elif code in known:normal.append(r)
            else:raise ValueError('Código desconhecido: '+code)
    normalized=output/'Medidas_entrada.csv'
    with normalized.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=['codigo_medida','valor_medido','evidencia_campo'],extrasaction='ignore');writer.writeheader();writer.writerows(normal)
    return dimensional.entradas(cenario=normalized),aux


def adjust(report,doc,aux):
    """Worst-corner envelope check; fixed boxes and panels remain fixed.

    PD refers to the low/reference finished-floor level. PISO is the rise from
    that reference to the high contact point; do not enter a local PD twice.
    ESQUADRO is |angle-90°|; tan(angle)*orthogonal cabinet span is a conservative
    intrusion allowance, not a reconstruction of the wall polygon.
    """
    by_room={v:k for k,v in ROOMS.items()}
    index={(r['movel'],r['cota']):r for r in doc['regras']}
    for r in report['resultados']:
        target=doc['alvos'][r['movel']];room=target['room'];prefix=by_room.get(room)
        if not prefix:continue
        floor=aux.get(f'CAMPO-{prefix}-PISO',0)
        angle=aux.get(f'CAMPO-{prefix}-ESQUADRO',0)
        rule=index[(r['movel'],r['cota'])]
        if rule.get('eixo') in [0,1]:
            axis=rule['eixo'];box=target['box_planta'];span=box[4-axis]-box[1-axis]
            r['folgas_mm']['fim']-=math.tan(math.radians(angle))*span
        elif rule.get('eixo')==2 or r['tipo']=='fechamento':
            r['folgas_mm']['topo']-=floor
            if r['tipo']=='fechamento':r['depois_mm']-=floor;r['delta_mm']-=floor
        if r['folgas_mm'] and min(r['folgas_mm'].values()) < -1e-6:r['status']='NÃO CABE'
    return report


def evaluate(rows,doc,aux=None):
    result=adjust(dimensional.calcular(rows,doc),doc,aux or {})
    if aux and any(c.startswith('PAREDE-') for c in aux):
        from sensibilidade import model,minimum
        m=model(doc);gg=gap_map(result)
        for name,t in m['targets'].items():t['ceiling']=gg[name+'/Z/topo']
        result['menor_folga_paredes_medidas_mm']=minimum(m,aux)
    return result


def gap_map(report):
    result={}
    for r in report['resultados']:
        if r['tipo'] not in ['envelope','fechamento']:continue
        axis='Z' if r['tipo']=='fechamento' or r['cota']=='altura' else 'X' if r['cota']=='extensao_x' else 'Y'
        for edge,value in r['folgas_mm'].items():result[f'{r["movel"]}/{axis}/{edge}']=value
    return result


def derive_panels(doc,report,dest):
    dest.mkdir()
    base=furacao.panels(ROOT/'06_Entregas/Fichas_fabricacao');records=[];pending=[]
    for p in base.values():
        axes=[r for r in doc['regras'] if r['movel']==p['mod'] and r.get('eixo') is not None]
        fixed=bool(axes) and all(r['modo']=='fixa_com_folga_variavel' for r in axes)
        records.append(dict(movel=p['mod'],peca=p['id'],modo='caixa fixa' if fixed else 'vinculo por peca pendente',C_R54=p['c'],L_R54=p['l'],C_cenario=p['c'],L_cenario=p['l'],delta_C_mm=0,delta_L_mm=0))
        if p['contour']!='Retangular':pending.append(dict(movel=p['mod'],peca=p['id'],tema='recorte manual',detalhe='Contorno especial preservado; não derivar recorte de medida de parede.'))
        if not fixed:pending.append(dict(movel=p['mod'],peca=p['id'],tema='regra por peça',detalhe='Envelope variável não autoriza esticar painéis, portas ou ferragens.'))
    for path in sorted((ROOT/'06_Entregas/Fichas_fabricacao').glob('P??-pecas.csv')):shutil.copyfile(path,dest/path.name)
    for r in report['resultados']:
        if r['delta_mm'] and r['tipo']!='envelope':pending.append(dict(movel=r['movel'],peca='',tema=r['cota'],detalhe=f'Variação {r["delta_mm"]:g}mm de referência/fechamento; sem vínculo a ID de corte.'))
    furacao.write_csv(dest.parent/'Pecas_diferencas.csv',records)
    furacao.write_csv(dest.parent/'Pendencias_propagacao.csv',pending,['movel','peca','tema','detalhe'])
    return records,pending


def hole_key(h):
    return tuple(h.get(k,'') for k in ['movel','peca','face','x','y','diametro','profundidade','tipo','par'])


def issue_key(r):
    # Stable under hole numbering changes.
    return tuple(str(r.get(k,'')) for k in ['movel','peca','face','x','y','tipo','outro'])


def formats(folder,dest):
    panels=corte.load_base(folder)
    plans=corte.make_plan(panels)
    json_out(dest/'Formatos.json',corte.triage_records(panels,[]))
    json_out(dest/'Chapas_virtuais.json',plans)
    return plans


def run(measures,output=None):
    started=time.perf_counter()
    output=outside(output) if output else Path(tempfile.mkdtemp(prefix='guedala-cadeia-'))
    if output.exists() and any(output.iterdir()):raise ValueError('Escolha pasta de saída nova/vazia')
    output.mkdir(parents=True,exist_ok=True)
    paths=source_paths();before={p.relative_to(ROOT).as_posix():sha(p) for p in paths}
    doc=document();nominal=evaluate(dimensional.entradas(nominal=True),doc)
    rows,aux=inputs(Path(measures),output);scenario=evaluate(rows,doc,aux)
    dimensional.escrever(scenario,output)
    records,pending=derive_panels(doc,scenario,output/'Pecas')
    timings={};stage=time.perf_counter()
    (output/'Furacao').mkdir()
    with contextlib.redirect_stdout(io.StringIO()):
        furacao.generate(output/'Pecas',output/'Furacao')
    timings['furacao_s']=time.perf_counter()-stage;stage=time.perf_counter()
    args=SimpleNamespace(pecas=output/'Pecas',margem=3,ferramenta_comprimento=100,ferramenta_raio=10)
    with contextlib.redirect_stdout(io.StringIO()):conflitos.execute(output/'Furacao',output/'Furacao',args)
    timings['conflitos_s']=time.perf_counter()-stage;stage=time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):quant=quantidades.generate(output/'Furacao',SimpleNamespace(tempos=None,setup_min=2,setup_max=5),pecas=output/'Pecas',furacao=output/'Furacao')
    timings['quantitativos_s']=time.perf_counter()-stage;stage=time.perf_counter()
    plans=formats(output/'Pecas',output);base_plans=corte.make_plan(corte.load_base())
    timings['formatos_s']=time.perf_counter()-stage
    baseline_holes=[h for p in sorted(furacao.OUT.glob('P??-coordenadas.csv')) for h in conflitos.read(p)]
    current_holes=[h for p in sorted((output/'Furacao').glob('P??-coordenadas.csv')) for h in conflitos.read(p)]
    old_h={hole_key(h) for h in baseline_holes};new_h={hole_key(h) for h in current_holes}
    old_issues=conflitos.audit(baseline_holes,furacao.panels(ROOT/'06_Entregas/Fichas_fabricacao'))[0]
    current_issues=conflitos.read(output/'Furacao/Conflitos.csv')
    old_i={issue_key(r) for r in old_issues};new_i=[r for r in current_issues if issue_key(r) not in old_i]
    furacao.write_csv(output/'Conflitos_novos.csv',new_i,conflitos.ISSUE_FIELDS)
    old_g=gap_map(nominal);new_g=gap_map(scenario)
    new_neg=[dict(folga=k,antes_mm=old_g[k],depois_mm=v) for k,v in new_g.items() if v < -1e-6 and old_g[k]>=-1e-6]
    furacao.write_csv(output/'Folgas_negativas_novas.csv',new_neg,['folga','antes_mm','depois_mm'])
    budget=dict(base='R44; provisão preservada',delta_furos=len(new_h)-len(old_h),delta_ferragens={k:quant['ferragens_por_familia'].get(k,0)-v for k,v in furacao.load('04_Moveis/Furacao/Quantitativos.json')['ferragens_por_familia'].items()},chapas_extras_por_arranjo={p['id']:p['virtual_sheets']-b['virtual_sheets'] for p,b in zip(plans,base_plans)},delta_reais_total=None,motivo='Sem preços unitários e sem ID/composição dos fechamentos/recortes; não converter provisão em custo por peça.',delta_reais_quantificavel=0)
    json_out(output/'Diferenca_orcamento.json',budget)
    after={p.relative_to(ROOT).as_posix():sha(p) for p in paths}
    if before!=after:raise RuntimeError('Fonte mudou durante a execução; repetir com base estável')
    timings['total_s']=time.perf_counter()-started
    report=dict(base='R54/exportação; 249 IDs das fichas',cad_sha256=doc['cad_sha256'],pecas_total=len(records),pecas_alteradas=sum(r['delta_C_mm']!=0 or r['delta_L_mm']!=0 for r in records),furos=len(current_holes),furos_novos=len(new_h-old_h),furos_perdidos=len(old_h-new_h),conflitos_novos=len(new_i),novas_folgas_negativas=len(new_neg),pendencias_propagacao=len(pending),auxiliares_informados=aux,auxiliares_nao_medidos=sorted(set(AUX)-set(aux)),tempos=timings,fontes_sha256=before,medidas_sha256=sha(Path(measures)),orcamento=budget,limites='Caixas fixas; referências não são peças. Ausência de furos novos não resolve 104 peças sem centros, escareados e mecanismos sem cobertura. Fita é regra proposta; valor total permanece pendente.')
    json_out(output/'Cadeia.json',report)
    lines=['# Cadeia de medidas — nominal', '', f'Base R54; {len(records)} peças preservadas. {report["pecas_alteradas"]} peças mudaram; {report["furos_novos"]} furos novos, {report["furos_perdidos"]} perdidos; {len(new_i)} conflitos de furação novos; {len(new_neg)} folgas ficaram negativas.', '', f'Tempo: {timings["total_s"]:.3f}s. Saídas em Pecas/, Furacao/, Formatos.json e Chapas_virtuais.json. Diferença de orçamento em Diferenca_orcamento.json: quantidade comparável, preço total desconhecido.', '', report['limites'], '', 'Esquadro/floor: canais CAMPO-QUA/COZ/LAV/ESC/BAN/SAL/CIR-ESQUADRO (desvio absoluto de90°, deg) e -PISO (elevação máxima desde piso de referência, mm). Folga consome tan(ângulo)×extensão ortogonal da caixa e elevação do piso. Hipótese conservadora de canto; não reconstrói paredes. Se PD já foi medido no ponto alto, não descontar o piso novamente. Auxiliar ausente permanece não medido, zero somente na reprodução nominal.', '', 'Pendencias_propagacao.csv lista recortes e referências sem ID. Caixas/bancadas não são redimensionadas por diferença da parede. As fichas descritivas e fontes permanecem intactas; nenhum FCStd é lido pelo orquestrador.']
    (output/'Cadeia.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return report,output


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--medidas',type=Path,required=True);ap.add_argument('--saida',type=Path);args=ap.parse_args()
    try:
        result,out=run(args.medidas,args.saida);print(json.dumps(dict(saida=str(out),tempo_s=result['tempos']['total_s'],pecas_alteradas=result['pecas_alteradas'],novas_folgas_negativas=result['novas_folgas_negativas']),ensure_ascii=False))
    except (ValueError,KeyError) as exc:raise SystemExit('ERRO: '+str(exc))
