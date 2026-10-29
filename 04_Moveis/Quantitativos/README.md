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


## Massa e manuseio — base corrente das fichas, 28/10/2026

Estudo separado das propostas históricas acima: **249 painéis**, volume de envelopes **1,060405325 m³**. Foram lidas as 20 fichas `06_Entregas/Fichas_fabricacao/Pxx-pecas.csv` vigentes, sem abrir ou salvar o FreeCAD. Não se incorporaram as 36 peças propostas. A identificação R15 das fichas não prova uma extração R54: o metadado de `fabrication-data.js` ainda indicava R53 durante esta leitura. Os SHA256 das entradas ficam no resumo externo; havendo regeneração das fichas, rodar novamente. Isto é triagem nominal de transporte/manuseio, sem conclusão sobre suspensão ou carga de uso.

[Resumo por móvel](Massas_por_movel.csv): 20 linhas com volume, cobertura do cenário de massa, maior envelope entre os painéis com fonte, alertas e lacunas. Os campos vazios de massa **não significam zero**; não há massa total montada completa para nenhum móvel. As 83 peças marcadas `Recortado/especial` conservam o envelope bruto: não foi calculado volume líquido. Também nas retangulares não se deduziram furação e usinagem.

### Fonte e cálculo sustentado

O [fabricante Greenplac — Arenza Colore](https://greenplac.com.br/products/mdf-arenza-linha-colore), consultado em 28/10/2026, publica chapa MDF de 2750 × 1850 × 18 mm e massa de 63,2 kg. A base documental do [P03](../P03/README.md) identifica MDF BP convencional, mas mantém SKU/lote pendentes. Derivou-se **densidade equivalente da chapa acabada de 690,144690 kg/m³**: 63,2 / (2,75 × 1,85 × 0,018). Não é densidade medida do núcleo e não se soma outra camada BP. Massa do cenário = volume do envelope × essa densidade.

A equivalência de catálogo foi aplicada **condicionalmente** apenas aos 39 IDs cuja ficha nomeia Greenplac Arenza com 18 mm. A ficha especifica acabamento, não confirma por si só substrato, linha e SKU; portanto os valores não são pesos comprovados das peças. Somam **131,651 kg de envelopes neste cenário parcial**. Não se extrapolou a 30 mm nem a “Arenza” genérico. P03 possui cenário para seus sete painéis: **33,992 kg**, antes de ferragens e componentes adicionais; os maiores são Peca262 e Peca263, **10,316 kg cada**. Para os demais móveis, “maior massa” no CSV significa somente maior entre os painéis com cenário, nunca maior de todo o móvel quando há lacunas.

**210 painéis permanecem sem massa**: Branco TX, padrões indefinidos, referências sem marca/linha/substrato suficientes e produtos cuja massa aplicável não foi obtida. A [página oficial Branco TX Guararapes](https://www.guararapes.com.br/produto/branco-tx/) identifica MDF e formatos, mas não fornece ali a massa necessária nem estabelece que seja o Branco TX do projeto. Não se adotaram valores genéricos 650/800/900 dos estudos históricos como densidades comprovadas. Espelhos e outras camadas distintas não receberam massa de madeira; as fichas de painel-base não completam a massa desses componentes.

As ferragens em `04_Moveis/Furacao/Ferragens_por_movel.csv` foram relacionadas separadamente, com massa unitária em branco. Não há massa de catálogo rastreável às linhas nas fontes consultadas; capacidade “40 kg” de corrediça é carga de uso, não peso da ferragem. Não foi considerado peso zero para ferragens, fitas, adesivos, puxadores ou componentes ausentes da lista de painéis. A tentativa Firecrawl falhou por saldo insuficiente; a referência pública Greenplac foi conferida pela ferramenta web, sem contato com terceiros.

### Referência de planejamento para os 249 painéis

Para não deixar o transporte sem número, o CSV traz também `massa_referencia_paineis_kg`: **todos** os envelopes × a mesma densidade equivalente de 690 kg/m³ da chapa Greenplac acima. É ordem de grandeza para combinar frete e ajudantes, **não peso**: Branco TX, Azul Petróleo e demais produtos podem ter densidade diferente, e espelhos, ferragens, fitas e recortes não entram. Total dos painéis: **~732 kg**. Por móvel: P01 ~221 kg; P20 ~59; P17 ~54; P06 ~43; P03 ~34; P10 ~31; P05 ~30; os demais entre 4 e 29 kg.

Único painel acima de 25 kg nessa referência: **P01/Peca208, fundo Branco TX 2096 × 1964 × 18, ~51 kg** — prever duas pessoas e confirmar o peso real com o fornecedor. As portas de correr P01/Peca247 e Peca248 (1999 × 995 × 18) ficam em ~24,7 kg, no limite: tratar também como manuseio a dois até haver peso real.

### Triagem de manuseio

- **Nenhum dos 249 envelopes tem dimensão maior que 2200 mm.** É o critério pedido, não certificação de manuseio individual.
- Nenhum dos 39 envelopes do cenário de catálogo supera 25 kg. Nos outros 210, o teste de massa fica indeterminado; não se conclui que todos os painéis pesem menos que 25 kg.
- Cada painel tem o limiar matemático `25 / volume_envelope` em kg/m³. Isso não atribui densidade ao material. P01/Peca208 tem 0,074097792 m³ e limiar **337,392 kg/m³**; Peca247/Peca248 têm 0,035802090 m³ e limiar **698,283 kg/m³**. Priorizar a confirmação de material/composição e peso dessas peças para planejar transporte. Em contornos especiais, ultrapassar esse limiar pelo envelope não prova que a peça recortada passe de 25 kg.
- Planejamento de duas pessoas: aplicar o critério solicitado quando a massa real/especificada superar 25 kg ou a dimensão superar 2,2 m; o estudo incompleto não substitui avaliação de pega, percurso e montagem.

### Pendências exatas, sem reabrir a escolha de acabamento

1. Qual substrato (MDF ou MDP), fabricante/linha, SKU, composição e massa nominal correspondem a cada família ainda sem vínculo, especialmente Branco TX e peças com espessuras 7, 16, 16,2, 20 e 30 mm? Confirmar também a equivalência Greenplac 18 antes de usar o cenário como peso de transporte.
2. Quais massas unitárias de catálogo correspondem aos SKUs de ferragens efetivamente especificados? Componentes candidatos não devem ser somados cumulativamente às alternativas.
3. Qual espessura/área e massa dos espelhos e camadas separadas, além de painéis-base? Qual volume líquido dos contornos especiais, se for necessário fechar massa? São lacunas de ficha/fornecedor, sem necessidade de escolher novamente a cor.

### Reprodução e arquivos externos

```powershell
python -B ferramentas/estudos/massas_manuseio.py
python -B -m unittest discover -s ferramentas/estudos -p test_massas_manuseio.py
```

Cinco testes: referência de planejamento, conversão exata da chapa publicada e expansão por ID, recusa de extrapolação por cor/espessura, limiar e contorno especial, erro por quantidade inconsistente. A execução gera `Massas_por_movel.csv` nesta pasta; detalhe externo em `../outputs/Massas_manuseio/`, fora do git. O resumo externo registra os hashes das 20 fichas e do inventário de ferragens. Após regeneração, atualizar os hashes abaixo.

| Arquivo externo | SHA256 |
|---|---|
| Massas_por_peca.csv | `95628cb8585e4ddafea06c5bc5c909af1de46ac2a3efab3615de596a79317f1c` |
| Ferragens_sem_massa.csv | `900484e9957be882332b1b322fd2fc67b16f61dbdaed6d5aad13ca43a18a892f` |
| Resumo.json | `f7aeffc75a3d93f9fcac471e08660f7ace8603e57c429fe7602993cb1e710143` |
