# Banheiro — portas comuns R12

[Apartamento atual](Guedala_Park_R12_Banheiro_Simples.FCStd) · [Fechado](Banheiro_Fechado_R12.png) · [Aberto](Banheiro_Aberto60_R12.png) · [Montagem](Montagem_R12.json) · [Entorno corrigido](Entorno_corrigido_R12.json)

A R12 incorpora a R11 e substitui as duas frentes volumétricas do banheiro por propostas de portas comuns. Preserva gabinete suspenso fechado, bege liso/sem puxador saliente, laterais claras e armário raso com toda a frente espelhada, conforme [decisões vigentes](../../../Banheiro/Decisoes_consolidadas_2026-09-18.md). Nenhuma cota, vidro, adesivo, furação ou compra liberados. Simplicidade é a prioridade autorizada por Elias.

## Proposta

| Elemento | Dimensão/solução de estudo |
|---|---|
| Gabinete inferior | Envelope600×420×545 preservado; duas portas297×543×18, dobradiças nas laterais externas |
| Interior inferior | Centro sem divisória, vão de madeira564×382×509; sifão/conexões e recortes ainda não detalhados |
| Espelhado | Envelope600×150×750 preservado; duas folhas297×748 com painel18 e espelho4 aplicado |
| Camadas do espelhado | Frente do vidro y0–4, madeira4–22, início do corpo24, traseira150; contato ideal sem camada de adesivo modelada |
| Interior espelhado | Vão de madeira564×108×714; não retirar espaço para tubulação sem escolher/revisar o percurso |
| Prateleiras removíveis | Duas560×104×18, posições z244/488; três alturas livres nominais226, folgas2 nas laterais/frente/trás |
| Dobradicas | Dez71B3550 e dez173H7100: duas por folha inferior e três por folha espelhada;60 componentes individuais válidos |
| Juntas das portas | Externas2 e central2; recobrimento16/K5/calço distância0, canecos Ø35×13 |
| Fixação do calço | Linha37 a partir da borda frontal da lateral: y57 inferior/y61 espelhado; passo32 |
| Curso de estudo | 0–86° por expressão; limitador comum70T3553 candidato, montagem/contato físico pendentes |

O espelho aplicado sobre painel permite a mesma dobradiça comum, sem caneco no vidro. Substrato/proteção para banheiro, tipo/espessura do espelho, arestas, adesivo/retenção e suas espessuras/carga devem ser definidos com os fornecedores antes de fabricação. O vidro e a madeira estão em contato ideal no CAD; a fixação não foi homologada. Não classificar o modelo como espelho instalado seguro apenas por não haver colisões.

As prateleiras são propostas com quatro apoios comuns por peça; pinos/furação/carga não foram modelados ou liberados. As embalagens do programa ainda precisam de conferência. O fundo inferior continua inteiro como referência, sem recortes arbitrários para pontos desconhecidos; centro livre não comprova a instalação hidráulica nem a manutenção do sifão.

## Quantidade e peso de referência

A calculadora oficial Blum recomendou **três dobradiças** no cenário da frente748×297×18/MDF900 kg/m³ com adicional2,5 kg, peso arredondado6,1 kg. [Prova](Fontes/Quantidade_espelhado_BlUM.png) e [parâmetros](Fontes/Quantidade_espelhado_BlUM.json). O campo “peso do puxador” foi usado para somar **espelho + pega + reserva**, não para especificar puxador de2,5 kg. Hipótese do espelho4/2500 kg/m³:2,22 kg; pega0,2; arredondamento para2,5. Densidades/material/peso reais não confirmados. O ensaio inicial19 mm foi corrigido para18 antes de registrar a referência usada.

Pelos volumes CAD já com canecos, cenário900/2500/pega0,2: inferior2,79 kg por folha; espelhado5,99 kg. A calculadora usa painel bruto e reserva adicional, por isso o número6,1 não é a mesma conta. Duas dobradiças inferiores são candidatas por massa/altura abaixo da referência C4,7 kg/1016 mm R10; não nova calculadora individual. `Medidas_carga_R12.json`. Regulagem comum de profundidade0,5 proposta, como R10; quantidade de parafusos/material/carga de parede ainda pendentes.

## Conflitos encontrados e correções simples

**Luzes:** as duas barras laterais ilustrativas originais interceptavam folhas/espelho e braços da dobradiça a30/60/86. Agora são propostas duas barras frontais **fixas**, acima e abaixo do espelhado,560×7×20: x4060/y5130, z1110/1910. Mantida a intenção de luz frontal para maquiagem; luminária, difusão, potência/fotometria, elétrica e conforto visual não foram definidos. A localização lateral era proposta de imagem, não posição executiva aprovada. Não criar cabeamento móvel nas portas.

**Entrada:** a folha de referência do banheiro está representada aberta a90°, com700 mm não medidos. Intercepta a porta direita do gabinete inferior durante a abertura60° (225.029 mm³ no ensaio). A condição simples proposta é **fechar a entrada antes de abrir o gabinete inferior**. Não há intertravamento físico ou eletrônico. O controle `PortaEntradaBanheiroR12` permite estudar entrada0 fechada/90 original aberta; eixo, folha, maçaneta e medidas acabadas continuam desconhecidos. Manter a porta original conforme decisão aprovada e reconferir essa condição quando houver levantamento; não transformar700 em cota medida.

**110°:** portas direitas atingem a parede, e o espelho aplicado chega a interceptar a própria lateral (1102,24 mm³). Mantido estudo86 e limitador padrão candidato. Isso não é resolvido por um limite de software: exige batente físico correto antes da execução. Não alterar material nem deslocar ferragem arbitrariamente para apagar contatos. Diagnóstico inicial em `Entorno_R12.json`.

## Conferência

- Quatro painéis com canecos, dois espelhos e60 componentes de ferragem válidos.16 posições individuais0/30/60/86 contra própria madeira/vidro, frentes vizinhas fechadas e ferragens, sem interpenetração relevante. Três cenários simultâneos iguais passaram. Resíduos eixos1,29e−12/caneco1,02e−12 mm: reconstrução, não homologação física. `Auditoria_R12.json` inclui vidro; auditoria inicial só do painel foi preservada separadamente.
- Varredura planar173 posições por folha/0,5° até86, incluindo a espessura total do conjunto espelhado: dois pares com alturas sobrepostas separados por envoltórias amostradas, mínimo projetado1,59 mm. Não é distância euclidiana, prova contínua ou tolerância. `Varredura_frentes_R12.json`.
- Com luzes corrigidas e **entrada ideal fechada**,16 posições de frentes/espelhos/ferragens contra80 paredes inteiras e volumes diretos do banheiro, sem hits. Não valida a alavanca real da Arion, todos os estados da entrada, pessoa, sifão ou tubulação. Cuba/torneira são os volumes de referência existentes. `Entorno_corrigido_R12.json`.
- Adição das duas prateleiras: oito posições das duas folhas superiores contra as novas peças, mais madeira estática, sem hits; formas válidas. Não repetidos os testes das revisões anteriores nem a varredura das frentes, que não mudou. `Prateleiras_R12.json`.
- R12 salva/reaberta; primeiro controle inferior e último espelhado30→0 válidos/atualizados. Entrada0/90 válida,90 reproduz exatamente a caixa original da folha. Estado salvo: quatro portas0, entrada90 original. `Reabertura_R12.json`. Prateleiras adicionadas depois desta conferência de controles e salvas, sem mudar as expressões. Duas vistas estáticas salvas/inspecionadas, equipamentos simplificados.

## Edição, limites e continuação

Editar **Abertura** dos quatro controles no grupo`R12 - abrir portas comuns (Abertura em graus)`, nomes no campo`control` de `Montagem_R12.json`; a propriedade da folha é vinculada/somente leitura. Curso86 é estudo, não confirmação do70T3553. Juntas informativas bloqueadas; alterar dimensões exige revisar vidro, canecos, ferragem, carga, iluminação e encontro com a entrada. Grupos históricos das frentes anteriores ficam ocultos.

Sobreposições internas da71B3550 já presentes na fonte STEP, MOVENTO/fundo e70T3553 seguem sem causa determinada. Nenhuma compensação especial criada. Carga, fixação na madeira/parede, tolerâncias, proteção do banheiro, vidro/adesivo, hidráulica e porta real continuam pendentes. Não liberar corte ou compra.

Próximo trabalho independente: gaveta baixa de limpeza, que não faz parte das nove R08 e ainda tem caixa hipotética442; depois trilhos/roldanas comuns do roupeiro/maleiro e basculante do cesto, preservando o programa. Não repetir testes prontos para tentar substituir dados físicos ausentes.

Reprodução por etapas, apenas em revisão nova: `montar_banheiro.py`, depois `corrigir_luzes_entrada.py`, vistas e `prateleiras_espelhado.py`. Gerador/correções protegidos contra duplicação; não reexecutar sobre revisão pronta. Auditorias guardam métodos e escopos, não são validação de instalação.
