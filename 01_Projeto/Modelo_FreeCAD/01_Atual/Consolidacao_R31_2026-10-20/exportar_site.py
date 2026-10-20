"""Exporta painéis e peças visíveis da base R31, somente leitura, para o site."""
from pathlib import Path
import json,math,hashlib,traceback
import FreeCAD as App,Part
here=Path(__file__).resolve().parent;project=here.parents[2];root=project.parent
status=root/'tmp/exportacao_site_r31_status.json'
status.write_text(json.dumps({'status':'iniciando'}),encoding='utf-8')
try:
 d=App.ActiveDocument
 assert Path(d.FileName).name=='Guedala_Park_R31_Consolidado.FCStd'
 before=hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()
 mapping={'Modulo':'wardrobe','Modulo001':'bedcabinet','Modulo002':'bedcabinet','Modulo003':'bedcabinet',
  'Modulo004':'sinkstorage','Modulo005':'kitchenbase','Modulo006':'kitchenbase','Modulo007':'lowdrawer',
  'Modulo008':'kitchenupper','Modulo009':'kitchenupper','Modulo010':'kitchenupper','Modulo011':'kitchenupper',
  'Modulo012':'microwave','Modulo013':'laundrybase','Modulo014':'laundryupper','Modulo015':'drawers',
  'Modulo016':'officecab','Modulo017':'bathvanity','Modulo018':'bathmirror','Modulo019':'bench',
  'Peca308':'kitchenbase','Peca357':'laundrybase','Peca399':'bathvanity','Peca421':'bench','Peca275':'mirror',
  'FischerInfinityR31':'oven','Peca351':'microwave','CabeceiraDoisPaineisR25':'headboard',
  'PainelCabeceiraR25':'headboard','PainelCabeceiraR001':'headboard','Peca188':'bathlight','Peca189':'bathlight'}
 rooms={'wardrobe':'quarto','bedcabinet':'quarto','mirror':'quarto','headboard':'quarto',
  'sinkstorage':'cozinha','kitchenbase':'cozinha','lowdrawer':'cozinha','kitchenupper':'cozinha','microwave':'cozinha','oven':'cozinha',
  'laundrybase':'lavanderia','laundrybasket':'lavanderia','laundryupper':'lavanderia','drawers':'escritorio','officecab':'escritorio',
  'bathvanity':'banho','bathmirror':'banho','bathlight':'banho','bench':'sala'}
 links=[o for o in d.getObject('ApartamentoEspelhadoR20').OutListRecursive if o.TypeId=='App::Link' and o.LinkedObject and o.ViewObject.Visibility]
 linked={o.LinkedObject.Name for o in links}
 roots=[d.getObject(n) for n in mapping if n in linked]
 skipped=[];parts=[];seen=set()
 def visit(o,item,ancestors=(),first=False):
  if o.Name in seen:return
  if not first and not o.ViewObject.Visibility:return
  if o.Name.startswith(('Historico','Dobradica','ReferenciaCorrer','Ferragem','PrincipalBlum','AjusteProfundidade','CorpoArticulado','PinoArticulado','GavetaComum','MontagemG2')):
   skipped.append(o.Name);return
  if hasattr(o,'Group'):
   for c in o.Group:visit(c,item,ancestors+(o.Name,),False)
   return
  if not hasattr(o,'Shape') or o.Shape.isNull() or o.Shape.Volume<1e-6:return
  seen.add(o.Name)
  s=o.Shape.copy();s.Placement=o.getGlobalPlacement()
  b=s.BoundBox
  if min(b.XLength,b.YLength,b.ZLength)<.01:return
  verts,faces=s.tessellate(1.2)
  if not faces:return
  vv=[[round((v.x-b.XMin)/10,5),round((v.z-b.ZMin)/10,5),round((v.y-b.YMin)/10,5)] for v in verts]
  tt=[]
  for a,bb,c in faces:
   # Troca Y/Z muda orientação: inverter a ordem mantém normais externas.
   v1=[vv[c][k]-vv[a][k] for k in range(3)];v2=[vv[bb][k]-vv[a][k] for k in range(3)]
   cr=[v1[1]*v2[2]-v1[2]*v2[1],v1[2]*v2[0]-v1[0]*v2[2],v1[0]*v2[1]-v1[1]*v2[0]]
   if sum(t*t for t in cr)>1e-14:tt.append([a,c,bb])
  material=str(getattr(o,'MaterialReferencia',''))
  color='#'+''.join(f'{round(v*255):02x}' for v in o.ViewObject.ShapeColor[:3])
  role=str(getattr(o,'TipoPeca',''))
  front=role in ['Porta','Frente','Tampa','Almofada'] or any(a.startswith(('Folha','Porta','Tampa')) for a in ancestors)
  if item=='laundrybase' and any(a.startswith('BasculanteCesto') for a in ancestors):item='laundrybasket'
  slide='tray' if o.Name in ['BancoPlataformaR31','BancoAba_frenteR31','BancoAba_trasR31','BancoReceptorR31'] else 'leaf' if o.Name=='BancoFolhaR31' else ''
  parts.append({'key':'cad/'+o.Name,'source':o.Name,'label':o.Label,'id':item,'room':rooms[item],
   'x':round(b.XMin/10,5),'y':round(b.ZMin/10,5),'z':round(b.YMin/10,5),
   'w':round(b.XLength/10,5),'h':round(b.ZLength/10,5),'d':round(b.YLength/10,5),
   'c':color,'mat':material if material else color,'kind':'cad','upper':b.ZMin>=1300,'front':front,'slide':slide,
   'opacity':1-float(o.ViewObject.Transparency)/100,'v':vv,'t':tt})
 for o in roots:visit(o,mapping[o.Name],first=True)
 assert len(parts)>150,('Exportação insuficiente',len(parts))
 ids=sorted(set(p['id'] for p in parts));assert all(i in ids for i in ['oven','bench','wardrobe','kitchenbase','officecab','bathmirror','bedcabinet'])
 data={'revision':'R31','source_sha256':before,'coordinate_system':'Base nativa não espelhada emcm; a câmera do site aplica o espelhamento, comum às peças e anotações.','parts':parts,'replacements':ids}
 out=project/'Estudo_interativo/src/cad-data.js'
 out.write_text('/* Geometria derivada do FreeCAD R31; detalhes de ferragens omitidos para visualização. */\nconst CAD_DATA='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
 assert hashlib.sha256(Path(d.FileName).read_bytes()).hexdigest()==before
 summary={'revision':'R31','source':d.FileName,'sha256':before,'parts':len(parts),'triangles':sum(len(p['t']) for p in parts),
  'roots':[o.Name for o in roots],'replaced_item_ids':ids,'excluded_hardware_groups':skipped,
  'bytes':out.stat().st_size,'source_unchanged':True,'limits':'Tesselação1,2mm para visualização; não exporta mecanismos completos. Estados dinâmicos gerais continuam ilustrações. Não é novo ensaio de instalação.'}
 (here/'Exportacao_site_R31.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
 status.write_text(json.dumps({'status':'pronto',**summary},ensure_ascii=False),encoding='utf-8')
except Exception:
 status.write_text(json.dumps({'status':'erro','trace':traceback.format_exc()}),encoding='utf-8');raise
