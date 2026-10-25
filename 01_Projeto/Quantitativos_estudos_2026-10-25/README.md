# Quantitativos separados das propostas de marcenaria

25/10/2026 · avançoT07/T09. **36 registros de peças propostas:11 substituições e25 acréscimos**, em sete propostas e seis arquivos parciais. Os BREP foram lidos diretamente dos arquivos gravados, incluindo aR51, sem usar documentos modificados na sessão. Nenhuma proposta foi incorporada à lista de materiais ou ao orçamento vigente.

## Diferenças por proposta

Áreas líquidas geométricas de uma face das chapas18. “A fabricar na proposta” inclui a peça substituta inteira; “acréscimo” deduz a peça original. Não são quantidade de chapas de compra, nem plano de corte.

| Proposta separada | Peças a fabricar | Dessas, substituições | Área das peças propostas | Acréscimo de área | Acréscimo nominal aρ800 |
|---|---:|---:|---:|---:|---:|
| P01 duas prateleiras723 | 2 | 2 | 0,7953m² | 0,0198m² | 0,285kg |
| P01 socoR01 | 21 | 0 | 0,7756m² | 0,7756m² | 11,169kg |
| P01/P03 encontro traseiro | 2 | 2 | 5,0060m² | 0,0590m² | 0,850kg |
| P04 fundo308 | 1 | 1 | 0,5433m² | 0,0635m² | 0,914kg |
| P15 composição36/laterais/fundo | 4 | 3 | 1,1218m² | 0,3043m² | 4,382kg |
| P17 fundo550 | 1 | 1 | 1,0802m² | 0,0707m² | 1,018kg |
| Bancada de marcenaria | 5 | 2 | 1,9328m² | 1,7264m² | 24,861kg |

São alternativas ainda condicionadas, não um kit total aprovado. Não somar todas automaticamente nem converter os58/74 marcadores de juntas em novas ferragens. [Linhas por objeto, volumes, dimensões e massas650/800/900](Diferencas_nominais.json).

NoP15, a camada superior existente é preservada: a tabela conta a camada inferior acrescentada, duas laterais substitutas e o fundo substituto. Na bancada, os cinco painéis somam27,833kg brutos a800; descontando as duas laterais atuais de madeira, o incremento nominal é24,861kg. Os dois pés esquemáticosP111/P112 têm material/peso desconhecidos e não geraram crédito fictício de massa de madeira ou economia financeira.

## Massa geométrica e massa de cálculo

As quantidades acima vêm da espessura nominal18 dos BREP persistidos. Os cálculos de chapa usam espessuras resistentes menores e, em vários casos,18,3 por camada para a sensibilidade de massa. São grandezas diferentes. ExemploP17: o incremento geométrico do fundo é1,018kg a800; o cálculo usa1,035kg ao considerar18,3 de massa. A diferença não representa perda de peça nem alteração no arquivoCAD.

Massa real depende de painel, revestimento, adesivo, ferragens e fabricação. Não usar a massa hipotética como pesagem ou contrapeso garantido. Atualizar a demanda global quando uma proposta for demonstrada e adotada.

## Formato de chapa: pendência concreta do fundoP01

O fundoP01 atual já mede1964×2096×18; o estudo traseiro passa a1964×2114×18. **Nenhum dos dois cabe em uma única chapa2750×1850, em qualquer rotação.** Não é um problema criado apenas pelo aumento18. A triagem das36 peças encontra esse caso; as outras cabem individualmente nesse formato antes de refilo/serra/orientação decorativa.

O fabricanteGuararapes publica2750×1850 para BrancoTX. Isso é uma referência comercial específica, não a marca selecionada para todo o projeto. [Produto oficial](https://www.guararapes.com.br/produto/branco-tx/).

A fichaARAUCO MelaminaMDF2024 também relaciona2750×2100 para18; esse retângulo comporta nominalmente o fundo inteiro em uma orientação. **PadrãoBrancoTX, faces, estoque, fornecimento e margem de corte não estão confirmados.** Não foi selecionado fornecedor ou substituído acabamento. [Ficha primária, página2](https://arauco.com/brasil/wp-content/uploads/sites/17/2024/05/ARAUCO-MELAMINA-MDF-1-1-2024.pdf).

Pergunta exata para produto/oficina, não enviada: “É possível fornecer o painel real escolhido em formato que permita cortar o fundoP01 inteiro1964×2114×18, com refilo e acabamento previstos? Confirmar marca/padrão/faces, dimensão útil e transporte/montagem. Se não, propor emenda com posição, apoios e ligação calculados, preservando aparência e o caminho estrutural do fundo; não dividir a chapa silenciosamente.”

Uma emenda altera o painel que participa dos cálculos. Não adotar duas metades apenas porque somam a mesma área. O [teste de formatos por linha](Formatos_e_pendencias.json) é uma triagem de um retângulo, sem encaixe conjunto, perdas, veio, bordas, serra, transporte ou capacidade da oficina.

## Como usar na revisão de custos

Após escolher uma proposta demonstrada, substituir as linhas antigas correspondentes pelas novas; manter o restante da lista-base. Recalcular plano de corte por padrão/espessura/faces e formato útil, bordas, colagem/prensagem e operações. Só então reconciliar ferragens e cotação. O pequeno acréscimo de área não informa sozinho quanto custa fabricar uma peça inteira em outro formato.

Não há preços novos, chapas compradas ou mudança no orçamento. Nenhum tubo ou quadro metálico foi reintroduzido.

## Reprodução e integridade

[extrair.py](extrair.py), noFreeCAD, lê os arquivosFCStd comoZIP e importa apenas os BREP selecionados em memória. Não abre ou fecha documentos e não altera preferências/objetos da sessão. A pasta temporária própria é verificada dentro deste diretório antes da limpeza. ASCII e binário foram lidos pelos métodos nativos, sem converter geometrias para simplificação.

Depois executar `python analisar.py` e [verificar.py](verificar.py). [Verificação](Verificacao.json) confere36 objetos retangulares18,11 substituições, volumes/áreas/massas, sete arquivos persistidos comCRC/hash e formato. Geometria nominal não é fabricação liberada nem ensaio físico.
