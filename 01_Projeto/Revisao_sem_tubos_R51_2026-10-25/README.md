# Modelo R51 com alternativa tubular cancelada retirada

25/10/2026. [Abrir o modelo completo R51](Guedala_Park_R51_Sem_estudo_tubular.FCStd).

Elias determinou que não quer tubos sustentando chapas de madeira. A R51 retira **somente o grupo oculto** `R45_Ref_Bancada_Estrutura_R45_R02_ESTUDO`:60 objetos de uma alternativa antiga da bancada, incluindo cinco longarinas, duas travessas, quatro pés tubulares, contraventamentos, tampo com bolsões e cópias de contexto. Esse conjunto não sustentava as peças ativas.

O arquivo R50 e o estudo separado da bancada ficam preservados como histórico. **Qualquer futura proposta de tubo para sustentar chapa exige autorização prévia de Elias.** As alternativas P11/P15 também estão canceladas no escopo ativo. [Decisão completa](../Cargas_e_ligacoes_R50_2026-10-25/Decisao_sem_tubos.md).

| Conferência | Resultado |
|---|---|
| Objetos |5.893 →5.833; diferença restrita aos60 objetos do estudo oculto |
| Peças mantidas | Nenhuma diferença de tipo, nome, rótulo, geometria, Placement, cor, transparência ou visibilidade na comparação feita |
| Expressões |7.702 preservadas; objetos retirados não possuíam expressões |
| Referências externas ao ramo retirado | Apenas o grupo organizador `R45_Estudos`; nenhuma dependência funcional encontrada |
| Persistência | Gravação binária otimizada, formas vazias normalizadas; arquivo reaberto no FreeCAD com5.833 objetos e7.702 expressões |
| R50 histórica | SHA256 preservado |

[Comparação](Verificacao_R51.json) · [reabertura](Reabertura_R51.json). SHA256 R51: `ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16`. Tamanho19.799.395 bytes. Não foi feito novo benchmark de abertura nem repetido o ensaio dinâmico de18 movimentos nesta revisão; o ramo retirado era independente e as expressões/Placements das peças mantidas foram comparados.

Os dois pés esquemáticos ativos da bancada (`Peca111`/`Peca112`,30×30×720) não têm material nem seção oca definidos no CAD. A solução de marcenaria que os substituirá continua em desenvolvimento; não se declarou sua capacidade ou estabilidade. A bancada não fica aprovada apenas por excluir o estudo anterior.

Os novos estudos [P15/P04 sem tubos](../Solucoes_marcenaria_sem_tubos_2026-10-25/README.md) e [P01 com prateleiras723](../Cargas_e_ligacoes_R50_2026-10-25/README.md) permanecem separados. A R51 não incorpora alterações de espessura, dimensões ou furação dessas propostas. Site/ZIP publicados continuam na revisão anterior até uma publicação autorizada.

Para salvar a R51 novamente, usar o macro/helper de [salvamento otimizado](../Otimizacao_FreeCAD_R50_2026-10-24/README.md), ajustando o destino ao arquivo R51. Não sobrescrever a R50 histórica.
