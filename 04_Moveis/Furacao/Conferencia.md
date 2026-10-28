# Conferência da furação nominal

**REPROVADO**: 37 ocorrências geométricas/acesso e 0 posições incompletas. 4 portas fora do envelope nominal de quantidade/proporção.

## Dez ocorrências de maior prioridade

| Peça | Face | x; y mm | Tipo | Outro | Medida mm |
|---|---|---|---|---|---|
| ApoioOpostoR001 | B | 34.0; 60.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 34.0; 120.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 238.0; 76.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 238.0; 136.0 | ACESSO | ApoioComumR004 |  |
| Peca213 | B | 76.0; 321.0 | ACESSO | GavetaComumR002 |  |
| Peca213 | B | 324.0; 321.0 | ACESSO | GavetaComumR002 |  |
| Peca213 | B | 60.0; 34.0 | ACESSO | GavetaComumR002 |  |
| Peca213 | B | 308.0; 34.0 | ACESSO | GavetaComumR002 |  |
| Peca228 | B | 60.0; 34.0 | ACESSO | GavetaComumR026 |  |
| Peca228 | B | 308.0; 34.0 | ACESSO | GavetaComumR026 |  |

Ocorrências são pares/regiões, não peças únicas. Interseção intencional do corpo/pino Minifix no mesmo grupo é excluída. Profundidade desconhecida não passa: fica incompleta. Distâncias entre faces diferentes só são calculadas com diâmetro, profundidade e referência espacial conhecidos, exigindo também a margem proposta3mm. Topos usam o curso da madeira no eixo do furo, não os 18 mm transversais.

## Cobertura e limites

Os canecos têm referência 2D histórica de porta; não há transformação suficiente para confrontá-los com peças vizinhas. Bases 37/32, linhas System32 e corrediças não individualizadas continuam sem verificação espacial: pendências de cobertura, não zero conflitos. Também não são simulados recortes, ponta cônica da broca, fita, parafusos já montados, mão ou mandril. AABB é triagem conservadora nos painéis especiais.

Ferramenta: cilindro proposto de raio 10 e curso 100 mm. Acesso bloqueado produz precedência em Montagem.csv; se houver ciclo, sequência executiva fica pendente. O CSV contém proposta para todos os 20 móveis, sem supor montagem/parede estáveis.

Portas.csv: área × espessura × 700 kg/m³, referência Sonae Arauco MDF ST CARB2/EPA >12–19 mm, p.1; não é densidade medida da Greenplac. Tabela Blum p.718/manual local p.2: envelopes 2/750/6, 3/1500/12, 4/2100/17, 5/2500/22 (dobradiças/mm/kg). Largura600–650 acrescenta uma; >650, >2500 ou >22 fica fora. Usar o maior requisito entre altura e peso é triagem conservadora, não interpolação da curva nem conclusão sobre retenção. MDF sem puxador, espelho ou revestimento: massa acabada permanece a confirmar. Portas abaixo de 4 kg exigem prova funcional.

Fontes: [Blum planejamento p.718](https://publications.blum.com/2024/catalogue/en/718/), [orientação Blum por largura](https://ea.blum.com/en/number-of-hinges/), [densidade nominal p.1](https://www.sonaearauco.com/media/vt5gihec/tds0356sair01_mdf-standard-carb2_epa_en.pdf).

Reproduzir: `python -B ferramentas/estudos/conferir_furacao.py`. Código1 é esperado enquanto houver conflitos ou parâmetros. Opções `--entrada`, `--saida`, `--margem`, `--ferramenta-comprimento`, `--ferramenta-raio` permitem ensaios externos; valores propostos não são mínimos do fabricante.

## Correção nominal e comparação

Antes: 3 conflitos de distância/sobreposição +43 acessos, com2.130 posições condicionadas. Ao preencher os catálogos sem mudar posições aparecem mais20 cruzamentos internos. Depois dos parâmetros propostos: 0 conflitos geométricos e 37 restrições de ferramenta; ver Antes_depois.json. O estado continua REPROVADO enquanto a sequência não for demonstrada.

P20: fase oposta16 em vez de32 move o corpo F02009 de(1730;92) para(1730;76), afastando F01978; cavilhas da junta J019 ficam20mm após o conector. Pares se movem juntos. P04 J004/J006 recebem+16mm; P07 J002 recebe−44mm e J005−28mm. Envelopes das peças preservados.

P17: os oito acessos em ApoioComumR001/ApoioOpostoR18 usavam as faces coladas uma à outra; os corpos passam às faces opostas livres (centro do pino A9 preservado). Proposta de montagem: usinar e ensaiar peças soltas; unir o par de divisórias; apresentar horizontais; apertar pelas faces livres; fechar fundo; instalar frentes por último. Aparência/tampas dos corpos nessas faces precisa de confirmação. Alternativa se não se aceitar corpo aparente: Confirmat+cavilha/cola nessas quatro juntas, com acesso exterior antes do fechamento; não adotada no mapa de316 Minifix.

Os 43 acessos anteriores pertenciam a P01/P03/P04/P06/P17/P20, somente8 ao P17. Permanecem37 após a nova distribuição: gavetas entram após o aperto; travessas/fundos bloqueadores entram depois dos apertos listados. Essa precedência é proposta, não prova de encaixe ou estabilidade. Não apagar os alertas por assumir a ordem.

Ø7×espessura do Confirmat é passagem intencional, com marcação explícita; apenas essa operação é excluída da regra de furo cego. Escareado exterior Ø10: perfil e batente dependem do SKU, continuam pendentes. Os2.286 centros têm Ø/profundidade, mas bases/corrediças/System32 ainda sem centros não estão nesse denominador.

As tabelas completas ficam fora do git. Regenerar com `python -B ferramentas/estudos/conferir_furacao.py --detalhes C:/Temp/gp-furacao`. Código1 preserva os alertas. SHA256 em Conferencia.json e README.md; saída externa via `--saida` também recebe as tabelas. A execução padrão no projeto mantém somente resumo, dez ocorrências, portas e montagem.
