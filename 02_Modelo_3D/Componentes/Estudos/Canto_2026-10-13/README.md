# Canto do quarto no FreeCAD - conferência de 13/10/2026

[Prancha em cinco páginas](../../../../06_Entregas/pdf/Canto_quarto_FreeCAD_R03_2026-10-13.pdf) · Revisão editável do apartamento

A conferência encontrou três colisões no modelo de pivôs ideais: a folha B contra a primeira porta do aéreo da R01; a folha B contra uma faixa fixa aplicada na mesma face; e o retorno da folha B ao maleiro sem limitar o curso principal. A versão anterior do apartamento foi preservada.

## Proposta para aprofundar

- Principal candidata Blum CLIP top 71T7550 com limitador 70T7553.09 de 92°; articulação candidata 79T8500 de 60°. Os canecos das duas famílias pertencem à folha A. A 71T tem fechamento por mola e não recebe amortecimento integrado por inferência.
- Faixa fixa nominal de 150 mm recuada 40 mm, entre base, tampo e lateral; quatro faixas móveis de 412,5 mm, com a primeira dobradiça no lado afastado do canto. São cotas propostas, não escolhidas pelo usuário.
- Comparação alternativa: faixa nominal de 200 mm e quatro faixas móveis de 400 mm. Ela aumenta a separação à vizinha, mas não aumenta a margem ao maleiro.
- Preservados roupeiro de 650 mm, aéreo de 250 mm, face inferior a 2132 mm, topo de estudo a 2440 mm e programa inferior R02.

A faixa recuada usa um painel interno, descontando a lateral e as chapas horizontais. A faixa aplicada na face é uma frente externa completa. Essa diferença construtiva está representada nas expressões, para não criar sobreposições com a caixa.

## O que foi conferido

[Resultados dos envelopes](Resultados_envelopes.json): 88.929 pares de ângulos, principal de 0 a 92° e articulação de 0 a 60°, passo de 0,25°. A porta vizinha inteira foi envolvida por um disco que contém seu giro contínuo. O desconto entre amostras é 2,621 mm.

| Proposta | Separação inferior à vizinha no modelo ideal |
|---|---:|
| Faixa nominal de 150 mm | 48,242 mm |
| Faixa nominal de 200 mm | 95,454 mm |

A separação da folha B ao envelope dos dois planos de correr do maleiro é pelo menos 43,957 mm nesse modelo. Para a faixa recuada 40 mm, a separação analítica é pelo menos 22 mm. Esses valores não representam folgas garantidas nas ferragens reais.

[Conferência em sólidos FreeCAD](Conferencia_FreeCAD.json): oito poses, com cálculos de interseção volumétrica. Os contraexemplos são principal a 10°/articulação a 0°/vizinha a 11,055° na R01; principal a 1°/articulação a 0° com faixa aplicada; e principal a 155°/articulação a 60° contra o maleiro. A candidata recuada não apresentou essas interseções nas poses conferidas. As imagens mostram azul=A, ocre=B e vermelho=vizinha/colisão.

Os testes de sensibilidade com deslocamentos de 20+20 ou 30+30 mm são hipóteses de estudo. Não foram fornecidos pelo fabricante como limites cinemáticos. Não utilizar a dimensão de planejamento de 32 mm a 90° do catálogo como se ela fosse limite de translação do curso inteiro.

## Como usar o arquivo

Abra a revisão FCStd e selecione a planilha **Canto - ângulos e variantes - giro ideal**. Alpha/Beta/Vizinha controlam as três aberturas. Faixa = 150/200 mm compara as candidatas; Faixa = 0 reproduz a R01. Recuo = 0 mostra a faixa aplicada; Recuo = 40 mm mostra a candidata interna. As propriedades não impõem limites mecânicos.

O modelo salvo abre com as frentes fechadas e a proposta de 150/40 mm. A vista exibida ao final da conferência deixa a principal a 23,75° e a vizinha a 24° para examinar a separação. Essa pose de visualização não altera o arquivo salvo.

Os gabaritos ocultos de canecos são referências visuais. Não são dobradiças CAD reais nem gabaritos de furação. As faixas de 400 mm e as folhas de 394 mm com junta de 3 mm são hipóteses; dimensões de corte devem ser recalculadas pela aplicação Blum, incluindo calços, recobrimentos, junta e batente.

## O que impede validar as ferragens reais

O acesso ao Blum E-SERVICES foi concluído em 13/10/2026. Foram obtidos os STEP oficiais das candidatas 71T7550 e 79T8500 e importados em uma [biblioteca FreeCAD separada](Blum_oficial/README.md), com sete e quatro componentes sólidos válidos. A aplicação de canto está disponível no configurador na modalidade rápida; a mudança para a modalidade detalhada geradora de CAD/CAM provoca conflito com essa construção.

O catálogo mostra posições e regulagens, mas não foi obtida uma aplicação com a cinemática completa dos braços. É necessário reconstruir/verificar o movimento dos componentes ou montar um gabarito com ferragens e calços reais. Um STEP estático isolado ajuda no encaixe, mas não certifica toda a trajetória.

Conferir todas as combinações de abertura contra caixa, faixa, vizinhas, maleiro, pegas e trilhos, nos ajustes extremos definidos. Fechar quantidade, fixação, carga e recobrimentos antes de liberar corte. Não foi selecionado calço, amortecedor adicional ou quantidade executiva de dobradiças.

Fontes oficiais: [planejamento do canto](https://publications.blum.com/2024/catalogue/en/117/), [principal e limitadores](https://publications.blum.com/2024/catalogue/en/84/), [Blum ID20027](https://www.blum.com/file/iak0027-id20027_at_dok_bau?country=ca&language=en), [instrução do limitador](https://www.blum.com/file/clp0004-ma-481-0_ma_dok_bau?country=ca&language=en), [acesso aos dados CAD](https://www.blum.com/us/en/services/e-services/onlineproductconfigurator/). Catálogo US2025 local, páginas31/32/47, consultado visualmente. Fichas novas preservadas em `fontes`.
