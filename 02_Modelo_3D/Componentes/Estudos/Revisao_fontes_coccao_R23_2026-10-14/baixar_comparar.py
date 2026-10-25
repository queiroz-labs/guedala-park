from pathlib import Path
import hashlib, json, urllib.request, zipfile, io
from pypdf import PdfReader

here = (Path(__file__).resolve().parent / '.').resolve()
repo = (Path(__file__).resolve().parent / '../../../..').resolve()
out = []
for label, saved, reference in [
    ('Venax', 'venax-oficial.json', 'Venax_Forno_embutir_gas_50_90L_26019.pdf'),
    ('Electrolux', 'ke4gc-oficial.json', 'Electrolux_KE4GR_KE4GC_Manual_250405XATF.pdf'),
]:
    scraped = json.loads(((Path(__file__).resolve().parent / '.firecrawl').resolve()/saved).read_text(encoding='utf-8'))
    url = next(u for u in scraped['links'] if ('manuais_' in u if label == 'Venax' else '.pdf' in u))
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read()
    package = here / (label+'_manual_atual'+('.zip' if label == 'Venax' else '.pdf'))
    package.write_bytes(data)
    if label == 'Venax':
        archive = zipfile.ZipFile(io.BytesIO(data))
        entries = [n for n in archive.namelist() if n.lower().endswith('.pdf')]
    else:
        entries = [package.name]
    for entry in entries:
        pdf = archive.read(entry) if label == 'Venax' else data
        dest = here / (label+'_'+Path(entry).name if label == 'Venax' else package.name)
        dest.write_bytes(pdf)
        original = (Path(__file__).resolve().parent / '../../../../09_Referencias/Plantas_e_manuais/Manuais').resolve()/reference
        sha = hashlib.sha256(pdf).hexdigest()
        old_sha = hashlib.sha256(original.read_bytes()).hexdigest()
        reader = PdfReader(io.BytesIO(pdf))
        (here/(dest.name+'.txt')).write_text('\n'.join('PDF_PAGE '+str(i+1)+'\n'+(p.extract_text() or '') for i,p in enumerate(reader.pages)), encoding='utf-8')
        out.append(dict(fabricante=label,url=url,arquivo=dest.name,sha256=sha,referencia=str(original),sha256_referencia=old_sha,identico=sha==old_sha,paginas=len(reader.pages),conteudo_pacote=entry))
((Path(__file__).resolve().parent / 'Comparacao_binaria.json').resolve()).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=True,indent=2))
