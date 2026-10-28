"""Release agreement, immutable package and safe isolated publication targets."""
from pathlib import Path
import hashlib,json,unittest,os
from unittest.mock import patch
from current_release import ROOT,STUDY,load_release,validate_sources,normalized_payload,canonical_source
from build_share_package import source_paths,write_immutable,build,verify_sealed_package
from preparar_pages import build as prepare_web
TESTROOT=Path(os.environ.get('GUEDALA_TEST_ROOT',ROOT.parent/'outputs/Publicacao/Testes'))
class CurrentReleaseTests(unittest.TestCase):
 def test_cad_and_project_agree_with_release(self):
  r=validate_sources(load_release());self.assertEqual(r['cadRevision'],'R54');self.assertEqual(r['packageRevision'],'R27')
 def test_current_document_labels_use_same_release(self):
  from plain_language import DOCUMENT_COPY
  r=load_release();self.assertIn(r['cadRevision'],DOCUMENT_COPY['cad'][0]);self.assertIn(r['packageRevision'],DOCUMENT_COPY['pacote-compartilhar'][0]);self.assertIn(r['cadRevision'],DOCUMENT_COPY['pacote-compartilhar'][1]);self.assertNotIn('R49',DOCUMENT_COPY['cad'][0])
 def test_local_release_cannot_request_publication(self):
  local=dict(load_release(),publicationStatus='local_only')
  with patch('preparar_pages.load_release',return_value=local):
   with self.assertRaisesRegex(ValueError,'Publication has not been authorized'):
    prepare_web(TESTROOT/'not-authorized',publication_ready=True)
 def test_package_technical_allowlist(self):
  paths=source_paths(load_release());self.assertEqual(len(paths),len(set(paths)))
  self.assertTrue(all(p=='07_Imovel/Medidas_e_impactos.csv' or Path(p).parts[0]in ['ESTADO_ATUAL.md','01_Programa_e_decisoes','02_Modelo_3D','03_Ambientes','04_Moveis','05_Orcamento_e_cronograma','06_Entregas','09_Referencias','ferramentas']for p in paths))
  self.assertFalse(any('06_Contratos' in p or'guedala-pessoal'in p for p in paths))
 def test_immutable_write_and_mismatch_rejection(self):
  TESTROOT.mkdir(parents=True,exist_ok=True);p=TESTROOT/'immutable.txt'
  write_immutable(p,b'original');stamp=p.stat().st_mtime_ns;self.assertFalse(write_immutable(p,b'original'));self.assertEqual(p.stat().st_mtime_ns,stamp)
  with self.assertRaises(FileExistsError):write_immutable(p,b'different')
  self.assertEqual(p.read_bytes(),b'original')
 def test_existing_site_is_not_default_target(self):
  if not(ROOT/'.site').exists():self.skipTest('No local snapshot to protect')
  with self.assertRaisesRegex(FileExistsError,'Existing .site preserved'):prepare_web()
 def test_foreign_output_directory_is_rejected(self):
  p=TESTROOT/'foreign';p.mkdir(parents=True,exist_ok=True);sentinel=p/'sentinel.txt';write_immutable(sentinel,b'untouched')
  with self.assertRaises(FileExistsError):prepare_web(p)
  self.assertEqual(sentinel.read_bytes(),b'untouched')
 def test_canonical_text_ignores_line_endings_and_bom(self):
  a=b'line 1\r\nline 2\r\n';b=b'line 1\nline 2\n';self.assertEqual(normalized_payload('example.csv',a),b);self.assertEqual(normalized_payload('example.csv',b'\xef\xbb\xbf'+a),b);self.assertEqual(normalized_payload('example.FCStd',a),a)
 def test_publication_state_is_not_technical_content(self):
  a=load_release(False);b=dict(a,publicationStatus='published',lastPublishedCadRevision=a['cadRevision'],lastPublishedPackageRevision=a['packageRevision']);p='ferramentas/site/current_release.json';self.assertEqual(canonical_source(p,json.dumps(a).encode()),canonical_source(p,json.dumps(b).encode()))
 def test_sealed_package_is_verified_without_recompression(self):
  r=load_release();p=ROOT/r['packageDirectory']/r['packageFile']
  if not p.exists():self.skipTest('Run package build first')
  before=(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns)
  with patch('build_share_package.package_payload',side_effect=AssertionError('No recompression permitted')):result=verify_sealed_package()
  self.assertFalse(result['recompressed']);self.assertEqual(before,(hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_mtime_ns))
if __name__=='__main__':unittest.main()
