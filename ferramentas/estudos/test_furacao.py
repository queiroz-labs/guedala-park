"""Casos adversariais: rejeicao de pares quebrados e interferencias internas."""
import unittest
from conferir_furacao import audit,required_hinges,segment_distance


class Conferencia(unittest.TestCase):
    def panel(self):
        return dict(id='fixture',mod='P01',c=200,l=200,t=15,box=[0,0,0,200,200,15],axes=[0,1,2])

    def h(self,**kw):
        h=dict(movel='P01',peca='fixture',furo='A',face='A',x=50,y=50,diametro=8,profundidade=8,situacao='nominal/proposta',parametros='',par='',papel='',grupo='',gx=50,gy=50,gz=0,nx=0,ny=0,nz=1,curso_material=15,tipo='cavilha')
        h.update(kw);return h

    def codes(self,holes):
        return {i['tipo'] for i in audit(holes,{'fixture':self.panel()})[0]}

    def test_15mm_reserva_3mm_inclusiva(self):
        self.assertIn('PROFUNDIDADE',self.codes([self.h(profundidade=12)]))
        self.assertNotIn('PROFUNDIDADE',self.codes([self.h(profundidade=11.9)]))

    def test_par_ausente(self):
        self.assertIn('PAR_AUSENTE',self.codes([self.h(par='P',papel='topo')]))

    def test_passagem_confirmat_intencional_nao_exime_furo_cego(self):
        h=self.h(tipo='Confirmat passagem face',diametro=7,profundidade=15,passante_previsto='sim; passagem Confirmat')
        self.assertNotIn('PROFUNDIDADE',self.codes([h]))
        h['tipo']='cavilha'
        self.assertIn('PROFUNDIDADE',self.codes([h]))

    def test_catalogo_e_correcao_preservam_pares(self):
        import tempfile
        from pathlib import Path
        from gerar_furacao import generate,ROOT,panels
        from conferir_furacao import read
        with tempfile.TemporaryDirectory() as tmp:
            dest=Path(tmp);generate(ROOT/'06_Entregas/Fichas_fabricacao',dest)
            holes=[h for p in dest.glob('P??-coordenadas.csv') for h in read(p)]
            self.assertEqual(len(holes),2286)
            self.assertTrue(all(h['diametro'] and h['profundidade'] for h in holes))
            self.assertFalse(any(h['tipo']=='Minifix Ø8 topo' for h in holes))
            issues,_,_=audit(holes,panels(ROOT/'06_Entregas/Fichas_fabricacao'))
            self.assertEqual({r['tipo'] for r in issues},{'ACESSO'})
            self.assertFalse(any(r['movel']=='P17' for r in issues))

    def test_tolerancia_de_par(self):
        a=self.h(par='P',papel='topo');b=self.h(furo='B',par='P',papel='face',gx=50.51,nz=-1)
        self.assertIn('PAR_DESALINHADO',self.codes([a,b]))
        b['gx']=50.5;self.assertNotIn('PAR_DESALINHADO',self.codes([a,b]))

    def test_faces_opostas(self):
        a=self.h();b=self.h(furo='B',face='B',gz=15,nz=-1)
        self.assertIn('CRUZAMENTO_INTERNO',self.codes([a,b]))
        b.update(x=82,gx=82);self.assertNotIn('CRUZAMENTO_INTERNO',self.codes([a,b]))

    def test_cruzamento_topos(self):
        a=self.h(face='topo-C0',gx=0,gy=50,gz=7.5,nx=1,nz=0,profundidade=80,curso_material=200)
        b=self.h(furo='B',face='topo-L0',gx=50,gy=0,gz=7.5,ny=1,nz=0,profundidade=80,curso_material=200)
        self.assertIn('CRUZAMENTO_INTERNO',self.codes([a,b]))
        self.assertEqual(segment_distance([0,50,0],[80,50,0],[50,0,0],[50,80,0]),0)

    def test_cup_runner_overlap(self):
        self.assertIn('SOBREPOSICAO_FACE',self.codes([self.h(tipo='caneco',diametro=35),self.h(furo='B',tipo='corredica',x=54,diametro=5)]))

    def test_grupo_intencional(self):
        self.assertNotIn('SOBREPOSICAO_FACE',self.codes([self.h(grupo='G'),self.h(furo='B',grupo='G')]))

    def test_dado_ausente_nao_passa(self):
        self.assertIn('PARAMETRO',self.codes([self.h(profundidade='')]))

    def test_borda(self):
        self.assertIn('BORDA',self.codes([self.h(x=3)]))

    def test_envelope_blum(self):
        self.assertEqual(required_hinges(500,1016,4),3)
        self.assertEqual(required_hinges(620,750,5),3)
        self.assertIsNone(required_hinges(700,750,5))

    def test_ferramenta_bloqueada_por_fechamento(self):
        p=self.panel();block=dict(id='bloqueador',mod='P01',c=200,l=200,t=15,box=[0,0,-15,200,200,0],axes=[0,1,2])
        h=self.h(tipo='Minifix Ø15 corpo')
        issues,_,deps=audit([h],{'fixture':p,'bloqueador':block})
        self.assertIn('ACESSO',{i['tipo'] for i in issues})
        self.assertEqual(deps[0]['antes_de_instalar'],'bloqueador')


if __name__=='__main__':unittest.main()
