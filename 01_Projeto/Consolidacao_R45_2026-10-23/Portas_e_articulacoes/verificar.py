import json,pathlib,re
p=pathlib.Path(__file__).parent
d=json.loads((p/'Calculos.json').read_text(encoding='utf8'))
report=(p/'Relatorio.html').read_text(encoding='utf8')
missing=[u for u in re.findall(r'href="([^"]+)"',report) if not u.startswith('http') and not (p/u).exists()]
result={'familias':len(d['portas']),'folhas_abrir':sum(r['folhas'] for r in d['portas'] if r['dobradicas_por_folha']),'dobradicas_estudo':sum(r['folhas']*r['dobradicas_por_folha'] for r in d['portas']),'poses_banco':sum(r['poses'] for r in d['abertura_frontal']),'links_locais_ausentes':missing,'aprova_ferragem':False}
assert result['dobradicas_estudo']==52
assert result['folhas_abrir']==24
assert not missing
(p/'Verificacao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(result)
