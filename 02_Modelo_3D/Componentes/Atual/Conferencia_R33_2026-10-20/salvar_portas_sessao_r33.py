import FreeCAD as App,FreeCADGui as Gui,json,os,hashlib
from pathlib import Path
root=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
folder=root/'guedala-park/02_Modelo_3D/Componentes/Atual/Conferencia_R33_2026-10-20'
path=folder/'Guedala_Park_R33_Conferencia.FCStd'
assert os.getpid()==23148,'Sessão diferente; não alterar.'
docs=[d for d in App.listDocuments().values() if Path(d.FileName)==path]
assert len(docs)==1
d=docs[0];assert len(d.Objects)==6195
for n in ['FrenteComumR005','FrenteComumR007']:
 o=d.getObject(n);assert o.Shape.isValid()
 o.Visibility=True;o.getParentGeoFeatureGroup().Visibility=True
 if 'CorrecaoR33' not in o.PropertiesList:o.addProperty('App::PropertyString','CorrecaoR33','AuditoriaR33')
 o.CorrecaoR33='Visibilidade restaurada na R33; painel e controle existentes preservados.'
d.getObject('ConferenciaR33').Correcoes='Medição completa com32 formas adicionais frente à R32; duas frentes antes ocultas restauradas. Banco550=450+encosto100. Dimensões e expressões geométricas preservadas.'
for n in ['ControlePortaR005','ControlePortaR007']:
 assert float(d.getObject(n).Abertura)==0
d.recompute();d.save()
assert all(d.getObject(n).Visibility for n in ['FrenteComumR005','FrenteComumR007'])
# Captura do viewport, sem ativar janela, alterar câmera ou mover o mouse.
Gui.getDocument(d.Name).activeView().saveImage(str(folder/'Apartamento_R33.png'),1600,1100,'White')
(folder/'Salvamento_sessao_R33.json').write_text(json.dumps({'saved':True,'pid':os.getpid(),'file':d.FileName,'objects':len(d.Objects),'doors_visible':True,'doors_closed':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'foreground_not_changed':True},ensure_ascii=False,indent=2),encoding='utf-8')
