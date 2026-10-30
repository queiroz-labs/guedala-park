"""Integração com cópia do CSV; dados fictícios nunca preenchem o projeto."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import subprocess
from unittest.mock import patch
import importar_medidas_site as importer
from importar_medidas_site import ROOT,DEFAULT_CSV,import_file

sys.path.insert(0,str(ROOT/'ferramentas/pranchas'))
from medidas import carregar,resolver

FIXTURE=ROOT/'ferramentas/site/fixtures/Medidas_reais_ficticio_teste.json'


class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gp_import_medidas_');self.p=Path(self.temp.name)
        self.csv=self.p/'07_Imovel/Medidas_e_impactos.csv';self.csv.parent.mkdir();shutil.copyfile(DEFAULT_CSV,self.csv)
        self.report=self.p/'Relatorio_teste.md';self.input=self.p/'Entrada_teste.json'
        self.payload=json.loads(FIXTURE.read_text(encoding='utf-8'));self.original=self.csv.read_bytes()

    def tearDown(self):self.temp.cleanup()

    def run_import(self,payload=None):
        self.input.write_text(json.dumps(payload or self.payload,ensure_ascii=False),encoding='utf-8')
        return import_file(self.input,self.csv,self.report)

    def read_rows(self):
        with self.csv.open(encoding='utf-8-sig',newline='') as f:return {r['codigo_medida']:r for r in csv.DictReader(f)}

    def test_fixture_and_measured_precedence(self):
        real_hash=hashlib.sha256(DEFAULT_CSV.read_bytes()).hexdigest()
        result=import_file(FIXTURE,self.csv,self.report);rows=self.read_rows()
        self.assertEqual(result['preenchidos'],2);self.assertEqual(result['incompletos'],1)
        self.assertEqual(rows['PD-QUA']['valor_medido'],'2584 mm')
        self.assertEqual(rows['DIM-01']['valor_medido'],'2442 × 2946 mm')
        self.assertIn('TESTE FICTÍCIO',rows['PD-QUA']['evidencia_campo'])
        self.assertEqual(rows['ANC-P04']['valor_medido'],'')
        values=carregar(self.p)
        self.assertEqual(resolver(values,'PD-QUA').mm,2584)
        self.assertEqual(resolver(values,'DIM-01/1').mm,2946)
        self.assertEqual(resolver(values,'PD-QUA').origem,'medido')
        report=self.report.read_text(encoding='utf-8');self.assertIn('-16 mm',report);self.assertIn('P01|P02|P03|P04'.replace('|','\\|'),report)
        self.assertIn('arquivos',report.lower());self.assertIn('04_Moveis',report)
        self.assertEqual(real_hash,hashlib.sha256(DEFAULT_CSV.read_bytes()).hexdigest())

    def test_only_two_columns_and_supplied_rows_change(self):
        before=self.read_rows();self.run_import();after=self.read_rows()
        for code,row in before.items():
            for key,value in row.items():
                if key not in ('valor_medido','evidencia_campo') or code not in ('PD-QUA','DIM-01','ANC-P04'):
                    self.assertEqual(after[code][key],value,(code,key))

    def test_partial_dimension_does_not_use_nominal(self):
        p=copy.deepcopy(self.payload);p['medidas']=[p['medidas'][1]]
        self.run_import(p);row=self.read_rows()['DIM-01']
        self.assertEqual(row['valor_medido'],'');self.assertIn('2442 mm',row['evidencia_campo'])
        self.assertIn('DIM-01/1',self.report.read_text(encoding='utf-8'))

    def test_null_keeps_previous_measured_value(self):
        self.run_import();p=copy.deepcopy(self.payload);p['medidas']=[{**p['medidas'][0],'valor_mm':None}]
        self.run_import(p);self.assertEqual(self.read_rows()['PD-QUA']['valor_medido'],'2584 mm')

    def test_unknown_duplicate_bool_nan_negative_date_atomic(self):
        cases=[]
        for key,value in [('codigo','NAO-EXISTE'),('valor_mm',True),('valor_mm',float('nan')),('valor_mm',-3),('data_hora','2026-02-30T00:00:00Z'),('status','aceito')]:
            p=copy.deepcopy(self.payload);p['medidas'][0][key]=value;cases.append(p)
        p=copy.deepcopy(self.payload);p['medidas'].append(p['medidas'][0]);cases.append(p)
        for p in cases:
            with self.subTest(p=p):
                with self.assertRaises(ValueError):self.run_import(p)
                self.assertEqual(self.csv.read_bytes(),self.original);self.assertFalse(self.report.exists())

    def test_old_export_does_not_replace_later_field(self):
        self.run_import();before=self.csv.read_bytes();p=copy.deepcopy(self.payload)
        for r in p['medidas']:r['data_hora']='2026-10-29T00:00:00Z';r['valor_mm']=None
        result=self.run_import(p);self.assertEqual(result['antigos_ignorados'],3);self.assertEqual(self.csv.read_bytes(),before)

    def test_repeated_input_is_idempotent(self):
        self.run_import();first=self.csv.read_bytes();self.run_import();self.assertEqual(first,self.csv.read_bytes())

    def test_fixture_cannot_write_real_project(self):
        with self.assertRaisesRegex(ValueError,'Fixture'):import_file(FIXTURE,DEFAULT_CSV,self.report)
        self.assertFalse(self.report.exists())

    def test_single_command_fixture_chain_and_no_source_changes(self):
        real_hash=hashlib.sha256(DEFAULT_CSV.read_bytes()).hexdigest()
        output=self.p/'saida'
        proc=subprocess.run([sys.executable,'-B',str(ROOT/'ferramentas/estudos/medidas_do_celular.py'),
                             '--entrada',str(FIXTURE),'--csv',str(self.csv),'--saida',str(output)],
                            capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(proc.returncode,0,proc.stdout+proc.stderr)
        with (output/'campo.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
        self.assertEqual({r['codigo_medida'] for r in rows},{'PD-QUA','DIM-01'})
        self.assertTrue(all(r['valor_medido'].strip() and r['evidencia_campo'] for r in rows))
        self.assertEqual(next(r for r in rows if r['codigo_medida']=='DIM-01')['valor_medido'],'2442 × 2946 mm')
        summary=json.loads((output/'Cadeia/Cadeia.json').read_text(encoding='utf-8'))
        self.assertEqual(summary['pecas_alteradas'],0);self.assertEqual(summary['novas_folgas_negativas'],0)
        self.assertGreater(summary['pendencias_propagacao'],0)
        for name in ('Cadeia.md','Impacto.md','Pecas_diferencas.csv','Pendencias_propagacao.csv'):
            self.assertTrue((output/'Cadeia'/name).is_file());self.assertIn(name,proc.stdout)
        self.assertEqual(real_hash,hashlib.sha256(DEFAULT_CSV.read_bytes()).hexdigest())

    def test_field_path_must_be_external_before_import(self):
        with self.assertRaisesRegex(ValueError,'fora do repositório'):
            import_file(FIXTURE,self.csv,self.report,ROOT/'campo.csv')
        self.assertEqual(self.csv.read_bytes(),self.original);self.assertFalse(self.report.exists())

    def test_field_rejects_partial_dim_and_preserves_outputs(self):
        rows=list(self.read_rows().values());row=next(r for r in rows if r['codigo_medida']=='DIM-01')
        row['valor_medido']='2442 mm'
        with self.assertRaisesRegex(ValueError,'eixos'):importer.field_csv(rows)
        row['valor_medido']='2442 × 2946'
        with self.assertRaisesRegex(ValueError,'unidade'):importer.field_csv(rows)

    def test_single_command_fixture_real_guard_and_nonempty_output(self):
        from medidas_do_celular import run
        with self.assertRaisesRegex(ValueError,'Fixture'):run(FIXTURE,self.p/'bloqueada')
        self.assertFalse((self.p/'bloqueada').exists())
        with self.assertRaisesRegex(ValueError,'nova/vazia'):run(FIXTURE,self.p,self.csv)

    def test_nonobject_and_missing_inputs(self):
        self.input.write_text('[]',encoding='utf-8')
        with self.assertRaises(ValueError):import_file(self.input,self.csv,self.report)
        with self.assertRaises(FileNotFoundError):import_file(self.p/'ausente.json',self.csv,self.report)
        self.assertEqual(self.csv.read_bytes(),self.original)

    def test_failed_csv_write_restores_report(self):
        self.input.write_text(json.dumps(self.payload),encoding='utf-8');self.report.write_text('relatório anterior',encoding='utf-8')
        real_write=importer.atomic_write
        def fail_csv(path,content):
            if Path(path)==self.csv:raise PermissionError('CSV de teste bloqueado')
            return real_write(path,content)
        with patch.object(importer,'atomic_write',side_effect=fail_csv):
            with self.assertRaises(PermissionError):import_file(self.input,self.csv,self.report)
        self.assertEqual(self.report.read_text(encoding='utf-8'),'relatório anterior')
        self.assertEqual(self.csv.read_bytes(),self.original)


if __name__=='__main__':unittest.main()
