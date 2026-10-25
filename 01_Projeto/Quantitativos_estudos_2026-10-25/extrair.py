"""Diferencas nominais lidas dos BREP GRAVADOS; nao usa docs alterados em memoria."""
from pathlib import Path
import json,hashlib,zipfile,tempfile,xml.etree.ElementTree as ET
import Part
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
SOURCE=ROOT/'Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
SHA='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
cases=[]
def add(kit,file,obj,source=None,proxy=None):cases.append(dict(kit=kit,file=ROOT/file,study_object=obj,source_object=source,proxy_retired=proxy))
for n in ['Peca245','Peca246']:add('P01_prateleiras723','Cargas_e_ligacoes_R50_2026-10-25/P01_estudo_apoios_723.FCStd','Proposta_'+n,n)
soco=json.loads((ROOT/'P01_apoios_ao_piso_2026-10-25/Resultados.json').read_text(encoding='utf8'))
for p in soco['new_boards']:add('P01_socoR01','P01_apoios_ao_piso_2026-10-25/P01_soco_sem_tubos_R01_ESTUDO.FCStd',p['id'])
for n in ['Peca208','Peca262']:add('P01_P03_traseiro','P01_P03_caminho_superior_2026-10-25/P01_P03_apoio_traseiro_ESTUDO.FCStd','Estudo_'+n,n)
add('P04_fundo308','Solucoes_marcenaria_sem_tubos_2026-10-25/P15_P04_estudos_sem_tubos.FCStd','P04_fundo','Peca268')
for obj,n in [('P15_lateral_E','Peca360'),('P15_lateral_D','Peca359'),('P15_fundo','Peca361'),('P15_base_inferior',None)]:
 add('P15_composta36','Solucoes_marcenaria_sem_tubos_2026-10-25/P15_P04_estudos_sem_tubos.FCStd',obj,n)
add('P17_fundo550','P17_base_fundo_ligacoes_2026-10-25/P17_fundo_inteiro_ligacoes_ESTUDO.FCStd','Estudo_Peca386','Peca386')
bench=json.loads((ROOT/'Bancada_marcenaria_2026-10-25/Manifesto_estudo.json').read_text(encoding='utf8'))
for p in bench['new_panels']:
 n=p['source_replaces'];wood=n if n in ['Peca367','Peca368']else None
 add('Bancada_marcenaria','Bancada_marcenaria_2026-10-25/Bancada_marcenaria_pedestal_ESTUDO.FCStd',p['id'],wood,n if n in ['Peca111','Peca112']else None)
assert len(cases)==36
archives={};hashes={}
def archive(path):
 if path not in archives:
  z=zipfile.ZipFile(path);assert z.testzip()is None
  xml=ET.fromstring(z.read('Document.xml'));shape_files={}
  for o in xml.findall('./ObjectData/Object'):
   for prop in o.findall('./Properties/Property'):
    if prop.get('name')=='Shape' and prop.get('type')=='Part::PropertyPartShape':
     shape_files[o.get('name')]=prop[0].get('file')
  archives[path]=(z,shape_files);hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 return archives[path]
def read_shape(path,obj,tmp):
 z,files=archive(path);name=files[obj];payload=z.read(name);assert payload
 sh=Part.Shape()
 if name.endswith('.bin'):
  fp=tmp/(hashlib.sha256((str(path)+obj).encode()).hexdigest()+'.bin');fp.write_bytes(payload);sh.importBinary(str(fp))
 else:sh.importBrepFromString(payload.decode('utf8'),False)
 assert not sh.isNull() and sh.isValid(),obj
 return sh
rows=[]
try:
 with tempfile.TemporaryDirectory(prefix='brep_leitura_',dir=HERE)as tmpstr:
  tmp=Path(tmpstr).resolve();assert tmp.is_relative_to(HERE.resolve())
  for c in cases:
   new=read_shape(c['file'],c['study_object'],tmp);b=new.optimalBoundingBox();dims=sorted([b.XLength,b.YLength,b.ZLength]);V=new.Volume
   assert abs(dims[0]-18)<1e-5 and abs(V-dims[0]*dims[1]*dims[2])<.01,(c['study_object'],dims,V)
   old=read_shape(SOURCE,c['source_object'],tmp)if c['source_object']else None
   oldV=old.Volume if old else 0.;assert V>=oldV-1e-5
   olddims=None
   if old:
    ob=old.optimalBoundingBox();olddims=sorted([ob.XLength,ob.YLength,ob.ZLength]);assert abs(olddims[0]-18)<1e-5
   rows.append(dict(kit=c['kit'],study_file=str(c['file'].relative_to(ROOT)),study_object=c['study_object'],source_object=c['source_object'],
    role='replacement'if old else 'new_wood',proxy_retired=c['proxy_retired'],new_sorted_nominal_dims_mm=dims,old_sorted_nominal_dims_mm=olddims,
    new_volume_mm3=V,old_volume_mm3=oldV,delta_volume_mm3=V-oldV,
    proposed_fabrication_face_area_m2=V/18/1e6,old_face_area_m2=oldV/18/1e6,delta_face_area_m2=(V-oldV)/18/1e6,
    delta_mass_kg_at650_800_900=[(V-oldV)*rho/1e9 for rho in (650,800,900)],
    status='ESTUDO nao incorporado. Area geometrica liquida, sem perdas/veio/bordas/processo. Nao compra nem corte.'))
  proxies=[]
  for n in ['Peca111','Peca112']:
   sh=read_shape(SOURCE,n,tmp);proxies.append(dict(source=n,volume_mm3=sh.Volume,material_and_mass_unknown=True,wood_mass_credit_kg=None))
  # A limpeza automatica abaixo atinge somente este diretorio temporario proprio verificado.
  assert tmp.is_relative_to(HERE.resolve())
finally:
 for z,_ in archives.values():z.close()
groups=[]
for kit in dict.fromkeys(r['kit']for r in rows):
 selected=[r for r in rows if r['kit']==kit]
 groups.append(dict(kit=kit,proposed_wood_parts=len(selected),replacements=sum(r['role']=='replacement'for r in selected),new_wood=sum(r['role']=='new_wood'for r in selected),
  proposed_fabrication_face_area_m2=sum(r['proposed_fabrication_face_area_m2']for r in selected),delta_face_area_m2=sum(r['delta_face_area_m2']for r in selected),
  delta_volume_m3=sum(r['delta_volume_mm3']for r in selected)/1e9,delta_mass_800_kg=sum(r['delta_mass_kg_at650_800_900'][1]for r in selected),
  inclusion='Nao selecionado. Nao somar kits automaticamente nem alterar lista/orcamento R51.'))
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SHA
out=dict(source=str(SOURCE),source_sha256=SHA,rows=rows,kits=groups,retired_schematic_supports_only_if_bench_adopted=proxies,
 persisted_archives_sha256=hashes,script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 total_proposed_wood_records=36,replacement_records=sum(r['role']=='replacement'for r in rows),
 change_to_approved_bill_of_materials=False,physical_tests=0,
 scope='BREP dos arquivos gravados, sem abrir/fechar documentos ou usar versoes modificadas da sessao. Quantitativo separado de opcoes; nao mede massa real nem chapa de compra.')
(HERE/'Diferencas_nominais.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(kits=groups,records=len(rows),replacements=out['replacement_records']),ensure_ascii=False))
