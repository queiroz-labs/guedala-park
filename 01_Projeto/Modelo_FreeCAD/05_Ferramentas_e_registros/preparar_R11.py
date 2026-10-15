from pathlib import Path
import ast, shutil
root=(Path(__file__).resolve().parent / '..').resolve()
out=(Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Apoios_R11_2026-10-14').resolve()
out.mkdir(exist_ok=True)
source=((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Dobradicas_R10_2026-10-14/montar_dobradicas.py').resolve()).read_text(encoding='utf-8')
prefix=source[:source.index("for moduleName in")].replace('R10','R11')
prefix=prefix.replace("base=root.parent/'Portas_R09_2026-10-14'/'Guedala_Park_R09_Portas_Comuns.FCStd'", "base=root.parent/'Dobradicas_R10_2026-10-14'/'Guedala_Park_R10_Dobradicas_Comuns.FCStd'")
prefix=prefix.replace('Guedala_Park_R11_Dobradicas_Comuns','Guedala_Park_R11_Apoios_Simples')
prefix=prefix.replace("doc.Label='Guedala Park - R11 - dobradiças comuns propostas, 6 pares'", "doc.Label='Guedala Park - R11 - apoios simples escritório/cabeceira - proposta'")
prefix=prefix.replace("sheet.Label='R11 - quatro barras dos pares comuns'", "sheet.Label='R11 - quatro barras escritório/cabeceira'")
setup='''
supports=[]; configurations=[]; old_office=[]
def support(module,x,label):
 o=doc.addObject('Part::Box','ApoioComumR11');module.addObject(o);o.Label=label+' - proposta18'
 o.Length=18;o.Width=float(module.Profundidade)-38;o.Height=float(module.Altura)-36
 o.Placement.Base=App.Vector(x,20,18);o.ViewObject.ShapeColor=(.86,.86,.81)
 o.addProperty('App::PropertyString','Status');o.Status='Proposta: fixação, material/carga e tolerâncias pendentes'
 supports.append(o);return o
office=doc.getObject('Modulo016')
office.Condicoes='Envelope2000x350x550 preservado. Proposta R11 quatro portas comuns, três apoios18; quantidade/divisões/fixação/carga não liberadas.'
history=doc.addObject('App::Part','HistoricoFrentesEscritorioR11');office.addObject(history);history.Label='Histórico oculto - cinco folhas ilustrativas anteriores'
for g in list(office.Group):
 if hasattr(g,'Abertura'):
  g.setExpression('Abertura','0 deg');office.removeObject(g);history.addObject(g);g.Visibility=False;old_office.append(g.Name)
history.Visibility=False
for i in range(1,4):support(office,500*i,'Apoio interno escritório '+str(i))
for i in range(4):
 g=doc.addObject('App::Part','FolhaEscritorioR11');office.addObject(g);g.Label='Escritório porta '+str(i+1)+' - proposta'
 g.addProperty('App::PropertyAngle','Abertura');g.addProperty('App::PropertyAngle','CursoEstudo');g.CursoEstudo=86
 g.addProperty('App::PropertyString','Movimento');g.Placement.Base=App.Vector(2+i*500,0,1)
 p=doc.addObject('Part::Box','PainelEscritorioR11');g.addObject(p);p.Label='Frente escritório '+str(i+1)+' - proposta'
 p.Length=496;p.Width=18;p.Height=548;p.ViewObject.ShapeColor=(.86,.86,.81)
 configurations.append((office,g,2+i*500,496))
head=doc.getObject('Modulo003')
head.Condicoes='Envelope1800x250x308 preservado. Três folhas comuns R11 com dois apoios18; vizinha/canto R04 e faixa25 recuada40 preservados. Proposta, sem fabricação.'
corner=doc.getObject('Modulo001');corner.Label='Canto integrado em L - R04 simples - proposta'
corner.Condicoes='Proposta R04: duas portas independentes271x306, faixas fixas142/124, vizinha e faixa25 recuada40. Fixação/carga/batente/cotas executivas pendentes.'
for i,n in enumerate(['Folha','Folha001','Folha002']):
 g=doc.getObject(n);g.setExpression('Abertura',None);g.Abertura=0
 x=2+i*443.75
 if i:support(head,x-2,'Apoio interno cabeceira '+str(i))
 configurations.append((head,g,x,440.75))
doc.recompute()
'''
body=source[source.index("  left=index==0;"):source.index('doc.recompute();doc.save()')]
body='\n'.join(line[2:] if line.startswith('  ') else line for line in body.splitlines())
body=body.replace("left=index==0;letter=", "left=True;letter=")
body=body.replace("mx=18 if left else width-18;myPlate=57;depthAdjustment=.5;myHinge=myPlate-depthAdjustment", "mx=initialX+16;myPlate=57;depthAdjustment=.5;myHinge=myPlate-depthAdjustment")
body=body.replace("initialX=2 if left else width-2;initialY=0", "initialY=0")
body=body.replace("  panel.setExpression('Length',module.PlanilhaDimensoes.Name+'.Comprimento/2 - '+control.Name+'.JuntaCentralProposta/2 - '+control.Name+'.JuntaExternaProposta')", "  panel.setExpression('Length',None);panel.Length=frontWidth")
# The block was dedented above.
body=body.replace("panel.setExpression('Length',module.PlanilhaDimensoes.Name+'.Comprimento/2 - '+control.Name+'.JuntaCentralProposta/2 - '+control.Name+'.JuntaExternaProposta')", "panel.setExpression('Length',None);panel.Length=frontWidth")
body=body.replace('R10','R11')
body=body.replace("control.addProperty('App::PropertyLength','JuntaExternaProposta');control.JuntaExternaProposta=2\ncontrol.addProperty('App::PropertyLength','JuntaCentralProposta');control.JuntaCentralProposta=2", "leftGap=2 if len(report) in [0,4] else (4 if module.Name=='Modulo016' else 3)\nrightGap=2 if len(report) in [3,6] else (4 if module.Name=='Modulo016' else 3)\nfor name,value in [('JuntaEsquerdaProposta',leftGap),('JuntaDireitaProposta',rightGap)]:\n control.addProperty('App::PropertyLength',name);setattr(control,name,value);control.setEditorMode(name,1)")
body=body.replace("g.setExpression('Abertura',control.Name+'.Abertura');g.setExpression('CursoEstudo',control.Name+'.CursoEstudo')", "\nif 'CursoEstudo' not in g.PropertiesList:g.addProperty('App::PropertyAngle','CursoEstudo')\ng.setExpression('Abertura',control.Name+'.Abertura');g.setExpression('CursoEstudo',control.Name+'.CursoEstudo')")
body=body.replace("control.Label='Abrir '+module.Label+' · '+('esquerda' if left else 'direita')", "control.Label='Abrir '+module.Label+' · '+g.Label")
body=body.replace("'front_source_dimensions':[originalDims[0]-1,originalDims[1],originalDims[2]]", "'front_source_dimensions':[frontWidth,originalDims[1],originalDims[2]],'hinge_support_inner_x_mm':mx,'closed_x_mm':initialX")
body=body.replace("'original_panel_dimensions_R09_mm':originalDims", "'panel_dimensions_before_canecos_mm':originalDims")
body=body.replace("'external_joint_mm':2", "'left_joint_mm':leftGap,'right_joint_mm':rightGap")
body=body.replace("g.Movimento='Quatro barras71B3550; junta externa2, K5/calço0/recobrimento16 e regulagem comum0.5 propostos. Estudo86, batente70T3553/fixação/carga ainda a conferir.'", "g.Movimento='Proposta R11: 71B3550/calço0/K5/recobrimento16; regulagem0.5; limites86 não comprovam batente. Após mudar dimensões, revisar apoios/canecos e montagem.'")
loop="for module,g,initialX,frontWidth in configurations:\n width,height=float(module.Comprimento),float(module.Altura)\n"+'\n'.join(' '+line if line else '' for line in body.splitlines())
tail='''
doc.recompute()
history.Visibility=False
doc.save()
data={'file':str(dest),'doors':report,'hardware_count':len(hardware),'hinge_count':sum(len(r['hinges']) for r in report),
 'supports':[{'name':o.Name,'label':o.Label,'dimensions_mm':[float(o.Length),float(o.Width),float(o.Height)],'position_mm':list(o.Placement.Base)} for o in supports],
 'historical_office_leaves':old_office,
 'invalid_hardware':[o.Name for o in hardware if not o.Shape.isValid()],'invalid_fronts':[o.Name for o in fronts if not o.Shape.isValid()],
 'scope':'R11 proposta: quatro folhas escritório, três cabeceira existentes com apoios, vizinha/canto R04 preservados. Mesma dobradiça comum. Não libera fabricação/carga/fixação.'}
(root/'Montagem_R11.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in data.items() if k!='doors'},ensure_ascii=False)
'''
code=prefix+setup+loop+tail
ast.parse(code)
((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Apoios_R11_2026-10-14/montar_apoios.py').resolve()).write_text(code,encoding='utf-8')
shutil.copy2((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Dobradicas_R10_2026-10-14/Eixos_71B3550.json').resolve(),(Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Apoios_R11_2026-10-14/Eixos_71B3550.json').resolve())
print((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Apoios_R11_2026-10-14/montar_apoios.py').resolve())
