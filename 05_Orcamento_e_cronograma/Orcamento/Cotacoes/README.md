# Comparador de cotações

**Nenhuma proposta real foi comparada.** Inventário de 29/10/2026: pasta externa `../outputs/Propostas_recebidas/` criada e vazia. Prazo solicitado de respostas: **30/10/2026 às 18 h, Brasília**; não confirma envio ou aceite do fornecedor. Ferramenta e modelos prontos; oito testes com fixture **FICTÍCIO** passaram. Decisão **PENDENTE de Elias**. Não houve envio, compra, mudança de orçamento ou CAD.

## Rodar e adicionar proposta

Da raiz do repositório, ativar `. ..\ferramentas_locais\ativar.ps1`. Usar `python -B` para evitar resíduos. Se o sandbox negar acesso ao temporário, definir `TEMP` e `TMP` para uma pasta externa autorizada antes dos testes; isso não muda o projeto.

1. Guardar PDF/planilha/DOCX/imagem/TXT recebido em `../outputs/Propostas_recebidas/`. Guardar a correspondência fornecedor ↔ Fxx **somente lá**, fora do git. Não publicar nomes de arquivos brutos que revelem dados pessoais.
2. Copiar [Modelo_entrada.csv](Modelo_entrada.csv) para essa pasta, com nome permanente por proposta. Abrir em planilha como UTF-8, separador `;`. Preencher fornecedor F01/F02…, campos e origens. Reunir propostas em um único CSV para comparar entre si; não repetir a mesma chave fornecedor+linha+campo. Campos não respondidos ficam vazios.
3. Conferir a transcrição na fonte. PDF: `pdftotext -layout recebido.pdf extraido.txt` do Poppler local; DOCX: parágrafos/tabelas com `python-docx`; XLSX: valores e fórmulas com `openpyxl`, sem confundir fórmula sem cache com zero. Texto extraído continua fora do git. Imagens/PDF sem texto exigem OCR ou transcrição; marcar no campo origem `OCR, página X, conferência pendente` e registrar trechos ilegíveis em observacoes. **Nenhum OCR foi executado** nesta entrega.
4. Rodar o comando abaixo. Nunca apontar `--saida` para dentro do repositório. Conferir `Perguntas.csv`, `Matriz_cobertura.csv` e `Ranking_condicional.csv` antes de usar; perguntas numeradas são rascunhos para Elias enviar.

```powershell
python -B ferramentas/estudos/comparador_cotacoes.py --data 2026-10-29
python -B ferramentas/estudos/comparador_cotacoes.py --entrada ../outputs/Propostas_recebidas/Normalizadas.csv --data 2026-10-30
python -B ferramentas/estudos/test_comparador_cotacoes.py
```

`--data` é a data da comparação, altere-a no uso real. Sem `--entrada`, só há inventário e saídas vazias, nunca proposta inventada. Para regenerar modelos: acrescentar `--modelos 05_Orcamento_e_cronograma/Orcamento/Cotacoes`; não sobrescrever uma entrada preenchida. JSON também é aceito, com estrutura abaixo. [Pesos.json](Pesos.json) é editável via `--pesos caminho.json`.

## Esquema CSV e JSON

Cada linha CSV guarda **um valor com sua própria origem**: `fornecedor;linha;campo;valor;unidade;origem`. `linha` vazia identifica condições da proposta; L001…L101 identificam as linhas físicas do [CSV fonte](../../../06_Entregas/Cotacao/Quantidades_referencia.csv), na mesma ordem, sem reescrevê-lo. [Linhas_referencia.csv](Linhas_referencia.csv) é índice de consulta. A posição é protegida pelo hash da fonte no resultado; se o CSV fonte mudar, revisar os vínculos antes de comparar entradas antigas.

JSON: objeto `propostas`, lista de objetos com `fornecedor`, `campos` e `linhas`. `campos` mapeia nome → `{valor, unidade, origem}`; `linhas` mapeia ID → mesmo mapa de campos. [Modelo_entrada.json](Modelo_entrada.json) começa vazio. O JSON normalizado externo preserva valores e origens; números calculados são separados. Zero explícito é aceito; vazio/`null` são ausência. Valores negativos, não finitos, IDs/campos desconhecidos, duplicação CSV e valor sem origem são rejeitados.

| Bloco | Campos e preenchimento |
|---|---|
| Identificação | `fornecedor`: só Fxx; `data`, `validade`: YYYY-MM-DD; `escopo`: integral, etapa, ferragens ou iluminacao, sem misturar bases |
| Preço e inclusões | `preco_total`: BRL declarado; `fabricacao`, `entrega`, `montagem`, `medicao_in_loco`, `retirada`: sim/nao. `frete_incluso`, `impostos_inclusos`: sim/nao; quando nao, frete/impostos são **adicionais fora do total**, em BRL |
| Condições | `pagamento`, `exclusoes`, `premissas`, `reajuste`, `multa`, `observacoes`: texto; `sinal_percentual`: 0–100; `garantia_meses`: número. `risco_reajuste`: baixo/medio/alto, avaliação documental com origem, sem decisão automática |
| Prazo | `producao_dias`, `entrega_dias`, `montagem_dias`: durações sucessivas, não cumulativas; `inicio_semana_chaves`: início da produção relativo às chaves; `calendario`: corridos/uteis; `gatilho_prazo`: evento contratual e premissas. Calendário útil exige conversão validada antes de calcular |
| Linha | `situacao`: incluida/excluida/esclarecer; `quantidade` + unidade; `preco_unitario`, `preco_total_linha`: BRL, descritivos do total declarado, sem somá-los novamente |
| Especificação | `marca_modelo`, `sku`, `cor`, `espessura_mm`, `formato` (2750x1850), `tipo_fita`, `regra_borda`, `equivalencia` e `observacoes`. Em ferragens, copiar o item exato da referência para o produto original; qualquer nome diferente é substituição a conferir, mesmo com alegação de equivalência |
| Origem | Código neutro de arquivo + página/célula/linha, por exemplo `F01_doc01.pdf, p.2, item 4`; os nomes reais e documentos ficam externos. A origem permite conferência, não certifica leitura/OCR |

Quantidades aceitam vírgula decimal; fita aceita m/cm/mm e converte para metros; unidade não é par. Não se converte rolo em metro sem metragem documentada. Os 23 registros de fita sem regra já estão entre as 101 linhas. As 33 exclusões de corte usam `CORTE-ID`; as 40 ferragens sem quantidade usam `FER-PEND-01…40`. `P19-MINIFIX` preserva a pergunta **12 documentais × 8 no mapa**. Para lacunas, `incluida` significa inclusão explícita no preço a conferir; `esclarecer` significa que pediu esclarecimento; vazio significa que não respondeu.

## Comparação e custo equivalente

A matriz classifica cada linha: coberta / coberta com quantidade diferente / não mencionada / excluída. Linha incluída sem quantidade numérica não equivale a zero nem confirma quantidade. Especificação de ferragem ausente é pendência. Cobertura mede menção documental, não suficiência técnica; substituições aparecem à parte e exigem preço da especificação original e crédito da troca.

- **Chapas:** 14 no misto, **8 de 2750×1850 + 6 de 2750×2100**, 216 painéis classificáveis; o estudo todo em 1850 usa 15 para 215 painéis, limite inferior agregado 14 e P01/Peca208 fora. A matriz mostra encontrado/LI de 1850 por grupo e diferenças de formato. Confirmar SKU, processo e cobertura dos 33 bloqueados. Nenhum formato é intercambiável automaticamente.
- **Fita:** referência 191,136 m e **210,2496 m com 10%**, não arredondar antes de comparar. Divergência por linha acima de 10% e ausência de regra de borda geram perguntas. Os 23 painéis sem regra não entram como fita grátis. A linha comparativa L101 não é compra adicional.
- **Custos:** declarado + adicionais declarados de frete/impostos + faltas quantificáveis. Primeiro busca preço unitário da mesma linha em outra proposta de **mesmo escopo**, com unidade/especificação compatíveis; depois faixa histórica por padrão/espessura/formato em Custos_chapas. Preserva mínimo–máximo e origem. Branco 16/Louro sem preço e formatos 2100 não herdam preços de 1850. Fita HF e parciais de Custos_cenarios/Custos_propostas não são preços por linha nem total de materiais: não são usados como faltas completas. Off-white não herda opção Lume sem escolha/SKU.
- **Sem base:** lacuna não quantificada, troca sem crédito, formato diferente ou serviço sem preço impedem total equivalente fechado e pontuação. O parcial mínimo–máximo é incompleto, não teto de gasto. Painéis agregados e comparações L100/L101 não são somados com chapas/ferragens/fita. Não há rateio artificial por móvel.
- **Verba:** deltas do parcial são indicativos; folga até 35 mil só aparece com custo completo. Provisão de marcenaria 46.500 e execução **R44 137.748,11** estão no arquivo histórico chamado Orcamento_R43.md. Cenário global só substitui 46.500 por escopo integral completo. D05-C vigente de 37 mil/127.101,22 permanece condicionado e não é alterado; uma proposta da etapa não é comparável ao integral.

Validade vencida, dados ausentes, sinal acima de 30% e garantia abaixo de 12 meses geram alertas. **30% e 12 meses são hipóteses de triagem, sem juízo jurídico.** Conferir reajuste, pagamento, multa, garantia e medição na origem. O cronograma alvo é obra em oito semanas e mudança até 12. O motor soma apenas produção→entrega→montagem com calendário corrido e início/gatilho explícitos. Mesmo cabendo, pedras, RT e obra final continuam pendentes; dias úteis ou dados ausentes deixam a conclusão indeterminada.

Ranking condicional: preço equivalente máximo 35%, cobertura 25%, reajuste 15%, prazo 10%, garantia 10%, substituições 5%. Preço recebe 100×menor máximo/máximo da proposta, só no mesmo escopo; cobertura é percentual das 101 linhas sem troca; reajuste baixo/medio/alto vale 100/50/0; prazo até semana 8/12/acima vale 100/50/0; garantia satura em 12 meses; cada troca desconta 20 pontos do critério. Pesos não negativos, soma positiva, editáveis. Dados faltantes deixam pontuação vazia, nunca nota zero presumida. Não escolhe fornecedor.

## Saídas e integridade

[Matriz vazia para preencher](Matriz_cobertura_modelo.csv) · [cabeçalho das perguntas](Perguntas_modelo.csv). Resultados ficam em `../outputs/Codex_cotacao_e_chaves/`: inventário, JSON normalizado, Comparacao.json, matriz, custos, perguntas, ranking e relatório curto. Dados recebidos não entram no git. Integração com o pipeline das chaves usa `--dependencias ../outputs/Codex_cotacao_e_chaves/Linhas_dependentes_medidas.csv` quando gerado; o campo `premissa_medida_in_loco` marca as linhas afetadas. Sem esse insumo, permanece a conferir.

SHA256 de `Comparacao.json` sem propostas: `cca7e4a8fda86b7c5be83371662787b74571688aab758e756d40db7b8901f162`. O JSON registra hashes das fontes de quantidade, custos e cronograma. Testes não alimentam resultados reais: fixture identificada em `ferramentas/estudos/testes/Cotacoes_ficticias.json`.

Integração das chaves preparada: 42.469 vínculos externos em Linhas_dependentes_medidas.csv (hash no README de 07_Imovel). A comparação vazia com esse insumo tem SHA256 `d39b8099706864518fa5bc7218f6702b223e0e5e49262763b38037e9e89f78bd`; continua sem proposta real.
