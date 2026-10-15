# Revisão integrada — implantação e programa

Revisão iniciada por solicitação de Elias para procurar erros de posição e colisões até19h de14/10. Arquivo atual: [R25](../Programa_R25_2026-10-14/Guedala_Park_R25_Programa_Conferido.FCStd). Bases R23/R24 preservadas.

## Achados corrigidos

- Sofá Daiane: sinal incorreto de rotação do importador colocou o corpo do lado errado da parede. R24 restaura posição documentada, preservando modelo/dimensões.
- Exibição: tanque anterior e duas referências exclusivas do modo hóspedes estavam visíveis na rotina diária; vínculos ocultos, fontes preservadas.
- Espelho lateral: R25 recompõe centralização na lateral atual650mm, deslocando15mm; vidro500×1800×5/base200 preservados. Fixação/adesivo/apoios reais permanecem pendentes.
- Cabeceira: R25 representa os dois painéis aprovados dentro do mesmo envelope; sem definir junta ou medidas de corte.

## Conferências novas e limites

[Implantação contra arquitetura](../Auditoria_implantacao_R23_2026-10-14/README.md) selecionou20módulos e927 sólidos exibidos contra27paredes inteiras/novepisos. Dois positivos reais do sofá foram corrigidos. Não existe teto sólido modelado.

[Encontros entre módulos](Encontros_modulos_R23.json):398480 pares entre raízes distintas com ao menosum módulo, quatro positivos. Dois tanquehistórico×tanqueatual deixam de integrar a exibição R24. Dois tanque/vazioútil×bancada 'a recortar' continuam pendência de produto e recorte real; não foi inventado recorte.

[Encontros de famílias de móveis/equipamentos R24](Encontros_moveis_R24.json):127 sólidos importados selecionados,7469 pares entre famílias distintas,13 comuns/nenhum erro. Esses comuns NÃO foram apagados para declarar solução:

| Encontros | Classificação documental | Pendência |
|---|---|---|
| Dez comuns mesa×Lina | Caixas cheias conservadoras ocupam os vazios de cadeira; as posições são exatamente as do estudo23/09 | Cadeira/pés/encosto/sapata/guias/altura livre reais; não garante guarda nem autoriza mover a disposição aceita |
| Três comuns enchimento×reservas do box | Enchimento30cm e vidro/perfis são gabaritos; altura/forma físicas não medidas | Desenho/medição do enchimento e box, vedação/abertura; não remover enchimento ou deslocar box sem dados |

[Aderência documental](../Aderencia_programa_R24_2026-10-14/README.md) separa geometria aprovada, propostas e dados indisponíveis;13 conjuntos comparados/73raízes indexadas, sem afirmar cobertura de todos os bens ou decoração.

[Novos movimentos contra arquitetura](../Movimentos_arquitetura_R24_2026-10-14/README.md):47 situações das12portas comuns/canto/G2,24516 pares separados pelo BBox, sem contatos/erros. [Complementos direcionados](../Complementos_R24_2026-10-14/README.md) tratam retirada elevada das bandejas e encontros do escritório com o sofá corrigido, usando envoltórias/intervalos e sem repetir as varreduras anteriores.

As alterações de R25 foram conferidas apenas no trecho afetado: espelho contra959 alvos e igualdade volumétrica da cabeceira subdividida. Os armários e controles permanecem iguais àR24. Sem contato interno de ferragens reavaliado, homologia de movimento contínuo geral, tolerância física, carga/fixação/batente ou liberação de fabricação.
