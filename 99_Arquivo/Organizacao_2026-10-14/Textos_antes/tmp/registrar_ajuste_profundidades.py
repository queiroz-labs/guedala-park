from pathlib import Path
root=Path(__file__).resolve().parents[1]
stamp='**12/10/2026 - gavetas de 40 cm e proposta de profundidade do roupeiro:**'
summary=(stamp+' Elias aceitou o ajuste do escritório para corrediças nominais de 400 mm, com abertura total. '
    'Módulo externo preservado em 40 L × 45 P × 24 A cm; os 40 cm não são profundidade útil. '
    'Curso de estudo 40 cm chega a y110, sem folga garantida diante da cama aberta. '
    'Para o guarda-roupa, desenvolvida proposta de 65 cm totais com pelo menos 55 cm livres entre a face interna do fundo e a intrusão mais próxima de portas/ferragens em todo o movimento. '
    'Com fundo hipotético de 1,8 cm, pacote frontal limitado a 8,2 cm. Gabarito vestido de 50 cm mais 2,5 cm de cada lado é hipótese de estudo, não medição das roupas. '
    'A passagem cai de 54 para 49 cm no cenário de quarto 295, reserva de janela 20, cama 160 e proteção posterior mínima 1. '
    'Aumento de profundidade ainda é proposta para escolha de circulação; não registrar como aceite de Elias. '
    'Se adotado no conjunto até o teto, aéreo lateral em L passa de 222 para 217 cm, preservada junta de 3 cm. Ferragem do maleiro continua pendente. ')
files={'README.md':'output/pdf/', '01_Projeto/Resumo.md':'../output/pdf/',
       '01_Projeto/Registro_de_decisoes.md':'../output/pdf/', '01_Projeto/Painel_de_decisoes.md':'../output/pdf/',
       '01_Projeto/Portas_e_quarto/Guarda_roupa_interior_R02.md':'../../output/pdf/',
       '01_Projeto/Portas_e_quarto/Aereos_continuos_quarto_2026-09-25.md':'../../output/pdf/'}
for rel,prefix in files.items():
    p=root/rel;s=p.read_text(encoding='utf-8')
    if stamp not in s:
        first,sep,rest=s.partition('\n')
        note=summary+f'[Corte e comparação de passagem]({prefix}Ajuste_gavetas_e_profundidade_roupeiro_2026-10-12.pdf). Registros anteriores mantêm valor histórico onde superados.\n\n'
        p.write_text(first+'\n\n'+note+rest.lstrip('\n'),encoding='utf-8')
p=root/'01_Projeto/Escritorio/Setup_e_caixa_R10.md'
s=p.read_text(encoding='utf-8')
if stamp not in s:
    first,sep,rest=s.partition('\n')
    note=stamp+' Ajuste aceito: corrediças nominais 400 mm e abertura total; manter módulo 40 L × 45 P × 24 A cm e duas frentes próximas de 12 cm. Marca e amortecimento ainda não escolhidos. Na construção hipotética com frente e fundo de 18 mm, 414 mm disponíveis acomodam a referência MOVENTO 400 (403 mm, ou 404 mm na condição de montagem indicada); lateral de caixa 390 mm, não 400 mm úteis. [Desenho atualizado](../../output/pdf/Ajuste_gavetas_e_profundidade_roupeiro_2026-10-12.pdf).\n\n'
    s=first+'\n\n'+note+rest.lstrip('\n')
    s=s.replace('Com curso de45 cm apenas como hipótese, a gaveta aberta alcança y115. No modo diário, sofá começa y152:37 cm de separação longitudinal entre envelopes. Não há colisão estática entre gaveta e sofá nessa hipótese, mas operador e cadeira precisam de espaço.',
        'Atualização de 12/10: com curso de estudo de 40 cm, a gaveta aberta alcança y110. No modo diário, sofá começa y152:42 cm de separação longitudinal entre envelopes. Operador e cadeira precisam de espaço; curso efetivo depende da ferragem escolhida. A hipótese anterior de 45 cm foi superada.')
    s=s.replace('No modo hóspedes, cama começa y110 e sobrepõe a faixa x15..55: gaveta alcançaria5 cm sobre o envelope da cama em planta.',
        'No modo hóspedes, cama começa y110 e sobrepõe a faixa x15..55: frente aberta e início da cama coincidem nominalmente, sem folga de uso. A sobreposição anterior de 5 cm foi eliminada no ensaio de curso.')
    p.write_text(s,encoding='utf-8')
print('Atualizados seis registros gerais/do quarto e o estudo do escritório.')
