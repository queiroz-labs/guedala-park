# Origem das medidas

[Voltar ao assunto](README.md) · [Resumo do projeto](../Resumo.md)

Referência original: A01.2. As capas dos PDFs conservam esse código.

**R00 | 08/09/2026 | Estudo preliminar | Etapas 1 a 3**

[Abrir as seis pranchas em PDF](Plantas_e_instalacoes_R00.pdf)

## Resultado

Base consolidada na orientação de P01, avaliação de estimativas gráficas e inventário de 23 registros de instalações/elementos. As nove tomadas em sete placas foram mantidas sem duplicar pontos que reaparecem em fotografias. Não foi iniciada a distribuição final dos módulos nem alterada escolha de material.

Elias informou o 8º andar, dentro do intervalo do 4º ao 16º declarado em P01. Torre 2 e final 06 são a identificação da planta recebida; a resposta desta etapa informou apenas o andar. Elias não tem as medidas dos revestimentos originais mostrados no vídeo.

## 1. Geometria documental

| Cota de P01 | Interpretação |
|---|---|
| 1,29 m | Trecho da área de serviço paralelo à frente da cozinha, da face da parede da janela ao limite desenhado entre setores. |
| 1,54 m | Dimensão perpendicular da área de serviço junto ao limite com a cozinha. Não é uma alternativa de comprimento para a mesma parede. |
| 3,52 m | Trecho da cozinha depois da faixa desenhada entre setores, até a face lateral junto à entrada. |
| 1,55 m | Dimensão transversal indicada no setor da cozinha. Não é largura de circulação livre depois dos móveis. |

P01 tem uma faixa estreita entre os trechos cotados. Sua natureza não foi confirmada. A soma das duas cotas longitudinais é 4,81 m, mas exclui a faixa gráfica intermediária e não define a bancada. O alcance da bancada a partir do fim da geladeira depende do layout e do equipamento escolhido.

A prancha 1 usa um recorte da planta original, preservando paredes, aberturas, símbolos e ressaltos. J/L3 = parede da janela; K1 = parede da pia/equipamentos; L1/L2 = tanque e retorno técnico; E = entrada; F = faixa desenhada entre setores. A correspondência dos detalhes do vídeo é topológica, não uma medição.

## 2. Estimativas gráficas

As estimativas vêm do desenho de P01, e não de medidas reais do imóvel. Foram comparadas três cotas: 1,29 m, 3,52 m e 1,55 m. A escala mediana é 44,093 pontos de PDF por metro; a dispersão entre as escalas é aproximadamente 0,52%. Cada extremidade foi variada em 0,4 ponto para a análise de sensibilidade, também usando a menor e a maior escala. Os intervalos publicados foram arredondados para fora.

**Essas faixas medem sensibilidade de leitura do desenho. Não são tolerâncias de obra, intervalos estatísticos ou garantia de exatidão física. A cota escrita prevalece sobre o traço.**

| ID | Trecho | Estimativa | Sensibilidade gráfica | Limite |
|---|---|---|---|---|
| G-01 | Vão desenhado da janela de serviço | 0,99 m | 0,96-1,01 m | Extremos da abertura em P01; não é passagem livre de ar. |
| G-02 | Abertura representada da entrada | 0,81 m | 0,78-0,83 m | Representação do vão; não comprova largura útil entre batentes. |
| G-03 | Largura do símbolo da pia | 1,20 m | 1,17-1,22 m | Dimensão do símbolo em P01; não identifica a pia entregue. |
| G-04 | Profundidade do símbolo da pia | 0,53 m | 0,50-0,55 m | Dimensão gráfica; não especifica a bancada futura. |
| G-05 | Entre contorno do ressalto e início da pia | 1,15 m | 1,12-1,17 m | Trecho gráfico; tem instalações no vídeo e não está livre para móveis. |
| G-06 | Extensão transversal entre faces laterais | 4,84 m | 4,80-4,87 m | Inclui a faixa F; projeção entre faces, não percurso de pedra. |
| G-07 | Recuo do contorno estrutural junto ao tanque | 0,20 m | 0,17-0,22 m | Apenas a linha de contorno de P01; não é a profundidade total do shaft. |

### Memória dos segmentos de P01

Coordenadas em pontos de PDF, com origem no canto superior esquerdo. G-01: y=314,60 a 358,16; G-02: y=331,28 a 366,92; G-03: x=385,40 a 438,20; G-04: y=350,00 a 373,28; G-05: x=334,88 a 385,40; G-06: x=300,68 a 513,92; G-07: y=364,76 a 373,52. G-07 mede o recuo da linha estrutural, não todo o fechamento técnico. Conferir o traço com a prancha original se houver dúvida sobre a interpretação.

### Avaliação do vídeo

COZ-02 é útil para relacionar janela, grelha, tanque, retorno técnico, gás e pia. LAV-07 mostra as interferências inferiores. LAV-08 e AD-0322 mostram o alto. AD-0246 e AD-0302 aproximam os pontos próximos à máquina. As imagens permitem mapear os elementos e comparar proporções, mas não há referência vertical medida nem calibração de lente.

Um teste piloto com os quatro cantos externos da janela em COZ-02 produziu uma razão de largura grelha/janela de 0,455. Com perturbações uniformes de até 5 pixels em todos os vértices, 1.000 amostras (semente 9) variaram de 0,415 a 0,493. Esse resultado não é independente da seleção de bordas; há distorção de lente não modelada e possível diferença entre os planos da esquadria e da grelha. Não foi convertido em centímetros, nem adotado como dimensão de compra ou de ventilação. A altura física da janela não foi determinada pela transformação.

Método de referência: [documentação oficial do OpenCV sobre homografia e retificação de planos](https://docs.opencv.org/4.10.0/d9/dab/tutorial_homography.html). A análise numérica foi realizada com os pontos registrados no arquivo de rastreabilidade.

## 3. Mapa de instalações

Os pontos estão identificados nas fotografias e relacionados às faces na planta. Suas coordenadas reais X/Y/Z não foram inferidas. Os lados direito/esquerdo nas descrições abaixo se referem à unidade filmada. O espelhamento não implica igualdade dos eixos entre unidades.

| ID | Face | Elemento | Quantidade visível | Evidência | Pendência |
|---|---|---|---|---|---|
| K-E01 | K1 | Tomada próxima à entrada | 1 | AD-0166 | Circuito, tensão e posição na unidade. |
| K-E02 | K1 | Placa dupla à direita da pia no vídeo | 2 | AD-0166/0170 | Circuitos e altura da bancada futura. |
| K-E03 | K1 | Tomada alta | 1 | AD-0178 | Função, circuito e altura. |
| K-E04 | K1 | Tomada acima da pia | 1 | AD-0186 | Altura e relação com frontão. |
| K-E05 | K1 | Tomada sob a pia | 1 | AD-0202/0206 | Acesso pelo gabinete e circuito. |
| K-E06 | K1 | Placa dupla próxima ao retorno técnico | 2 | AD-0246 | Circuitos e posição. |
| K-E07 | K1 | Tomada abaixo de K-E06 | 1 | AD-0246 | Equipamento atendido e circuito. |
| K-G01 | K1 | Registro de gás entre pia e tanque | 1 | AD-0238/0246 | Posição real e acesso à conexão. |
| K-H01 | K1 | Torneira da pia, dois comandos | conj. | AD-0218 | Identificar água fria/quente. |
| K-H02 | K1 | Sifão, fechamento e suportes da pia | conj. | AD-0202/0206 | Volume ocupado e acesso. |
| L-H01 | L1 | Tanque suspenso e torneira | conj. | AD-0262 | Eixos, fixação e geometria. |
| L-H02 | L1 | Duas conexões na região do aquecedor | 2 | AD-0278 | Identificar cada entrada/saída. |
| L-G01 | L1 | Válvula de gás junto ao aquecedor | 1 | AD-0278 | Ligação, manual e acesso. |
| L-H03 | L2 | Ponto tampado e abertura inferior | 2 | AD-0302 | Provável máquina; função e diâmetros. |
| L-H04 | L1 | Registro abaixo do tanque | 1 | AD-0262 | Trecho da rede que ele isola. |
| L-G02 | L1/L2 | Tubulação aparente sob o tanque | - | AD-0262/0246 | Rede provável de gás; percurso completo. |
| L-D01 | piso AS | Ralo próximo ao tanque | 1 | AD-0262 | Localização, acesso e caimentos. |
| L-V01 | J/L3 | Grelha abaixo da janela | 1 | LAV-07 | Dimensões, função e área livre. |
| L-V02 | J/L3 | Abertura circular acima da janela | 1 | LAV-08 | Função de exaustão ainda não comprovada. |
| L-C01 | L1/L2 | Ressalto e volumes superiores | conj. | AD-0322 | Profundidades e alturas reais. |
| L-I01 | oposta | Interfone | 1 | AD-0334 | Posição e acesso à operação. |
| E-C02 | oposta | Duas teclas junto ao interfone | 2 | AD-0334 | Retorno de cada comando. |
| T-I01 | teto | Saídas no conjunto social/cozinha/AS | 4 | AD-0446 | Separar ambientes, eixos e circuitos. |

Os identificadores originais da R02 foram preservados. T-I01 abrange também o setor social; suas quatro saídas não significam quatro pontos exclusivos da cozinha e lavanderia. Na unidade filmada, o aquecedor ainda não estava instalado. Não foram presumidos circuitos, tensão, bitolas, alimentação de água quente ou função definitiva da abertura circular.

## Pendências remanescentes

| Informação | Por que importa | Como fechar |
|---|---|---|
| Pé-direito e alturas dos rebaixos | Limites dos aéreos e espaço do varal | Levantamento ou corte oficial cotado. |
| Peitoril, altura da janela, ventilação | Relação com bancada e área técnica | Medidas e documentação da esquadria/sistema. |
| Volume técnico completo | Espaço efetivo sob tanque, ao lado da máquina e acima | Croqui cotado e projeto de instalações. |
| Eixos e alturas de cada ponto | Compatibilização com gabinete, cesto e equipamentos | Planta de instalações ou levantamento na unidade. |
| Tipo da faixa F e interface cozinha/serviço | Continuidade da pedra e passagem | Manual, detalhe oficial ou observação na unidade. |
| Modelos dos equipamentos | Vãos, folgas e ponto inicial da bancada após geladeira | Modelos e manuais; necessários na próxima etapa de layout. |

## Correções que orientam a continuidade

- O A04.1 R00 tratava a direção de 1,29/1,54 m como pendência. A leitura documental desta etapa resolve a orientação; continua faltando a medida acabada, não qual direção cada cota representa.
- As conclusões de cabimento do A04.1 R00 baseadas em dimensões típicas de máquina e tanque não são adotadas como prova de viabilidade. A mudança de posição do tanque ou um degrau na pedra não ficam autorizados por essas hipóteses.
- A estimativa anterior de pé-direito de 2,60 m não foi incorporada.
- O apoio de aproximadamente 15 cm é requisito do briefing. Não foi encontrado nem medido em P01 ou no vídeo. A direção e a forma desse apoio deverão aparecer no próximo estudo.
- A R01 permanece a referência documental, complementada pela R02. O frame de 11:06 ainda mostra A; a associação provável é A → Dormitório 02 e B → Dormitório 01.
- Permanecem preservadas as decisões do memorial e do briefing, inclusive a ausência de azul nos móveis do quarto.

## Arquivos e verificação

- PDF: seis pranchas de consulta e revisão.
- Este memorial: resultados, método, referências e pendências.
- `Dados_das_medidas_R00.json`: cotas, segmentos, cálculos e inventário com coordenadas reais em branco.

Fontes: `02_Plantas_e_manuais/Planta_oficial.pdf`; HTMLs A01.1 R01 e R02 e seus frames; memorial de decisões v2; briefing e resposta de Elias sobre o andar. Os documentos originais foram preservados. Esta R00 complementa o levantamento e não libera fabricação ou intervenção nas instalações.
