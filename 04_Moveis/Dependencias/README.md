# Dependências dimensionais dos móveis

**Fonte vigente R54, 27/10/2026:** SHA e caminho sincronizados com o pedestal Berlin e afastamento de 15 mm da cadeira lateral. Os 24 envelopes usados no recálculo dimensional permanecem iguais; fórmulas e medidas nominais preservadas.

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

## Dia das chaves — passo a passo

1. Meça teto/piso em vários pontos, paredes na base/topo, vãos e pontos; registre unidades, eixos, fotos e evidência. Use o menor vão livre, não a média.
2. Crie CSV externo com `codigo_medida,valor_medido,evidencia_campo`, códigos da base e ambos os eixos DIM. Não reutilize valores fictícios do ensaio.
3. Rode `python ferramentas/medidas/recalcular.py --cenario C:/Temp/campo.csv --saida C:/Temp/impacto`.
4. Abra Impacto.md; separe conflito nominal, novo NÃO CABE, folga e referência de instalação. Espaço livre total não é peça de arremate.
5. Levante PR-WALLS, pisos/vãos e continuidade entre ambientes: DIM não define para que lado uma parede mudou.
6. Rode `python ferramentas/pranchas/gerar.py --cenario C:/Temp/campo.csv --saida C:/Temp/pranchas`; revise PDF, Impacto.html e Impacto_moveis.json.
7. Decida com oficina/RT quais caixas mudar e como fechar encontros/recortes; documente antes de trocar o modo nas regras.
8. Incorpore somente medições reais conferidas ao CSV, com evidência/data; preserve nominais. Repita com CSV externo conferido e testes. O relatório versionado continua nominal.
9. Havendo mudança física, edite FreeCAD pela GUI em tarefa autorizada; reexporte e atualize regras/fichas/pranchas. Execute verificação completa, sem ajustar base para esconder conflito.
10. Rode verificar_tudo.py e revise antes de entregar. O resultado automático é estudo, não executivo de corte.

## Ensaio fictício — 27/10/2026

[Fixture](../../ferramentas/medidas/cenarios/ensaio_chaves.csv). Repetir: `python ferramentas/medidas/ensaiar.py` (apaga saídas temporárias). `--saida C:/Temp/ensaio` conserva resultados em pasta externa nova.

| Passo | Tempo observado |
|---|---:|
| Recálculo via comando real | 0,1408 s |
| 20 pranchas SVG/HTML/PDF e impacto | 0,4775 s |
| Conferência cruzada dos relatórios | 0,1096 s |
| Fluxo automático total | 0,7279 s |
| Segunda geração para idempotência | 0,4690 s |

Medição única nesta máquina; inclui inicialização dos processos, exclui medição no imóvel, digitação, revisão visual e edição CAD. Hashes do CSV, fatos, FCStd, relatórios nominais e entregas vigentes: preservados. Repetição: zero alterações e PDF idêntico. Oito testes rápidos integram o verificador. A regressão antiga de pranchas também passou (99 cotas e quatro conflitos no cenário próprio).

Resultados: 28 referências/fechamentos mudaram; as 72 dimensões de envelope ficaram fixas. 406 OK, 25 ajustes de arremate, 24 revisões de fabricação/interface e 14 NÃO CABE. Destes, quatro já eram nominais; dez são novos avisos de fundo por prumo (P05–P13 e bancada Peca308). As pranchas registraram 84 mudanças de cota/origem contra a entrega vigente; 209 avisos incluem repetições por folha e pendências existentes, não 209 defeitos distintos.

P02/P03/P04: fechamento 160 → 30 mm; P17: 150 → 20 mm. Água C05 relativa ao início X de P05: 220 → 300 mm; peitoril relativo à base P01: 950 → 990 mm. Folga final X: quarto +18 mm, cozinha −25 mm, lavanderia −30 mm; sala −20 mm na folga ao teto. Folga final Y da cozinha: −12 mm pelo prumo simulado. Nenhuma caixa encolhida automaticamente.

Detalhe da pergunta 2: P07 −13 mm e P09 −25 mm na origem X da cozinha; P15 −15 mm e Peca357 −40 mm no fim X da lavanderia. Conflitos com o **retângulo principal**, não prova de colisão: existe faixa complementar na cozinha. Conferir limites locais e continuidade antes de mudar caixas.

20 páginas rasterizadas; visão geral e E05 inspecionadas. Formato A3 e carimbo “recalculado, não modelado” em todas. Nenhum PDF fictício versionado. SHA256 da fixture: `3835deec53ad1014d654ac3a8d0e22226805aa76bdd5921b533af137b8ebb582`.

### O que quebrou ou continuou manual

- Git/hook e temporários falharam no sandbox Windows; executados com permissão fora dele, sem desativar verificações. Não é falha do modelo.
- Encaminhamento de argumentos ao Python com ReportLab corrigido para cenário/saída; Geometria.json separado da saída externa. Cenários preservam entregas.
- Prumo agora reduz a folga limitante de fundo. Vãos internos ficam pendentes se o envelope mudar; painéis/ferragens não são esticados.
- DIM não resolve topologia. Aviso acrescentado às plantas; distribuição entre faces/ambientes exige medição humana.
- Reduzir caixa, mudar implantação, criar fechamento e refazer recortes continuam decisões humanas. Ponto fora do envelope não comprova colisão; o relatório detecta mudança.
- Revisão automática bloqueou documentação por risco de tamanho do ESTADO_ATUAL.md. Resolvido reduzindo seu resumo e mantendo detalhes aqui; limites preservados.

### FreeCAD — trabalho manual e estimativa por móvel

Faixas de planejamento, **não cronometradas**: localizar parâmetros/peças, fazer um ajuste simples já decidido e conferir visualmente. Caixa preservada não precisa de edição; fechamento novo precisa ser modelado. Interfaces compartilhadas não são serviços independentes.

| Móvel | Ainda manual no CAD | Estimativa se alterar |
|---|---|---:|
| P01 | Caixa/portas e encontro P02/P03 | 30–60 min |
| P02 | Retorno L, quina, juntas e fechamento | 40–90 min |
| P03 | Fechamento, folhas e encontro P01 | 25–50 min |
| P04 | Fechamento e implantação na cabeceira | 20–40 min |
| P05 | Recortes/acesso hidráulico e bancada | 30–60 min |
| P06 | Caixa, frentes e guias | 25–50 min |
| P07 | Nicho de cocção e folgas do produto | 30–60 min |
| P08 | Caixa móvel, rodízios e retirada | 25–50 min |
| P09 | Fechamento, depurador e implantação | 20–40 min |
| P10 | Fechamento, divisões e portas | 20–40 min |
| P11 | Fechamento e nicho do micro | 25–50 min |
| P12 | Fechamento e nicho da geladeira | 20–40 min |
| P13 | Apoio e posição do micro | 15–30 min |
| P14 | Caixa, tanque/cesto e recortes | 30–60 min |
| P15 | Enquadramento ao teto e encontro cozinha | 25–50 min |
| P16 | Gavetas, bancada e guias | 25–50 min |
| P17 | Fechamento e implantação escritório | 20–40 min |
| P18 | Portas, frente removível, cuba/acessos | 30–60 min |
| P19 | Espelho/portas e encontros | 20–40 min |
| P20 | Banco/tampas, parede e acesso | 25–50 min |

Bancadas Peca110/308/357/399: 20–45 min cada para contorno/recortes, com decisões e medidas disponíveis. Depois: reexportação/regeneração, revisão conjunta e verificação completa do modelo (referência do projeto: ~8 min, não executada aqui). Ligações, oficina e RT fora dessas estimativas.

Pergunta 5: criar planilha mestre no CAD? Recomendação: sim para parâmetros estáveis de implantação, caixas e fechamentos, após definir cotas variáveis; não automatizar inicialmente recortes, ferragens ou distribuição entre módulos. O ensaio mede velocidade do relatório, não da remodelagem: caixas conservadas por falta de decisão de redimensionar.
