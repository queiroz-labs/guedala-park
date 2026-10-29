"""Contraprovas da auditoria, sem importar calculadores anteriores."""
import copy
import unittest
from decimal import Decimal as D
from auditoria_independente import (expand_panels,tape_from_edges,hardware_from_sources,
                                    validate_sheet,rounded,RHO)


class IndependentAudit(unittest.TestCase):
    def test_expand_counts_ids_not_grouped_rows(self):
        rows=[{'IDs CAD':'a | b','Qtd':'2','C nominal mm':'2000','L nominal mm':'500',
               'Esp. envelope mm':'18','Especificação documental':'x','Contorno':'Retangular'}]
        self.assertEqual(len(expand_panels(rows,'P01')),2)
        rows[0]['Qtd']='3'
        with self.assertRaises(ValueError):expand_panels(rows,'P01')

    def test_tape_orientation_and_missing_is_not_zero(self):
        panel={'c':D(2000),'l':D(500)}
        row={'C0':'1','C1':'0','L0':'1','L1':'0','metros_propostos_retos':'2.5'}
        self.assertEqual(tape_from_edges(panel,row),D('2.5'))
        row['metros_propostos_retos']=''
        self.assertIsNone(tape_from_edges(panel,row))

    def test_piece_rounding_differs_from_group_rounding(self):
        values=[D('.00006'),D('.00006')]
        self.assertNotEqual(sum(rounded(v*D('1.1'),4) for v in values),rounded(sum(values)*D('1.1'),4))

    def test_hardware_does_not_double_count_decisions_or_minifix_components(self):
        row={'item':'Caixas Minifix','quantity':12,'unit':'unidades'}
        hardware={'P19':{'hardwareRows':[row,dict(row,item='Pinos Minifix')],
                         'decisions':[row,dict(row,item='Pinos Minifix')]}}
        joints=[{'movel':'P19','conector':'Minifix 15','quantidade':'8','cavilhas':'8'}]
        inv,pending,doc=hardware_from_sources({'modules':hardware},joints)
        self.assertEqual(inv['P19','Minifix 15','conjunto','proposta condicional'],8)
        self.assertEqual(doc['P19','Caixas Minifix'],12)
        self.assertEqual(pending,[])

    def test_missing_hardware_never_becomes_zero(self):
        tech={'modules':{'P01':{'hardwareRows':[{'item':'fixador','quantity':None,'unit':'un'}]}}}
        inv,pending,_=hardware_from_sources(tech,[])
        self.assertEqual(inv,{})
        self.assertEqual(pending,[('P01','fixador')])

    def test_sheet_rejects_kerf_or_duplicate_placement(self):
        panels={'p':{'c':D(50),'l':D(40)}}
        sheet={'placements':[{'id':'p','x':10,'y':10,'w':50,'h':40,'rotated':False}],
               'cuts':[{'parent':[10,10,80,80],'piece':'p','w':50,'h':40,'vertical_first':True,
                        'children':[[63.2,10,26.8,80],[10,53.2,50,36.8]]}],
               'free':[[63.2,10,26.8,80],[10,53.2,50,36.8]]}
        self.assertEqual(validate_sheet(sheet,panels,100,100)[0],['p'])
        wrong=copy.deepcopy(sheet);wrong['cuts'][0]['children'][0][0]=60
        with self.assertRaises(ValueError):validate_sheet(wrong,panels,100,100)
        wrong=copy.deepcopy(sheet);wrong['placements']*=2
        with self.assertRaises(ValueError):validate_sheet(wrong,panels,100,100)

    def test_sheet_rejects_rotation_when_directional(self):
        panel={'p':{'c':D(50),'l':D(40)}}
        sheet={'placements':[{'id':'p','x':10,'y':10,'w':40,'h':50,'rotated':True}],
               'cuts':[],'free':[]}
        with self.assertRaises(ValueError):validate_sheet(sheet,panel,100,100,directional=True)

    def test_density_comes_from_finished_sheet_and_not_rounded_generic_value(self):
        self.assertAlmostEqual(float(RHO),690.1446901446901)
        self.assertEqual(RHO*D('2.75')*D('1.85')*D('.018'),D('63.20000000000000000000000000'))


if __name__=='__main__':unittest.main()
