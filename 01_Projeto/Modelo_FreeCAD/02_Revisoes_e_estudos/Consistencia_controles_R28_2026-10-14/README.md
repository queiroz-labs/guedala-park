# Conferência adicional da R28 — controles e encontro com o sofá corrigido

Elias pediu procurar mais inconsistências até a avaliação das18h30. O arquivo vigente continua R28, SHA256 `2b623c09beddb4d01b581f474468ed707b9b41d8b9dc7cddc1312474fd5ecc99`. Esta etapa não alterou o CAD, não gerou nova revisão e não reexecutou poses, reaberturas, galerias ou varreduras globais.

## Instrução desatualizada corrigida

O guia R26 incorporava uma linha antiga do cesto dizendo que o endereço temporário da lixeira ainda não estava definido. No próprio CAD, `ControleCestoR15.Sequencia` e `ControleLoopManutencaoR26.Sequencia` já apontavam para o estacionamento proposto650 mm, mantendo o lugar habitual0. Foi publicado um [guia vigente reconciliado](Guia_controles_vigentes_R28.md); o guia anterior foi preservado como histórico. Endereço/percurso CAD têm evidênciaR26; manuseio, pega, piso, retenção e carga físicos continuam pendentes.

## Campos e acessos

[Leitura do arquivo aberto](Leitura_controles_R28.json) e [conferência dos acessos](Conferencia_acessos_R28.json):46 acessos,46 controles originais,57 campos de comando. Cada controle tem um único acesso; nenhum campo ausente, oculto ou somente leitura entre os campos de entrada. Nenhuma expressão sobrescreve esses campos. As gavetas e a entrada comandam o próprio Placement; outros controles possuem dependências de expressão externas. Planilha do canto usa B2/B3. Isso não comprova todos os domínios de fórmulas ou um mecanismo físico/intertravamento.

## Lacuna específica: banco × sofá depois da R24

O banco foi conferido antes da restauração da orientação do sofá Daiane. A complementação anteriorR24 cobria as gavetas do escritório e seu aéreo. Esta leitura acrescenta somente a dependência do banco em relação às cinco primitivas diárias do sofá corrigido, sem refazer as poses do banco ou seus encontros inalterados.

[Projeções longitudinais](Banco_sofa_corrigido_R28.json):a direção longitudinal localX do banco coincide com −Y global. Os quatro eixos de tampa são localX; girar preserva essa projeção. Os percursos registrados de almofadas, conteúdo e folha foram comparados por seus intervalos projetados. São22 intervalos; o menorY é3750 e o maiorY do sofá atual2920, deixando830 mm nominais entre projeções. A reflexão do apartamento conservaY, portanto a comparação também vale para a implantação espelhada.

Esta separação cobre somente os comandos e trajetos documentados, contra o sofá fechado diário. Não cobre valores arbitrários, pessoas, sofá transformado em cama, transferência da folha para a mesa, peças reais, carga, tolerâncias ou ferragens. Não foram feitos novos booleanos ou movimentos no arquivo aberto.

O hash canônico e os valores dos controles permaneceram iguais. Uma sondagem inicial da ferramenta omitiu `import FreeCAD as App` e retornou NameError antes de ler o modelo; chamada corrigida em seguida, sem mutaçãoCAD. Esse erro da sondagem não é uma falha geométrica do projeto.

Revisão final Astra ainda reservada para18h30, na mesma conversa. Não há liberação de corte, furação, compra ou fabricação.
