# Dependências dimensionais dos móveis

Regras geométricas da R53, 27/10/2026. [Dados](regras.json). Nenhuma medida real incorporada e nenhum FCStd aberto.

469 cotas/referências: 20 módulos e quatro bancadas. X/Y são eixos globais da planta, não largura/profundidade comercial.

| Alvo | Regras |
|---|---:|
| P01 | 9 |
| P02 | 10 |
| P03 | 10 |
| P04 | 10 |
| P05 | 22 |
| P06 | 22 |
| P07 | 22 |
| P08 | 22 |
| P09 | 23 |
| P10 | 23 |
| P11 | 23 |
| P12 | 23 |
| P13 | 22 |
| P14 | 24 |
| P15 | 25 |
| P16 | 9 |
| P17 | 10 |
| P18 | 33 |
| P19 | 33 |
| P20 | 6 |
| Peca110 | 9 |
| Peca308 | 22 |
| Peca357 | 24 |
| Peca399 | 33 |

## Critério e perguntas

1. Manter caixas fixas e variar folgas/fechamentos? Recomendação: sim, até confirmar quais peças podem mudar. A diretriz de teto não autoriza aumentar portas. P04 é quarto; P17 escritório; aéreos da cozinha são P09–P12.
2. Folgas grandes são espaço para outros módulos/circulação, não largura de arremate. Recomendação: medir faces e interfaces locais antes de distribuir sobra. Valores negativos precisam de conferência, sem deslocamento automático.
3. P15 deve receber fechamento ao teto? Recomendação: confirmar enquadramento e acesso antes de criar peça.
4. Pontos e vãos são referências assinadas relativas ao envelope. Recomendação: manter caixas e revisar recortes/acessos com oficina/RT quando mudarem; o script não decide a tubulação.

## Folgas a conferir (mm)

Calculadas como posição inicial menos origem do ambiente e fim do ambiente menos extremidade R53. Não foram inventadas folgas laterais iguais. A soma inclui espaços ocupados por outros objetos. Altura usa PD nominal atual menos topo, evitando o PD histórico 2600 do banheiro gravado na exportação.

- P01 extensao_x: folga_fim=440
- P01 extensao_y: folga_inicio=2290
- P01 altura: folga_topo=468
- P02 extensao_x: folga_fim=1790
- P02 extensao_y: folga_inicio=1890
- P02 altura: folga_topo=160
- P03 extensao_x: folga_inicio=660, folga_fim=440
- P03 extensao_y: folga_inicio=2290
- P03 altura: folga_topo=160
- P04 extensao_x: folga_fim=2190
- P04 extensao_y: folga_inicio=90, folga_fim=1060
- P04 altura: folga_topo=160
- P05 extensao_x: folga_inicio=600, folga_fim=2270
- P05 extensao_y: folga_inicio=940
- P05 altura: folga_topo=1700
- P06 extensao_x: folga_inicio=1250, folga_fim=1651
- P06 extensao_y: folga_inicio=940
- P06 altura: folga_topo=1700
- P07 extensao_x: folga_inicio=-13, folga_fim=2920
- P07 extensao_y: folga_inicio=952.5
- P07 altura: folga_topo=1700
- P08 extensao_x: folga_inicio=600, folga_fim=1651
- P08 extensao_y: folga_inicio=1020
- P08 altura: folga_topo=2420
- P09 extensao_x: folga_inicio=-25, folga_fim=2895
- P09 extensao_y: folga_inicio=1200
- P10 extensao_x: folga_inicio=625, folga_fim=2348
- P10 extensao_y: folga_inicio=1200
- P11 extensao_x: folga_inicio=1172, folga_fim=1651
- P11 extensao_y: folga_inicio=1200
- P12 extensao_x: folga_inicio=1869, folga_fim=850
- P12 extensao_y: folga_inicio=1200
- P13 extensao_x: folga_inicio=1172, folga_fim=1651
- P13 extensao_y: folga_inicio=1080
- P13 altura: folga_topo=1050
- P14 extensao_x: folga_fim=700
- P14 extensao_y: folga_inicio=910
- P14 altura: folga_topo=1680
- P15 extensao_x: folga_inicio=470, folga_fim=-15
- P15 extensao_y: folga_inicio=1190
- P15 altura: folga_topo=370
- P16 extensao_x: folga_inicio=150, folga_fim=1750
- P16 extensao_y: folga_inicio=250, folga_fim=2270
- P16 altura: folga_topo=1880
- P17 extensao_x: folga_fim=1950
- P17 extensao_y: folga_inicio=900
- P17 altura: folga_topo=150
- P18 extensao_x: folga_inicio=1490
- P18 extensao_y: folga_inicio=770
- P18 altura: folga_topo=1755
- P19 extensao_x: folga_inicio=1490
- P19 extensao_y: folga_inicio=1090
- P19 altura: folga_topo=600
- P20 extensao_x: folga_inicio=1900, folga_fim=100
- P20 extensao_y: folga_inicio=1900, folga_fim=100
- P20 altura: folga_topo=2200
- Peca110 extensao_x: folga_inicio=150, folga_fim=150
- Peca110 extensao_y: folga_fim=2250
- Peca110 altura: folga_topo=1850
- Peca308 extensao_x: folga_fim=1651
- Peca308 extensao_y: folga_inicio=920
- Peca308 altura: folga_topo=1680
- Peca357 extensao_x: folga_fim=-40
- Peca357 extensao_y: folga_inicio=790
- Peca357 altura: folga_topo=1680
- Peca399 extensao_x: folga_inicio=1490
- Peca399 extensao_y: folga_inicio=790
- Peca399 altura: folga_topo=1735

## Cobertura e limites

As três extensões de cada envelope são fixas; o recálculo verifica encaixe nos limites do ambiente. Nove fechamentos seguem o teto. Portas/janelas e pontos hidráulicos/gás do ambiente são monitorados em coordenadas relativas, inclusive quando fora da projeção do móvel: não significam colisão. Bancadas: Peca308 cozinha, Peca357 lavanderia, Peca399 banheiro, Peca110 escritório.

Mesa, sofá e cadeiras: independentes, fora das regras. Peças internas, furações, recortes, espessuras, movimento de portas, alinhamentos entre módulos e distribuição de sobras permanecem manuais: não há dependência executiva documentada para inferi-los. O desvio DEP-COZ-PRUMO é nominal zero (parede plana do modelo); medir base/topo com sinal positivo para dentro. Outros trechos precisam de levantamento próprio.

## Executar e interpretar

[Relatório nominal](Impacto.md) · [resultado completo](Impacto.json) · [comandos e testes](../../ferramentas/medidas/README.md). Reprodução: 469 fórmulas sem diferença nominal; 72 cotas de envelope conferidas diretamente contra R53. Os nove fechamentos e 388 referências são distâncias derivadas, não 397 peças modeladas.

Prumo positivo reduz a folga de fundo dos módulos da cozinha: se a parede avançar 12 mm sobre uma caixa sem folga nominal, NÃO CABE, mesmo preservando sua dimensão. Limites de fabricação não documentados ficam nulos; não foi inventada tolerância de 50 mm. Esse número apenas seleciona perguntas de folga.
