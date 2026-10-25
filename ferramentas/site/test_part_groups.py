import copy
import csv
import json
from pathlib import Path
import unittest
from part_groups import group_panels

STUDY=Path(__file__).resolve().parent

def panel(identifier, **changes):
    return dict(id=identifier,name='Prateleira',dimensions=[400,355,18],thickness=18,rectangular=True,cadMaterial='TX',specifiedMaterial='Branco TX',finishComplete=True,remainingFinish=None,quantity=1,**changes)

class PanelGroupingTest(unittest.TestCase):
    def test_names_and_ids_do_not_split_equivalent_panels(self):
        a=panel('A');b=panel('B');b['name']='Prateleira 2'
        groups=group_panels({'panels':[a,b]}, {})
        self.assertEqual(len(groups),1);self.assertEqual(groups[0]['quantity'],2);self.assertEqual(groups[0]['ids'],['A','B'])
    def test_material_finish_grain_and_dimensions_remain_distinct(self):
        for field,value in [('specifiedMaterial','Arenza'),('thickness',15),('dimensions',[400.01,355,18]),('remainingFinish','Face externa pendente'),('grain','longitudinal'),('edges',{'front':'2mm'})]:
            with self.subTest(field=field):
                a=panel('A');b=panel('B');b[field]=value
                self.assertEqual(len(group_panels({'panels':[a,b]},{})),2)
    def test_drilling_and_drawings_remain_distinct(self):
        for field,rows in [('drilling',[{'partIds':['A'],'pattern':'x=20'},{'partIds':['B'],'pattern':'x=30'}]),('drawings',[{'partId':'A','holes':[{'x':20}]},{'partId':'B','holes':[{'x':30}]}])]:
            self.assertEqual(len(group_panels({'panels':[panel('A'),panel('B')],field:rows},{})),2)
        same={'panels':[panel('A'),panel('B')],'drilling':[{'id':'F01','item':'A','partIds':['A'],'pattern':'x=20'},{'id':'F02','item':'B','partIds':['B'],'pattern':'x=20'}]}
        self.assertEqual(len(group_panels(same,{})),1)
    def test_same_envelope_different_special_geometry_stays_separate(self):
        a=panel('A');b=panel('B');a['rectangular']=b['rectangular']=False
        parts={'A':{'v':[[0,0,0],[1,0,0],[0,1,0]],'t':[[0,1,2]]},'B':{'v':[[0,0,0],[1,0,0],[1,1,0]],'t':[[0,1,2]]}}
        self.assertEqual(len(group_panels({'panels':[a,b]},parts)),2)
        parts['B']={'v':[[4,5,0],[5,5,0],[4,6,0]],'t':[[2,1,0]]}
        self.assertEqual(len(group_panels({'panels':[a,b]},parts)),1)
        self.assertEqual(len(group_panels({'panels':[a,b]},{})),2)
    def test_all_modules_keep_every_id_quantity_and_csv(self):
        raw=(STUDY/'src/fabrication-data.js').read_text(encoding='utf-8');modules=json.loads(raw.split('=',1)[1].strip().rstrip(';'))['modules']
        totals=[0,0]
        for code,module in modules.items():
            with self.subTest(module=code):
                groups=module['panelGroups'];ids=[i for g in groups for i in g['ids']]
                self.assertCountEqual(ids,[p['id'] for p in module['panels']]);self.assertEqual(len(ids),len(set(ids)))
                self.assertEqual(sum(g['quantity'] for g in groups),len(module['panels']))
                dest=STUDY.parent.parent/'06_Entregas/Fichas_fabricacao'
                with (dest/(code+'-pecas.csv')).open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
                self.assertEqual(len(rows),len(groups));self.assertEqual(sum(int(r['Qtd']) for r in rows),len(ids))
                self.assertEqual([r['IDs CAD'].split(' | ') for r in rows],[g['ids'] for g in groups])
                totals[0]+=len(ids);totals[1]+=len(groups)
        self.assertEqual(len(modules),20);self.assertEqual(totals[0],249)
        p01=modules['P01'];self.assertEqual(len(p01['panelGroups']),15)
        shoe=next(g for g in p01['panelGroups'] if 'Peca211' in g['ids']);self.assertEqual(shoe['quantity'],6)
        print('Peças físicas / grupos:',totals)

if __name__=='__main__':unittest.main()
