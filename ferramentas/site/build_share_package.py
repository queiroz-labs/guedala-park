"""Immutable local share package; explicit technical allowlist, no legacy aliases."""
from pathlib import Path
from html import escape
from urllib.parse import urlsplit,unquote,quote
import hashlib,io,json,posixpath,re,zipfile
from current_release import ROOT,STUDY,load_release,validate_sources,normalized_payload,canonical_source
from plain_language import plain_html
FBASE='06_Entregas/Fichas_fabricacao/'
PBASE='06_Entregas/Planta_cotada/'
BATH='03_Ambientes/Banheiro/Fechamento_pre_entrega/'
LIGHT='03_Ambientes/Iluminacao/Fechamento_custo_beneficio/'
VISUAL='09_Referencias/Iluminacao_CB02/'
COLORS='02_Modelo_3D/Historico/Cores/'
CASTERS='03_Ambientes/Cozinha/Rodizios_gaveta/'
SITE='ferramentas/site/Guedala_Park_Interativo.html'

def source_paths(release):
 manifest=json.loads((ROOT/FBASE/'manifest.json').read_text(encoding='utf8'))
 paths=[release['cadPath'],release['cadReadme'],'ferramentas/site/current_release.json',SITE,'01_Programa_e_decisoes/Caderno_de_especificacoes.md','09_Referencias/Plantas_e_manuais/Planta_oficial.pdf']
 paths += [str(Path(release['cadReadme']).parent/n).replace('\\','/')for n in release['cadEvidence']]
 paths += [FBASE+n for n in manifest['files']]+[PBASE+n for n in ['index.html','Planta_cotada.svg','Planta_oficial.png','Cotas.json']]
 paths += [COLORS+n for n in ['README.md','Plano_de_cores.json','Verificacao_cores.json','Verificacao_geometria.json']]
 paths += [CASTERS+n for n in ['Selecao.md','Selecao.json','Verificacao_CAD.json']]
 paths += [BATH+n for n in ['Fechamento.html','Escolhas.json','Situacao.json','Iluminacao_e_materiais.json','Luminarias_selecao_L02.html','Luminarias_selecao_L02.json','Verificacao_luminarias_L02.json','Hidraulica_cenarios.json','Verificacao_unioes_P19.json','P19_Unioes_nominais.csv','Espelheiro_P19_Unioes_NOMINAIS.FCStd']]
 paths += [LIGHT+n for n in ['Revisao_quarto_CB02.md','Composicao_CB02.json']]+[VISUAL+n for n in ['Galeria.md','01_Quarto_economico.png','02_Cozinha_lavanderia.png','03_Sala_escritorio.png','04_Banheiro_L02.png']]
 paths += [p for item in release.get('technicalDocuments',[])for p in [item['path']]+item.get('files',[])]
 paths=list(dict.fromkeys(paths))
 for name in paths:
  p=Path(name)
  if p.is_absolute()or'..'in p.parts or p.parts[0]not in ['ESTADO_ATUAL.md','01_Programa_e_decisoes','02_Modelo_3D','03_Ambientes','04_Moveis','05_Orcamento_e_cronograma','06_Entregas','09_Referencias','ferramentas']:raise ValueError('File outside technical allowlist: '+name)
  if any(x.lower()in name.lower()for x in ['contrato','reembolso','protocolo','guedala-pessoal','blum_g2_pagina_'])or p.suffix.lower()in ['.msg','.eml']:raise ValueError('Private material excluded: '+name)
  if not(ROOT/name).is_file():raise FileNotFoundError(ROOT/name)
 return paths

def package_payload(release):
 from build_workshop_docs import markdown,page
 paths=source_paths(release);raw={p:(ROOT/p).read_bytes()for p in paths};payload={p:normalized_payload(p,b)for p,b in raw.items()};source_hash={p:hashlib.sha256(b).hexdigest()for p,b in raw.items()};canonical_hash={p:hashlib.sha256(canonical_source(p,b)).hexdigest()for p,b in raw.items()};source_path={p:p for p in paths}
 for p in paths:
  if p.endswith('.md'):
   payload[p+'.html']=page(Path(p).stem,markdown(payload[p].decode('utf-8-sig'))).encode('utf8');source_path[p+'.html']=p
 mapping={p:p+'.html'if p.endswith('.md')else p for p in paths}
 omissions=[];local_links=[];external_links=[]
 def html_links(src,content):
  def link(m):
   attr,delimiter,url=m.group(1,2,3);parsed=urlsplit(unquote(url))
   if parsed.scheme in ['data','mailto','tel']or url.startswith('#')or not url:return m[0]
   if parsed.scheme in ['http','https']:
    external_links.append(dict(source=src,reference=url));return m[0]
   resolved=posixpath.normpath(posixpath.join(posixpath.dirname(src),parsed.path))
   if resolved in mapping:resolved=mapping[resolved]
   if resolved in payload:
    local_links.append(dict(source=src,target=resolved));rel=posixpath.relpath(resolved,posixpath.dirname(src));return attr+'='+delimiter+quote(rel,safe='/')+('#'+parsed.fragment if parsed.fragment else '')+delimiter
   omissions.append(dict(source=src,reference=url,reason='Outside explicit technical package allowlist'))
   # Preserve the original reference without an offline link to a missing file.
   return 'data-omitted-reference='+delimiter+escape(url,quote=True)+delimiter
  # Inline site scripts already carry their own packaged navigation resolver.
  chunks=re.split(r'(<script\b[^>]*>.*?</script>)',content,flags=re.I|re.S)
  return ''.join(chunk if chunk.lower().startswith('<script')else re.sub(r'\b(href|src)\s*=\s*([\"\'])(.*?)\2',link,chunk,flags=re.I)for chunk in chunks)
 for p in list(payload):
  if p.endswith('.html'):
   content=payload[p].decode('utf-8-sig')
   if p==SITE:
    info=dict(root='../../',contentFiles=list(payload),files=list(payload)+['COMECE_AQUI.html','manifest.json'],fileCount=len(payload)+2,cadPath=release['cadPath'],packageRevision=release['packageRevision'])
    content=content.replace('<head>','<head><script>globalThis.GUEDALA_PACKAGE='+json.dumps(info,ensure_ascii=False,separators=(',',':'))+';</script>',1)
   payload[p]=html_links(p,content).encode('utf8')
 cad=release['cadPath'];readme=mapping[release['cadReadme']]
 body=f'''<h1>Guedala Park · comece aqui</h1><p>Pacote {release['packageRevision']} · FreeCAD {release['cadRevision']} · fichas {release['fabricationRevision']} · {release['releaseDate']}.</p>
<p>Extraia o ZIP inteiro e abra este arquivo. As entregas anteriores são preservadas.</p>
<nav><a href="{cad}">Abrir FreeCAD {release['cadRevision']}</a><a href="{SITE}">Explorar o apartamento offline</a><a href="{release['technicalDocuments'][0]['path']}.html">Avanços e pendências</a><a href="{FBASE}index.html">20 fichas dos móveis</a><a href="{FBASE}Pendencias.html">Pendências de projeto, oficina e apartamento</a><a href="{FBASE}Levantamento.html">Folha para medidas reais</a><a href="{PBASE}index.html">Planta cotada</a><a href="01_Programa_e_decisoes/Caderno_de_especificacoes.md.html">Caderno de especificações</a><a href="{readme}">O que mudou e limites da {release['cadRevision']}</a><a href="manifest.json">Arquivos e integridade</a></nav>
<p>{escape(release['notes'])}</p><p>A geometria, as dimensões nominais e os ensaios não liberam corte, carga, ligação ou instalação. Medidas reais do apartamento e verificações de oficina continuam nas fichas. A cafeteira continua sem volume ou encaixe simultâneo demonstrados.</p>
<p>HTML, imagens, SVG e CSV incluídos abrem localmente. Links de fabricantes e outros endereços externos exigem internet. Referências locais fora desta seleção foram desativadas e estão discriminadas no manifesto; o acervo completo não está neste pacote.</p><footer>SHA256 do CAD: {release['cadSHA256']}</footer>'''
 payload['COMECE_AQUI.html']=('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · pacote '+release['packageRevision']+'</title><style>body{font:16px/1.6 system-ui;color:#263f3b;background:#f7f6f2;max-width:900px;margin:auto;padding:32px}nav{display:grid;gap:12px}a{color:#2c5947}footer{font-size:11px;overflow-wrap:anywhere}</style>'+plain_html(body)+'</html>').encode('utf8')
 info=dict(revision=release['packageRevision'],cadRevision=release['cadRevision'],cadPath=cad,cadSHA256=release['cadSHA256'],fabricationRevision=release['fabricationRevision'],appearanceRevision=release['appearanceRevision'],lightingRevision=release['lightingRevision'],publicationStatus=release['publicationStatus'],legacyAliasesModified=False,scope='Explicit technical package only; no personal repository, contracts, emails or protocols. Local HTML navigation is restricted to included entries.',files=['manifest.json']+list(payload),entries=[dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),sourcePath=source_path.get(p),sourceSHA256=source_hash.get(source_path.get(p)),sourceCanonicalSHA256=canonical_hash.get(source_path.get(p)))for p,b in payload.items()],offlineLocalLinks=len(local_links),externalLinks=external_links,omittedLocalReferences=omissions)
 payload['manifest.json']=(json.dumps(info,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 return payload,info

def write_immutable(path,content):
 if path.exists():
  if path.read_bytes()!=content:raise FileExistsError(str(path)+' already exists with different content; use a new package revision')
  return False
 path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content);return True

def build(destination=None):
 release=validate_sources(load_release());payload,info=package_payload(release);memory=io.BytesIO();dt=tuple(map(int,release['releaseDate'].split('-')))+(12,0,0)
 with zipfile.ZipFile(memory,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6)as archive:
  for name,b in payload.items():
   z=zipfile.ZipInfo(release['archiveRoot']+'/'+name,date_time=dt);z.compress_type=zipfile.ZIP_DEFLATED;z.external_attr=0o644<<16;archive.writestr(z,b)
 data=memory.getvalue()
 with zipfile.ZipFile(io.BytesIO(data))as archive:
  assert archive.testzip()is None
  assert hashlib.sha256(archive.read(release['archiveRoot']+'/'+release['cadPath'])).hexdigest()==release['cadSHA256']
 dest=Path(destination).resolve()if destination else ROOT/release['packageDirectory'];dest.mkdir(parents=True,exist_ok=True)
 target=dest/release['packageFile'];created=write_immutable(target,data);write_immutable(dest/'manifest.json',payload['manifest.json'])
 readme=f"# Pacote {release['packageRevision']}\n\nExtraia `{release['packageFile']}` inteiro e abra `{release['archiveRoot']}/COMECE_AQUI.html`.\n\nCAD {release['cadRevision']}; fichas {release['fabricationRevision']}; entrega com HTML offline e documentação técnica selecionada.\n\nZIP SHA256: `{hashlib.sha256(data).hexdigest()}`.\n\nCRC de todos os arquivos e SHA do CAD verificados. Manifesto detalha os arquivos incluídos, links externos e referências locais omitidas. Originais R16 e aliases não são alterados.\n"
 write_immutable(dest/'LEIA-ME.md',readme.encode('utf8'))
 result=dict(path=str(target),revision=release['packageRevision'],cadRevision=release['cadRevision'],cadSHA256=release['cadSHA256'],sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),files=len(payload),created=created,crcPassed=True,offlineLinks=info['offlineLocalLinks'],omittedLocalReferences=len(info['omittedLocalReferences']))
 print(json.dumps(result,ensure_ascii=False));return result

def verify_sealed_package(destination=None):
 release=validate_sources(load_release());dest=Path(destination).resolve()if destination else ROOT/release['packageDirectory'];target=dest/release['packageFile']
 expected=set(source_paths(release));source_seen=set();prefix=release['archiveRoot']+'/'
 with zipfile.ZipFile(target)as archive:
  names=archive.namelist()
  if len(names)!=len(set(names))or any(not n.startswith(prefix)or'..'in Path(n).parts for n in names):raise ValueError('Invalid archive paths')
  if archive.testzip()is not None:raise ValueError('ZIP CRC failed')
  manifest=json.loads(archive.read(prefix+'manifest.json'))
  for key,value in [('revision',release['packageRevision']),('cadRevision',release['cadRevision']),('cadPath',release['cadPath']),('cadSHA256',release['cadSHA256'])]:
   if manifest.get(key)!=value:raise ValueError('Sealed release mismatch: '+key)
  for entry in manifest['entries']:
   if hashlib.sha256(archive.read(prefix+entry['path'])).hexdigest()!=entry['sha256']:raise ValueError('Entry checksum mismatch: '+entry['path'])
   source=entry.get('sourcePath')
   if source:
    if source not in expected:raise ValueError('Source outside current technical allowlist: '+source)
    if hashlib.sha256(canonical_source(source)).hexdigest()!=entry['sourceCanonicalSHA256']:raise ValueError('Sealed input changed; prepare a new package revision: '+source)
    source_seen.add(source)
  if source_seen!=expected:raise ValueError('Source allowlist changed; prepare a new package revision')
  if hashlib.sha256(archive.read(prefix+release['cadPath'])).hexdigest()!=release['cadSHA256']:raise ValueError('CAD checksum mismatch')
 result=dict(revision=release['packageRevision'],cadRevision=release['cadRevision'],cadSHA256=release['cadSHA256'],zipPath=(Path(release['packageDirectory'])/release['packageFile']).as_posix(),sha256=hashlib.sha256(target.read_bytes()).hexdigest(),bytes=target.stat().st_size,files=len(names),canonicalSourcesVerified=len(source_seen),crcPassed=True,recompressed=False)
 print(json.dumps(result,ensure_ascii=False));return result

def ensure_package(mode='auto'):
 release=load_release();target=ROOT/release['packageDirectory']/release['packageFile']
 if mode not in ['auto','verify','build']:raise ValueError('Unknown package mode')
 if mode=='verify'or(mode=='auto'and target.exists()):result=verify_sealed_package()
 else:build();result=verify_sealed_package()
 evidence=ROOT/release['packageDirectory']/'Verificacao_pacote.json';evidence.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 return result

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir');parser.add_argument('--verify',action='store_true');a=parser.parse_args()
 if a.verify:verify_sealed_package(a.output_dir)
 else:build(a.output_dir)
