from pathlib import Path
import json
import FreeCAD as App
root=(Path(__file__).resolve().parent / '.').resolve()
doc=next(d for d in App.listDocuments().values() if d.FileName and Path(d.FileName).resolve()==(Path(__file__).resolve().parent / 'Guedala_Park_R12_Banheiro_Simples.FCStd').resolve())
assert doc.getObject('PortaEntradaBanheiroR12') is None,'Correção já aplicada; não duplicar controle de entrada'
old=[]
for name,z,label in [('Peca188',1110,'Luz frontal fixa inferior - proposta'),('Peca189',1910,'Luz frontal fixa superior - proposta')]:
 o=doc.getObject(name);old.append({'name':name,'placement':str(o.Placement),'dimensions_mm':[float(o.Length),float(o.Width),float(o.Height)]})
 o.Length=560;o.Width=7;o.Height=20;o.Placement.Base=App.Vector(4060,5130,z);o.Label=label
 if 'Status' not in o.PropertiesList:o.addProperty('App::PropertyString','Status')
 o.Status='Proposta geométrica: luz frontal fixa acima/abaixo, luminária/potência/fotometria e instalação pendentes. Sem aprovação de posição executiva.'
door=doc.getObject('Peca075');before=door.getGlobalPlacement();room=next(p for p in door.InList if p.Name.startswith('Ambiente_'))
g=doc.addObject('App::Part','PortaEntradaBanheiroR12');room.addObject(g);g.Label='Entrada banheiro - folha700 de referência, NÃO medida'
g.addProperty('App::PropertyAngle','Abertura');g.Abertura=90
g.addProperty('App::PropertyString','Status');g.Status='Estudo:90 reproduz porta original aberta,0 fecha volume ideal. Eixo/folha/maçaneta reais desconhecidos. Fechar entrada antes de abrir gabinete inferior; sem intertravamento físico.'
g.Placement=App.Placement(App.Vector(4540,4050,0),App.Rotation(App.Vector(0,0,1),0))
room.removeObject(door);g.addObject(door);door.Placement=g.getGlobalPlacement().inverse().multiply(before)
g.setExpression('Placement.Rotation.Angle','90 deg - min(90 deg,max(0 deg,Abertura))')
doc.recompute();doc.save()
report={'old_lights':old,'new_lights':{'dimensions_mm':[560,7,20],'x':4060,'y':5130,'lower_z':1110,'upper_z':1910},
 'entrance_control':g.Name,'original_open_pose_input_deg':90,'closed_study_input_deg':0,
 'entrance_reference_leaf_mm':[float(door.Length),float(door.Width),float(door.Height)],
 'scope':'Somente propostas geométricas. Sem medição de porta/maçaneta, fotometria ou instalação; não muda escolha de manter porta original. Luz lateral da imagem não era posição executiva aprovada.'}
((Path(__file__).resolve().parent / 'Luzes_entrada_R12.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
result=report
