from pathlib import Path
import ast,shutil
root=(Path(__file__).resolve().parent / '..').resolve();out=(Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Banheiro_R12_2026-10-14').resolve();out.mkdir(exist_ok=True)
source=((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Dobradicas_R10_2026-10-14/montar_dobradicas.py').resolve()).read_text(encoding='utf-8')
prefix=source[:source.index('for moduleName in')].replace('R10','R12')
prefix=prefix.replace("base=root.parent/'Portas_R09_2026-10-14'/'Guedala_Park_R09_Portas_Comuns.FCStd'", "base=root.parent/'Apoios_R11_2026-10-14'/'Guedala_Park_R11_Apoios_Simples.FCStd'")
prefix=prefix.replace('Guedala_Park_R12_Dobradicas_Comuns','Guedala_Park_R12_Banheiro_Simples')
prefix=prefix.replace("if dest.exists():dest=dest.with_stem(dest.stem+'_'+datetime.now().strftime('%Y%m%d_%H%M%S'))", "assert not dest.exists(),'A revisão já existe: preservar e iniciar nova pasta/revisão, sem reexecutar gerador pronto.'")
prefix=prefix.replace("doc.Label='Guedala Park - R12 - dobradiças comuns propostas, 6 pares'", "doc.Label='Guedala Park - R12 - banheiro portas comuns - proposta'")
setup='''
historical=[]
for moduleName in ['Modulo017','Modulo018']:
 module=doc.getObject(moduleName);width,height=float(module.Comprimento),float(module.Altura)
 isMirror=moduleName=='Modulo018';backingOffset=4 if isMirror else 0
 old=doc.getObject('Peca405' if isMirror else 'Peca398')
 history=doc.addObject('App::Part','HistoricoFrenteBanheiroR12');module.addObject(history);history.Label='Histórico oculto - frente volumétrica anterior'
 module.removeObject(old);history.addObject(old);old.Visibility=False;history.Visibility=False;historical.append(history)
 if isMirror:
  for name in ['Peca400','Peca401','Peca403','Peca404']:
   o=doc.getObject(name);o.setExpression('Placement.Base.y','24 mm')
   o.setExpression('Width',module.PlanilhaDimensoes.Name+'.Profundidade - '+('24 mm' if name in ['Peca400','Peca401'] else '24 mm - '+module.PlanilhaDimensoes.Name+'.Fundo'))
 module.Condicoes=('R12 proposta: duas folhas MDF18 + espelho4, frente22 dentro de profundidade150; vidro/fixação/carga/torneira/tubulação pendentes.' if isMirror else 'R12 proposta: duas portas comuns, sem divisória central; sifão/pontos/fundo e fixação/carga ainda pendentes. Envelope600x420x545 preservado.')
 leaves=[]
 for i in range(2):
  g=doc.addObject('App::Part','FolhaBanheiroR12');module.addObject(g);g.Label=('Espelhado' if isMirror else 'Gabinete')+' · '+('esquerda' if i==0 else 'direita')+' - proposta'
  g.addProperty('App::PropertyAngle','Abertura');g.addProperty('App::PropertyAngle','CursoEstudo');g.CursoEstudo=86
  g.addProperty('App::PropertyString','Movimento');g.Placement.Base=App.Vector(2 if i==0 else width-2,0,1)
  panel=doc.addObject('Part::Box','PainelBanheiroR12');g.addObject(panel);panel.Label='Painel18 comum · '+g.Label
  panel.Length=width/2-3;panel.Width=18;panel.Height=height-2
  panel.Placement.Base=App.Vector(0 if i==0 else -float(panel.Length),backingOffset,0)
  panel.ViewObject.ShapeColor=(.77,.64,.46) if isMirror else old.ViewObject.ShapeColor
  panel.addProperty('App::PropertyString','Status');panel.Status='Proposta, sem liberação de corte/furação/compra'
  leaves.append(g)
 for index,g in enumerate(leaves):
'''
body=source[source.index('  left=index==0;'):source.index('doc.recompute();doc.save()')].replace('R10','R12')
body=body.replace('myPlate=57;', 'myPlate=57+backingOffset;')
body=body.replace("App.Vector(22.5 if left else -22.5,18,level-1)", "App.Vector(22.5 if left else -22.5,18+backingOffset,level-1)")
body=body.replace("levels=[80,height-80]", "levels=([80,height/2,height-80] if isMirror else [80,height-80]) # Scenario of composite mirrored front requires three common hinges.")
body=body.replace("'original_panel_dimensions_R09_mm':originalDims", "'panel_dimensions_before_canecos_mm':originalDims")
body=body.replace("'front_source_dimensions':[originalDims[0]-1,originalDims[1],originalDims[2]]", "'front_source_dimensions':[width/2-3,18,height-2],'backing_front_offset_mm':backingOffset")
body=body.replace("'plate_hole_row_y':57", "'plate_hole_row_y':myPlate")
body=body.replace("  g.Movimento='Quatro barras71B3550; junta externa2, K5/calço0/recobrimento16 e regulagem comum0.5 propostos. Estudo86, batente70T3553/fixação/carga ainda a conferir.'", "  g.Movimento='R12 proposta: quatro barras71B3550/K5/calço0; estudo86 não é batente físico. Peso/material/fixação/hidráulica pendentes.'")
body=body.replace("  doc.recompute()\n  for o in tools+[panel,fused]", "  if isMirror:\n   mirror=doc.addObject('Part::Box','EspelhoAplicadoR12');g.addObject(mirror);mirror.Label='Espelho4 sobre painel comum - proposta'\n   mirror.Length=width/2-3;mirror.Width=4;mirror.Height=height-2;mirror.Placement.Base.x=0 if left else -float(mirror.Length)\n   mirror.ViewObject.ShapeColor=(.72,.83,.86);report[-1]['mirror']=mirror.Name;mirror.addProperty('App::PropertyString','Status');mirror.Status='Proposta: vidro/adesivo/retenção/arestas/carga devem ser definidos com fornecedor'\n  doc.recompute()\n  for o in tools+[panel,fused]")
tail='''
doc.recompute()
for o in historical:o.Visibility=False
doc.save()
data={'file':str(dest),'doors':report,'hardware_count':len(hardware),'hinge_count':sum(len(r['hinges']) for r in report),
 'invalid_hardware':[o.Name for o in hardware if not o.Shape.isValid()],'invalid_fronts':[o.Name for o in fronts if not o.Shape.isValid()],
 'scope':'R12 proposta: gabinete duas portas comuns, espelhado duas folhas madeira18 + espelho4 dentro de150. Não libera corte/vidro/adesivo/carga/fixação.'}
(root/'Montagem_R12.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
result=json.dumps({k:v for k,v in data.items() if k!='doors'},ensure_ascii=False)
'''
code=prefix+setup+body+tail;ast.parse(code);((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Banheiro_R12_2026-10-14/montar_banheiro.py').resolve()).write_text(code,encoding='utf-8')
shutil.copy2((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Dobradicas_R10_2026-10-14/Eixos_71B3550.json').resolve(),(Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Banheiro_R12_2026-10-14/Eixos_71B3550.json').resolve())
print((Path(__file__).resolve().parent / '../02_Revisoes_e_estudos/Banheiro_R12_2026-10-14/montar_banheiro.py').resolve())
