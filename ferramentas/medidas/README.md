# Recálculo dimensional

Alturas nominais 2550/2300 mm e portas 800/700×2100 mm: Elias,01/11/2026, nesta conversa. Caixas preservadas; folgas ao teto e distâncias aos vãos recalculadas nas 469 regras. Nenhuma medida de campo preenchida.

**Fonte vinculada ao R55 corrigido:** 24 alvos conferidos no CAD; os envelopes do recálculo continuam iguais, com fórmulas preservadas. Parede/lavanderia e Loop incorporadas: Elias,01/11/2026, “Sim, incorporar essa correção”. Pranchas R02 seguem históricas; a seleção não inclui os novos objetos arquitetônicos.

`python ferramentas/medidas/recalcular.py` lê o CSV efetivo e aplica [regras](../../04_Moveis/Dependencias/regras.json). Somente resultado nominal vai para Dependencias/Impacto.md e Impacto.json. Se houver valor medido ou cenário, a saída padrão é temporária fora do repositório; o comando imprime o caminho. `--nominal` ignora medidos explicitamente e serve à reprodução da base.

`python ferramentas/medidas/recalcular.py --cenario C:/Temp/campo.csv --saida C:/Temp/impacto`

O cenário contém `codigo_medida,valor_medido,evidencia_campo`. Uma linha por código; m/cm/mm; dimensões compostas como `2468 x 2950 mm`. Sobrepõe apenas os códigos fornecidos, mantém o resto do CSV, não grava nele. Código desconhecido, repetido, valor vazio, sem unidade ou dimensão não positiva interrompe o processamento.

Pranchas: `python ferramentas/pranchas/gerar.py --cenario C:/Temp/campo.csv --saida C:/Temp/pranchas`. Preserva as entregas versionadas. Gera PDF, SVG, relatório geral e Impacto_moveis.json. Quando há mudança de envelope, omite os painéis internos congelados em vez de esticar ferragens. NC1 deixa vãos internos pendentes nos módulos alterados. Carimbo: recalculado, não modelado.

As fórmulas só aceitam números, constantes, soma/subtração e `m("codigo")`; não executam Python. Limites técnicos sem fonte permanecem nulos. Geometria negativa acusa NÃO CABE; alteração de interface acusa ajuste de fabricação (revisar recorte/implantação), sem afirmar colisão.

Teste: `python -B ferramentas/medidas/test_recalcular.py`, também no verificar_tudo.py e CI. Confere todas as fórmulas, 72 extensões contra envelopes da exportação, nove fechamentos, referências, prumo, precedência, entradas inválidas e integração. SHA do CAD é conferido por leitura binária, sem abrir FreeCAD.

## Ensaio completo

`python ferramentas/medidas/ensaiar.py` usa a [fixture fictícia](cenarios/ensaio_chaves.csv), cronometra comandos reais, compara relatórios, repete PDF, verifica hashes e apaga saídas. `--saida C:/Temp/ensaio` conserva resultados em pasta externa nova. [Tempos e limites manuais](../../04_Moveis/Dependencias/README.md).
