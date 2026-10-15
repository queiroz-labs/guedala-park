from pathlib import Path
import json,math
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve();p=(Path(__file__).resolve().parent / 'Guedala_Park_R16_Banco_Simples.FCStd').resolve();data=json.loads(((Path(__file__).resolve().parent / 'Montagem_R16.json').resolve()).read_text(encoding='utf-8'))
assert not ((Path(__file__).resolve().parent / 'Reabertura_R16.json').resolve()).exists(),'Reabertura já conferida'
d=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==p)
d.getObject('Ambiente_sala').Visibility=True;meta=d.getObject('Documentacao');meta.Revisao='R16 - banco/apoios/acessos, proposta; R15 e anteriores incorporadas'
meta.Cinematica='Banco R16 giros ideais/almofadas e conteúdo-gabarito. Ferragens/retenção/estrutura/carga reais pendentes. Cesto/correr/rodas são gabaritos; MOVENTO estático; portas comuns pelos eixos STEP.'
d.recompute();d.save();assert d.isSaved() and p.exists() and p.stat().st_size>100000
App.closeDocument(d.Name);d=App.openDocument(str(p));checks=[]
for row in data['lids']:
 c=d.getObject(row['control']);angle=90 if row['separate_cushion'] else 45
 if row['separate_cushion']:c.ElevarAlmofada=50;c.DeslocamentoAlmofada=abs(row['parking_source_v']-row['pad_v'])
 c.Abertura=angle;d.recompute();driver=d.getObject(row['driver']);vec=driver.Placement.Rotation.multVec(App.Vector(0,-448,0));expected=App.Vector(0,-448*math.cos(math.radians(angle)),448*math.sin(math.radians(angle)))
 checks.append({'sector':row['id'],'control':c.Name,'angle_deg':float(c.Abertura),'rotation_error_mm':(vec-expected).Length,'lid_valid':d.getObject(row['lid']).Shape.isValid(),'lid_state':list(d.getObject(row['lid']).State),'pad_global_placement':str(d.getObject(row['cushion']).getGlobalPlacement()),'pad_valid':d.getObject(row['cushion']).Shape.isValid()})
 c.Abertura=0
 if row['separate_cushion']:c.ElevarAlmofada=0;c.DeslocamentoAlmofada=0
d.recompute();d.save();out={'checks':checks,'final_controls_zero':all(float(d.getObject(r['control']).Abertura)==0 and (not r['separate_cushion'] or float(d.getObject(r['control']).ElevarAlmofada)==0 and float(d.getObject(r['control']).DeslocamentoAlmofada)==0) for r in data['lids']),'saved':d.isSaved(),'file':str(p)}
((Path(__file__).resolve().parent / 'Reabertura_R16.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');result=out
