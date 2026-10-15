from pathlib import Path
from collections import Counter
import json,hashlib,re

root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve()
r=json.loads(((Path(__file__).resolve().parent / 'Leitura_controles_R28.json').resolve()).read_text(encoding='utf-8'))
issues=[]
nav=Counter(e['original'] for e in r['navigation'])
for c in r['catalog']:
    if nav[c['control']]!=1:issues.append({'kind':'navigation_count','control':c['control'],'count':nav[c['control']]})
    for f in c['fields']:
        if f['value'] is None or f['editor_mode'] in ['missing','unresolved'] or (isinstance(f['editor_mode'],list) and ('ReadOnly' in f['editor_mode'] or 'Hidden' in f['editor_mode'])):
            issues.append({'kind':'unusable_field','control':c['control'],'field':f})
        incoming=[e for p,e in c['expressions'] if p.lstrip('.')==f['field']]
        if incoming:issues.append({'kind':'input_overwritten_by_expression','control':c['control'],'field':f['field'],'expressions':incoming})
    assert c['bindings'] or c['expressions'], c['control']
summary={'accesses':len(r['navigation']),'controls':len(r['catalog']),'input_fields':sum(len(c['fields']) for c in r['catalog']),'issues':issues,'source_sha256':r['sha256'],'source_unchanged':r['sha256']==r['sha256_after'],'limits':'Field existence, editing mode, navigation uniqueness and a dependency are checked; does not prove physical actuator, all formula domains or interlocks. Drawer/entrance commands drive their own Placement. No recompute, movement or collision retest.'}
((Path(__file__).resolve().parent / 'Conferencia_acessos_R28.json').resolve()).write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')

# Only a new dependency on the corrected sofa. Existing routes are not rerun.
b=r['bank'];axis=b['longitudinal_world_axis'];assert abs(axis[0])<1e-12 and abs(axis[1]+1)<1e-12 and abs(axis[2])<1e-12
matrix=b['placement_matrix'];assert abs(matrix[5])<1e-12 and abs(matrix[6])<1e-12
origin_y=matrix[7];ranges=[]
for row in b['lids']:
    assert row['driver_axis']==[1.0,0.0,0.0]
    assert row['driver_expressions']==[['.Placement.Rotation.Angle','-'+row['control']+'.Abertura']]
    ranges.append({'item':row['lid'],'y_min':row['lid_bbox'][1],'y_max':row['lid_bbox'][4],'reason':'LocalX rotation preserves longitudinal projection for every angle.'})
    if not row['separate']:
        ranges.append({'item':row['cushion'],'y_min':row['cushion_bbox'][1],'y_max':row['cushion_bbox'][4],'reason':'First cushion follows same lid axis.'})
    else:
        travel={2:711,3:733,4:873}[row['sector']]
        sign=1 if row['sector']==4 else -1
        x0=row['cushion_placement_matrix'][3];x1=x0+sign*travel
        expected=('' if sign==1 else str(int(x0))+' mm - ')+row['control']+'.DeslocamentoAlmofada'
        assert dict(row['cushion_expressions'])['.Placement.Base.x']==expected
        ranges.append({'item':row['cushion'],'y_min':origin_y-max(x0,x1)-row['pad_length_mm'],'y_max':origin_y-min(x0,x1),'reason':'Endpoints bound complete fixed-orientation translation; vertical lift does not changeY.'})
content={q['object']:q for q in b['content']}
audit=json.loads(((Path(__file__).resolve().parent / '../Banco_R16_2026-10-14/Auditoria_R16.json').resolve()).read_text(encoding='utf-8'))
for route in audit['content_routes']:
    box=content[route['name']]['bbox'];length=box[4]-box[1]
    xs=[node[0] for seg in route['segments'] for node in [seg['from_mm'],seg['to_mm']]]
    ranges.append({'item':route['name'],'y_min':origin_y-max(xs)-length,'y_max':origin_y-min(xs),'reason':'Recorded native translation path, all endpoint projections; no replay.'})
leaf=content[b['leaf']]['bbox']
ranges.append({'item':b['leaf'],'y_min':leaf[1],'y_max':leaf[4],'reason':'R16 final leaf route changes only localY/Z, preserving longitudinalX.'})
sofa_max=max(s['bbox'][4] for s in r['sofa'])
for q in ranges:q['gap_to_sofa_mm']=q['y_min']-sofa_max
assert all(q['gap_to_sofa_mm']>0 for q in ranges)
bankreport={'scope':'Affected dependency: bank documented lid/cushion/content/leaf access versus only five daily sofa primitives restoredR24; original bank/other-target tests are not rerun. Source frame and mirrored frame shareY unchanged.','sofa_max_y':sofa_max,'projection_ranges':ranges,'minimum_projected_gap_mm':min(q['gap_to_sofa_mm'] for q in ranges),'limits':'Only ideal longitudinal envelopes for documented commands; no arbitrary control entries, people, physical sofa bed mechanism, transfer of leaf to tabletop, loading, tolerances or hardware. No booleans or poses executed. Native models and source file unchanged.'}
((Path(__file__).resolve().parent / 'Banco_sofa_corrigido_R28.json').resolve()).write_text(json.dumps(bankreport,ensure_ascii=False,indent=2),encoding='utf-8')

# Preserve the older guide as a historical revision; write a reconciled current guide.
guide=((Path(__file__).resolve().parent / '../Manutencao_R26_2026-10-14/Guia_controles_R26.md').resolve()).read_text(encoding='utf-8')
old='retirar temporariamente a lixeira é proposta ainda sem endereço/manuseio comprovados. Não usar essa retirada como percurso livre.'
new='a proposta R26 define estacionamento temporário em ControleLoopManutencaoR26.Afastamento650, antes de retirar a armação. Endereço/percurso CAD conferidos; manuseio, retenção, carga e piso reais pendentes. Repor armação/painel e fechar cesto antes de devolver a lixeira0; sem intertravamento.'
assert guide.count(old)==1
guide=guide.replace(old,new).replace('# Guia R26 —46 acessos','# Guia vigente R28 —46 acessos',1)
guide=guide.replace('[Sequência e limites](README.md)','[Sequência e limites](../Manutencao_R26_2026-10-14/README.md)')
guide=guide.replace('../Rotulos_R23_2026-10-14/Cobertura_modulos_R23.md','../Rotulos_R23_2026-10-14/Cobertura_modulos_R23.md').replace('../../04_Documentacao/Entrega_atual_R23.md','../../04_Documentacao/Entrega_atual_R28.md')
guide='A R28 mantém os controles e incorpora a proposta de descer o aéreo completo do escritório20 mm. Base1900/topo2450, caixa2000×350×550 preservada; teto2470 hipotético. [Folga e limites](../Folga_teto_R28_2026-10-14/README.md).\n\n'+guide
((Path(__file__).resolve().parent / 'Guia_controles_vigentes_R28.md').resolve()).write_text(guide,encoding='utf-8')
assert hashlib.sha256(Path(r['file']).read_bytes()).hexdigest()==r['sha256']
print(json.dumps({'controls':summary['controls'],'fields':summary['input_fields'],'issues':issues,'bank_projection_ranges':len(ranges),'bank_sofa_gap_mm':bankreport['minimum_projected_gap_mm'],'cad_unchanged':True}))
