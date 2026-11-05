"""Testes do portao de medidas. Executar: python -B ferramentas/test_verificar_medidas.py"""
import unittest
import verificar_medidas as v


class PortaoDeMedidas(unittest.TestCase):
    def erros(self, linha_medidas, extra=''):
        texto = '"""Estudo."""\n' + (linha_medidas + '\n' if linha_medidas else '') + extra
        return v.julgar('ferramentas/estudos/novo.py', texto)

    def test_sem_cabecalho_reprova(self):
        self.assertEqual(len(self.erros('')), 1)

    def test_fontes_validas_passam(self):
        for fonte in ['# MEDIDAS: oficial, 09_Referencias/Plantas_e_manuais/Planta_oficial.pdf',
                      '# MEDIDAS: fatos.json (pe-direito)',
                      '# MEDIDAS: manual Blum, p. 12',
                      '# MEDIDAS: campo, 07_Imovel/Medidas_e_impactos.csv',
                      '# MEDIDAS: Elias 04/11/2026 no chat: vao de 80 cm',
                      '# MEDIDAS: nao se aplica - so le o CSV existente e confere somas']:
            self.assertEqual(self.erros(fonte), [], fonte)

    def test_fonte_vaga_reprova(self):
        self.assertEqual(len(self.erros('# MEDIDAS: valores tipicos')), 1)
        self.assertEqual(len(self.erros('# MEDIDAS: nao se aplica')), 1)
        self.assertEqual(len(self.erros('# MEDIDAS: nao se aplica - curto')), 1)

    def test_hipotese_sem_elias_reprova(self):
        self.assertEqual(len(self.erros('# MEDIDAS: oficial, mas com hipotese de 3 cm de folga')), 1)
        self.assertEqual(self.erros('# MEDIDAS: Elias 04/11/2026 pediu hipotese de folga 3 cm'), [])

    def test_cabecalho_depois_da_linha_15_nao_conta(self):
        texto = '\n' * 20 + '# MEDIDAS: oficial\n'
        self.assertEqual(len(v.julgar('ferramentas/estudos/novo.py', texto)), 1)

    def test_escopo(self):
        self.assertTrue(v.escopo('ferramentas/estudos/novo.py'))
        self.assertTrue(v.escopo('04_Moveis/P03/calcular.py'))
        self.assertFalse(v.escopo('ferramentas/verificar_x.py'))
        self.assertFalse(v.escopo('ferramentas/estudos/test_x.py'))
        self.assertFalse(v.escopo('ferramentas/site/build_web.py'))
        self.assertFalse(v.escopo('04_Moveis/README.md'))


if __name__ == '__main__':
    unittest.main()
