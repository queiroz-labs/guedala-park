# Perguntas em aberto

**34 perguntas deduplicadas**, a partir de 1725 trechos de 74 arquivos. Nada enviado. Cadastro por tema; classificação documental para revisão, sem parecer técnico.
[Perguntas](Perguntas.csv) · [todas as origens/citações por PQ](Origens.csv) · [decisões já respondidas](Respostas_decisoes.csv). IDs semânticos estáveis PQ-001…PQ-034; lacunas de numeração não são perda de pergunta.

## Destinatários

| Destinatário | Perguntas | Modelo |
|---|---:|---|
| Elias | 1 | [mensagem](Mensagens/elias.md) |
| RT | 7 | [mensagem](Mensagens/rt.md) |
| Construtora | 8 | [mensagem](Mensagens/construtora.md) |
| Condomínio/administração | 4 | [mensagem](Mensagens/condominio_administracao.md) |
| Oficina/marceneiro | 6 | [mensagem](Mensagens/oficina_marceneiro.md) |
| Fornecedor | 6 | [mensagem](Mensagens/fornecedor.md) |
| Concessionária de gás | 1 | [mensagem](Mensagens/concessionaria_de_gas.md) |
| Outro | 1 | [mensagem](Mensagens/outro.md) |

## Bloqueios e cinco maiores abrangências

| Etapa | Perguntas que a bloqueiam |
|---|---:|
| compra | 24 |
| corte | 13 |
| fabricação | 11 |
| obra | 27 |
| mudança | 12 |
| protocolo da reforma | 14 |

Top 5 por **número de classes de etapa diretamente bloqueadas**, sem duplicar a mesma classe. Isso mede abrangência documental, não dias ganhos ou quantidade de peças. Empate: caminho declarado da marcenaria, segurança/conformidade, depois custo. Não há caminho crítico global comprovado.

- PQ-001: 5 = compra + corte + fabricação + mudança + obra
- PQ-002: 4 = corte + fabricação + mudança + obra
- PQ-021: 4 = compra + corte + mudança + obra
- PQ-008: 4 = corte + fabricação + obra + protocolo da reforma
- PQ-022: 4 = compra + corte + fabricação + obra

## Uso e limites

`python -B ferramentas/estudos/pacote_perguntas.py` (raiz, Python local); testes: `python -B ferramentas/estudos/test_pacote_perguntas.py`.
Varre READMEs recursivos de 01/03/04/05/07/08, estado, plano/roteiro oficial, checklist B1/B2/B3, roteiro de campo, medidas e descrição física; consulta as saídas externas disponíveis. O Registro é consultado somente por rg em códigos/temas, nunca lido inteiro.
Origens.csv mantém uma linha por PQ/origem, com citação curta; Perguntas.csv traz duas citações de consulta e a chave para todas as demais, sem células gigantes. Texto integral extraído e manifesto de hashes ficam em ../outputs/Codex_perguntas_e_risco/. Linha de CSV é registro lógico + cabeçalho; campos multilinha exigem conferência no arquivo. Deduplicação por objetivo semântico conserva as origens; responder por origem/código quando os casos diferirem.
D01–D06 não são reabertas: respostas com fonte estão na tabela separada. Solicitar amostras A/C já foi respondido; a seleção final por amostra e a comprovação técnica continuam pendentes. Decisão de layout não equivale a cumprimento de manual ou ensaio. Remover pergunta respondida exige fonte; resposta parcial permanece. Não inferir resposta de mero uso da palavra confirmado num histórico.
Dependências no CSV representam precedência documental; conferir medidas/datum e contratar RT antes de protocolo, e medição/executivo antes de corte/fabricação. Os 15 primeiros por prioridade recebem consequência A/B conservadora, ligada às próprias origens; não autoriza mudar decisão, peça ou orçamento.
Mensagens são modelos por destinatário, com placeholders. RT separa contratação e pareceres; construtora separa por documento; condomínio cobre protocolo, horários/taxas, piso/ruído e elevador. Sem dados pessoais, contatos ou nome de profissional. Campo Outro exige identificação do destinatário antes de enviar.
Classificação automática tem limites: revisar agrupamentos e contexto nas origens antes de enviar. Trechos históricos não provam pendência atual; decisões explícitas correntes prevalecem. A varredura é rastreável, não certificação de completude técnica.
Publicação: nenhuma alteração em current_release.json/document_library ou no site. Falta registrar este pacote na biblioteca e regenerar/verificar o site em frente autorizada de publicação.

SHA256 Extracao_perguntas.json: `95d7156c83bf7f9326d84cbe281bfdcc1d789ac8f673b859c42197db1858b83c`; Perguntas.csv: `1d607b7e6af1691bc32b9aef6fa112e9412fa12632a4203b13b1774bafb46af4`.
