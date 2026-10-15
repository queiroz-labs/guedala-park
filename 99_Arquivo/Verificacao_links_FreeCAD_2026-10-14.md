# Organização do FreeCAD e verificação de referências

Data: 14/10/2026.

A pasta do FreeCAD foi separada em versão atual (R30), revisões e estudos, recursos, documentação histórica e ferramentas/registros. O guia e o comando de abertura apontam para a R30. A galeria geral R28 foi identificada como histórica.

Foram movidos 868 arquivos, sem excluir modelos ou revisões. Os 366 arquivos binários movidos, incluindo 69 modelos FCStd, conservaram seus hashes. Os 171 scripts Python passaram na conferência de sintaxe; caminhos estáticos, fontes CSV e caminhos montados por scripts foram ajustados. Os scripts de construção não foram executados.

## Referências

Resultado final: **678 Markdown, 9.830 referências locais e zero destinos locais ausentes**. Catálogo geral com 2.224 arquivos de conteúdo.

A verificação percorre os Markdown do projeto, incluindo arquivos históricos, cópias de trabalho e pesquisas locais. Inclui links inline, imagens, definições de referência e atributos HTML href/src. Também foram corrigidos caminhos identificáveis em trechos de texto. Pastas de Git, dependências de terceiros e cache Python são excluídas. Endereços de internet e âncoras internas não foram testados; existência de um destino não comprova que seu conteúdo representa a revisão atual.

Os resultados finais, contagens e arquivos eventualmente sem referência direta estão no [relatório verificável](Organizacao_FreeCAD_2026-10-14/Verificacao.json). A conferência das galerias locais também foi realizada. O [catálogo geral](../INDICE_DE_ARQUIVOS.md) permite localizar os arquivos de conteúdo, inclusive imagens, dados e scripts que antes não possuíam link direto em Markdown.

## Recuperação e rastreabilidade

- [Mapa de movimentações e hashes anteriores](Organizacao_FreeCAD_2026-10-14/Plano.json).
- [Textos anteriores à reorganização](Organizacao_FreeCAD_2026-10-14/Antes_da_organizacao.zip).
- [Textos anteriores ao reparo complementar](Organizacao_FreeCAD_2026-10-14/Antes_reparo_links.zip).
- [Reparos complementares](Organizacao_FreeCAD_2026-10-14/Reparos_complementares.json).
- [Ajustes adicionais nos geradores](Organizacao_FreeCAD_2026-10-14/Caminhos_geradores.json).

A conexão com o FreeCAD estava indisponível durante a checagem final; a abertura pela interface não foi testada. Nenhum modelo foi aberto, recalculado ou salvo nesta organização. Caso haja uma sessão aberta com o caminho antigo, reabra pelo comando atualizado antes de continuar a edição.

[Guia do FreeCAD](../01_Projeto/Modelo_FreeCAD/README.md) · [Início](../README.md).
