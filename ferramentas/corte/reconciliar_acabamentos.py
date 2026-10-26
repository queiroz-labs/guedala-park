"""Reemite o estudo de corte pela regra de uma decoracao por chapa fisica.

Reusa o empacotador existente; nao escolhe acabamento/substrato nem altera CAD,
fichas, ferragens, custos, propostas separadas ou dados comerciais.
"""
from collections import Counter
import contextlib,csv,hashlib,importlib.util,io,json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Proximas_decisoes/Corte_e_formatos'
AUDIT=ROOT/'04_Moveis/Acabamentos_por_peca.csv'
RULE=ROOT/'ferramentas/site/fabrication/Decisao_acabamentos_R13.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def load(name,file):
    spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
    gen=load('corte_base',OUT/'analisar.py')
    with AUDIT.open(encoding='utf-8-sig',newline='') as f:audits=list(csv.DictReader(f,delimiter=';'))
    assert len(audits)==len({r['id'] for r in audits})==248
    audit={r['id']:r for r in audits}
    old=read(OUT/'Lista_base_249.json');old_ids={r['id']:r for r in old}
    current=gen.load_base();current_ids={r['id']:r for r in current}
    assert old_ids.keys()==current_ids.keys() and len(current_ids)==249
    for name,p in current_ids.items():
        assert (p['C_mm'],p['L_mm'],p['thickness_mm'],p['module'])==tuple(old_ids[name][k] for k in ['C_mm','L_mm','thickness_mm','module'])
        if name in audit:
            a=audit[name];assert a['face_1']==a['face_2'],name
            if a['situacao']!='whole_piece_finish_pending':
                assert p['specification'].startswith(a['padrao_atual']),name
    missing=sorted(current_ids.keys()-audit.keys());assert missing==['Peca350']
    assert all(current_ids[i]['packing_blockers'] for i in missing)
    # As superficies ainda sem escolha nao se tornam outra cor/segunda chapa.
    params_before=sha(OUT/'Parametros.json')
    fixed_sources=[*gen.input_paths(),AUDIT,RULE,ROOT/'04_Moveis/Acabamentos_por_peca.json',
                   ROOT/'02_Modelo_3D/Guedala_Park_R52_Corrigido.FCStd']
    source_hashes={p.relative_to(ROOT).as_posix():sha(p) for p in fixed_sources}
    # Somente arquivos SVG comprovadamente produzidos pelo gerador legado.
    prior_svg={p.name:p for p in (OUT/'Planos_svg').glob('*.svg')}
    with contextlib.redirect_stdout(io.StringIO()):gen.main()
    plans=read(OUT/'Planos_preliminares.json');summary=read(OUT/'Resumo.json')
    scenarios=plans['scenarios'];expected={s['svg'].split('/')[-1] for g in scenarios[0]['groups'] for s in g['sheets']}
    notices=[]
    for name,p in prior_svg.items():
        if name in expected:continue
        previous=p.read_text(encoding='utf-8')
        assert 'Envelopes geométricos; não é corte executivo.' in previous or 'CAMINHO_SUPERADO' in previous,name
        # Mantem o caminho antigo com aviso, sem apagar/mover arquivo de outro
        # trabalho e sem deixar um desenho de corte obsoleto parecendo vigente.
        notice='''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 260">
<!-- CAMINHO_SUPERADO: aviso de compatibilidade, nao representa uma chapa -->
<rect width="1000" height="260" fill="#f4f1eb"/>
<text x="35" y="65" font-family="sans-serif" font-size="28">Agrupamento de corte substituido em25/10/2026</text>
<text x="35" y="115" font-family="sans-serif" font-size="22">Este caminho antigo nao representa uma chapa vigente.</text>
<text x="35" y="160" font-family="sans-serif" font-size="22">Regra atual: um acabamento por peca fisica, igual nas duas faces.</text>
<a href="../README.md"><text x="35" y="215" font-family="sans-serif" font-size="22" fill="#225a45">Consultar o estudo atual e sua lista de desenhos</text></a>
</svg>'''
        p.write_text(notice+'\n',encoding='utf-8');notices.append(name)
    after={p.relative_to(ROOT).as_posix():sha(p) for p in fixed_sources}
    assert source_hashes==after and params_before==sha(OUT/'Parametros.json')
    assert all('face interna Branco TX; face aparente' not in p['specification'] for p in current)
    assert all(not ('+' in g['specification'] and 'Branco TX' in g['specification']) for s in scenarios for g in s['groups'])
    changes=[dict(id=p['id'],module=p['module'],previous_specification_from_finish_audit=audit[p['id']]['especificacao_anterior'],
                  current_specification=p['specification']) for p in current if p['id'] in audit and audit[p['id']]['especificacao_anterior']!=p['specification']]
    for name in expected:ET.parse(OUT/'Planos_svg'/name)
    report=dict(date='2026-10-25',rule=RULE.relative_to(ROOT).as_posix(),base_panels=249,
        audited_panels=248,not_in_finish_audit_ids=missing,all_missing_excluded_from_packing=True,
        current_opposite_finish_pairs=sum(r['face_1']!=r['face_2'] for r in audits),
        finish_pending_in_audit=[r['id'] for r in audits if r['situacao']=='whole_piece_finish_pending'],
        geometry_249_unchanged=True,original_sources_unchanged=True,proposals_adopted=0,purchase_ready=False,
        groups=[dict(id=g['id'],specification=g['specification'],thickness_mm=g['nominal_thickness_mm'],panels=g['pieces'],virtual_sheets=len(g['sheets'])) for g in scenarios[0]['groups']],
        scenarios=summary['plans'],excluded_ids=scenarios[0]['excluded_ids'],
        primary_exclusion_reasons=dict(Counter(p['packing_blockers'][0].split(':')[0] for p in current if p['packing_blockers'])),
        reconciled_against_finish_audit=changes,previous_mixed_finish_panel_count=sum(r['cores_opostas_antes']=='sim' for r in audits),notice_svg_paths=notices,current_svg_paths=sorted(expected),
        source_sha256=source_hashes,generator_sha256=sha(Path(__file__)),
        limits=['Formatos e rotacao sao virtuais;nenhum estoque/substrato/veio/fita/processo confirmado.',
                '11 acabamentos pendentes na auditoria maisP13 sem entrada;nao escolher padrao ou inserir segunda chapa.',
                '34 exclusoes do ensaio nao equivalem a34 cores por escolher:incluem referencia,espessura e espelho separado.',
                'Planos nao incluem os kits de propostaP03/C01/soco nem contam as alternativas como adotadas.',
                'Avisos nos caminhos antigos nao sao chapas adicionais nem planos atuais.'])
    (OUT/'Reconciliacao_acabamentos.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    # Executar o verificador original usa import local; nao altera fontes.
    import sys
    sys.path.insert(0,str(OUT));verifier=load('conferencia_corte',OUT/'verificar.py')
    with contextlib.redirect_stdout(io.StringIO()):verifier.main()
    print(json.dumps(dict(reconciled=249,audit=248,missing=missing,included=scenarios[0]['included_panels'],excluded=len(scenarios[0]['excluded_ids']),virtual_sheets=scenarios[0]['virtual_sheets'],same_finish_both_faces=True,sources_preserved=True),ensure_ascii=False))

if __name__=='__main__':main()
