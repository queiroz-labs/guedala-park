import FreeCAD as A, Part, json, pathlib, hashlib, math
from xml.sax.saxutils import escape
root=pathlib.Path(__file__).parent
src=root.parent.parent/'Modelo_FreeCAD/01_Atual/Cesto_R41_2026-10-20/Guedala_Park_R41_Estudo_Frente500.FCStd'
digest=lambda:hashlib.sha256(src.read_bytes()).hexdigest()
before=digest(); source=A.openDocument(str(src)); study=A.newDocument('Berlin_Estudo')
def world(o):
 s=o.Shape.copy();s.Placement=o.getGlobalPlacement();return s
def bb(s):
 b=s.BoundBox;return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def add(name,label,s,group=None):
 o=study.addObject('PartDesign::Feature',name);o.Label=label;o.Shape=s
 o.addProperty('App::PropertyString','StatusEstudo');o.StatusEstudo='Estudo dimensional; nao e medida de campo nem desenho de fabricacao'
 if group:group.addObject(o)
 return o
context={}
context['sofa']=Part.makeCompound([world(source.getObject('Peca%03d'%i)) for i in range(77,84)])
context['geladeira']=world(source.getObject('Peca138'))
context['banco']=world(source.getObject('Modulo019'))
context['encosto']=world(source.getObject('Peca421'))
cg=study.addObject('App::DocumentObjectGroup','Contexto_R41')
for k,s in context.items():add(k,k+' - geometria copiada da R41',s,cg)
chairsrc=world(source.getObject('CadeiraLinaR30_1'))
def chair(target,angle):
 s=chairsrc.copy();s.rotate(A.Vector(),A.Vector(0,0,1),angle);b=s.BoundBox;s.translate(A.Vector(target[0]-b.XMin,target[1]-b.YMin,-b.ZMin));return s
def face(x,y,w,l,z):return Part.Face(Part.makePolygon([A.Vector(x,y,z),A.Vector(x+w,y,z),A.Vector(x+w,y+l,z),A.Vector(x,y+l,z),A.Vector(x,y,z)]))
results=[]; scenarios=[]
for idx,(name,L,alternative) in enumerate([('Fechada_110',1100,False),('Aberta_170',1700,False),('Aberta_cadeira_lateral',1700,True)]):
 g=study.addObject('App::DocumentObjectGroup',name);lo=4650-L/2;hi=4650+L/2;cx=875;x=475
 top=add(name+'Tampo','Berlin - superficie superior z790; espessura desconhecida',face(x,lo,800,L,790),g)
 # Only a floor footprint is drawn: pedestal height/profile and axis orientation are not confirmed.
 add(name+'Sapata','Sapata - projecao hipotetica 330x500; orientacao por confirmar',face(cx-165,4400,330,500,1),g)
 targets=[('Ponta_sofa',(cx-220,lo-210),-90),('Ponta_cozinha',(cx-220,hi-260),90),('Lateral',(1275-260,4430),0)]
 if alternative:targets=[('Lateral_sofa',(1015,3863.333333),0),('Lateral_centro',(1015,4430),0),('Lateral_cozinha',(1015,4996.666667),0)]
 chairs=[]; checks=[]
 for label,target,ang in targets:
  s=chair(target,ang);o=add(name+label,label+' - gabarito Lina R41, projecao externa hipotetica 210mm',s,g);chairs.append((label,s))
  for key,obs in context.items():
   b=s.BoundBox;c=obs.BoundBox;ovx=min(b.XMax,c.XMax)-max(b.XMin,c.XMin);ovy=min(b.YMax,c.YMax)-max(b.YMin,c.YMin)
   vol=s.common(obs).Volume if ovx>0 and ovy>0 else 0
   checks.append({'cadeira':label,'obstaculo':key,'overlap_bbox_xy_mm':[round(max(0,ovx),2),round(max(0,ovy),2)],'intersecao_formas_mm3':round(vol,2),'distancia_formas_mm':round(s.distToShape(obs)[0],2)})
 results.append({'cenario':name,'tampo_bbox_mm':bb(top.Shape),'cadeiras':{k:bb(s) for k,s in chairs},'checks':checks,'dist_tampo_IB6_mm':6152.5-hi,'dist_envelope_cadeira_IB6_mm':6152.5-max(ss.BoundBox.YMax for _,ss in chairs),'dist_tampo_sofa_mm':lo-3650,'folga_envelope_cadeira_sofa_mm':lo-210-3650 if not alternative else None})
 scenarios.append((name,L,lo,hi,chairs))
study.addObject('App::DocumentObjectGroup','LeiaMe').addProperty('App::PropertyString','Premissas')
study.LeiaMe.Premissas='Copia PARCIAL de contexto R41. Berlin e superficie/envelope, nao modelo do fabricante. Cadeiras sao gabaritos R41. Projecao210mm e hipotese, nao encaixe confirmado. Sapata orientada330transversalx500longitudinal apenas como hipotese. Sem tampo inferior/esteira e sem pessoas/portas abertas. Aberta: tres cadeiras na lateral conforme pedido; encaixe fisico pendente. Todos os comprimentos em mm.'
study.recompute();out=root/'Berlin_estudo_dimensional.FCStd';study.saveAs(str(out));A.closeDocument(study.Name)
check=A.openDocument(str(out));valid=[o.Name for o in check.Objects if hasattr(o,'Shape') and not o.Shape.isNull() and not o.Shape.isValid()]
after=digest()
report={'fonte':str(src),'sha256_antes':before,'sha256_depois':after,'fonte_preservada':before==after,'freecad_version':A.Version(),'contexto_bboxes_mm':{k:bb(s) for k,s in context.items()},'premissas':{'insercao_cadeira_mm':260,'projecao_cadeira_mm':210,'centro_mesa_mm':[875,4650],'largura_berlin_mm':800,'altura_superficie_mm':790,'altura_banco_mm':470,'sapata_orientacao':'hipotese330transversal500longitudinal','campo':'nao medido','alternativa':'tres laterais conforme pedido; sem verificacao fisica'},'cenarios':results,'verificacao_reabertura':{'objetos':len(check.Objects),'formas_invalidas':valid}}
(root/'Conferencia_Berlin.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
# SVG plan is generated directly from bounding boxes extracted by the FreeCAD kernel.
W,H=1500,1030;svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">','<rect width="100%" height="100%" fill="#f6f4ef"/>','<style>text{font-family:Arial,sans-serif;fill:#253039}.title{font-size:28px;font-weight:bold}.sub{font-size:16px}.lab{font-size:13px}</style>', '<text x="35" y="44" class="title">Berlin no apartamento — conferência dimensional no FreeCAD</text>', '<text x="35" y="72" class="sub">Contexto extraído da R41 · medidas de projeto · cadeiras com projeção hipotética de 21 cm</text>']
for idx,(name,L,lo,hi,chairs) in enumerate(scenarios):
 ox=35+idx*490;oy=130;scale=.145
 def xy(x,y):return ox+25+x*scale,oy+(7000-y)*scale
 def rect(b,color,stroke='#56616a',alpha='1'):
  px,py=xy(b[0],b[4]);w=(b[3]-b[0])*scale;h=(b[4]-b[1])*scale
  svg.append(f'<rect x="{px:.2f}" y="{py:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{color}" fill-opacity="{alpha}" stroke="{stroke}" stroke-width="1.5"/>')
 svg.append(f'<text x="{ox}" y="112" class="sub">{["1. Fechada 110 × 80 cm","2. Aberta 170 × 80 cm","3. Aberta: três cadeiras na lateral"][idx]}</text>')
 for k,s in context.items():rect(bb(s),{'sofa':'#c7c5be','geladeira':'#a7b6bf','banco':'#c99e72','encosto':'#9b7654'}[k])
 rect([475,lo,0,1275,hi,790],'#7db2a4',alpha='.40');rect([710,4400,0,1040,4900,1],'#567b70',alpha='.50')
 for k,s in chairs:rect(bb(s),'#e9b66c',alpha='.65')
 for label,x0,y0 in [('SOFÁ',200,2800),('BANCO',80,4600),('IB6',1030,6520)]:
  px,py=xy(x0,y0);svg.append(f'<text x="{px}" y="{py}" class="lab">{label}</text>')
 r=results[idx]
 lines=[f'Tampo–IB6: {r["dist_tampo_IB6_mm"]/10:.2f} cm',f'Cadeira–IB6: {r["dist_envelope_cadeira_IB6_mm"]/10:.2f} cm', 'Não é passagem livre com pessoa sentada.']
 if idx==0:lines+=['Cadeira–sofá: 24 cm nominais.','As duas pontas cabem nos envelopes.']
 elif idx==1:lines+=['Cadeira sobrepõe o sofá em 6 cm.','Este arranjo não passa no ensaio de envelopes.']
 else:lines+=['Sem sobreposição cadeira–sofá neste cenário.','12,67 cm entre cadeiras; sem pessoas no ensaio.']
 for n,line in enumerate(lines):svg.append(f'<text x="{ox}" y="{900+n*21}" class="lab">{escape(line)}</text>')
svg+=['<text x="35" y="1018" class="lab">Não representa ferragem, estrutura ou vão inferior da Berlin. Testar cadeira, banco e abertura reais antes da compra.</text>','</svg>']
(root/'Berlin_comparativo.svg').write_text('\n'.join(svg),encoding='utf-8')
print(json.dumps({'saved':str(out),'report':report['verificacao_reabertura'],'source_unchanged':before==after,'results':results},ensure_ascii=False))
