"""Prepare a local web artifact from the current release; no deploy or legacy writes."""
from pathlib import Path
import argparse,json,os,runpy,shutil,subprocess
from current_release import ROOT,STUDY,load_release,validate_sources

def build(output_dir=None,regenerate=False,package_mode='auto',publication_ready=False):
 release=validate_sources(load_release())
 if publication_ready and release['publicationStatus']not in ['publication_authorized','published']:raise ValueError('Publication has not been authorized in the release configuration')
 site=Path(output_dir).resolve()if output_dir else ROOT/'.site'
 # A developer's existing published snapshot is an input, never a build target.
 if site==ROOT/'.site'and site.exists()and any(site.iterdir()):
  raise FileExistsError('Existing .site preserved. Choose --output-dir for an isolated local artifact.')
 if site.exists()and any(site.iterdir()):
  identity=site/'versao.json'
  if not identity.exists()or json.loads(identity.read_text(encoding='utf8')).get('cadSHA256')!=release['cadSHA256']:
   raise FileExistsError('Output directory contains another artifact; choose a new output directory.')
 site.mkdir(parents=True,exist_ok=True)
 if regenerate:runpy.run_path(str(STUDY/'build_floorplan.py'),run_name='__main__')
 docs=runpy.run_path(str(STUDY/'build_workshop_docs.py'));docs['build'](regenerate=regenerate,build_package=False,export_docs=False)
 runpy.run_path(str(STUDY/'construir.py'),run_name='__main__')
 runpy.run_path(str(STUDY/'build_share_package.py'))['ensure_package'](package_mode)
 docs=runpy.run_path(str(STUDY/'build_workshop_docs.py'));docs['build'](target=site/'docs',regenerate=False,build_package=False)
 (site/'moodboard').mkdir(exist_ok=True)
 shutil.copyfile(ROOT/'09_Referencias/Moodboard_visual_atualizado_R01.png',site/'moodboard.png')
 subprocess.run(['node',str(STUDY/'build_web.mjs'),str(site)],check=True)
 (site/'.nojekyll').write_text('',encoding='utf8')
 metadata=dict(revisao=release['cadRevision']+'-'+release['packageRevision'],cad=release['cadRevision'],cadSHA256=release['cadSHA256'],pacote=release['packageRevision'],fichas=release['fabricationRevision'],cores=release['appearanceRevision'],iluminacao=release['lightingRevision'],publicationStatus=release['publicationStatus'],publicationReady=publication_ready,commit=os.environ.get('GITHUB_SHA','local'))
 (site/'versao.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8')
 print(json.dumps(dict(directory=str(site),metadata=metadata,remotePublication=False),ensure_ascii=False));return metadata

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output-dir');parser.add_argument('--regenerate-sources',action='store_true');parser.add_argument('--package-mode',choices=['auto','verify','build'],default='auto');parser.add_argument('--publication-ready',action='store_true');a=parser.parse_args();build(a.output_dir,a.regenerate_sources,a.package_mode,a.publication_ready)
