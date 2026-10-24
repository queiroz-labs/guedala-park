import pathlib,json,zipfile,re,hashlib
p=pathlib.Path(__file__).parent
a=zipfile.ZipFile(p.parent/'Consolidacao_R43_2026-10-21/Guedala_Park_R43_Consolidado.FCStd');b=zipfile.ZipFile(p/'Guedala_Park_R44_Consolidado.FCStd')
r=json.loads((p/'Comparacao_BREP_R43_R44.json').read_text());out=[]
pattern=r'[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?'
for n in r['changed_or_missing_brep']:
 x=a.read(n).decode();y=b.read(n).decode();xx=re.findall(pattern,x);yy=re.findall(pattern,y)
 delta=max((abs(float(v)-float(w)) for v,w in zip(xx,yy)),default=0)
 out.append({'name':n,'non_numeric_identical':re.sub(pattern,'#',x)==re.sub(pattern,'#',y),'numeric_token_count_equal':len(xx)==len(yy),'max_numeric_delta':delta})
r['serialization_differences']=out;r['within_1e_10']=all(v['non_numeric_identical'] and v['numeric_token_count_equal'] and v['max_numeric_delta']<1e-10 for v in out)
colors=[n for n in a.namelist() if n.endswith(('.col','.mat'))];r['original_color_files']=len(colors);r['changed_color_files']=[n for n in colors if n not in b.namelist() or a.read(n)!=b.read(n)]
(p/'Comparacao_BREP_R43_R44.json').write_text(json.dumps(r,indent=2))
v=json.loads((p/'Verificacao_R44.json').read_text(encoding='utf8'));v['original_objects']=v.pop('original_solid_objects');v['new_reference_objects']=v.pop('new_manufacturer_solid_objects');v['new_manufacturer_solid_objects']=12;v['original_properties_checked']=['Label','Placement','ShapeColor','Visibility'];v['geometry_comparison']='Comparacao_BREP_R43_R44.json';(p/'Verificacao_R44.json').write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf8')
print('Numeric equivalent',r['within_1e_10'],'maxdelta',max(v['max_numeric_delta'] for v in out),'color files',len(colors),'changed',r['changed_color_files'])
