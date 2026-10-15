from pathlib import Path
import json,hashlib,re,zipfile
from urllib.parse import unquote
here=Path(__file__).resolve().parent
geo=json.loads((here/'Geometria_atual.json').read_text(encoding='utf-8'))
check=json.loads((here/'Verificacao_apoios.json').read_text(encoding='utf-8'))
targets={'B01':'PecaBancoR003','B02':'PecaBancoR002','B03':'PecaBancoR002','B04':'Peca408','C01':'Peca352','C02':'Peca353','C03':'PecaCestoR15'}
contacts=[]
for s in check['supports']:
    t=next(r for r in geo[s['group']]['parts'] if r['name']==targets[s['id']])
    p=s['origin_mm'];size=s['envelope_mm'];b=t['bbox_local_mm']
    assert abs(p[2]+size[2]-b[2])<1e-6
    dx=min(p[0]+size[0],b[3])-max(p[0],b[0]);dy=min(p[1]+size[1],b[4])-max(p[1],b[1])
    assert dx>0 and dy>0
    contacts.append({'support':s['id'],'supported_part':t['name'],'top_z_mm':p[2]+size[2],'rectangular_bearing_area_mm2':dx*dy,'limit':'Contato entre faces retangulares de referência; área não define resistência ou capacidade.'})
assert hashlib.sha256(Path(check['source']).read_bytes()).hexdigest()==check['source_sha256_before']
with zipfile.ZipFile(here/'Estudo_Apoios_Banco_Cesto_R30.FCStd') as z:
    assert z.testzip() is None
    xml=z.read('Document.xml').decode('utf-8')
    for code in targets:assert f'name="{code}"' in xml
missing=[];count=0
for p in [here/'README.md',here/'Caderno_construtivo.html']:
    text=p.read_text(encoding='utf-8')
    links=re.findall(r'\]\(([^)]+)\)',text) if p.suffix=='.md' else re.findall(r'(?:href|src)="([^"]+)"',text)
    for link in links:
        if '://' in link or link.startswith('#'):continue
        count+=1
        if not (p.parent/unquote(link.split('#')[0])).exists():missing.append(link)
assert not missing,missing
report={'bearing_contacts':contacts,'links_checked':count,'missing_links':missing,'source_fcstd_unchanged':True,'study_archive_valid':True,'study_has_all_seven_supports':True}
(here/'Verificacao_entrega.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
root=here.parents[1];catalog=root/'INDICE_DE_ARQUIVOS.md';text=catalog.read_text(encoding='utf-8');add=[]
for p in sorted(here.iterdir()):
    if p.is_file():
        rel=p.relative_to(root).as_posix()
        if f']({rel})' not in text:add.append(f'- [{rel}]({rel})')
if add:catalog.write_text(text+'\n## Detalhamento construtivo baseado na R30\n\n'+'\n'.join(add)+'\n',encoding='utf-8')
print(json.dumps({'contacts':len(contacts),'links':count,'source_preserved':True,'study_valid':True}))
