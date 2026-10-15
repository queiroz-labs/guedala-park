from pathlib import Path
import runpy,json,math
HERE=(Path(__file__).resolve().parent / '.').resolve()
a=runpy.run_path(str((Path(__file__).resolve().parent / 'auditar_xml.py').resolve()))
val=a['val'];world=a['world'];bounds=a['bounds'];coverage=a['coverage'];reflect=a['REFLECT'];mul=a['mul']
parts=[
 ('Peca122',-70,-90,140,90,8,28,True),
 ('Peca123',-66,-87,132,68,36,11,True),
 ('Peca124',-68,-19,136,19,35,47,True),
 ('Peca125',-70,-89,14,71,35,26,True),
 ('Peca126',56,-89,14,71,35,26,True),
 ('Peca127',-59,-46,56,31,47,7,False),
 ('Peca128',3,-46,56,31,47,7,False)
]
rows=[]
for n,x,y,w,d,z,h,display in parts:
    # app.js yaw rotates X,Z via [cos,+sin;-sin,cos]; in CAD XY this is -yaw.
    intended=[[0.,-1.,0.,2570-y*10],[1.,0.,0.,2220+x*10],[0.,0.,1.,z*10],[0.,0.,0.,1.]]
    dims=[val(n,k) for k in ['Length','Width','Height']]
    assert dims==[w*10,d*10,h*10],(n,dims)
    c=coverage(n)
    rows.append(dict(object=n,label=a['label'](n),source_links=c['mirror_links'],native_dimensions_mm=dims,
      saved_base_matrix=world(n),saved_base_bbox=bounds(world(n),dims),
      intended_base_matrix_from_existing_JS=intended,intended_base_bbox=bounds(intended,dims),
      intended_mirrored_matrix=mul(reflect,intended),intended_mirrored_bbox=bounds(mul(reflect,intended),dims),
      intended_visible_in_work_state=display,actual_links_visible=c['root_link_visible']))
tank=coverage('Peca358');tank['dims']=[val('Peca358',k) for k in ['Length','Width','Height']]
tank['mirrored_bbox']=bounds(tank['mirrored_world_matrix'],tank['dims'])
tank['link_properties']=[r for r in a['link_rows'] if r['source']=='Peca358']
g2=[r for r in a['equipment'] if r['object'].startswith('Peca15')]
cesto=json.loads(((Path(__file__).resolve().parent / '../Cesto_R15_2026-10-14/Montagem_R15.json').resolve()).read_text(encoding='utf-8'))
tank['current_tank_R15']=coverage(cesto['tank'])
report=dict(base_file=str(a['FILE']),new_factual_issues=[
  'Importador usa yaw com sinal oposto ao transformador da fonte JS em X,Z; sete peças Daiane fora da implantação diária já documentada',
  'Duas referências Daiane com opacity0 no estado work da fonte JS têm links visíveis',
  'Volume antigo do tanque, explicitamente ocultado na R15, tem vínculo espelhado visível'],
  sofa_source='Estudo_interativo/src/app.js:123-128 e249',
  import_source='Modelo_FreeCAD/gerar_modelo.py:202,215-218',
  documentary_placement='Escritorio/Ajuste_sofa_e_UltraComfort_R07.md: x local2..92 e y152..292; escritório global origemX255cm conforme app.js113',
  intended_daily_envelope_base_mm=[2570,1520,80,3470,2920,820],
  intended_daily_envelope_mirrored_mm=[3930,1520,80,4830,2920,820],
  sofa_parts=rows,historical_tank=tank,
  correction_status='Somente entrega de evidência e matrizes de restauração para revisão do responsável. Não altera CAD, não reprojeta sofá e não verifica colisões/movimento/fixação/mecanismo reais.')
((Path(__file__).resolve().parent / 'Sofa_tanque_evidencias.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(parts=len(rows),tank_link=tank['mirror_links'],current_tank=cesto['tank']),ensure_ascii=False))
