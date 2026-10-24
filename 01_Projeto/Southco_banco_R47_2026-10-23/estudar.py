import FreeCAD as A, FreeCADGui as G, Part, pathlib, json, math, hashlib
p=pathlib.Path(__file__).parent
s=A.getDocument('Guedala_Park_R45_EM_REVISAO') or A.getDocument('Guedala_Park_R44_Consolidado')
assert s
def w(n):
 o=s.getObject(n);q=o.Shape.copy();q.Placement=o.getGlobalPlacement();return q
def box(x,y,z,dx,dy,dz):return Part.makeBox(dx,dy,dz,A.Vector(x,y,z))
d=A.newDocument('Southco_Banco_R47_ESTUDO');d.Label='Southco banco — fixação proposta, ferragem NÃO validada'
def group(n):return d.addObject('App::DocumentObjectGroup',n)
ctx=group('Contexto');fix=group('Fixacao_proposta');env=group('Envelopes_nao_CAD_Southco');cuts=group('Alivios_somente_corpo');cols=group('Conflitos_almofadas')
def add(g,n,q,c=(.7,.65,.55),trans=0):
 o=d.addObject('PartDesign::Feature',n);o.Shape=q;g.addObject(o);o.ViewObject.ShapeColor=c;o.ViewObject.Transparency=trans;return o
names=['Peca407','Peca408','PecaBancoR16','Peca406AtualR31','PecaBancoR003','PecaBancoR004','PecaBancoR005','PecaBancoR007AtualR31','Peca421','BancoR43_Painel1','BancoR43_Painel2','BancoR43_Almofada1','BancoR43_Almofada2']
for n in names:add(ctx,n,w(n),trans=75 if 'Almofada' in n or n=='Peca421' else 30)
inventory=json.loads((p.parents[2]/'outputs/estudo-dimensional-2026-10-23/banco_visivel.json').read_text(encoding='utf8'))
contents=[r['name'] for r in inventory if 'gabarito' in r['label'] or r['name'] in ['PecaBancoR036','PecaBancoR037']]
for n in contents:add(ctx,n,w(n),(.25,.65,.5),50)
centers=[(1,3890),(1,4580),(2,4870),(2,5400)]
results=[];collision=[];plates=[]
for i,(idx,y) in enumerate(centers):
 # Dimensional proposal: actual hinge offset still unknown; shown with assumed e=10.
 lower=box(110,y-40,390,26,80,10)
 for yy in [y-23,y+23]:lower=lower.cut(Part.makeCylinder(2.5,10,A.Vector(125,yy,390)))
 add(fix,'Contraplatina_'+str(i+1),lower,(.3,.4,.5));plates.append((idx,lower))
 pocket=box(109.5,y-40.5,389.5,27,81,10.5)
 o=add(cuts,'Rebaixo_corpo_'+str(i+1),pocket,(.95,.65,.1),70);o.Visibility=False
 # Body-only post and recessed receiving plate; layout not a production drawing.
 post=box(94,y-40,260,6,80,130).fuse(box(84,y-40,390,16,80,6)).fuse(box(84,y-40,396,6,80,84))
 receive=box(112,y-40,270,6,80,100)
 for yy in [y-23,y+23]:
  for zz in [280,360]:
   post=post.cut(Part.makeCylinder(3.35,40,A.Vector(80,yy,zz),A.Vector(1,0,0)))
   receive=receive.cut(Part.makeCylinder(2.5,6,A.Vector(112,yy,zz),A.Vector(1,0,0)))
 add(fix,'Suporte_recuado_'+str(i+1),post,(.35,.4,.45));add(fix,'Placa_receptora_'+str(i+1),receive,(.4,.45,.5))
 mobile=box(102,y-40,420,32.75,80,4.5)
 add(env,'Aba_movel_ENVELOPE_'+str(i+1),mobile,(.1,.2,.8),25)
 fixed=box(90,y-40,440,4.5,80,30)
 add(env,'Aba_fixa_ENVELOPE_'+str(i+1),fixed,(.1,.2,.8),25)
 for yy in [y-23,y+23]:
  head=Part.makeCylinder(5,7.6,A.Vector(125,yy,424.5))
  add(env,'Cabeca_arruela_HIPOTESE_'+str(i+1),head,(.1,.2,.8))
 hit=mobile.common(w('BancoR43_Almofada'+str(idx)))
 add(cols,'Colisao_almofada_'+str(i+1),hit,(1.0,.1,.1))
 collision.append({'hinge':i+1,'cushion':idx,'volume_min_aba_mm3':hit.Volume,'altura_min_interferencia_mm':4.5,'cabeca_arruela_hipotese_mm':7.6})
 for n in contents:
  for kind,q in [('contraplatina',lower),('suporte',post),('receptora',receive)]:
   if q.BoundBox.intersect(w(n).BoundBox):
    v=q.common(w(n)).Volume
    if v>.001:results.append({'fixacao':i+1,'tipo':kind,'conteudo':n,'volume':v})
 # All material removal is in body support, not lids; exact residual support still needs design.
 bodyhits=[]
 for n in ['Peca408']+['Ref_Sarrafo_tras'+str(j)+'R31' for j in range(4)]:
  v=pocket.common(w(n)).Volume
  if v>.001:bodyhits.append({'objeto':n,'volume_rebaixo_mm3':v})
 collision[-1]['rebaixos_corpo']=bodyhits
rot=[]
for idx in [1,2]:
 q0=w('BancoR43_Painel'+str(idx))
 groupmoving=Part.makeCompound([q0]+[q for k,q in plates if k==idx])
 for e in [0,5,10,15,20.3]:
  hits=[]
  for ang in range(91):
   q=groupmoving.copy();q.rotate(A.Vector(100,0,420+e),A.Vector(0,-1,0),ang)
   for n in contents+['PecaBancoR007AtualR31']:
    sh=w(n)
    if q.BoundBox.intersect(sh.BoundBox):
     v=q.common(sh).Volume
     if v>.001:hits.append([ang,n,v])
  rot.append({'tampa':idx,'eixo_hipotetico':[100,420+e],'poses':91,'colisoes_conteudo_prateleira':hits})
calc=[]
for idx,m,t in [(1,7.830144,19.8),(2,6.6528,17.2)]:
 r=math.hypot(.226,.0303);moment=m*9.80665*r
 # Budget only: up to 0.5kg moving metal entirely within 60mm of axis.
 met=.5*9.80665*.060
 calc.append({'tampa':idx,'massa_painel_cenario900_kg':m,'braco_max_faixa_m':r,'momento_painel_Nm':moment,'torque_min_par_Nm':t,'orcamento_metal_movel_kg':.5,'limite_raio_metal_m':.060,'momento_metal_orcado_Nm':met,'margem_Nm':t-moment-met,'acabamento_distribuido_adicional_limite_teorico_kg':(t-moment-met)/(9.80665*r)})
meta=d.addObject('App::FeaturePython','LeiaMe')
for k,v in {'Escopo':'Estudo de fixação; não é CAD de ferragem Southco. Abas são envelopes. e=10mm na vista é hipótese, não cota do fabricante.', 'Preservacao':'Dimensões/posição tampas e conteúdo mantidas. Fixação exige furos normais nas tampas; nenhuma usinagem de rebaixo nelas. Rebaixos são só no corpo.', 'Pendencias':'Offset real do eixo, sentido F0/R0, almofada, batente, painel/ligação e tolerâncias. Não fabricar nem comprar com base neste arquivo.'}.items():
 meta.addProperty('App::PropertyString',k);setattr(meta,k,v)
d.recompute();G.activeDocument().activeView().viewAxonometric();G.activeDocument().activeView().fitAll();d.saveAs(str(p/'Southco_Fixacao_ESTUDO.FCStd'))
data={'posicoes_y_mm':centers,'fixacao_conteudo_colisoes':results,'almofadas_rebaixos':collision,'giros_hipoteticos':rot,'capacidade':calc,'contraplatina':{'dim_mm':[26,80,10],'massa_2_por_tampa_kg':2*26*80*10*7.85e-6,'centros_furos_x':125,'centros_furos_y_rel':[-23,23],'furos_roscados_M6_nao_desenho_exec':True},'limites':'Giros testam tampas+contraplatinas contra conteúdo/prateleira; não ensaiam ferragem real, encosto modificado, parafusos, batente nem dinâmica. Offset eixo não cotado pelo fabricante. Folga de bolsão0,5 é proposta.'}
(p/'Resultados.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
result={'documento':d.Name,'fixacao_conteudo_hits':len(results),'poses':sum(r['poses'] for r in rot),'giros_com_colisao':sum(bool(r['colisoes_conteudo_prateleira']) for r in rot),'almofada_interferencias':len(collision)}
