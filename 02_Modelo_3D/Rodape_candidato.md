# Rodapé de parede — candidato externo

**Situação: entrega limitada à macro e ao teste, por instrução de Elias nesta conversa.** R54, base e release permanecem vigentes e intactos.

Altura **80 mm**, Z global de 0 a 80 mm: Elias, 30/10/2026, “deixe o rodapé de todo meu projeto em 8cm”. Espessura **15 mm nominal, a confirmar**, sem produto presumido. Branco liso fosco, sem frisos; referência visual offwhite, não Branco TX.

Arquivo nativo: `../outputs/Rodape_candidato/Guedala_Park_Rodape_8cm_candidato.FCStd`, salvo pela GUI. Grupo novo `Rodape_8cm`, sete subgrupos de ambiente e 47 caixas por trechos. `EspessuraNominal` concentra a espessura; as dimensões normais e os recuos usam expressões. Alterá-la exige repetir recortes e verificações. Nenhum objeto anterior foi movido ou renomeado.

## Comprimentos geométricos

| Ambiente | Referência do site, antes dos móveis (m) | Faces nativas sem recortes (m) | Candidato, após interferências e juntas (m) |
|---|---:|---:|---:|
| quarto | 12,25 | 11,050 | 8,32997 |
| escritorio | 9,75 | 8,700 | 8,52999 |
| sala | 8,90 | 7,590 | 7,46000 |
| circulacao | 0,80 | 1,290 | 0,86000 |
| cozinha | 5,33 | 4,120 | 3,19093 |
| lavanderia | 4,12 | 3,130 | 2,82897 |
| banho | 5,96 | 5,560 | 2,69495 |

Áreas vinílicas: **28.37089 m**, versus 37,03 m da referência e 35 m da verba com transições. Diferenças geométricas de -8.65911 m e -6.62911 m, respectivamente. Não são sobra financeira nem revisão da verba: não incluem perdas/transições e o escopo atrás de móveis depende da contratação.
Todos os ambientes: **33.89481 m**. Banheiro/lavanderia são contados separadamente e continuam com acabamento e solução de borda pendentes. A comparação da verba de 35 m usa somente as áreas vinílicas.

## Onde há e onde não há

- Faces internas das paredes inteiras nativas, adjacentes aos pisos existentes. Nenhuma correção das diferenças entre CAD e planta gráfica do site.
- Sem parede virtual em janelas, peitoris, portas ou vergas. A exclusão sob janelas explica parte da diferença em relação à referência de 37,03 m, que as conta.
- Interrompido em toda a projeção da interseção exata com objetos existentes: fundo/proteção posterior do guarda-roupa, apoios, folhas e elementos do banheiro. Margem computacional de 0,01 mm no recorte; não é tolerância de instalação.
- No box, piso, enchimento e revestimentos ocupam a faixa global de 0–80 mm. Esses encontros ficaram interrompidos; não se elevou o rodapé nem se alterou a geometria existente. A solução física do box permanece pendente.
- Dois retornos de 100 mm na circulação encontram a representação `Peca062` (parede em corte), sendo omitidos sem alterar sua visibilidade. Isso não decide eliminar retornos físicos da parede.
- Juntas de topo nos cantos, sem sólidos sobrepostos. O rodapé do móvel do cesto, `PecaCestoR001`, não mudou.

## Interferências e preservação

33 ocorrências por objeto/parede (arquivo externo: `../outputs/Rodape_candidato/Rodape_interferencias.csv`): penetrações normais de 5, 10 ou 15 mm; projeções sobrepostas são unidas antes de medir o desconto. A caixa de interseções B-spline é limitada à faixa inicial de 15 mm, pois a superfície de suporte pode ter caixa maior que o recorte. Nenhum móvel foi deslocado.

47 trechos (arquivo externo: `../outputs/Rodape_candidato/Rodape_trechos.csv`) e resumo/assinaturas (arquivo externo: `../outputs/Rodape_candidato/Rodape_resumo.json`). As 1.489 geometrias próprias anteriores conservam volume, área, faces, vértices, caixa, centro de massa e posição global; expressões anteriores preservadas. Assinaturas completas ficam com o candidato, com SHA no resumo. A inspeção preliminar isolada executada antes da interrupção passou nos 106 cenários. A composição com o piso e sua verificação integral pertencem à terceira sessão.

## Reprodução

`ferramentas/estudos/modelar_rodape.FCMacro` executa na GUI com GP_REPO e GP_RODAPE_DIR apontando ao repositório e à saída externa. Recusa qualquer candidato existente. A saída deve ser uma pasta externa vazia; não há dependência da macro do piso. `GP_RODAPE_CLOSE_GUI=1` só fecha uma instância que começou sem documentos. As funções ortogonais estão incorporadas à macro; teste independente em `ferramentas/estudos/test_rodape_geometria.py`, sem abrir FreeCAD.

## Perguntas para concluir

1. A espessura nominal de 15 mm pode ser adotada após definir produto e repetir as conferências?
2. Banheiro e lavanderia receberão o mesmo material/perfil branco ou outra solução de borda?
3. Dentro do box, o encontro existente entre piso e revestimento substitui o rodapé ou será necessário um detalhe próprio?
4. Após ler o relatório integral, qual é a decisão sobre promover o candidato e atualizar a base com citação e data? A base não foi atualizada.

## Coordenação e arquivos compartilhados

Elias, nesta conversa: limitar esta frente à macro `modelar_rodape.FCMacro` e ao teste, sem alterar os quatro documentos compartilhados, a R54 ou candidato de outra sessão. As notas de rodapé que tinham sido acrescentadas aos READMEs/estado já estão neste documento. A redução de parágrafos históricos e demais condensações foram desfeitas com a restauração dos compartilhados. O relatório preliminar foi preservado abaixo e também fora do repositório; não representa composição com o piso.

A macro usa a R54 original e seus contornos existentes, sem importar ou executar a macro do piso. Nenhuma nova aplicação do CAD será feita nesta frente. Base e release não foram atualizados; sem push.

Observações para a composição: o XML do candidato preliminar contém 119 expressões novas (7.821 no total), enquanto a leitura inicial do inspetor contabilizou 7.702. Conferir a restauração/parametrização no ambiente da composição. O acabamento fosco foi corrigido no código para atribuir novamente a lista de materiais; essa correção de código ainda não foi reaplicada ao candidato externo, conforme a interrupção.

## Relatório preliminar preservado

# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 30/10/2026 22:51. Revisão `Rodapé 8 cm candidato`. SHA256 `4a2996ee63dd` → `da7980b7a203`.

**Aprovação de Elias:** PENDENTE: nada daqui vale sem a decisão de Elias

Candidato externo em `../outputs/Rodape_candidato/Guedala_Park_Rodape_8cm_candidato.FCStd`. R54, base e release permanecem vigentes e intactos. Altura 80 mm; espessura 15 mm nominal, a confirmar.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5834 | 5889 |
| Expressões | 7702 | 7702 |
| Formas ativas | 1134 | 1181 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 12 |
| Cenários de movimento | 106 | 106 |

## Objetos novos (55)

- `RodapeTrecho_001` Rodapé · banho · Peca049 · 15 mm nominal, a confirmar
- `RodapeTrecho_002` Rodapé · banho · Peca049 · 15 mm nominal, a confirmar001
- `RodapeTrecho_003` Rodapé · banho · Peca051 · 15 mm nominal, a confirmar
- `RodapeTrecho_004` Rodapé · banho · Peca053 · 15 mm nominal, a confirmar
- `RodapeTrecho_005` Rodapé · banho · Peca055 · 15 mm nominal, a confirmar
- `RodapeTrecho_006` Rodapé · circulacao · Peca025 · 15 mm nominal, a confirmar
- `RodapeTrecho_007` Rodapé · circulacao · Peca027 · 15 mm nominal, a confirmar
- `RodapeTrecho_008` Rodapé · circulacao · Peca029 · 15 mm nominal, a confirmar
- `RodapeTrecho_009` Rodapé · circulacao · Peca051 · 15 mm nominal, a confirmar
- `RodapeTrecho_010` Rodapé · circulacao · Peca053 · 15 mm nominal, a confirmar
- `RodapeTrecho_011` Rodapé · circulacao · Peca055 · 15 mm nominal, a confirmar
- `RodapeTrecho_012` Rodapé · circulacao · Peca057 · 15 mm nominal, a confirmar
- `RodapeTrecho_013` Rodapé · circulacao · Peca059 · 15 mm nominal, a confirmar
- `RodapeTrecho_014` Rodapé · cozinha · Peca035 · 15 mm nominal, a confirmar
- `RodapeTrecho_015` Rodapé · cozinha · Peca037 · 15 mm nominal, a confirmar
- `RodapeTrecho_016` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar
- `RodapeTrecho_017` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar001
- `RodapeTrecho_018` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar002
- `RodapeTrecho_019` Rodapé · escritorio · Peca011 · 15 mm nominal, a confirmar
- `RodapeTrecho_020` Rodapé · escritorio · Peca017 · 15 mm nominal, a confirmar
- `RodapeTrecho_021` Rodapé · escritorio · Peca019 · 15 mm nominal, a confirmar
- `RodapeTrecho_022` Rodapé · escritorio · Peca021 · 15 mm nominal, a confirmar
- `RodapeTrecho_023` Rodapé · escritorio · Peca023 · 15 mm nominal, a confirmar
- `RodapeTrecho_024` Rodapé · escritorio · Peca025 · 15 mm nominal, a confirmar
- `RodapeTrecho_025` Rodapé · escritorio · Peca027 · 15 mm nominal, a confirmar
- `RodapeTrecho_026` Rodapé · escritorio · Peca029 · 15 mm nominal, a confirmar
- `RodapeTrecho_027` Rodapé · lavanderia · Peca039 · 15 mm nominal, a confirmar
- `RodapeTrecho_028` Rodapé · lavanderia · Peca039 · 15 mm nominal, a confirmar001
- `RodapeTrecho_029` Rodapé · lavanderia · Peca041 · 15 mm nominal, a confirmar
- `RodapeTrecho_030` Rodapé · lavanderia · Peca049 · 15 mm nominal, a confirmar
- `RodapeTrecho_031` Rodapé · quarto · Peca009 · 15 mm nominal, a confirmar
- `RodapeTrecho_032` Rodapé · quarto · Peca011 · 15 mm nominal, a confirmar
- `RodapeTrecho_033` Rodapé · quarto · Peca013 · 15 mm nominal, a confirmar
- `RodapeTrecho_034` Rodapé · quarto · Peca015 · 15 mm nominal, a confirmar
- `RodapeTrecho_035` Rodapé · quarto · Peca015 · 15 mm nominal, a confirmar001
- `RodapeTrecho_036` Rodapé · quarto · Peca017 · 15 mm nominal, a confirmar
- `RodapeTrecho_037` Rodapé · quarto · Peca027 · 15 mm nominal, a confirmar
- `RodapeTrecho_038` Rodapé · quarto · Peca053 · 15 mm nominal, a confirmar
- `RodapeTrecho_039` Rodapé · quarto · Peca057 · 15 mm nominal, a confirmar
- `RodapeTrecho_040` Rodapé · quarto · Peca059 · 15 mm nominal, a confirmar
- … e mais 15

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.

Arquivos finais desta frente no repositório: somente esta nota, `ferramentas/estudos/modelar_rodape.FCMacro` e `ferramentas/estudos/test_rodape_geometria.py`. CSVs, resumo, verificação e assinaturas preliminares ficam na saída externa.
