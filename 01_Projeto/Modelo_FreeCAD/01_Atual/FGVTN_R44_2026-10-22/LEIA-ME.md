# R44 — referências FGVTN 400 recebidas por email

A R44 acrescenta os STEP oficiais de 400 mm à R43. A geometria instalada do apartamento permanece igual à R43: Berlin, cores, banco com duas tampas, banheiro e retirada dos apoios são preservados. As caixas do estudo R04 não foram incorporadas como montagem aprovada.

## Como consultar no FreeCAD

Abra `Guedala_Park_R44_Consolidado.FCStd`. O grupo `FGVTN_R44_Referencia` inicia oculto. Seus subgrupos `FGVTN_R44_FECHADA` e `FGVTN_R44_ABERTA` contêm seis sólidos cada, nas coordenadas originais dos STEP. Exiba somente um estado de cada vez; não são ferragens instaladas no apartamento. Para comparar os estados isolados, abra `Comparacao_STEP400_ESTUDO.FCStd`: fechada à esquerda, aberta à direita, deslocadas apenas para visualização.

## O que a geometria permite afirmar

- Uma lateral foi fornecida; não foi criado um par oficial por espelhamento.
- O estágio móvel se desloca 374,3 mm; o intermediário, 256,35 mm. O curso móvel está no intervalo documental de 375 ± 3 mm.
- O conjunto fechado ocupa 406,3 mm longitudinalmente; o aberto, 629,068 mm.
- A peça chamada `BASE_400mm` mede 297 mm no eixo longitudinal. Na montagem fechada, a extremidade móvel está 42,232 mm atrás da extremidade dianteira da base. O nome da peça não resolve essas referências.
- Não há engate removível identificado entre os produtos fornecidos. A peça `PONTEIRA` não foi assumida como engate. Não foram inventados recortes, retenções, parafusos ou arquivos de 500 mm.

## Ensaio de posicionamento — hipótese rejeitada, não prova de inviabilidade

`Ensaio_datum_HIPOTESE.json` registra uma hipótese explícita: plano Y=0 do STEP na parede X=4318; extremidade da base em Y=676; topo do perfil móvel apoiado sob o fundo das caixas R04. A transformação corrigida é rotação de −120° sobre (1,1,1), que leva X para Z, Y para X e Z para Y. O ensaio usa apenas a lateral fornecida.

Nessa hipótese, há interseção com a lateral de madeira nas duas gavetas e com a base da carcaça na gaveta inferior, tanto fechada como aberta. Os volumes de cada interseção constam no JSON. Isso rejeita esse posicionamento; não prova incompatibilidade geral do produto, pois o datum e a interface com os engates ainda não foram estabelecidos. Nenhuma madeira foi recortada para eliminar essas colisões.

O estudo R04 continua com capacidade útil 323 × 364 × 60,4/54 mm e fixação frontal direta conforme seus registros. Não há autorização de fabricação. Medidas aqui são da geometria do projeto e dos arquivos fornecidos, não do apartamento construído.

## Evidências

`Inspecao_STEP_400.json`: importação e dimensões; `Verificacao_R44.json`: comparação da R43 com a R44 reaberta, hashes e visibilidade; `STEP400_mesma_escala.png`: comparação única. As imagens iniciais `STEP400_*_axono/frente.png` usaram câmeras em transição e não servem para comparar escala ou estado de extensão.

Os arquivos STEP foram exportados em 2022 e recebidos em 22/10/2026; a data do recebimento não representa uma revisão geométrica de 2026. Fontes originais e hashes estão na pasta `Fontes`.

## Verificação final

R44 salva e reaberta nativamente. As propriedades verificadas dos 5.653 objetos originais permanecem iguais. Dos 1.429 BREP originais, 1.361 são idênticos byte a byte; 68 apresentam somente diferenças numéricas de serialização de até 1,11 × 10⁻¹⁶, com estrutura e número de valores iguais. As 7.243 propriedades de cores/materiais com arquivos associados permanecem idênticas quando comparadas pelo objeto correspondente (a numeração interna dos arquivos mudou).

Verificados separadamente: 12 novos sólidos de fabricante, 15 formas Berlin, duas tampas do banco e 76 formas BC43, todos não nulos e válidos. Apoios Peca108/Peca109 ausentes. R43 preservada com SHA-256 `ff9352b6c137e344525a68e65fe22290e3fa28d33cadd88235cfa24358a80449`; R44 `9187c163d7d827e12387e7e9c9e953b0380c55bcc8aaed3e872f83c4665d839e`.
