from pathlib import Path
import json, math, runpy
H=(Path(__file__).resolve().parent / '.').resolve()
a=runpy.run_path(str((Path(__file__).resolve().parent / 'auditar_xml.py').resolve()))
base=json.loads(((Path(__file__).resolve().parent / '../../05_Ferramentas_e_registros/Base_interativa.json').resolve()).read_text(encoding='utf-8'))
skip={'wardrobe','bedcabinet','mirror','officecab','drawers','kitchenbase','sinkstorage','kitchenupper','laundrybase','laundrybasket','laundryupper','bathvanity','bathmirror','bench','lowdrawer','microwave'}
rows=[];number=0
def rz(t,point):
 c,s=math.cos(t),math.sin(t);return [[c,-s,0,point[0]],[s,c,0,point[1]],[0,0,1,point[2]],[0,0,0,1]]
for i,n in enumerate(base['nodes']):
    if n['kind']=='wall':number+=2;continue
    if n['id'] in skip:continue
    name='Peca'+(f'{number:03d}' if number else '');number+=1
    if not (n.get('yaw') or n.get('rot') or n.get('opacity')==0):continue
    assert name in a['DATA'],name
    dims=[n[k]*10 for k in ('w','d','h')]
    assert dims==[a['val'](name,p) for p in ('Length','Width','Height')]
    x,y,z=[n[k]*10 for k in ('x','z','y')]
    if n.get('yaw'):
        t=-n['yaw'];c,s=math.cos(t),math.sin(t);px,py=n['rootX']*10,n['rootZ']*10
        intended=rz(t,[px+(x-px)*c-(y-py)*s,py+(x-px)*s+(y-py)*c,z])
    else:
        t=-n.get('rot',0);c,s=math.cos(t),math.sin(t);cx=x+dims[0]/2;cy=y+dims[1]/2
        intended=rz(t,[cx-c*dims[0]/2+s*dims[1]/2,cy-s*dims[0]/2-c*dims[1]/2,z])
    saved=a['world'](name)
    oldbox=a['bounds'](saved,dims);newbox=a['bounds'](intended,dims)
    changed=max(abs(x-y) for x,y in zip(oldbox,newbox))>1e-6
    rows.append(dict(base_index=i,key=n['key'],id=n['id'],room=n['room'],object=name,label=a['label'](name),dims_mm=dims,
      linked_roots=a['by_source'].get(name),links_visible=[l for l in a['by_source'].get(name,[]) if a['visible'](l)],
      yaw_rad=n.get('yaw'),rot_rad=n.get('rot'),source_opacity=n.get('opacity',1),
      saved_world_matrix=saved,intended_matrix=intended,saved_bbox=oldbox,intended_bbox=newbox,footprint_changed=changed,
      mismatch_classification='Implantação diária diverge da fonte e do documentoR07' if changed else 'Frame/heading oposto aoJS; Part::Box simétrica mantém o MESMO envelope. Não prova novo choque ou direção visual de encosto, pois detalhe da cadeira não foi modelado'))
report=dict(file=str(a['FILE']),source_file=str((Path(__file__).resolve().parent / '../../05_Ferramentas_e_registros/Base_interativa.json').resolve()),base_export_date=base['exportDate'],nodes_total=len(base['nodes']),matched_nodes=len(rows),nodes=rows,
  summary=dict(yaw_nonzero=sum(bool(n.get('yaw')) for n in base['nodes']),rot_nonzero=sum(bool(n.get('rot')) for n in base['nodes']),opacity_zero=sum(n.get('opacity')==0 for n in base['nodes']),other_nonzero_tilt=sum(bool(n.get('tiltZ')) for n in base['nodes'])),
  method='Rastreio ordinal do loop de gerar_modelo.py, conferência de dimensões e matrizes XML; sem executar importador ou CAD',
  limits='Não modifica gerador/modelos. Três cadeiras têm orientação de frame oposta, mas caixas atuais idênticas geometricamente. Corrigir semântica de heading só com revisão responsável; não aplicar ajuste indiscriminado nem declarar colisão com base nisso.')
((Path(__file__).resolve().parent / 'Nos_base_rotacao_opacidade.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report['summary']));print([(r['object'],r['key'],r['footprint_changed'],r['source_opacity']) for r in rows])
