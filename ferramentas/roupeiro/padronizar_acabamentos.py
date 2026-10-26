"""Aplica a decisao de25/10: um acabamento por peca, igual nas duas faces.

Atualiza fontes documentais e registra o inventario anterior por ID. Nao abre CAD.
Espelho/estofado sao componentes aplicados separados, nao outra cor no painel.
"""
from pathlib import Path
from collections import Counter,defaultdict
import copy,csv,json,hashlib

ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/'ferramentas/site/fabrication'
RULE='ferramentas/site/fabrication/Decisao_acabamentos_R13.md'
CSV=ROOT/'04_Moveis/Acabamentos_por_peca.csv'
JOUT=ROOT/'04_Moveis/Acabamentos_por_peca.json'
POLICY='Cada chapa fisica tem um acabamento igual nas duas faces. Duas pecas distintas podem combinar externa18 no padrao do projeto e interna15 BrancoTX; identificar ambas e conferir33mm,vaos,ligacoes e cargas. Nao presumir caixa dupla nem acrescentar15 automaticamente. P03 atual:pecas unicas18,sem caixa interna15 continua. Espelho/estofado sao pecas separadas.'

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def write(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def canonical(s,code):
    if code=='P03':return 'Greenplac Arenza liso'
    if s and 'Arenza' in s:
        return 'Arenza liso (referência; código/amostra a confirmar)' if 'referência' in s else 'Greenplac Arenza liso'
    return s

REPLACEMENTS={
 'Definir mapa de faces e solução construtiva para Branco TX interno + padrão aparente; não presumir chapa dual comercial pronta.':'Aplicar um único padrão nas duas faces de cada peça; Branco TX somente em peças exclusivamente internas. Não prever composição de cores opostas.',
 'Cor interna resolvida: Branco TX. Especificar fabricante/código, substrato, classe e processo de composição; são decisões técnicas, não medições de campo.':'Branco TX fica nas peças exclusivamente internas; peça aparente recebe seu padrão nas duas faces. Especificar fabricante/código, substrato e classe.',
 'Fabricante/código do Branco TX; substrato; espessura de compra; processo de composição das faces; bordas/veios e furação.':'Fabricante/código do padrão único de cada peça; substrato; espessura de compra; bordas/veios e furação.',
 'Códigos externos escolhidos em24/10: Arauco Beige Matt nas frentes do gabinete e Louro Freijó Poro nas laterais aparentes. Fechar substrato, composição com Branco TX, bordas/veios e faces ainda parciais; conferir amostra.':'Códigos escolhidos: frentes Beige Matt nas duas faces; laterais Louro Freijó Poro nas duas faces. Branco TX somente em peças exclusivamente internas; definir um único padrão nas peças ainda parciais, substrato e bordas.',
 'Fechar substrato e códigos de chapa, composição Branco TX/padrão aparente, bordas e veios por peça. As faces ainda parciais estão marcadas na lista de peças.':'Fechar substrato e códigos de chapa, com um único padrão nas duas faces de cada peça, bordas e veios. Peças de padrão ainda indefinido continuam marcadas na lista.',
 'sem reabrir Branco TX nos interiores':'mantendo Branco TX apenas nas peças exclusivamente internas',
 'A decisão de Branco TX resolve a cor dos interiores. Medidas, composição da chapa, fabricante/código, faces especiais, bordas, veios e uniões não são aprovados automaticamente.':'Regra25/10: um acabamento por peça nas duas faces; Branco TX apenas nas peças exclusivamente internas. Medidas, substrato, códigos, bordas e uniões ainda requerem conferência.',
 'Faces registradas separadamente; não implica chapa dupla pronta.':'Um padrão por peça, igual nas duas faces.',
}
def text_fix(o):
    if isinstance(o,str):
        for a,b in REPLACEMENTS.items():o=o.replace(a,b)
        return o
    if isinstance(o,list):return [text_fix(x) for x in o]
    if isinstance(o,dict):return {k:(v if k in ['sourceEvidence','evidence'] else text_fix(v)) for k,v in o.items()}
    return o

d=read(DATA/'finish-audit.json')
old_rows={}
if CSV.exists():
    with CSV.open(encoding='utf-8-sig',newline='') as f:old_rows={r['id']:r for r in csv.DictReader(f,delimiter=';')}
original=copy.deepcopy(d['overrides'])
rows=[];counts=Counter();by_module=Counter();partial=[]
for x in d['overrides']:
    code=x['module'];outer=x.get('exposedMaterial');inner=x.get('innerMaterial')
    stored=old_rows.get(x['source'])
    old_material=stored['especificacao_anterior'] if stored else x['material']
    was_mixed=stored['cores_opostas_antes']=='sim' if stored else bool(inner and outer and 'Espelho' not in outer and inner!=outer)
    was_mirror=stored['espelho_aplicado']=='sim' if stored else bool(outer and 'Espelho' in outer)
    if was_mixed:counts['mixed_wood_before']+=1;by_module[code]+=1
    if was_mirror:
        whole='Branco TX';x['appliedFacing']='Espelho, componente separado do painel-base'
        x['material']='Branco TX — duas faces do painel-base; Espelho (camada distinta do substrato) aplicado como peça separada'
        x['materialCode']=None;mode='whole_piece_with_separate_mirror';counts['separate_mirror']+=1
    elif code=='P03':
        whole='Greenplac Arenza liso';mode='whole_piece_same_finish'
        x['material']=whole+' — duas faces da mesma peça'
        x['finishCompleteForIdentifiedFaces']=True;x['remainingFinishQuestion']=None
    elif outer:
        whole=canonical(outer,code);mode='whole_piece_same_finish'
        x['material']=whole+' — duas faces da mesma peça'
    elif x.get('finishAssignmentMode')=='whole_piece_same_finish':
        whole=x['wholeBoardMaterial'];mode='whole_piece_same_finish'
        x['material']=whole+' — duas faces da mesma peça'
    elif x.get('finishCompleteForIdentifiedFaces'):
        whole=canonical(inner or 'Branco TX',code);mode='whole_piece_same_finish'
        x['material']=whole+' — duas faces da mesma peça'
    else:
        whole=None;mode='whole_piece_finish_pending'
        x['material']='Um único padrão para a peça inteira — a definir'
        question=x.get('remainingFinishQuestion') or 'Definir o padrão da peça.'
        if 'Regra25/10' not in question:question+=' Regra25/10: escolher um único padrão para a peça inteira, igual nas duas faces.'
        x['remainingFinishQuestion']=question;partial.append(x['source'])
    x['wholeBoardMaterial']=whole;x['finishAssignmentMode']=mode
    x['innerMaterial']=whole;x['exposedMaterial']=whole
    x['scope']='Padrão único por peça de chapa, igual nas duas faces. Não especifica substrato/furação/capacidade nem aprova fabricação.'
    x['finishRule']=RULE
    x['evidence']=RULE+'; decisão expressa de Elias em25/10/2026. Evidência anterior preservada em sourceEvidence e auditoria por ID.'
    evidence=x.setdefault('sourceEvidence',[])
    if not any(e.get('decisionKey')=='same_finish_per_piece_2026_10_25' for e in evidence):
        evidence.append(dict(path=RULE,type='explicit_user_decision',decisionKey='same_finish_per_piece_2026_10_25',excerpt=POLICY))
    rows.append(dict(id=x['source'],module=code,movel=d['modules'][code]['name'],peca=x['label'],
                     especificacao_anterior=old_material,cores_opostas_antes='sim' if was_mixed else 'nao',
                     padrao_atual=whole or 'A definir, único para a peça inteira',
                     face_1=whole or 'A definir',face_2=whole or 'A definir',
                     espelho_aplicado='sim' if was_mirror else 'nao',situacao=mode))

d=text_fix(d)
d['scope']='Acabamentos por peça: regra25/10 substitui a antiga distribuição por faces; CAD e fabricação preservados.'
d['userDecision']=dict(path=RULE,date='2026-10-25',type='explicit_user_decision',excerpt=POLICY)
d['materialSemantics']['dualFace']='Não adotado neste projeto: cada peça usa o mesmo padrão nas duas faces.'
d['materialSemantics']['wholePiece']=POLICY
d['materialSemantics']['Branco TX — faces internas']='Somente peças exclusivamente internas, no mesmo Branco TX nas duas faces.'
d['limitations']=[text_fix(x) for x in d.get('limitations',[])]+[POLICY] if POLICY not in d.get('limitations',[]) else d['limitations']
for code,m in d['modules'].items():
    assigned=[x for x in d['overrides'] if x['module']==code]
    m['faceAssignments']=copy.deepcopy(assigned)
    patterns=list(dict.fromkeys(x['wholeBoardMaterial'] for x in assigned if x['wholeBoardMaterial']))
    if code=='P03':summary='Maleiro inteiro em Arenza liso nas duas faces de cada peça; MDF BP Greenplac18 no estudo separado. Abertura A ainda condicionada; geometria CAD vigente preservada.'
    else:summary='Um acabamento por peça, igual nas duas faces. Padrões neste móvel: '+', '.join(patterns)+'. Branco TX somente em peças exclusivamente internas.'
    if not patterns:summary='Padrão da peça inteira ainda a definir; referência Arenza no CAD não fecha especificação. Confirmar acabamento antes da fabricação.'
    if code=='P19':summary+=' Espelho aplicado é peça separada do painel-base Branco TX.'
    m['finishSummary']=summary
    m['finishSpecs']=[dict(area='Peças inteiras, duas faces no mesmo padrão',material=v,status='Diretriz25/10; código/substrato/oficina conforme ficha',evidence=RULE) for v in patterns]
    if any(not x['wholeBoardMaterial'] for x in assigned):
        m['finishSpecs'].append(dict(area='Peças ainda sem padrão fechado',material='Escolher um único padrão por peça, sem faces de cores opostas',status='Pendente',evidence=RULE))
    m['boardChoices']['interiorFinish']='Arenza nas duas faces de todas as peçasP03' if code=='P03' else 'Branco TX somente nas peças exclusivamente internas; demais peças seguem o padrão aparente nas duas faces.'
    m['boardChoices']['sameFinishBothFaces']=True
    m['technicalChecks']=[text_fix(v) for v in m.get('technicalChecks',[]) if 'Cor interna resolvida' not in v]
    if POLICY not in m['technicalChecks']:m['technicalChecks'].append(POLICY)
    m['partialFaceSourceIds']=[x['source'] for x in assigned if not x['wholeBoardMaterial']]
summary=d['summary'];summary.update(dualFaceAssignments=0,sameFinishWholePieceAssignments=sum(bool(x['wholeBoardMaterial']) for x in d['overrides']),
                                  partialWholePieceAssignments=len(partial),correctedOppositeFinishPanels=counts['mixed_wood_before'],separateMirrorPanels=counts['separate_mirror'])
write(DATA/'finish-audit.json',d)

technical=read(DATA/'technical-r14.json')
mechanical_before={k:copy.deepcopy({n:v for n,v in m.items() if n not in ['projectChecks','technicalChecks','workshopChecks']}) for k,m in technical['modules'].items()}
for code,m in technical['modules'].items():
    for key in ['projectChecks','technicalChecks','workshopChecks']:
        if key in m:m[key]=text_fix(m[key])
assert mechanical_before=={k:{n:v for n,v in m.items() if n not in ['projectChecks','technicalChecks','workshopChecks']} for k,m in technical['modules'].items()}
technical['finishRule']=RULE;write(DATA/'technical-r14.json',technical)

with CSV.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';');writer.writeheader();writer.writerows(rows)
report=dict(date='2026-10-25',rule=POLICY,source=RULE,panels_audited=len(rows),
            previous_opposite_finish_wood_panels=counts['mixed_wood_before'],affected_modules=len(by_module),
            previous_mixed_by_module=dict(sorted(by_module.items())),separate_mirror_panel_count=counts['separate_mirror'],
            pending_whole_piece_finish_ids=partial,p03_all_same_finish=all(x['wholeBoardMaterial']=='Greenplac Arenza liso' for x in d['overrides'] if x['module']=='P03'),
            current_opposite_finish_pairs=sum(x.get('innerMaterial')!=x.get('exposedMaterial') for x in d['overrides']),
            mechanical_revision_preserved=True,inventory_csv='04_Moveis/Acabamentos_por_peca.csv')
assert report['current_opposite_finish_pairs']==0 and report['p03_all_same_finish']
write(JOUT,report)
print(json.dumps(report,ensure_ascii=True))
