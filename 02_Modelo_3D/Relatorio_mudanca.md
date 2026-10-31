# Relatório de mudança do modelo

Gerado por `verificar_modelo.py` em 31/10/2026 18:36. Revisão `R55`. SHA256 `4a2996ee63dd` → `d5ed97df437b`.

**Aprovação de Elias:** Elias, 31/10/2026, nesta conversa: “ok eu aprovo” (limpeza), escopo “Tudo do estudo limpo (R55)”; atualizar o modelo 3D do site

## Resumo

| | Base anterior | Agora |
|---|---:|---:|
| Objetos | 5834 | 6028 |
| Expressões | 7702 | 8049 |
| Formas ativas | 1134 | 1147 |
| Peças com geometria própria inválida | 0 | 0 |
| Contêineres com forma montada inválida (informativo) | 12 | 14 |
| Cenários de movimento | 106 | 106 |

## Objetos removidos (152)

- `Aberta_170`
- `Aberta_170Lateral`
- `Aberta_170Ponta_cozinha`
- `Aberta_170Ponta_sofa`
- `Aberta_170Sapata`
- `Aberta_170Tampo`
- `AuditoriaDimensionalR32`
- `ComparacaoFrente500R41`
- `ConclusaoFrente500R41`
- `ConferenciaR32`
- `ConferenciaR33`
- `ConsolidacaoR42`
- `ConsolidacaoR52`
- `DocumentacaoProjetoR41`
- `EsforcosCestoR41`
- `FGVTN_R42`
- `FGVTN_R42_Dobradicas`
- `FGVTN_R42_Gaveta`
- `FGVTN_R42_Gaveta001`
- `FGVTN_R42_Gaveta002`
- `FGVTN_R42_Gaveta003`
- `FGVTN_R42_Gaveta004`
- `FGVTN_R42_Gaveta005`
- `FGVTN_R42_Gaveta006`
- `FGVTN_R42_Gaveta008`
- `FGVTN_R42_Gaveta009`
- `FGVTN_R44_ABERTA`
- `FGVTN_R44_ABERTA_Part__Feature`
- `FGVTN_R44_ABERTA_Part__Feature001`
- `FGVTN_R44_ABERTA_Part__Feature002`
- `FGVTN_R44_ABERTA_Part__Feature003`
- `FGVTN_R44_ABERTA_Part__Feature004`
- `FGVTN_R44_ABERTA_Part__Feature005`
- `FGVTN_R44_FECHADA`
- `FGVTN_R44_FECHADA_Part__Feature`
- `FGVTN_R44_FECHADA_Part__Feature001`
- `FGVTN_R44_FECHADA_Part__Feature002`
- `FGVTN_R44_FECHADA_Part__Feature003`
- `FGVTN_R44_FECHADA_Part__Feature004`
- `FGVTN_R44_FECHADA_Part__Feature005`
- … e mais 112

## Objetos novos (346)

- `Area_Banheiro` Area_Banheiro
- `Area_Circulacao` Area_Circulacao
- `Area_Cozinha` Area_Cozinha
- `Area_Escritorio` Area_Escritorio
- `Area_Lavanderia` Area_Lavanderia
- `Area_Quarto` Area_Quarto
- `Area_Sala` Area_Sala
- `Areas_Geometricas` Areas_Geometricas
- `Auditorias_Legadas` Auditorias_Legadas
- `Banheiro_Travertino_Reale_Greige` Porcelanato Travertino Reale Greige
- `Batente_Banheiro` Envelope_grafico_Batente_Banheiro
- `Batente_Banheiro_Compatibilizado` Batente_Banheiro_Compatibilizado
- `Batente_Entrada` Batente_Entrada
- `Batente_Escritorio` Envelope_grafico_Batente_Escritorio
- `Batente_Escritorio_Compatibilizado` Batente_Escritorio_Compatibilizado
- `Batente_Quarto` Batente_Quarto
- `BuildingPart` Nivel de estudo - Z0 / 2570 mm nominal - PENDENTE
- `Cabeceira_Estofada` Cabeceira_Estofada
- `Caixa_Persiana_Escritorio` Caixa_Persiana_Escritorio
- `Caixa_Persiana_Quarto` Caixa_Persiana_Quarto
- `Caixilho_Banheiro` Caixilho_Banheiro
- `Caixilho_Escritorio` Caixilho_Escritorio
- `Caixilho_Lavanderia` Caixilho_Lavanderia
- `Caixilho_Quarto` Caixilho_Quarto
- `Caixilho_Sala` Caixilho_Sala
- `Camera_Banheiro_Canto_1` Camera_Banheiro_Canto_1
- `Camera_Banheiro_Canto_2` Camera_Banheiro_Canto_2
- `Camera_Banheiro_Canto_3` Camera_Banheiro_Canto_3
- `Camera_Banheiro_Canto_4` Camera_Banheiro_Canto_4
- `Camera_Banheiro_Planta` Camera_Banheiro_Planta
- `Camera_Circulacao_Canto_1` Camera_Circulacao_Canto_1
- `Camera_Circulacao_Canto_2` Camera_Circulacao_Canto_2
- `Camera_Circulacao_Canto_3` Camera_Circulacao_Canto_3
- `Camera_Circulacao_Canto_4` Camera_Circulacao_Canto_4
- `Camera_Circulacao_Planta` Camera_Circulacao_Planta
- `Camera_Cozinha_Canto_1` Camera_Cozinha_Canto_1
- `Camera_Cozinha_Canto_2` Camera_Cozinha_Canto_2
- `Camera_Cozinha_Canto_3` Camera_Cozinha_Canto_3
- `Camera_Cozinha_Canto_4` Camera_Cozinha_Canto_4
- `Camera_Cozinha_Eixo` Camera_Cozinha_Eixo
- … e mais 306

## Geometria alterada (13)

- `AcessoControleR34`: volume 28700000.0 → - mm³
- `Ambiente_banho`: volume 560377005.822 → 326872280.0 mm³
- `Ambiente_circulacao`: volume 58500000.0 → - mm³
- `Ambiente_cozinha`: volume 1797411572.831 → 1157152045.0 mm³
- `Ambiente_escritorio`: volume 1427115888.015 → 828710874.702 mm³
- `Ambiente_lavanderia`: volume 891838849.651 → 450052000.0 mm³
- `Ambiente_quarto`: volume 3183732016.335 → 2140748000.0 mm³
- `Ambiente_sala`: volume 2119988599.178 → 1508002041.769 mm³
- `ApartamentoR34`: volume 19475644127.477 → 17794985583.922 mm³
- `MinifixR14`: volume 128648.219 → - mm³
- `ParedesCortadas`: volume 1093440000.0 → - mm³
- `ParedesInteiras`: volume 8343240000.0 → - mm³
- `PortaEntradaBanheiroR12`: volume 28700000.0 → - mm³

## Aparência alterada (77)

- `Peca`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca001`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca002`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca003`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca004`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca005`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca006`: cor 9DB9C9 → 9DB9C9, transparência 0 → 0%
- `Peca007`: cor C3D4DC → C3D4DC, transparência 0 → 0%
- `Peca008`: cor AABCC6 → AABCC6, transparência 0 → 0%
- `Peca009`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca010`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca011`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca012`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca013`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca014`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca015`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca016`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca017`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca018`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca019`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca020`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca021`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca022`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca023`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca024`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca025`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca026`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca027`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca028`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca029`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca030`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca031`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca032`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca033`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca034`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca035`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca036`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca037`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca038`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- `Peca039`: cor D2DFE4 → D2DFE4, transparência 0 → 0%
- … e mais 37

## Visibilidade alterada (77)

- `Peca`: visível → oculto
- `Peca001`: visível → oculto
- `Peca002`: visível → oculto
- `Peca003`: visível → oculto
- `Peca004`: visível → oculto
- `Peca005`: visível → oculto
- `Peca006`: visível → oculto
- `Peca007`: visível → oculto
- `Peca008`: visível → oculto
- `Peca009`: visível → oculto
- `Peca010`: visível → oculto
- `Peca011`: visível → oculto
- `Peca012`: visível → oculto
- `Peca013`: visível → oculto
- `Peca014`: visível → oculto
- `Peca015`: visível → oculto
- `Peca016`: visível → oculto
- `Peca017`: visível → oculto
- `Peca018`: visível → oculto
- `Peca019`: visível → oculto
- `Peca020`: visível → oculto
- `Peca021`: visível → oculto
- `Peca022`: visível → oculto
- `Peca023`: visível → oculto
- `Peca024`: visível → oculto
- `Peca025`: visível → oculto
- `Peca026`: visível → oculto
- `Peca027`: visível → oculto
- `Peca028`: visível → oculto
- `Peca029`: visível → oculto
- `Peca030`: visível → oculto
- `Peca031`: visível → oculto
- `Peca032`: visível → oculto
- `Peca033`: visível → oculto
- `Peca034`: visível → oculto
- `Peca035`: visível → oculto
- `Peca036`: visível → oculto
- `Peca037`: visível → oculto
- `Peca038`: visível → oculto
- `Peca039`: visível → oculto
- … e mais 37

## Como usar

1. Leia as seções acima. Cada mudança listada foi pedida e é a esperada?
2. Só com a aprovação dele: `python ferramentas/verificar_modelo/verificar_modelo.py --completo --atualizar-base --aprovado-por "Elias, dd/mm/aaaa: o que aprovou"`.
3. Commite a base, este relatório, `current_release.json` (SHA) e o `ESTADO_ATUAL.md` juntos.
