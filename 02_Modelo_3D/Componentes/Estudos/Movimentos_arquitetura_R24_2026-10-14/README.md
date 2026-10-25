# Novas conferências de movimento contra arquitetura — R24

O levantamento de [cobertura documental](../Cobertura_movimentos_2026-10-14/Matriz_cobertura.md) identificou três famílias cuja arquitetura não estava explicitamente incluída nos testes da montagem atual. Esta entrega conferiu **somente essas lacunas**, usando a implantação R24 corrigida, sem repetir famílias prontas ou alterar o arquivo.

| Família | Seleção móvel efetiva | Novas poses | Pares contra 36 alvos arquitetônicos |
|---|---|---:|---:|
| Doze portas R10 — pia/A/B/C/D/lavanderia | Frente final e12 corpos/calços por folha, conforme Montagem_R10 | 30°,60°,86° individuais;36 casos | 16.848 |
| Duas portas do canto R04 | Frente final e12 ferragens por folha; BasePainel/ancestrais/Label de role conferidos | 30°,60°,86° individuais;6 casos | 2.808 |
| G2 atual R07 | 27 resultados sólidos móveis sob Gaveta005: caixa/travas/bandejas/programa; guias estáticas fora do conjunto | 100,200,300,400,500 mm;5 casos | 4.860 |

Resultado: **47 novas situações e24.516 pares**, todos afastados pelo BBox conservador com epsilon de 0,000001 mm. **Nenhum booleano foi necessário, nenhum contato volumétrico ou erro foi registrado.** Tempo12,297 s, dentro do orçamento de240 s. O critério para um eventual contato positivo seria volume acima de0,1 mm³, uma triagem CAD sem valor de tolerância certificada.

Os alvos foram as **27 paredes inteiras e nove pisos** do manifesto arquitetônico anterior, preservados naR24. Não existe sólido de teto nessa composição; não foi alegada conferência contra teto. As fontes e os alvos foram avaliados com `getGlobalPlacement()` no referencial-base, cuja reflexão comum conserva distâncias e colisões.

O processo FreeCADCmd1.1.4 rodou sem interface, e o documento permaneceu somente em memória. O hash daR24 antes/depois permaneceu `b2382d8a66045e430a3bd21e54c60e00406f9949c3ad47428449be4362dd04f9`. Não houve `save()`/`saveAs()`, geometria nova, corte, furação ou alteração de parâmetros salvos.

## Seleção e limites concretos

O campo `manifest.moving_roles` registra os nomes reais, rótulos atuais, controles, campos editados, ancestrais e todos os resultados sólidos. As frentes do canto foram confirmadas por seus painéis-base e ancestral `CantoSimplesR04`, sem presumir que o sufixo numérico sozinho identifica a função. As ferragens de cada role A/B foram selecionadas pelos rótulos fonte correspondentes e verificadas como12 por folha.

Para G2, a seleção foi limitada aos resultados atuais com ancestral geométrico `Gaveta005`. Os perfis/peças das guias pertencentes a `GuiasG2R07` ficaram estáticos e fora da translação. A translação rígida da caixa/travas/programa **não anima o telescópio MOVENTO nem comprova seu funcionamento físico**.

O estado fechado0 já estava coberto pela auditoria estática e não foi registrado como novo teste. Não foram recalculados pares frente×frente, madeira própria, intraferragem, R08/R11/R12/R13/R14/R15/R16 ou trajetórias de limpeza. As poses de outras folhas ficaram fechadas enquanto cada folha testada abria.

Essas amostras não comprovam todas as posições intermediárias, cargas, fixação, regulagens, tolerâncias reais, batentes, pessoas ou fabricação.86° continua limite de estudo sem comprovação do limitador mecânico70T3553. A retirada elevada das bandejas daG2 — elevar120/avançar40/elevar100 — permanece distinta da abertura da gaveta e fora desta entrega; o legado verificava esses segmentos contra o interior/bancada, sem arquitetura explícita.

## Evidências

- `Movimentos_arquitetura_R24.json`: manifesto de controles/peças/ancestrais, BBox de cada peça em cada nova pose, contadores por caso, contatos, erros e hashes.
- `auditar_lacunas.py`: processamento em memória com orçamento e checkpoints, encerrado sem salvar CAD.
- A matriz documental permanece como diagnóstico anterior; esta entrega fecha somente os cruzamentos novos descritos acima.

Não há liberação de corte, furação, compra, carga ou fabricação.
