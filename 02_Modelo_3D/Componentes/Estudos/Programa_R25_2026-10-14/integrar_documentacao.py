from pathlib import Path
import shutil
root=(Path(__file__).resolve().parent / '.').resolve();cad=(Path(__file__).resolve().parent / '../..').resolve();project=(Path(__file__).resolve().parent / '../../..').resolve();repo=(Path(__file__).resolve().parent / '../../../..').resolve()
def write(p,t):p.write_text(t,encoding='utf-8')

delivery=((Path(__file__).resolve().parent / '../../04_Documentacao/Entrega_atual_R24.md').resolve()).read_text(encoding='utf-8')
delivery=delivery.replace('Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd','Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd',1).replace('Guedala_Park_R24_Implantacao_Corrigida.FCStd','Guedala_Park_R25_Programa_Conferido.FCStd',1)
anchor='## Correções de implantação R24'
new='''## Ajustes do programa R25

Espelho lateral centralizado na lateral composta atual do roupeiro, corrigindo15mm sem alterar vidro/base. Cabeceira aprovada emdois painéis agora representada dentro do mesmo envelope; não definiu junta ou corte. [Alteração, conferência e limites](Programa_R25_2026-10-14/README.md): versão salva válida, espelho sem interpenetração contra959 alvos e ocupação da cabeceira exatamente preservada.

[Revisão integrada](Revisao_integrada_R23_2026-10-14/README.md) distingue erros corrigidos de contatos entre gabaritos e pendências físicas. As novas lacunas contra arquitetura foram conferidas:12portas comuns/canto/G2 em47 situações; retirada elevada das bandejas e encontros do escritório com sofá corrigido também concluídos em seus escopos. Não repetiu as varreduras antigas nem homologa fabricação.

'''
assert anchor in delivery;write((Path(__file__).resolve().parent / '../../04_Documentacao/Entrega_atual_R25.md').resolve(),delivery.replace(anchor,new+anchor,1))

state=(Path(__file__).resolve().parent / '../Canto_2026-10-13/Cinematica_R03/Estado_noturno.md').resolve()
t=state.read_text(encoding='utf-8').replace('apartamento R24 (implantação corrigida / base R23 / espelhamento R20)','apartamento R25 (programa conferido / implantação R24 / base R23)',1)
anchor='### Implantação R24 — correções comprovadas e continuidade'
new='''### Programa R25 — espelho/cabeceira e revisão ampliada

Arquivo atual: Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd; ler README/Entrega_atual_R25.md. Aderencia_programa_R24 confrontou13conjuntos/73raízes com documentos locais. Achados comprovados: espelho500×1800×5/base200 mantinha centro3600,15mm antes da lateral composta650mm (painelPeca207 de568 +apoioReferenciaCorrerR001 de82), centro3615. R25 desloca somenteY+15, margens nominais75/75. Face/apoios/fixação/adesivo continuam propostas; não centralizar só no painel568.

Cabeceira emdois painéis aprovada21/09 estava emblocoPeca107. R25 acrescenta2Part::Box e1Part::Compound no grupo-fonte do quarto, mantém envelope50×1600×950 e apontaLinkEspelhoPecaR010 para composto. Bloco antigo oculto/histórico preservado. Divisão central ILUSTRATIVA, não junta/corte/espessura acabada aprovada.5895 objetos anteriores: pais/expressões preservados, Placement do espelho e alvo doLink alterados, rótulos informativos;3objetos novos/5898final, nenhumaInvalid/R24SHAinalterado. Conferencia_R25 abre versão salva emprocessoisolado: espelho×959alvos separadoBBox seminterpenetração, diferença volumétrica novacabeceira−antiga eantiga−nova0, matrizes/envelopespersistentes. Não repetir esses testes. PlantaR25 inspecionada, índices/galeria atuaisR25.

Movimentos_arquitetura_R24 concluiu somentelacunas reais identificadas:12portasR10 +2cantoR04 em30/60/86, G2em100/200/300/400/500.47situações/24516pares afastadosBBox, semcomuns/erros; guiasMOVENTOestáticas fora translação. Complementos_R24:6segmentos exatos de2bandejas carregadas comG2aberta500 contra27paredes/9pisos=2052envoltórias afastadas;2gavetas escritório0–400 contra5sofaprimitivas corrigidas=80envoltórias afastadas,420mm nominalY;52peças do aéreo comrot/translaçõeshorizontais/Zinvariável,1101mm mínimo acima sofá. Semrepetir testes antigos. Esses resultados permanecem aplicáveis: armários/sofá não mudaramR25.

Encontros standalone:13comuns de gabaritos persistem classificados, não erros eliminados.10mesa×Lina: caixas cheias incluem vazios reais da cadeira, posiçõesiguais documento23/09;3enchimento×box:30cm/altura/forma/perfis são hipóteses sem medição. Não mover cadeiras/mesa/box/removerenchimento para chamar aprovado. Tanque×bancada 'a recortar' permanece pendência real de produto/recorte. Decoração não modelada não foi cancelada; não inventar cotas de render.

Continuar revisão direcionada até19h por solicitação expressa de Elias, procurando inconsistências ainda não documentadas no modelo/programa/posições. Reutilizar a matriz de cobertura e resultados concluídos; novos cálculos só emlacuna concreta/escopoafetado. Não repetir fotos/varreduras/reaberturas para preencherprazo, não mexer contatos internosSTEP semdados. Teto semsólido nãohomologado; medidas físicas/cargas/fixação/tolerâncias/batentes/instalação seguem pendentes. Fonte canônica éR25, anteriores preservadas. Fechar eencerrar agendamento até19h conforme plano.

'''
assert anchor in t;write(state,t.replace(anchor,new+anchor,1))

plan=(Path(__file__).resolve().parent / '../../04_Documentacao/Plano_ate_19h_2026-10-14.md').resolve();t=plan.read_text(encoding='utf-8')
t=t.replace('Revisão atual: [R24](Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd). [Conjunto atual e pendências](Entrega_atual_R24.md).','Revisão atual: [R25](Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd). [Conjunto atual e pendências](Entrega_atual_R25.md).')
write(plan,t)

index=(Path(__file__).resolve().parent / '../../04_Documentacao/Historico_FreeCAD.md').resolve();t=index.read_text(encoding='utf-8');heading='# Apartamento no FreeCAD — revisões de estudo\n'
new='''
[Programa conferido — R25](Programa_R25_2026-10-14/README.md): **apartamento atual**. Espelho centralizado na lateral atual e cabeceira emdois painéis, preservando envelopes e controles. [Arquivo/resultados](Entrega_atual_R25.md) · [Revisão integrada](Revisao_integrada_R23_2026-10-14/README.md) · [Galeria atual](Galeria.html).
'''
t=t.replace(heading,heading+new,1).replace('[Implantação corrigida — R24](Implantacao_R24_2026-10-14/README.md): **apartamento atual**.','[Implantação corrigida — R24](Implantacao_R24_2026-10-14/README.md): base preservada, incorporada àR25.',1);write(index,t)

gallery=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R28_2026-10-14.html').resolve();old=gallery.read_text(encoding='utf-8');archive=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R24_2026-10-14.html').resolve()
assert not archive.exists();shutil.copy2(gallery,archive)
t=old.replace('FreeCAD R24','FreeCAD R25').replace('FreeCAD · R24','FreeCAD · R25').replace('Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd','Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd').replace('Entrega_atual_R24.md','Entrega_atual_R25.md').replace('Implantacao_R24_2026-10-14/Planta_corrigida_R24.png','Programa_R25_2026-10-14/Planta_R25.png').replace('Planta atual R24:','Planta atual R25:')
t=t.replace('Referências de hóspedes e tanque antigo ocultas.','Referências de hóspedes e tanque antigo ocultas; espelho recentralizado e cabeceira em dois painéis ilustrativos.')
write(gallery,t)

for p in [(Path(__file__).resolve().parent / '../../../../README.md').resolve(),(Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),(Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),(Path(__file__).resolve().parent / '../../../../01_Programa_e_decisoes/Registro_de_decisoes.md').resolve(),(Path(__file__).resolve().parent / '../../../../01_Programa_e_decisoes/Painel_de_decisoes.md').resolve()]:
    t=p.read_text(encoding='utf-8').replace('**14/10/2026 — FreeCAD atual R24:**','**14/10/2026 — FreeCAD atual R25:**',1).replace('Entrega_atual_R24.md','Entrega_atual_R25.md',1)
    marker='A revisão global corrigiu o sinal de rotação do sofá Daiane e ocultou referências antigas, preservando o modelo e a implantação aprovada.'
    if marker in t:t=t.replace(marker,marker+' R25 recentraliza o espelho lateral e representa a cabeceira em dois painéis dentro do envelope preservado.',1)
    write(p,t)
print('DOCUMENTATION_R25_INTEGRATED')
