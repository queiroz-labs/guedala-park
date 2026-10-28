import FreeCAD as A, json, pathlib, zipfile, xml.etree.ElementTree as ET, hashlib, re
root=pathlib.Path(__file__).resolve().parents[2]
out=root/'ferramentas/site/src'
release=json.loads((root/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
source=root/release['cadPath']
before=hashlib.sha256(source.read_bytes()).hexdigest()
d=A.ActiveDocument
assert d and pathlib.Path(d.FileName).resolve()==source.resolve(), 'Abrir o modelo vigente na GUI antes de exportar'
gui=ET.fromstring(zipfile.ZipFile(source).read('GuiDocument.xml'))
vis={vp.attrib['name']:vp.find(".//Property[@name='Visibility']/Bool").attrib.get('value')=='true' for vp in gui.findall('.//ViewProvider') if vp.find(".//Property[@name='Visibility']/Bool") is not None}
# Never bootstrap classification from a previous export: older fallbacks labeled
# utensils, hydraulic reserves, mirrors and metal hardware as wood.
palette={'wood':'#c4a27b','petrol':'#294b51','offwhite':'#eeeae1','stone':'#ded7c7','bathbeige':'#c9bca8','lightwood':'#c8a77d','head':'#c9bbaa','black':'#282d2e'}
names=['Roupeiro','Canto em L','Maleiro','Aéreo da cabeceira','Gabinete da pia','Gaveteiro da cozinha','Módulo de cocção','Gaveta de limpeza','Aéreo D · depurador','Aéreo C · uso diário','Aéreo B · micro','Aéreo A · geladeira','Apoio do micro','Gabinete tanque e cesto','Aéreo da lavanderia','Gaveteiro do escritório','Aéreo do escritório','Gabinete do banheiro','Espelheiro','Banco baú']
ids=['wardrobe','bedcabinet','bedcabinet','bedcabinet','sinkstorage','kitchenbase','kitchenbase','lowdrawer','kitchenupper','kitchenupper','kitchenupper','kitchenupper','microwave','laundrybase','laundryupper','drawers','officecab','bathvanity','bathmirror','bench']
rooms=['quarto']*4+['cozinha']*9+['lavanderia']*2+['escritorio']*2+['banho']*2+['sala']
parts=[];modules=[];seen=set()
drawer_panels={'GavetaComumR08'} | {f'GavetaComumR{k:03d}' for start in [0,12,24,36,48,60,72,84] for k in range(max(1,start),start+6)} | {f'MontagemG2R{k:03d}' for k in range(16,21)}
# Functional panel evidence is separate from finish evidence. These identifiers
# are boards, fronts or wood supports in the R45 matrix / labeled active CAD.
# This allowlist deliberately omits cesto frame gabaritos, guides, contents,
# wheels, mirrors and steel grilles even when their envelopes are rectangular.
functional_panels = drawer_panels | {
 'PlacaL','PlacaL001','LateralApoioPrincipal','FrenteSimplesR04','FrenteSimplesR001',
 'ApoioPortaBR04','FaixaQuinaAR04','FaixaQuinaBR04','FaixaFixaEstudo','FrenteVizinhaR18',
 'BasePlanaR31','ApoioEsquerdoR31','ApoioCentralR31','ApoioDireitoR31',
 'ReguaInferiorBaixaR31','ReguaInferiorAltaR31','ReguaSuperiorBaixaR31','ReguaSuperiorAltaR31',
 'PecaBaixaR13','PecaBaixaR036','PecaBaixaR037',
 'PecaCestoR15','PecaCestoR001','PecaCestoR002','PecaCestoR003','FundoTanqueR29',
 'ApoioCestoC01R31','ApoioCestoC02R31','ApoioCestoC03R31',
 'BC43_LateralE','BC43_LateralD','BC43_Base','BC43_Travessa','BC43_CaixaE','BC43_CaixaD','BC43_CaixaBase',
 'PrateleiraEspelhadoR12','PrateleiraEspelhadoR001','PecaBancoR16','PecaBancoR029','PecaBancoR030',
 'Peca406AtualR31','PecaBancoR007AtualR31','PecaBancoR006AtualR31','BancoR43_Painel1','BancoR43_Painel2',
} | {f'PecaBaixaR{k:03d}' for k in range(1,6)} | {f'PecaBancoR{k:03d}' for k in range(1,6)}

def functional_panel(o):
 return o.Name in functional_panels or o.Name.startswith(('FrenteComum','ApoioComum','ApoioOposto','Ref_Apoio_B','Ref_Sarrafo_'))

def material_evidence(o,visited=()):
 if not o or o.Name in visited:return '',None
 mat=str(getattr(o,'MaterialReferencia',''))
 if mat:return mat,o.Name+'.MaterialReferencia'
 # A boolean-cut front keeps its parent board's material; tool material is irrelevant.
 base=getattr(o,'Base',None)
 if hasattr(base,'Name'):
  mat,source=material_evidence(base,visited+(o.Name,))
  if mat:return mat,source+' (via Base)'
 # Explicit finish directions in data.js and R45 matrix, not generic wood defaults.
 if o.Name in ['FrenteComumR11','FrenteComumR012','FrenteComumR013','FrenteComumR014']:
  return 'offwhite','data.js: officecab / offwhite; direção de acabamento, código de chapa pendente'
 if o.Name.startswith('BC43_Painel'):return 'bathbeige','Direção de acabamento do gabinete BC43; código de chapa pendente'
 if o.Name.startswith('BancoR43_Almofada'):return 'head','R43: almofada, tecido final pendente'
 return '',None

def local_envelope(ps,module_obj,panels_only=False):
 if not module_obj:return None
 inverse=module_obj.getGlobalPlacement().inverse()
 points=[]
 for p in ps:
  if panels_only and not p.get('piece'):continue
  for v in p['v']:
   points.append(inverse.multVec(A.Vector(7400-(p['x']+v[0])*10,(p['z']+v[2])*10,(p['y']+v[1])*10)))
 if not points:return None
 return [round(max(getattr(v,k) for v in points)-min(getattr(v,k) for v in points),2) for k in ['x','y','z']]
def visit(o,item,room,module,anc=(),force=False):
 if not o or o.Name in seen:return
 if not force and not vis.get(o.Name,False):return
 if o.Name.startswith(('GavetaComum','MontagemG2')) and o.Name not in drawer_panels:return
 if o.Name.startswith(('Historico','Dobradica','ReferenciaCorrer','Ferragem','PrincipalBlum','AjusteProfundidade','CorpoArticulado','PinoArticulado','BC43_Parafuso','BC43_Carro','BC43_Guia','BC43_Confirmat','BC43_Cavilha','BC43_Porca','BC43_M6')):return
 if hasattr(o,'Group'):
  for c in o.Group:visit(c,item,room,module,anc+(o.Name,),force=force)
  return
 if not hasattr(o,'Shape') or o.Shape.isNull():return
 seen.add(o.Name)
 shape=o.Shape.copy();shape.Placement=o.getGlobalPlacement();b=shape.BoundBox
 if max(b.XLength,b.YLength,b.ZLength)>10000:return
 verts,tri=shape.tessellate(1.2)
 if not tri:return
 # Viewer convention is the historical pre-R34 x axis; camera reflects it once.
 # R45 physical geometry stays unchanged. Reflect X and swap Y/Z => determinant +1.
 vv=[[round((7400-v.x)/10,5),round(v.z/10,5),round(v.y/10,5)] for v in verts]
 lo=[min(v[k] for v in vv) for k in range(3)];hi=[max(v[k] for v in vv) for k in range(3)]
 mat,mat_source=material_evidence(o)
 role=str(getattr(o,'TipoPeca',''))
 front=role in ['Porta','Frente','Tampa','Almofada'] or any(a.startswith(('Folha','Porta','Tampa','BancoR43_Tampa')) for a in anc) or o.Name.startswith(('BC43_Painel','BancoR43_Almofada'))
 material=palette.get(mat,mat if re.fullmatch(r'#[0-9a-fA-F]{6}',mat) else '#bbbdb7')
 item2='laundrybasket' if item=='laundrybase' and any(a.startswith('BasculanteCesto') for a in anc) else item
 p={'key':'cad/'+o.Name,'source':o.Name,'label':o.Label,'id':item2,'room':room,'module':module,'x':lo[0],'y':lo[1],'z':lo[2],'w':hi[0]-lo[0],'h':hi[1]-lo[1],'d':hi[2]-lo[2],'c':material,'mat':mat,'kind':'cad','upper':b.ZMin>=1300,'front':front,'opacity':1,'v':[[round(v[k]-lo[k],5) for k in range(3)] for v in vv],'t':[list(t) for t in tri]}
 # Unrotated local envelope: not a shop cutting dimension for shaped pieces.
 local=o.Shape.copy();local.Placement=A.Placement();lb=local.BoundBox
 dims=sorted([lb.XLength,lb.YLength,lb.ZLength],reverse=True)
 evidenced_material=mat in palette and mat not in ['stone','black','head']
 panel=(evidenced_material or functional_panel(o)) and min(dims)>0 and shape.Volume>0
 p['piece']= {'dimensions':[round(x,2) for x in dims], 'thickness':round(dims[2],2),'rectangular':abs(shape.Volume-lb.XLength*lb.YLength*lb.ZLength)<max(1,shape.Volume*.00001),'material':mat,'type':role or 'Peça do modelo'} if panel else None
 p['materialSource']=mat_source
 p['classification']=('painel com material de referência' if mat else 'painel identificado pela função; acabamento não especificado') if panel else 'componente visual; natureza não classificada para marcenaria'
 if p['piece']:
  p['piece']['materialSource']=mat_source
  p['piece']['panelEvidence']=mat_source if evidenced_material else 'Função de painel no objeto ativo R45 e matriz dos módulos; acabamento não especificado'
  p['piece']['materialLabel']=mat or 'Não especificado'
 parts.append(p)
for i in range(20):
 n='Modulo'+(f'{i:03d}' if i else '')
 code=f'P{i+1:02d}'
 start=len(parts)
 if i==17:
  # Old carcase still contains current side/floor pieces; hidden obsolete fronts omitted.
  visit(d.getObject(n),ids[i],rooms[i],code)
  visit(d.getObject('BanheiroCorrerR43'),ids[i],rooms[i],code)
 else:visit(d.getObject(n),ids[i],rooms[i],code)
 if i==19:visit(d.getObject('BancoDuasTampasR43'),ids[i],rooms[i],code)
 ps=parts[start:]
 bb=[round((max(p[a]+p[e] for p in ps)-min(p[a] for p in ps))*10,2) for a,e in [('x','w'),('z','d'),('y','h')]] if ps else []
 mo=d.getObject(n)
 modules.append({'code':code,'name':names[i],'item':ids[i],'room':rooms[i],'dimensions':bb,'dimensionsLocal':local_envelope(ps,mo),'classifiedPanelsEnvelopeLocal':local_envelope(ps,mo,True),'dimensionsMeaning':'Envelope dos componentes visíveis, incluindo reservas; não dimensão de corte. dimensionsLocal usa eixo local do módulo; classifiedPanelsEnvelopeLocal cobre painéis reconhecidos pela função ou material, pode ser parcial.','parts':[p['source'] for p in ps],'source':n,'status':'Conferir antes de fabricar'})
for n,it,room in [('Peca308','kitchenbase','cozinha'),('Peca357','laundrybase','lavanderia'),('Peca399','bathvanity','banho'),('Peca421','bench','sala'),('Peca275','mirror','quarto'),('FischerInfinityR31','oven','cozinha'),('Peca351','microwave','cozinha'),('CabeceiraDoisPaineisR25','headboard','quarto'),('Peca188','bathlight','banho'),('Peca189','bathlight','banho')]:visit(d.getObject(n),it,room,None)
# Berlin actual saved closed envelope and the documented alternative open scenario.
for n in ['Fechada_110','Aberta_cadeira_lateral']:
 start=len(parts);visit(d.getObject(n),'table','sala',None,force=True)
 for p in parts[start:]:p['scenario']='compact' if n=='Fechada_110' else 'extended';p['id']='table' if p['source'].endswith(('Tampo','Sapata','Pedestal')) else 'diningchairs'
# Same physical finish across the two table presentation scenarios.
for p in parts:
 if p.get('scenario')=='extended':
  p['finishSource']=next(('Fechada_110'+suffix for suffix in ('Tampo','Sapata','Pedestal') if p['source'].endswith(suffix)), 'Fechada_110Lateral')
data={'current_revision':release['cadRevision'],'current_source_path':release['cadPath'],'current_source_sha256':before,'current_revision_note':'Extracao da revisao vigente; detalhes de furacao R14 conservam fontes historicas e condicoes.','revision':release['cadRevision'],'source_sha256':before,'coordinate_system':'R45 transformada apenas para o eixo histórico do visualizador; câmera faz reflexão única. Medidas documentais em mm.','parts':parts,'modules':modules,'replacements':sorted(set(p['id'] for p in parts))}
assert len(parts)>200 and len(modules)==20
(out/'cad-data.js').write_text('/* Geometria vigente de consulta; nao corte executivo. */\nconst CAD_DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
unknown_panels=[{'source':p['source'],'label':p['label'],'module':p['module'],'dimensions':p['piece']['dimensions']} for p in parts if p['piece'] and not p['mat']]
summary={'revision':release['cadRevision'],'source_sha256':before,'source_unchanged':True,'parts':len(parts),'modules':len(modules),'triangles':sum(len(p['t']) for p in parts),'panel_rows':sum(bool(p['piece']) for p in parts),'drawer_panels_visible':sum(p['source'] in drawer_panels for p in parts),'unknown_finish_panels':len(unknown_panels),'classification_policy':'No material fallback. Panel eligibility uses explicit material or documented functional allowlist; finish can remain unspecified. Hardware, contents and unknown-purpose components stay piece=null.'}
(root/'ferramentas/site/fabrication/panels-unknown-finish.json').write_text(json.dumps(unknown_panels,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'ferramentas/site/fabrication/export.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(summary)

frames={m['code']:[list(d.getObject(m['source']).getGlobalPlacement().inverse().Matrix.A)[i:i+4] for i in range(0,16,4)] for m in modules}
(root/'ferramentas/site/fabrication/module-frames.json').write_text(json.dumps({'sha256':before,'frames':frames},indent=2),encoding='utf-8')
