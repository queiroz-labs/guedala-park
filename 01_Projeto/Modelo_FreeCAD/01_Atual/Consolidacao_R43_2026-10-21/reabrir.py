import FreeCAD as A, FreeCADGui as G, pathlib, json,hashlib
P=pathlib.Path(__file__).resolve().parent
f=P/'Guedala_Park_R43_Consolidado.FCStd'
d=A.getDocument('Guedala_Park_R43_Consolidado');d.save();A.closeDocument(d.Name)
(P/'Reabertura_em_curso.txt').write_text('Arquivo fechado. Abrindo R43 para verificar persistência.',encoding='utf-8')
d=A.openDocument(str(f));A.setActiveDocument(d.Name)
c=d.BC43_Controle;c.CursoEsquerda=268;c.CursoDireita=233;d.recompute()
r={'reopened':True,'objects':len(d.Objects),'front_x_max_travel':d.BC43_FolhaEsquerda.Placement.Base.x,'rear_x_max_travel':d.BC43_FolhaDireita.Placement.Base.x,'back_original_visible':d.Peca396.ViewObject.Visibility,'hypothetical_back_hidden':not d.BC43_Fundo.ViewObject.Visibility,'invalid_new_shapes':[o.Name for o in d.Objects if o.Name.startswith('BC43_') and hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]}
c.CursoEsquerda=0;c.CursoDireita=0;d.recompute();d.save()
r['closed_positions']=[d.BC43_FolhaEsquerda.Placement.Base.x,d.BC43_FolhaDireita.Placement.Base.x]
r['berlin']=[{'name':o.Name,'null':o.Shape.isNull(),'valid':o.Shape.isValid(),'visible':o.ViewObject.Visibility,'colors':len(o.ViewObject.DiffuseColor)} for o in d.Objects if not hasattr(o,'Group') and o.Name.startswith(('Fechada_','Aberta_')) and hasattr(o,'Shape')]
r['bank_lids']=[{'name':d.getObject('BancoR43_Painel'+str(i)).Name,'valid':d.getObject('BancoR43_Painel'+str(i)).Shape.isValid(),'angle':getattr(d.BancoR43_Controle,'Abertura'+str(i))} for i in [1,2]]
source=P.parent/'Consolidacao_R42_2026-10-22/Guedala_Park_R42_Consolidado.FCStd'
r['r42_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
r['r43_sha256']=hashlib.sha256(f.read_bytes()).hexdigest()
(P/'Reabertura_R43.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
G.activeDocument().activeView().setCamera('#Inventor V2.1 ascii\nOrthographicCamera { position 1000 4650 8000 orientation 0 0 1 0 nearDistance 1 farDistance 20000 focalDistance 7500 height 3000 }');G.updateGui()
