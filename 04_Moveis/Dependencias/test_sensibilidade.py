import copy,unittest
from sensibilidade import model,minimum,wall_gap

class Paredes(unittest.TestCase):
 def test_pano_compartilhado_tem_mesmo_deslocamento(self):
  m=model();w=m['walls']['PAREDE-15']
  for target in ['P05','P14']:
   self.assertIn('PAREDE-15',m['targets'][target]['walls'])
   self.assertAlmostEqual(wall_gap(w,m['targets'][target]['box'],10),-10)
 def test_datum_transladado_preserva_distancia(self):
  m=model();w=copy.deepcopy(m['walls']['PAREDE-15']);b=list(m['targets']['P05']['box']);old=wall_gap(w,b,5,.5)
  w['pivot'][0]+=100;w['pivot'][1]-=200;w['segment']=[x+100 for x in w['segment']]
  for a in [0,3]:b[a]+=100
  for a in [1,4]:b[a]-=200
  self.assertAlmostEqual(wall_gap(w,b,5,.5),old)
 def test_sem_parede_no_limite_aberto_da_cozinha(self):
  m=model()
  self.assertFalse(any(w['axis']==0 and w['position']==3880 for w in m['walls'].values()))
 def test_caixas_nao_sao_alteradas(self):
  m=model();before=copy.deepcopy(m['targets']);minimum(m,{'PAREDE-15-DESLOCAMENTO':20,'PAREDE-15-ANGULO':1});self.assertEqual(before,m['targets'])

if __name__=='__main__':unittest.main()
