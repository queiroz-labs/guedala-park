from pathlib import Path
import json,hashlib,zipfile,re
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Intersecoes_localizadas.json').read_text(encoding='utf8'));g=json.loads((HERE/'Referencia_G2_e_furos_P16.json').read_text(encoding='utf8'));a=json.loads((HERE/'Diagnostico.json').read_text(encoding='utf8'))
assert hashlib.sha256(Path(d['source']).read_bytes()).hexdigest()==d['source_sha256']==a['source_sha256']
for p,h in a['inputs_sha256'].items():assert hashlib.sha256((HERE/p).read_bytes()).hexdigest()==h,p
assert len(d['pairs'])==8 and len(a['classified'])==18
for r in d['pairs']:
 assert abs(sum(x['volume_mm3']for x in r['components'])-r['positive_intersection_volume_mm3'])<1e-6
 assert all(c['valid'] and c['volume_mm3']>0 for c in r['components'])
assert [len(r['components'])for r in g['reference_regions']]==[4,5]
for r in g['P16_bores']:
 assert len(r['holes'])==2
 for h in r['holes']:
  assert abs(h['radius_mm']-3)<1e-8 and abs(h['bore_depth_mm']-10)<1e-8 and abs(h['height_above_bottom_underside_mm']-11)<1e-8
with zipfile.ZipFile(d['source'])as z:assert z.testzip()is None
for p in re.findall(r'\]\(([^)]+)\)',(HERE/'README.md').read_text(encoding='utf8')):
 if p!='Verificacao.json' and not p.startswith(('http','#')):assert (HERE/p).exists(),p
pdf=HERE.parents[2]/'02_Modelo_3D/Componentes/Montagem/Fabricacao_corrigida/productionDrawings/MOVENTO-Gaveta-Sem-reling-40-kg-Comprimen.PDF'
out=dict(pairs=8,positive_pairs=4,positive_components=18,under_bottom_components=16,rear_bore_components=2,nominal_bores=4,
 official_G2_same_region_pattern=True,official_drawing_pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(),
 source_hash_crc=True,input_hashes=True,links=True,physical_tests=0,wood_or_guide_modified=False,
 status='Cotas/localizacao conferidas; causa e aceitabilidade da interferencia e configuracao individual400 permanecem condicionadas')
(HERE/'Verificacao.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8');print(json.dumps(out,ensure_ascii=False))
