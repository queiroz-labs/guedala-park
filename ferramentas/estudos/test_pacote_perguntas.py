"""FICTÍCIO: comportamento do consolidado; nenhum envio ou dado de pessoa real."""
import re
import unittest
import pacote_perguntas as p

class Perguntas(unittest.TestCase):
    def test_deduplicacao_conserva_origens(self):
        a=dict(pergunta='Qual prazo?',origens=['a:1'],citacoes=['a'],destinatario='RT')
        b=dict(pergunta='QUAL PRAZO!',origens=['b:2'],citacoes=['b'],destinatario='RT')
        result,_=p.deduplicate([a,b]);self.assertEqual(len(result),1);self.assertEqual(result[0]['origens'],['a:1','b:2'])
    def test_respondida_sai_e_parcial_fica(self):
        result,answered=p.deduplicate([dict(pergunta='FICTÍCIO A',status='respondida',resposta_fonte='FICTÍCIO:1'),dict(pergunta='FICTÍCIO B',status='respondida parcialmente')])
        self.assertEqual(len(result),1);self.assertEqual(len(answered),1)
        with self.assertRaises(ValueError):p.deduplicate([dict(pergunta='A',status='respondida')])
    def test_vazio_outro_alerta(self):
        r,_=p.deduplicate([dict(pergunta='FICTÍCIO',destinatario='')]);self.assertEqual(r[0]['destinatario'],'Outro');self.assertTrue(r[0]['alerta'])
    def test_sem_contato_gerado(self):
        text=p.safe('FICTÍCIO contato teste@example.invalid')
        self.assertNotIn('@',text)
        for rule in p.RULES:self.assertNotRegex(rule[3],r'[\w.+-]+@[\w.-]+\.[a-z]{2,}')
    def test_classificacao_e_fontes(self):
        rows=p.build([dict(arquivo='04_Moveis/P01/README.md',linha=10,texto='Confirmar medição do P01 antes do corte.'),dict(arquivo='04_Moveis/P03/README.md',linha=8,texto='Levantamento pendente.')])
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['id'],'PQ-001');self.assertEqual(len(rows[0]['origens']),2)

if __name__=='__main__':unittest.main()
