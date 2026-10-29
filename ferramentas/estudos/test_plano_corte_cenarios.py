"""Testes da extensão de cenários; sem CAD nem gravação de saídas."""
import copy
import csv
import json
import unittest
import plano_corte_cenarios as study


def panel(name,w,h,t=18):
    return dict(id=name,module='P01',w=w,h=h,thickness_mm=t,pattern='Branco TX',directional=False,packing_blockers=[])


class Scenarios(unittest.TestCase):
    def test_oversize_both_funds_all_scenarios(self):
        for scenario,trim,kerf in study.SCENARIOS:
            summaries,details=study.solve([panel('atual',2096,1964),panel('alternativo',2114,1964),panel('pequeno',500,500)],'teste',scenario,trim,kerf)
            r=summaries[0]
            self.assertEqual(r['paineis_cortaveis'],1)
            self.assertEqual(set(details[0]['plano']['oversized']),{'atual','alternativo'})
            self.assertFalse(r['grupo_completo_viavel'])

    def test_area_partition_and_trim(self):
        for scenario,trim,kerf in study.SCENARIOS:
            summary,details=study.solve([panel('a',1500,800),panel('b',500,800)],'teste',scenario,trim,kerf)
            r=summary[0]
            total=sum(r[k] for k in ['area_paineis_cortaveis_m2','area_refilo_m2','area_serra_m2','sobras_uteis_m2','sobras_menores_m2'])
            self.assertAlmostEqual(total,r['area_comprada_subconjunto_m2'],7)
            self.assertGreater(r['area_serra_m2'],0)
            self.assertEqual(r['area_refilo_m2']==0,trim==0)

    def test_reject_overlap_and_outside(self):
        p=[panel('a',500,500),panel('b',500,500)]
        _,details=study.solve(p,'teste','refilo10_serra4',10,4)
        old=study.motor.TRIM,study.motor.KERF
        study.motor.TRIM,study.motor.KERF=10,4
        try:
            for outside in (True,False):
                plan=copy.deepcopy(details[0]['plano'])
                first,second=plan['sheets'][0]['placements']
                second['x']=-1 if outside else first['x']
                second['y']=first['y']
                with self.assertRaises(AssertionError): study.motor.validate(plan,p,2730,1830)
        finally: study.motor.TRIM,study.motor.KERF=old

    def test_current_249_volumes_and_36_alternatives(self):
        base=study.motor.load_panels()
        with (study.ROOT/'04_Moveis/Quantitativos/Massas_por_movel.csv').open(encoding='utf-8-sig') as f:
            volumes=study.reconcile_mass(base,list(csv.DictReader(f,delimiter=';')))
        self.assertAlmostEqual(sum(volumes.values()),1.060405325,9)
        data=json.loads((study.ROOT/'04_Moveis/Quantitativos/Diferencas_nominais.json').read_text(encoding='utf-8'))
        variants,rows=study.alternatives(base,data)
        self.assertEqual(len(variants),7);self.assertEqual(len(rows),36)
        self.assertEqual(sum(r[2]=='replacement' for r in rows),11)
        for name,ps in variants.items():
            self.assertEqual(len(ps),len({p['id'] for p in ps}))
        self.assertEqual(sum(not p['packing_blockers'] for p in base),216)

    def test_direction_and_material_exclusion(self):
        a=panel('a',1800,1000);a['directional']=True;a['pattern']='Arenza'
        b=panel('b',100,100);b['packing_blockers']=['produto ausente']
        rows,details=study.solve([a,b],'teste','x',10,4)
        self.assertEqual(rows[0]['paineis_grupo'],1)
        self.assertFalse(details[0]['plano']['sheets'][0]['placements'][0]['rotated'])

    def test_quantity_edges_and_variants_do_not_inherit_tape(self):
        p=panel('a',1000,500)
        tape=dict(C0='1',C1='0',L0='1',L1='0',espessura_fita_mm='1.0',metros_propostos_retos='1.5',situacao='regra proposta')
        base=study.list_row('base',p,tape=tape)
        self.assertEqual(base['quantidade'],1)
        self.assertEqual(base['C0'],'1')
        self.assertEqual(base['metros_fita_propostos'],'1.5')
        for variant in ['P01_prateleiras723','sensibilidade_Peca245_18_para15']:
            alt=study.list_row(variant,p,tape=tape)
            self.assertEqual(alt['C0'],'')
            self.assertEqual(alt['metros_fita_propostos'],'')
            self.assertIn('pendente',alt['situacao_fita'])


if __name__=='__main__': unittest.main()
