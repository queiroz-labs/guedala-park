"""Aplicar as quatro decisões de 27/10 na GUI FreeCAD; não executa estudos."""
from pathlib import Path
import json
import FreeCAD as App
import FreeCADGui as Gui

ROOT = Path(__file__).resolve().parents[2]
doc = App.ActiveDocument
assert doc and Path(doc.FileName).name == 'Guedala_Park_R52_Corrigido.FCStd'
assert len(doc.Objects) == 5832
SOURCE = 'Elias, 27/10/2026: U1:A/U2:A/U3:A/U4:A; F13=A; R44=A; LIX=A. Aplicar decisoes ao CAD/fichas e criar R53, nesta conversa.'

def text(obj, name, value):
    if name not in obj.PropertiesList:
        obj.addProperty('App::PropertyString', name, 'Decisoes R53')
    setattr(obj, name, value)

changes=[]
doc.openTransaction('Decisoes R53 de 27/10/2026')
for o in doc.Objects:
    if 'CodigoFichaR14' in o.PropertiesList:
        code=o.CodigoFichaR14
        old=o.FichaR14
        o.FichaR14=f'06_Entregas/Fichas_fabricacao/{code}.html'
        text(o,'RevisaoFicha','R15')
        text(o,'FonteDecisaoR53',SOURCE)
        changes.append({'objeto':o.Name,'campo':'FichaR14','antes':old,'depois':o.FichaR14})
p02=doc.getObject('Modulo001')
text(p02,'UsoR53','Roupa de cama e volumes leves de uso eventual; requisito de conteudo total10kg incluindo organizadores. Capacidade nao demonstrada.')
text(p02,'OrganizacaoR53','Mais pesados na regiao apoiada; ponta do retorno para leves. Preservar vaos/aparencia; rever uso antes de mudar o movel.')
p13=doc.getObject('Peca350')
text(p13,'AcabamentoFacesR53','Greenplac Arenza liso nas duas faces; chapa18 preservada; produto, bordas e preco pendentes.')
text(p13,'FonteDecisaoR53',SOURCE)
text(doc.getObject('Modulo012'),'AcabamentoFacesR53',p13.AcabamentoFacesR53)
# MaterialReferencia wood e cor Arenza ja existentes permanecem.
for name,prop,delta in [('Peca144','LocalX',70),('Peca145','LocalX',70),('Peca146','LocalX',70),('Peca147','LocalY',60),('Peca148','LocalY',60),('Peca149','LocalY',60)]:
    o=doc.getObject(name); old=getattr(o,prop).Value
    setattr(o,prop,old+delta)
    text(o,'FonteDecisaoR53',SOURCE)
    o.Status='LIX=A: posicao nominal; conferir rodape, pedal/tampa, passagem e varal em gabarito fisico. Nao comprova encaixe real.'
    changes.append({'objeto':name,'campo':prop,'antes':old,'depois':old+delta,'unidade':'mm'})
ctl=doc.getObject('ControleLoopManutencaoR26')
ctl.Status='LIX=A, Elias27/10/2026: retirada temporaria aceita se demonstrada. Controle historico de manutencao nao define destino real livre do varal/passagem.'
text(doc.getObject('ApartamentoR34'),'EscopoTVR53','R44=A, Elias27/10/2026: manter TV da sala nesta etapa; metas de negociacao e custos faltantes pendentes.')
doc.recompute()
doc.Label='Guedala Park R53 - decisoes de uso e acabamentos'
doc.commitTransaction()
# Save in the GUI process to preserve GuiDocument.xml.
doc.saveAs(str(ROOT/'02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd'))
(ROOT/'02_Modelo_3D/Alteracoes_R53.json').write_text(json.dumps({'fonte':SOURCE,'base':'R52','revisao':'R53','alteracoes':changes,'limites':'Sem ensaio fisico; sem reforcos, nova carga comprovada ou mudanca de madeira; coordenadas das lixeiras nominais.'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
