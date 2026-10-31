# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 30/10/2026 23:41. Revisão `Candidato externo: Guedala_Park_Piso_rodape_candidato`. SHA256 `4a2996ee63dd` → `4800ce62941b`.

**Aprovação de Elias:** PENDENTE: nada daqui vale sem a decisão de Elias

**Resultado completo: REPROVADO.** Único erro: cinco pisos novos em Z −50..0 mm fora do envelope iniciado em Z=0, tolerância 1 mm. A base já registra os pisos antigos nessa mesma faixa negativa; a guarda admite somente os nomes anteriormente fora. Não houve alteração de regra/base ou promoção do candidato.

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5834 | 5905 |
| Expressões | 7702 | 7839 |
| Formas ativas | 1134 | 1184 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 12 |
| Cenários de movimento | 106 | 106 |

## Objetos novos (71)

- `Banheiro_Travertino_Reale_Greige` Porcelanato Travertino Reale Greige
- `Lavanderia_Iseo_Marfim` Eliane Iseo Marfim · área molhada
- `Piso_banheiro` Piso_banheiro
- `Piso_lavanderia` Piso_lavanderia
- `Piso_vinilico` Piso_vinilico
- `RodapeTrecho_001` Rodapé · banho · Peca049 · 15 mm nominal, a confirmar
- `RodapeTrecho_002` Rodapé · banho · Peca049 · 15 mm nominal, a confirmar001
- `RodapeTrecho_003` Rodapé · banho · Peca051 · 15 mm nominal, a confirmar
- `RodapeTrecho_004` Rodapé · banho · Peca053 · 15 mm nominal, a confirmar
- `RodapeTrecho_005` Rodapé · banho · Peca053 · 15 mm nominal, a confirmar001
- `RodapeTrecho_006` Rodapé · banho · Peca055 · 15 mm nominal, a confirmar
- `RodapeTrecho_007` Rodapé · banho · Peca055 · 15 mm nominal, a confirmar001
- `RodapeTrecho_008` Rodapé · circulacao · Peca025 · 15 mm nominal, a confirmar
- `RodapeTrecho_009` Rodapé · circulacao · Peca027 · 15 mm nominal, a confirmar
- `RodapeTrecho_010` Rodapé · circulacao · Peca029 · 15 mm nominal, a confirmar
- `RodapeTrecho_011` Rodapé · circulacao · Peca051 · 15 mm nominal, a confirmar
- `RodapeTrecho_012` Rodapé · circulacao · Peca053 · 15 mm nominal, a confirmar
- `RodapeTrecho_013` Rodapé · circulacao · Peca055 · 15 mm nominal, a confirmar
- `RodapeTrecho_014` Rodapé · circulacao · Peca057 · 15 mm nominal, a confirmar
- `RodapeTrecho_015` Rodapé · circulacao · Peca059 · 15 mm nominal, a confirmar
- `RodapeTrecho_016` Rodapé · cozinha · Peca035 · 15 mm nominal, a confirmar
- `RodapeTrecho_017` Rodapé · cozinha · Peca037 · 15 mm nominal, a confirmar
- `RodapeTrecho_018` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar
- `RodapeTrecho_019` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar001
- `RodapeTrecho_020` Rodapé · cozinha · Peca039 · 15 mm nominal, a confirmar002
- `RodapeTrecho_021` Rodapé · cozinha · Peca049 · 15 mm nominal, a confirmar
- `RodapeTrecho_022` Rodapé · escritorio · Peca011 · 15 mm nominal, a confirmar
- `RodapeTrecho_023` Rodapé · escritorio · Peca017 · 15 mm nominal, a confirmar
- `RodapeTrecho_024` Rodapé · escritorio · Peca019 · 15 mm nominal, a confirmar
- `RodapeTrecho_025` Rodapé · escritorio · Peca021 · 15 mm nominal, a confirmar
- `RodapeTrecho_026` Rodapé · escritorio · Peca023 · 15 mm nominal, a confirmar
- `RodapeTrecho_027` Rodapé · escritorio · Peca025 · 15 mm nominal, a confirmar
- `RodapeTrecho_028` Rodapé · escritorio · Peca027 · 15 mm nominal, a confirmar
- `RodapeTrecho_029` Rodapé · escritorio · Peca027 · 15 mm nominal, a confirmar001
- `RodapeTrecho_030` Rodapé · escritorio · Peca029 · 15 mm nominal, a confirmar
- `RodapeTrecho_031` Rodapé · escritorio · Peca029 · 15 mm nominal, a confirmar001
- `RodapeTrecho_032` Rodapé · lavanderia · Peca039 · 15 mm nominal, a confirmar
- `RodapeTrecho_033` Rodapé · lavanderia · Peca039 · 15 mm nominal, a confirmar001
- `RodapeTrecho_034` Rodapé · lavanderia · Peca041 · 15 mm nominal, a confirmar
- `RodapeTrecho_035` Rodapé · lavanderia · Peca049 · 15 mm nominal, a confirmar
- … e mais 31

## Geometria alterada (8)

- `Ambiente_banho`: volume 560377005.822 → 430797005.821 mm³
- `Ambiente_circulacao`: volume 58500000.0 → - mm³
- `Ambiente_cozinha`: volume 1797411572.831 → 1524611572.129 mm³
- `Ambiente_escritorio`: volume 1427115888.015 → 1087865888.075 mm³
- `Ambiente_lavanderia`: volume 891838849.651 → 787993849.65 mm³
- `Ambiente_quarto`: volume 3183732016.335 → 2768357016.155 mm³
- `Ambiente_sala`: volume 2119988599.178 → 1633488599.178 mm³
- `ApartamentoR34`: volume 19475644127.477 → 19458694128.249 mm³

## Aparência alterada (9)

- `Peca`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca001`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca002`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca003`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca004`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca005`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca006`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca007`: cor C3D4DC → C3D4DC, transparência 0 → 0%
- `Peca008`: cor AABCC6 → AABCC6, transparência 0 → 0%

## Visibilidade alterada (9)

- `Peca`: visível → oculto
- `Peca001`: visível → oculto
- `Peca002`: visível → oculto
- `Peca003`: visível → oculto
- `Peca004`: visível → oculto
- `Peca005`: visível → oculto
- `Peca006`: visível → oculto
- `Peca007`: visível → oculto
- `Peca008`: visível → oculto

## Objetos visíveis novos fora do apartamento (5)

- `Banheiro_Travertino_Reale_Greige`
- `Lavanderia_Iseo_Marfim`
- `Soleira_banheiro`
- `Soleira_cozinha_lavanderia`
- `Vinilico_continuo`

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.

## Escopo, preservação e aceite do candidato

Arquivo externo: `../outputs/Piso_rodape_candidato/Guedala_Park_Piso_rodape_candidato.FCStd`. SHA256 `4800ce62941b35463054d5a49fea19a4348280d93101258b8049ba241b863b33`. Composição na GUI: R54 original → `modelar_pisos.FCMacro` → `modelar_rodape.FCMacro`; um arquivo, sem R55 verde. R54, base, release e R55 conservam os hashes registrados em `Composicao.json`, junto ao candidato.

Pisos: nove antigos ocultos; cinco novos sólidos válidos (vinílico único, lavanderia, banheiro e duas soleiras), Z −50..0 mm. Grade 25 mm: **59.104 células; lista de células sem piso nem parede = []; sobreposições volumétricas = []**. Contatos das soleiras: 80.500/35.000 mm² por face, volume compartilhado zero. Reabertura nativa: 7839 expressões, iguais à GUI.

Rodapé: 54 trechos, 35,41680 m, altura 80 mm; 15 mm nominal. Parâmetros independentes do grupo para preservar as expressões na reabertura. As 1.489 geometrias próprias R54 foram preservadas na etapa do piso; as 1.494 anteriores ao rodapé também. Sem movimento de objeto anterior. GuiDocument.xml presente. Os 12 agregados inválidos continuam informativos; nenhuma peça própria inválida. Os 106 cenários passaram, com restauração, e os quatro pares de pisos/soleiras refinados têm interseção volumétrica zero. Isso não elimina o bloqueio do envelope.

Evidências externas: `Piso/Aceite_pisos.json`, `Piso/Assinaturas_geometricas.json`, `Rodape/Rodape.json`, `Rodape/Assinaturas_geometricas.json` e o retrato integral. Hash do aceite: `725d57e984dc2dfb070204a03c45bf98750cfb61b4bba734be17d2c951c7ab02`. Quantidades do site/orçamento e corte de paredes do site preservados. Dimensões e compras continuam nominais.

## Perguntas para Elias

1. Qual material ficará sob a folha do banheiro? O vinílico é hipótese visual.
2. Qual produto/perfil e espessura de junta serão usados nas duas soleiras?
3. Qual produto/espessura final do rodapé, e qual solução no banheiro, lavanderia e dentro do box? Os 15 mm e a referência branca são nominais.
4. Como compatibilizar a exigência de sólidos entre Z −50 e 0 mm com o envelope iniciado em Z=0? Nenhum ajuste de geometria, identidade de objetos, regra ou base foi feito para contornar o bloqueio. É necessária uma decisão explícita antes de continuar o modelo.
5. Após resolver o bloqueio e revisar o candidato, qual será a decisão sobre promoção e base, com citação datada para `--aprovado-por`? A base não foi alterada; o modo externo não permite atualizá-la.

## Proposta separada de revisão conjunta

R55 verde permanece inalterado, SHA256 `d1f74ac0dbd06f367360f086fe9ddcfa8f7b479b7fde18d1aae6ba0acabf298a`. Propor outra revisão, sem número reservado: reconstruir R54 → verde na janela → pisos → rodapé, compatibilizar a camada verde com os encontros e repetir o aceite e a inspeção completa. Essa composição adicional não foi executada nem promovida.
