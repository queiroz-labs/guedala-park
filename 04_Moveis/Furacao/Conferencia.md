# Conferência da furação nominal

**REPROVADO**: 46 ocorrências geométricas/acesso e 2130 posições incompletas. 4 portas fora do envelope nominal de quantidade/proporção.

## Dez ocorrências de maior prioridade

| Peça | Face | x; y mm | Tipo | Outro | Medida mm |
|---|---|---|---|---|---|
| PecaBancoR16 | A | 1736.0; 91.0 | SOBREPOSICAO_FACE | F02009 | -5.417 |
| ApoioComumR001 | A | 34.0; 60.0 | ACESSO | ApoioOpostoR18 |  |
| ApoioComumR001 | A | 34.0; 220.0 | ACESSO | ApoioOpostoR18 |  |
| ApoioComumR001 | A | 480.0; 92.0 | ACESSO | ApoioOpostoR18 |  |
| ApoioComumR001 | A | 480.0; 252.0 | ACESSO | ApoioOpostoR18 |  |
| ApoioOpostoR001 | B | 34.0; 60.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 34.0; 120.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 238.0; 92.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR001 | B | 238.0; 152.0 | ACESSO | ApoioComumR004 |  |
| ApoioOpostoR18 | B | 34.0; 60.0 | ACESSO | ApoioComumR001 |  |

Ocorrências são pares/regiões, não peças únicas. Interseção intencional do corpo/pino Minifix no mesmo grupo é excluída. Profundidade desconhecida não passa: fica incompleta. Distâncias entre faces diferentes só são calculadas com diâmetro, profundidade e referência espacial conhecidos. Topos usam o curso da madeira no eixo do furo, não os 18 mm transversais.

## Cobertura e limites

Os canecos têm referência 2D histórica de porta; não há transformação suficiente para confrontá-los com peças vizinhas. Bases 37/32, linhas System32 e corrediças não individualizadas continuam sem verificação espacial: pendências de cobertura, não zero conflitos. Também não são simulados recortes, ponta cônica da broca, fita, parafusos já montados, mão ou mandril. AABB é triagem conservadora nos painéis especiais.

Ferramenta: cilindro proposto de raio 10 e curso 100 mm. Acesso bloqueado produz precedência em Montagem.csv; se houver ciclo, sequência executiva fica pendente. O CSV contém proposta para todos os 20 móveis, sem supor montagem/parede estáveis.

Portas.csv: área × espessura × 700 kg/m³, referência Sonae Arauco MDF ST CARB2/EPA >12–19 mm, p.1; não é densidade medida da Greenplac. Tabela Blum p.718/manual local p.2: envelopes 2/750/6, 3/1500/12, 4/2100/17, 5/2500/22 (dobradiças/mm/kg). Largura600–650 acrescenta uma; >650, >2500 ou >22 fica fora. Usar o maior requisito entre altura e peso é triagem conservadora, não interpolação da curva nem conclusão sobre retenção. MDF sem puxador, espelho ou revestimento: massa acabada permanece a confirmar. Portas abaixo de 4 kg exigem prova funcional.

Fontes: [Blum planejamento p.718](https://publications.blum.com/2024/catalogue/en/718/), [orientação Blum por largura](https://ea.blum.com/en/number-of-hinges/), [densidade nominal p.1](https://www.sonaearauco.com/media/vt5gihec/tds0356sair01_mdf-standard-carb2_epa_en.pdf).

Reproduzir: `python -B ferramentas/estudos/conferir_furacao.py`. Código1 é esperado enquanto houver conflitos ou parâmetros. Opções `--entrada`, `--saida`, `--margem`, `--ferramenta-comprimento`, `--ferramenta-raio` permitem ensaios externos; valores propostos não são mínimos do fabricante.
