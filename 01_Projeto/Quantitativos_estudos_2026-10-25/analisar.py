from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent
d=json.loads((HERE/'Diferencas_nominais.json').read_text(encoding='utf8'))
formats=[dict(size_mm=[2750,1850],source='https://www.guararapes.com.br/produto/branco-tx/',scope='Produto BrancoTX publicado; nao marca escolhida do projeto'),
 dict(size_mm=[2750,2100],source='https://arauco.com/brasil/wp-content/uploads/sites/17/2024/05/ARAUCO-MELAMINA-MDF-1-1-2024.pdf',scope='Ficha de linha2024 inclui18; padrao,faces,estoque e fornecimento precisam de confirmacao')]
checks=[]
def fits(pair,sheet):
 a,b=pair;x,y=sheet;return (a<=x+1e-5 and b<=y+1e-5)or(a<=y+1e-5 and b<=x+1e-5)
for r in d['rows']:
 pair=r['new_sorted_nominal_dims_mm'][1:]
 checks.append(dict(kit=r['kit'],object=r['study_object'],nominal_face_mm=pair,
  formats=[dict(sheet_mm=f['size_mm'],fits_one_rectangle_allow_rotation=fits(pair,f['size_mm']))for f in formats],
  old_source_object=r['source_object'],old_face_fits2750x1850=None if not r['source_object']else fits(r['old_sorted_nominal_dims_mm'][1:],[2750,1850]),
  note='Triagem de retangulo unico sem refilo, serra, sentido decorativo, perdas, transporte ou montagem; nao plano de corte.'))
oversize=[c for c in checks if not c['formats'][0]['fits_one_rectangle_allow_rotation']]
assert len(oversize)==1 and oversize[0]['old_source_object']=='Peca208' and oversize[0]['old_face_fits2750x1850']is False
assert all(c['formats'][1]['fits_one_rectangle_allow_rotation']for c in checks)
out=dict(formats=formats,rectangle_checks=checks,oversize_for2750x1850=oversize,
 purchase_sheet_count=None,commercial_material_selected=None,budget_change_committed=False,
 source_quantities_sha256=hashlib.sha256((HERE/'Diferencas_nominais.json').read_bytes()).hexdigest(),
 note='Confirmar formato comercial antes de projetar emenda; nenhuma divisao do fundo ou escolha de fornecedor foi feita.')
(HERE/'Formatos_e_pendencias.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
print(json.dumps(dict(proposed_records=36,replacements=11,new_wood=25,oversize=[x['old_source_object']for x in oversize],cost_changed=False)))
