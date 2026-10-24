from pathlib import Path
import re,json,zipfile
p=Path(__file__).parent
refs=re.findall(r'(?:href|src)="([^"]+)"',(p/'Relatorio.html').read_text(encoding='utf8'))
missing=[r for r in refs if not r.startswith('http') and not (p/r).exists()]
with zipfile.ZipFile(p/'Southco_Fixacao_ESTUDO.FCStd') as z:bad=z.testzip()
d=json.loads((p/'Verificacao.json').read_text(encoding='utf8'))
d.update(links_ausentes=missing,zip_erro=bad)
(p/'Verificacao.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
assert not missing and bad is None
print(d)
