"""Verified release identity shared by package, documentation and publication builders."""
from pathlib import Path
import hashlib,json,re
STUDY=Path(__file__).resolve().parent
ROOT=STUDY.parent.parent
CONFIG=STUDY/'current_release.json'
TEXT_SUFFIXES={'.md','.html','.json','.js','.mjs','.cjs','.css','.csv','.svg','.txt','.py','.yml','.yaml'}
PUBLICATION_FIELDS={'publicationStatus','lastPublishedCadRevision','lastPublishedCadPath','lastPublishedPackageRevision'}

def normalized_payload(path,content):
 if Path(path).suffix.lower()in TEXT_SUFFIXES:
  return content.decode('utf-8-sig').replace('\r\n','\n').replace('\r','\n').encode('utf8')
 return content

def canonical_source(path,content=None):
 content=content if content is not None else(ROOT/path).read_bytes()
 result=normalized_payload(path,content)
 if Path(path).as_posix()=='01_Projeto/Estudo_interativo/current_release.json':
  data=json.loads(result);data={k:v for k,v in data.items()if k not in PUBLICATION_FIELDS}
  result=json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode('utf8')
 return result

def load_release(verify_cad=True):
 data=json.loads(CONFIG.read_text(encoding='utf-8-sig'))
 for key in ['cadPath','cadReadme','packageDirectory']:
  p=Path(data[key]);assert not p.is_absolute()and'..'not in p.parts,key
 assert re.fullmatch(r'R\d+',data['cadRevision'])and re.fullmatch(r'R\d+',data['packageRevision'])
 assert data['publicationStatus']in ['local_only','publication_authorized','published']
 if verify_cad:
  with(ROOT/data['cadPath']).open('rb')as f:sha=hashlib.file_digest(f,'sha256').hexdigest()
  if sha!=data['cadSHA256']:raise ValueError('CAD changed: update and verify the release configuration first')
 return data

def validate_sources(data=None):
 data=data or load_release()
 text=(STUDY/'src/cad-data.js').read_text(encoding='utf8')
 cad=json.loads(re.search(r'const CAD_DATA\s*=\s*(\{.*\});',text,re.S)[1])
 for field,key in [('current_revision','cadRevision'),('current_source_path','cadPath'),('current_source_sha256','cadSHA256')]:
  if cad[field]!=data[key]:raise ValueError('Release/CAD_DATA mismatch: '+field)
 project=(STUDY/'src/data.js').read_text(encoding='utf8')
 if json.dumps(data['projectRevision'],ensure_ascii=False)not in project or json.dumps(data['projectDate'],ensure_ascii=False)not in project:raise ValueError('Release/PROJECT metadata mismatch')
 return data
