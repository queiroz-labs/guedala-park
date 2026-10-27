# R31 — apartamento consolidado em 20/10/2026

Abrir o modelo editável · [Visão geral](Apartamento_R31.png) · [Voltar ao guia](../../README.md) · [Site atualizado](https://queiroz-labs.github.io/guedala-park/)

A R31 reúne no apartamento completo os estudos e decisões que ainda estavam separados da R30. As peças continuam editáveis, com os controles nativos preservados. A R30 e os arquivos de origem foram mantidos sem alteração.

**Banco: apenas anotar a preferência de 20/10.** Elias não gostou da bandeja entrando pela lateral e quer voltar depois à guarda convencional, abrindo o baú. Pediu expressamente não alterar agora. A representação lateral permanece como estudo a revisar; a reversão para o baú convencional não foi modelada nem executada. Não considerar a solução lateral aceita para fabricação.

| Frente | Atualização integrada | O que continua pendente |
|---|---|---|
| Cozinha | Fischer Infinity 50 L com grill, sem turbo, preto 127 V, no lugar do Venax; KE4GC preservado; base, três nervuras, contramarcos, duas grelhas e réguas de estudo R02; travessa avançada 27 mm | Apoio e fixação reais, resistência, comportamento térmico, circuito, ligações, corpo instalado do cooktop e medidas da unidade |
| Banco | Peças e apoios do estudo R02, com folha e bandeja articuladas pelos controles de estudo; preferência posterior registrada no módulo e nos controles | Retomar em etapa futura a guarda pelo baú, conforme anotação acima; capacidade, ligações e operação real ainda não comprovadas |
| Lavanderia | Apoios C01–C03 do cesto no modelo geral | Material, ligações, carga, retirada real e instalações |
| Quarto | Rótulos distinguem cama atual de viúvo com baú e queen futura escolhida | Medidas da cama atual, base queen final, circulação e cabimento no baú; envelope 160 × 200 é estudo |
| Escritório | Destino do ciclismo anotado no aéreo existente, com prateleiras reguláveis | Dimensões, carga e alcance; sem criar módulo baixo |
| Banheiro | Espelho 4000 K, indireta 3000 K e comandos físicos separados registrados | Produto, potência, posição e luz geral do teto |
| Programa geral | Inventário, TV com aplicativos na própria TV e todos os ambientes prontos antes da mudança | Produtos finais e compatibilização técnica |

## Conferência

[Verificação final](Verificacao_final_R31.json): 6.191 objetos, 1.094 sólidos nativos correntes conferidos, sem formas inválidas ou estados de erro nesse escopo. Quatro vínculos de navegação das gavetas foram ocultados porque exibiam cópias na origem; continuam acessíveis na árvore. Os dois auxiliares históricos inválidos já existentes não pertencem à geometria corrente e estão discriminados no [relatório de consolidação](Consolidacao_R31.json).

[Reabertura do arquivo salvo](Reabertura_R31.json) confirmada. [Conferência de movimentos](Conferencia_representacao_R31.json) verifica extração, movimento adicional da folha e retorno à pose inicial. A correção de composição das posições-base evita que as expressões removam deslocamentos originais; não é a futura revisão do banco.

[Exportação para o site](Exportacao_site_R31.json): 327 peças e 72.472 triângulos derivados do modelo, sem mecanismos completos. O site mantém ilustrações simplificadas para os demais movimentos. A geometria de estudo integrada não representa aprovação de fabricação, validação global de colisões, cálculo estrutural ou ensaio térmico. PDFs gerais anteriores continuam históricos.

## Fontes e manutenção

- [R30 preservada](../Cadeiras/Consistencia_R30_README.md).
- [Fischer e compatibilização](../../../03_Ambientes/Cozinha/Fischer_Grill/README.md), [apoios R01](../../../03_Ambientes/Cozinha/Fischer_Grill/Apoios_ventilacao/README.md) e [grelhas R02](../../../03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/README.md).
- [Estudo anterior do banco](../../../03_Ambientes/Sala_e_jantar/Retirada_ponta/Materiais_ligacoes_trava_R02.html), sujeito à preferência de revisão futura.
- `../../../ferramentas/componentes/Consolidacao/consolidar_r31.py` cria a revisão a partir da R30; `../../../ferramentas/componentes/Consolidacao/conferir_representacao.py` compõe as posições-base e registra a preferência; `../../../ferramentas/componentes/Consolidacao/finalizar_r31.py` ajusta a exibição e confere o modelo; `../../../ferramentas/componentes/Consolidacao/exportar_site.py` apenas lê e exporta para a visualização.

O arquivo salvo fica com a bandeja fechada. Use a pasta de controles para estudar movimentos; abra a base de edição somente para editar suas peças, preservando a relação com o apartamento espelhado.
