# Candidato: verde na janela do box

**Aprovação: PENDENTE.** Pedido de Elias, 30/10/2026, para verde também na parede da janela.

Macro GUI executado na cópia externa `../outputs/R55_candidato/Guedala_Park_R55_candidato.FCStd`, sem substituir R54 nem base. A camada usa espessura/material do fundo e recorta a janela, piso, enchimento e encontro com o revestimento existente.

[Assinaturas de preservação](Preservacao_verde_box.json): 1.489 objetos com geometria própria mantêm volume, área, faces, vértices, caixa, centro de massa e posição global. Hashes individuais antes/depois iguais; assinaturas completas e seu SHA ficam junto ao candidato. Interseções da nova camada com janela, vidro, piso, enchimento e fundo: zero.

[Inspeção completa](Verificacao_verde_box.json): 5.835 objetos, 7.702 expressões e 106 cenários; nenhuma invariante quebrada, peça inválida nova, colisão nova ou objeto novo fora do envelope. GuiDocument.xml preservado. Um par de caixas foi refinado por interseção exata, sem colisão. Nenhuma posição, expressão, aparência ou visibilidade anterior mudou. Os agregados `Ambiente_banho` e `ApartamentoR34` mudam pela inclusão de `RevestJanelaBoxR55`.

Camada: 20 mm, material/cor da Peca160, topo desenhado 2250 mm; não representa o teto nominal nem a hipótese orçamentária de 2470 mm. Recorte da abertura da Peca071 preservado. Nenhuma revisão executiva ou promoção a vigente foi feita.

A CLI oficial só seleciona o vigente. `ferramentas/estudos/verificar_candidato_verde_box.py --candidato <FCStd externo>` chama as mesmas funções oficiais de inspeção, invariantes, comparação e refinamento, sem mudar regras/base e sem executar a CLI. Usa FreeCADCmd somente para leitura; a gravação do candidato ocorreu na GUI. Definir LOCALAPPDATA para a instalação e TEMP externo.

SHA256 candidato: `d1f74ac0dbd06f367360f086fe9ddcfa8f7b479b7fde18d1aae6ba0acabf298a`. R54: `4a2996ee63dd6f2f3dc302025a73fb65011b3339bae510130732859706049528`. Aprovação continua PENDENTE.
