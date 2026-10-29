# Estudo fotométrico do apartamento

Estudo de 29/10/2026; hipóteses explícitas, sem seleção de produto ou alteração de orçamento/CAD. Gerado por `ferramentas/estudos/estudo_fotometrico.py`.

## Enquadramento e níveis-alvo

N1 trata de trabalho interior. Seus 500 lx mantidos, U0≥0,70, UGR≤19 e Ra≥80 são referência da tarefa de escritório; não uma exigência geral para todos os cômodos domésticos. N2 é referência histórica secundária residencial. Edição aplicável precisa ser confirmada pelo RT; a edição internacional ISO/CIE2025 não atualiza automaticamente a adoção ABNT. Os demais valores são metas de conforto deste estudo, não texto de norma.

| Ambiente | Tarefa | Plano m | Meta lx | U0 | Natureza e fonte |
|---|---|---:|---:|---:|---|
| sala | geral | 0.75 | 150 | 0.4 | conforto residencial adotado; N2 §5.3.65 |
| sala | mesa/leitura | 0.75 | 500 | 0.7 | meta residencial para leitura/jogos; N2 §5.3.65; N1 analogia tarefa |
| cozinha | geral | 0.75 | 150 | 0.4 | conforto residencial adotado; N2 §5.3.65 |
| cozinha | preparo | 0.85 | 500 | 0.7 | meta residencial exigente; N2 faixa local200–500; N1 analogia tarefa |
| cozinha | pia | 0.85 | 300 | 0.7 | meta residencial adotada; N2 §5.3.65 |
| lavanderia | geral | 0.75 | 150 | 0.4 | hipótese de conforto; H1; N2 analogia |
| lavanderia | tanque | 0.85 | 300 | 0.7 | meta residencial adotada; H1; N2 analogia tarefa |
| banho | geral | 0.75 | 150 | 0.4 | hipótese de conforto; H1; N2 analogia |
| banho | rosto vertical | 1.6 | 300 | 0.7 | meta residencial; faixa de teste150–500; H1; não é piso normativo para maquiagem |
| quarto | geral | 0.75 | 150 | 0.4 | conforto residencial adotado; N2 §5.3.65 |
| quarto | leitura cama | 0.45 | 300 | 0.7 | meta residencial adotada; N2 §5.3.65 |
| escritorio | geral | 0.75 | 150 | 0.4 | conforto residencial adotado; H1; N2 analogia |
| escritorio | mesa/monitores | 0.75 | 500 | 0.7 | referência normativa de tarefa laboral; N1 tabela5/22 e§4.3.4; UGR≤19,Ra≥80 |
| circulacao | piso | 0 | 100 | 0.4 | meta residencial adotada; N2 §5.3.65; não iluminação de emergência |
| sala | TV | 0.75 | 30 | 0 | faixa de conforto10–50, sem fonte visível/reflexo; H1; não requisito normativo |

Limpeza usa a geral+tarefas a100%, sem criar piso normativo próprio. Noite adota5–20 lx no percurso como hipótese de conforto, sem equivaler a iluminação de emergência. A meta TV refere-se ao ambiente, não iluminância da tela. Para maquiagem,300 lx verticais é meta de comparação residencial; não diagnóstico de cores ou suficiência para qualquer tarefa fina.

## Refletâncias e perdas

Acabamentos identificados no `data.js` e na decisão de chapas vigente; cor de imagem/RGB não é refletância fotópica medida. Faixas abaixo são hipóteses H2 de sensibilidade, não fichas dos materiais nem conversão automática de sRGB. Espelho e tela não podem ser tratados como difusores.

| Superfície vigente | ρ mínimo | ρ máximo | Premissa |
|---|---:|---:|---|
| teto branco | 0.70 | 0.85 | H2: pintura branca; não medido |
| Algodão Egípcio/off-white | 0.50 | 0.75 | H2: paredes claras foscas; não medido |
| Arenza/Beige Matt | 0.35 | 0.60 | H2: acabamento areia/fendi; não medido |
| Azul Petróleo/Sauge | 0.10 | 0.30 | H2: cores escuras/verde; não medido |
| Itaúnas | 0.45 | 0.70 | H2: pedra clara; componente especular não modelado |
| Olmo/greige | 0.15 | 0.35 | H2: piso; não medido |
| suede cinza/areia | 0.20 | 0.50 | H2: tecido; não medido |
| metal preto/tela apagada | 0.02 | 0.10 | H2: difusa apenas; reflexo especular não modelado |

H3: fatores de manutenção0,70/0,80/0,90 (baixo/central/alto); N1§4.8 exige justificar manutenção real, não usar estes fatores como garantia. H4: FU zonal0,30/0,45/0,60 para comparação; não são tabela do fabricante, nem derivados das refletâncias. O FU concentra distribuição e reflexões de forma agregada. A análise direta ponto a ponto não usa FU e não soma reflexão inventada.

H5: transmissão Jurerê0,50/0,65/0,85; âmbar0,40/0,55/0,75; perfil/difusor0,60/0,75/0,90. Faixas de ensaio escolhidas pelo estudo, não limites garantidos do produto. H6: distribuidores analíticos sem IES usam cosⁿ; n=1 como difuso e n=ln(0,5)/ln(cos(facho/2)) quando há facho. Um ângulo publicado não determina toda a curva; a aproximação precisa ser substituída pela fotometria do conjunto.

## Produtos e rastreabilidade

| Grupo | Fluxo nu lm | Potência W | Cor K | IRC | Fonte / limite |
|---|---:|---:|---|---|---|
| C13 | 2300 | 30 | 3000 | >90 | S1; IES |
| L11 | 2000 | 25 | 3000 | 80 | S2; cos110 |
| B11 | 2000 | 25 | 3000 | 80 | S3; cos110 |
| S03 | 1600 | 17.6 | 3000 branco de teste; RGB fora da fotometria | 80 | S4; diffuse |
| E04 | 1600 | 17.6 | 3000 branco de teste; RGB fora da fotometria | 80 | S4; diffuse |
| Q05 | 1440 | 18 | 3000 de teste; ajustável3000–6500 | dado ausente | S5; diffuse |
| S04 | 960 | 10.5 | 3000 | >80 | S7; isotropic |
| Q01 | 270 | 3 | 3000 | dado ausente | S6; cos30 |
| Q02 | 270 | 3 | 3000 | dado ausente | S6; cos30 |
| C14 | 1320 | 13.2 | 3000 | >90 | S8/P6; strip |
| S05 | 1200 | 12 | 3000 | >90 | S8/P6; indirect |
| Q06 | 2400 | 24 | 3000 | >90 | S8/P6; indirect |
| B09 | 1320 | 13.2 | 4000 | >90 comercial | S9/P5; mirror |
| B10 | 1060 | 9.6 | 3000 | 80 comercial | S10/P5; indirect |
| E05 | 1600 | 20 | 3000 de teste; ajustável/RGB | 80 | S11; indirect |

Fluxos de fitas resultam de comprimento nominal×lm/m. C2/S3/Q06 mantêm os comprimentos já usados em P6; não são comprimentos de compra. B09=2×0,55 m e B10≤2 m em P5; E05=kit2 m. Não há dado de fluxo por branco/RGB ou intensidade regulada; os cálculos funcionais consideram branco a100%. Faltam transmissão/curva dos conjuntos; IRC das EVY e do Elgin não está comprovado nas fontes usadas. Não confundir lista comercial e SKU conciliado.

IES EVO obtido diretamente do anexo oficial S1 em29/10: teste31/08/2021,2329 lm/35,65 W; catálogo2300 lm/30 W. A curva original é cenário histórico, não fotometria certificada do lote30 W. Serão mostrados separadamente curva original e comparação normalizada2300/2329; normalizar fluxo não resolve diferença construtiva. Curva numérica pequena preservada em `Fotometria_fontes.json`, com SHA do IES original.

## Geometria e evidências do vídeo

Planta oficial P3 conferida com a skill PDF; projeções PR-FLOORS e PR-PONTO de P4 fixam o sistema global da prancha em mm. Exportação R54 e modelo são vinculados por SHA. O FreeCAD não é aberto. Os `bounds` do site incluem margens de câmera e não são áreas dos cômodos. Usar união dos retângulos PR-FLOORS sem duplicar sobreposições; excluir footprints de caixas que atravessam o plano apenas na malha útil, mantendo a área bruta separada.

Elias,29/10/2026, nesta conversa: “tem imagens de um video de um apartamento semelhante ao meu (só q espelhado)”. V1–V5 foram conferidos: quatro saídas no conjunto social/cozinha/serviço; duas teclas junto ao interfone; três junto à circulação; tomada+interruptor junto ao lavatório. A→Dormitório02/escritório e B→Dormitório01/quarto é a correspondência provável corrigida pela R02. Orientação transferida pelas paredes e vãos da planta, não por inverter coordenadas de pixels. O vídeo sustenta quantidade e região, não centímetros, retorno, neutro ou circuito.

Para o cálculo: centros nominais dos pontos existentes; altura do teto2,60 m (banho2,50) menos corpo/hipótese do emissor. Não deduzir novamente forro de uma altura já acabada. Jurerê10 cm de corpo; EVO3,8 cm; Elgin/Firefly5 cm como hipótese, sem dimensão exata comprovada. Rebaixos/vigas sem cotas ficam como perguntas, sem inventar seção. Deslocamento de±25 cm será ensaio de sensibilidade, não precisão atribuída ao vídeo.

Planos pedidos0,75/0,85/0,45 m são comparadores; bancadas atuais chegam a0,92 m na cozinha e0,765 no banho; cama atual tem0,64 m. Registrar as duas referências, sem alterar móveis. Plano vertical do rosto separado da horizontal. Portas/varal e armários serão apenas envelopes de oclusão, não simulação contínua de interferências.

## Método a executar

Fluxo zonal: Emed=ΣΦ×transmissão×FU×FM/área bruta. Direta: E=ΣI(θ,φ)×cos(incidência)/r²×FM, com visibilidade por segmento×caixa; todas as coordenadas convertidas para metros. Não multiplicar a direta por FU novamente. Emed ponderada pela área das células; Emin por amostra e U0=Emin/Emed. Refinar malha só para testar erro numérico, sem redimensionar instalação condicionada.

UGR real requer luminância direcional, área luminosa aparente, luminância de fundo e índice de posição. Curva só da lâmpada/alegaçãoUGR<19 não comprova o ambiente. Sem esses dados, registrar indeterminado e risco/reflexo geométrico, sem fabricar um UGR numérico. Luz natural, Ambilight, telas acesas e iluminação do depurador não entram como fluxo conhecido.

## Resultados por cômodo e tarefa

**Veredito apenas do cenário direto. O desempenho real permanece indeterminado.** A faixa baixo–alto varia manutenção e transmissão; não limita todas as curvas/posições possíveis. Uniformidade é amostrada, não garantia entre pontos nem resultado mantido medido. Indiretas sem coordenadas/reflexões não recebem contribuição inventada.

| Caso | Plano m | Área útil m² | Emed baixo–alto lx (central) | Emin lx | U0 | Meta lx/U0 | Veredito condicional |
|---|---|---:|---:|---:|---:|---|---|
| quarto_geral | 0.75 | 6.98 | 52–67 (59) | 0 | 0.00 | 150/0.4 | não atende no cenário |
| escritorio_geral | 0.75 | 6.79 | 34–73 (50) | 21 | 0.42 | 150/0.4 | não atende no cenário |
| sala_geral | 0.75 | 9.67 | 34–76 (51) | 15 | 0.29 | 150/0.4 | não atende no cenário |
| circulacao_geral | 0 | 0.94 | 18–38 (26) | 0 | 0.00 | 100/0.4 | não atende no cenário |
| cozinha_geral | 0.75 | 4.44 | 151–218 (183) | 0 | 0.00 | 150/0.4 | não atende no cenário |
| lavanderia_geral | 0.75 | 1.72 | 127–164 (145) | 81 | 0.56 | 150/0.4 | marginal no cenário |
| banho_geral | 0.75 | 2.66 | 122–157 (139) | 60 | 0.43 | 150/0.4 | marginal no cenário |
| cozinha_preparo | 0.85 | 0.39 | não avaliável | — | — | 500/0.7 | não avaliável: plano dentro da base |
| cozinha_pia | 0.85 | 0.40 | não avaliável | — | — | 300/0.7 | não avaliável: plano dentro da base |
| lavanderia_tanque | 0.85 | 0.37 | não avaliável | — | — | 300/0.7 | não avaliável: plano dentro da base |
| sala_mesa | 0.79 | 1.36 | 52–117 (78) | 35 | 0.45 | 500/0.7 | não atende no cenário |
| escritorio_mesa | 0.75 | 0.70 | 29–64 (44) | 30 | 0.69 | 500/0.7 | não atende no cenário |
| quarto_leitura | 0.45 | 0.24 | 437–562 (500) | 379 | 0.76 | 300/0.7 | atende no cenário |
| banho_rosto | vertical1,35–1,75 | 0.16 | 255–493 (365) | 318 | 0.87 | 300/0.7 | marginal no cenário |
| cozinha_preparo_tampo92 | 0.92 | 0.39 | 365–615 (482) | 142 | 0.29 | 500/0.7 | não atende no cenário |
| cozinha_pia_tampo92 | 0.92 | 0.40 | 373–624 (490) | 246 | 0.50 | 300/0.7 | não atende no cenário |
| cozinha_preparo_tampo92_pessoa | 0.92 | 0.39 | 249–466 (349) | 142 | 0.41 | 500/0.7 | não atende no cenário |
| lavanderia_tanque_roupa | 0.85 | 0.37 | não avaliável | — | — | 300/0.7 | não avaliável: plano dentro da base |
| lavanderia_tanque_tampo92 | 0.92 | 0.37 | 116–149 (132) | 86 | 0.65 | 300/0.7 | não atende no cenário |
| lavanderia_tanque_roupa_tampo92 | 0.92 | 0.37 | 0–0 (0) | 0 | 0.00 | 300/0.7 | não atende no cenário |
| circulacao_geral_portas_fechadas | 0 | 0.94 | 18–38 (26) | 0 | 0.00 | 100/0.4 | não atende no cenário |

### Fluxo zonal, controle independente da direta

H4: FU0,30/0,45/0,60; E=ΣΦútil×FU×FM/área bruta, com FM e transmissões de H3/H5. Sem oclusão explícita, sem uso de FU como multiplicador da grade. A área inclui as zonas sob armários: não comparar diretamente com a média da área útil.

| Ambiente | Área bruta m² | Fluxo útil central lm | Emed zonal baixo–alto lx (central) | Fonte |
|---|---:|---:|---:|---|
| quarto | 8.383 | 1440 | 36–93 (62) | H3–H5; Q05 |
| escritorio | 6.785 | 1040 | 25–108 (55) | H3–H5; E04 |
| sala | 9.672 | 1568 | 26–116 (58) | H3–H5; S03,S04 |
| cozinha | 5.518 | 3290 | 118–341 (215) | H3–H5; C13,C14 |
| lavanderia | 1.987 | 2000 | 211–544 (362) | H3–H5; L11 |
| banho | 2.662 | 2000 | 158–406 (271) | H3–H5; B11 |

### Escuros, sombras e leitura correta

Cozinha: P09–P13 bloqueiam raios do teto; C14 está sob P10/P13 em dois trechos0,475/0,625 m, a7 mm da face inferior,30 mm da frente, hipóteses de posição. O cozinheiro e eletrodomésticos adicionais não foram representados como sólidos: sombras do uso podem reduzir mais. Pia/preparo a0,85 m atravessam as caixas inferiores de0,90 m na R54: o zero calculado representa ponto dentro do sólido, não falta de luz. Esses casos são não avaliáveis; usar os resultados físicos no tampo nominal0,92 m. Na lavanderia há a mesma incompatibilidade0,85×0,92; README local cita bancada0,75, divergência documental preservada para compatibilização.

Lavanderia: o caso roupa usa todo o envelope100×50 cm, com queda1,20 m, como opaco conservador; não é a transparência real das roupas nem a antiga chapa de ocultação removida. Geral/tanque sem roupa e tanque com roupa estão separados. A alteração observável não define posição final nem mecanismo do varal.

Banheiro: B09 foi distribuído em duas barras horizontais0,55 m, centros das propostas R54 Peca188/Peca189, orientadas para o rosto; não copiou as barras verticais do render. Plano do rosto a y=4,70 m,x=4,14–4,54,z=1,35–1,75 m é hipótese H7. P19 é caixa opaca, sem reflexão especular calculada. Pontos a0,75 m não substituem luz no rosto.

Leitura: duas áreas de40×30 cm a0,45 m, com EVY apontadas ao centro, hipótese H8; facho30° não é IES. A cama atual mede0,64 m de altura: plano0,45 é o comparador pedido, não a altura real do livro. Posição da cabeça/livro e ajuste do foco continuam pendentes; não usar pico central como prova de cobertura.

Circulação: sem luminária dedicada acrescentada. Compara luz emprestada de S03/E04/Q05 e paredes com/sem vãos de portas abertas. O fechamento é envelope conservador, não giro contínuo; indiretas ainda sem posição não cobrem o percurso por inferência. Noite com os quartos apagados exige nova conferência de trajeto, não circulação no escuro.

Sala: mesa Berlin aberta170×80 cm, tampo0,79 m, centrada nominalmente no S04. Cascata triangular compacta, bordas inferiores históricas155/170/185 cm mais7,5 cm até o centro luminoso (H9). Não foram espalhados globos ao longo da mesa. TV, quarto/cabeceira e E05 sem implantação não recebem lux de reflexão fictício. Escritório usa faixa frontal livre da mesa, excluindo a traseira ocupada pelos monitores.

O efeito do IES original EVO em comparação com sua normalização é2329/2300=1.01261 vezes a contribuição C13 (≈1,26% a mais); não35,65/30. Potência de ensaio e potência do catálogo não escalam automaticamente a iluminância. Mantida pendência de revisão do fabricante.

### Mapas e dados

[Resumo numérico](Resumo_lux.csv) e [grade resumida](Grades_lux.csv). Mapas mostram direta central a0,75 m (circulação:piso), com escala comum0–500 lx; branco = fora da malha/volume ocupado, contorno = geometria nominal. Não incluem luz natural. Dados detalhados podem ser regenerados externamente.



## Sensibilidade e reprodução

Deslocamentos±0,25 m dos plafons, um eixo por vez, em [Sensibilidade_luz.csv](Sensibilidade_luz.csv); mantidos fluxos/curvas/obstáculos. Não são incertezas estatísticas nem uma otimização da posição. Células de0,25 m em geral e0,10 m nas tarefas, divididas nas bordas; média ponderada pela área. Mínimo amostrado pode cair numa malha mais fina.

SHA R54: `4a2996ee63dd6f2f3dc302025a73fb65011b3339bae510130732859706049528`. IES original: `132f3d7fd250447ee887a9730acc88cd8ee9691c7cad17b15236b267fcd2e16c`. Regeneração não requer FreeCAD; lê a exportação com SHA e a curva numérica pequena. Dependência dos mapas: Pillow.

## Posições aproximadas pelas fotos do vídeo espelhado

| Elemento observado | Localização relativa transferível | Uso no estudo / limite |
|---|---|---|
| Quatro saídas sociais, V1 | duas na faixa da sala/jantar e duas na faixa cozinha/serviço, interpretação pela continuidade das paredes/vãos | quantidade compatível comS03/S04/C13/L11; não são quatro circuitos nem coordenadas obtidas dos pixels |
| Teto do quartoA, V6/V5 | saída na região central do quarto identificado provavelmente comoDormitório02/escritório | apoia uma geralE04; centroPR-PONTO é nominal, não medido no vídeo |
| Teto do quartoB, V7/V5 | saída na região central doDormitório01/quarto principal provável | apoia uma geralQ05; ponto nominal mantido |
| Interfone, V2 | duas teclas na parede oposta aos equipamentos, perto do interfone | funções cozinha/serviço são hipótese; retorno/neutro não identificados |
| Acesso íntimo, V3 | três teclas junto à circulação e portas | não deduzir três retornos utilizáveis ou três circuitos |
| Banheiro, V4 | placa com tomada+interruptor ao lado do lavatório/porta | posição relativa existe na outra unidade; não classificar volume/IP/circuito pela foto |
| Tomadas da cozinha, V5/K-E01–07 | parede de equipamentos: uma região de entrada, dupla junto à pia, alta e sob a pia, região de cocção | inventário prévio R02: 9 posições em 7 placas, sem duplicar reaparições; não é capacidade/circuito nem posição da unidade de Elias |
| Quadro, ENT-02 | junto à porta de entrada da outra unidade | símbolo de lâmpada visível; amperagem/curva e associação à unidade sem leitura confiável |

O espelhamento foi tratado pela relação pia/tanque/janelas/acesso íntimo da plantaP3 e pela correçãoV5, sem presumir que a própria imagem foi espelhada digitalmente. Não foi criado ponto em centímetros a partir da perspectiva. O ensaio±25 cm mostra a consequência de posições aproximadas, sem atribuir essa precisão ao vídeo. Estas evidências acrescentam informação útil de infraestrutura, mas não substituem o quadro/pontos da unidade real.

## Cenas, consumo e corrente a127 V

H11: perfil de uso ilustrativo, não informado pelo morador. Horas por cena abaixo são mutuamente exclusivas dentro do cômodo; trabalho8 h×22 dias, demais30 dias/mês. Dimerização proporcional à potência é hipótese ideal, sem curva de consumo. Fontes avulsas usam eficiência suposta80–90%, não fichaOpus; incluiu provisão1,2 W de cada Shelly permanentemente alimentado. Standby das WiZ/Elgin/kit/fonte/D1, perdas de cabos e tolerâncias desconhecidos **não estão fechados**. O total é subtotal modelado, não previsão de fatura. Não atribuir standby zero ao produto.

| Ambiente | Cena | h/dia ×dias | Grupos e fração de teste | W entrada cenário |
|---|---|---|---|---:|
| sala | geral | 0.5×30 | S03=1 | 18.9–19.1 |
| sala | leitura/jogos | 1×30 | S03=1;S04=1 | 29.4–29.6 |
| sala | relaxar/TV | 2.5×30 | S05=0.15 | 3.3–3.8 |
| sala | noite | 0.25×30 | S05=0.05 | 2.0–2.2 |
| sala | limpeza | 0.1×30 | S03=1;S04=1;S05=1 | 42.8–44.6 |
| cozinha | geral | 0.25×30 | C13=1 | 31.3–31.5 |
| cozinha | tarefa | 1.5×30 | C13=1;C14=1 | 46.0–48.0 |
| cozinha | relaxar/apoio | 0.25×30 | C14=0.25 | 5.0–5.6 |
| cozinha | noite | 0.25×30 | C14=0.1 | 2.8–3.1 |
| cozinha | limpeza | 0.1×30 | C13=1;C14=1 | 46.0–48.0 |
| lavanderia | geral | 0.1×30 | L11=1 | 25.0–25.0 |
| lavanderia | tarefa | 0.25×30 | L11=1 | 25.0–25.0 |
| lavanderia | relaxar | 0×30 | todos apagados | 0.0–0.0 |
| lavanderia | noite | 0.05×30 | L11=1 | 25.0–25.0 |
| lavanderia | limpeza | 0.1×30 | L11=1 | 25.0–25.0 |
| banho | geral | 0.15×30 | B11=1 | 25.0–25.0 |
| banho | rosto/tarefa | 0.5×30 | B11=1;B09=1 | 39.7–41.5 |
| banho | relaxar | 0.15×30 | B10=1 | 10.7–12.0 |
| banho | noite | 0.1×30 | B10=1 | 10.7–12.0 |
| banho | limpeza | 0.1×30 | B11=1;B09=1;B10=1 | 50.3–53.5 |
| quarto | geral | 0.25×30 | Q05=1 | 19.3–19.5 |
| quarto | leitura lado1 | 0.75×30 | Q01=1 | 4.3–4.5 |
| quarto | relaxar | 0.5×30 | Q06=0.25 | 8.0–9.0 |
| quarto | noite | 0.25×30 | Q06=0.05 | 2.7–3.0 |
| quarto | limpeza | 0.1×30 | Q05=1;Q01=1;Q02=1;Q06=1 | 52.0–55.5 |
| escritorio | geral | 0.5×30 | E04=1 | 17.6–17.6 |
| escritorio | trabalho | 8×22 | E04=1 | 17.6–17.6 |
| escritorio | relaxar/TV | 1.5×30 | E05=0.15 | 3.0–3.0 |
| escritorio | noite | 0.15×30 | E05=0.05 | 1.0–1.0 |
| escritorio | limpeza | 0.1×30 | E04=1;E05=1 | 37.6–37.6 |

Circulação: não cria grupo, cena ou consumo duplicado. Geral/limpeza depende de vizinhos e portas; noite não tem cobertura demonstrada. Lavanderia/banho gerais permanecem liga/desliga; não aplicar10% em interruptor comum. B09/B10 são dois comandos comuns separados, não Shelly novos. EVY independentes; Q05/WiZ devem permanecer alimentadas para smart, e o comando físico do Elgin é pendência. S04 usa D1 apenas como candidato. Percentuais0,05/0,10/0,15/0,25/1 são ensaio deste estudo, não mínimo estável nem cenas aceitas por Elias.

3000K é base funcional onde escolhida; espelho4000K. WiZ/Elgin em branco ajustável: fluxo nos extremos/RGB desconhecido, portanto não transportar o cenário branco100% para cores. IRC no inventário; IRC80/90 não substitui amostra nem temperatura. Nenhum UGR/cintilação/nível mínimo de dimmer foi deduzido do render.

| Ambiente | Subtotal mensal kWh no perfil |
|---|---:|
| banho | 0.94–0.99 |
| cozinha | 3.37–3.58 |
| escritorio | 3.61–3.61 |
| lavanderia | 0.38–0.38 |
| quarto | 1.42–1.57 |
| sala | 2.35–2.49 |
| **Total parcial** | **12.07–12.61** |

Não somar novamente kWh das cenas ao subtotal por grupo: a base de Shelly24h já está incluída uma vez no Consumo_luz.csv. Somar cenas isoladas não cobre as horas restantes de standby. Tarifa não fornecida: sem valor emR$/mês. Consumo real depende de horas, brilho, FP, perdas e standby medidos.

[Correntes por grupo](Correntes_luz.csv): Iativa=Pentrada/127. FP desconhecido: IRMS=P/(127×FP), sem limite superior demonstrado; FP0,5 no CSV é só sensibilidade, não dado de fabricante. Soma simultânea dos cenários a100%: 264.2 W, 2.08 A equivalentes ativos. Não atribuir a um circuito único. Projeto de pontos identifica funções, não disjuntor/cabo. Vídeo ENT-02 mostra símbolo de lâmpada no quadro, mas não sustenta curva/corrente ou que seja o quadro desta unidade. **Comparação com capacidade do circuito: indeterminada.**

## Ajustes mínimos condicionais e opções

O cenário falhar não prova falha do produto instalado. Não há menor alteração executiva demonstrável sem curvas/implantação do conjunto. Para quantificar o tamanho do problema sem escolher produto: acréscimo uniforme ideal ΔE=max(0,meta−Emed,(Umeta×Emed−Emin)/(1−Umeta)). É o menor ΔE espacialmente constante que resolve simultaneamente média eU0 no modelo. Não especifica fonte real; aumentar todos os lúmens preservaU0 e pode continuar falhando.

| Caso | Opção de estudo | Emed antes→depois lx | U0 antes→depois | Diferença material |
|---|---|---:|---:|---|
| sala_mesa | acréscimo espacialmente homogêneo mínimo, ideal matemático | 78→500 | 0.45→0.91 | sem produto cotado que comprove esta distribuição |
| escritorio_mesa | acréscimo espacialmente homogêneo mínimo, ideal matemático | 44→500 | 0.69→0.97 | sem produto cotado que comprove esta distribuição |
| cozinha_preparo_tampo92 | acréscimo espacialmente homogêneo mínimo, ideal matemático | 482→1135 | 0.29→0.70 | sem produto cotado que comprove esta distribuição |
| cozinha_pia_tampo92 | acréscimo espacialmente homogêneo mínimo, ideal matemático | 490→815 | 0.50→0.70 | sem produto cotado que comprove esta distribuição |
| lavanderia_tanque_tampo92 | acréscimo espacialmente homogêneo mínimo, ideal matemático | 132→300 | 0.65→0.85 | sem produto cotado que comprove esta distribuição |
| quarto_geral | acréscimo espacialmente homogêneo mínimo, ideal matemático | 59→150 | 0.00→0.61 | sem produto cotado que comprove esta distribuição |
| circulacao_geral | acréscimo espacialmente homogêneo mínimo, ideal matemático | 26→100 | 0.00→0.74 | sem produto cotado que comprove esta distribuição |
| sala_mesa | um Jurerê+2WiZ adicional, posição nominal de comparação | 78→146 | 0.45→0.59 | 258.59 |
| cozinha_preparo_tampo92 | recuar eixo do perfil para centro transversal da bancada | 482→494 | 0.29→0.37 | sem novo produto; remanejamento sem cotação |
| lavanderia_tanque_tampo92 | deslocar plafon35 cm rumo ao tanque e20 cm longitudinalmente | 132→168 | 0.65→0.75 | sem novo produto; remanejamento sem cotação |

H12: opção adicionalJurerê usa apenas preçosP1 de27/10:60,65+2×98,97=R$258,59, sem novo WiZmote se o grupo existente puder controlar o conjunto. Controle novo custaria maisR$117,73 da mesma lista, se necessário; compatibilidade térmica/SKU ainda pendente. Posição de comparação(6,17;4,75;2,50)m não coincide com a canoplaS04, mas sua instalação e abertura dos armários não foram validadas. Não é compra nem solução escolhida. Remanejamentos de perfil/plafon não têm mão de obra, cabos, gesso e acabamento cotados: diferença instalada desconhecida, nunca zero. As três opções geométricas são comparações fixas, não otimização iterativa de instalação condicionada.

## Riscos e lacunas

| ID/gravidade | Frente | Evidência | O que resolve |
|---|---|---|---|
| R01/alta | mesa escritório/jantar | malhas centrais abaixo da meta de tarefa; indireta/TV não é reforço direto quantificado | fotometria do conjunto e distribuição de tarefa; opções em Alternativas_luz.csv |
| R02/alta | UGR leitura/TV/escritório | UGR real indeterminado: luminância direcional/área aparente/Lb/índiceGuth ausentes; EVOUGR<19 de catálogo não é cálculo da sala | obter IES/LDT e tabelaUGR do conjunto; simular observadores e medir instalação; não inventar índice |
| R03/alta | compatibilidade elétrica | Opus36 W/3 A e Shelly4 A/canal não validam PWM/regulação/térmica nem contatoTramontina; G9/D1 ainda sem ensaio do trio10,5 W | respostasIL04–IL07/IL09;12VCC no controlador, nunca127V em I1; ensaio do trio antes de compra |
| R04/alta | fitas/dissipação | C14/S05/Q06 nominais13,2/12/24 W, mais<1,2 W/controlador;5m de fita=60 W excedem fonte36 W; perfilMOV4329 com fita12 W/m sem capacidade térmica confirmada | manter grupos e confirmar dissipação, área útil, terminais, proteção e temperatura; não alojar fonte no fluxo do depurador/micro |
| R05/alta | banheiro/IP | IP44 do plafon não valida todas as posições; IP65 da fita/IP67 da fonte não protegem cortes/emendas | N3§9.1:volumes pelo RT;IPX7/0,IPX4/1,IPX3/2,IPX1/3 na edição consultada;DR≤30mA§5.1.3.2.2; equipotencialização e classes; confirmar revisão aplicável |
| R06/média | sombra e giro | caixas de aéreos e roupa produzem sombras; cozinha EVO41cm em teto260cm ainda cruza altura do giro nominal; folga histórica13cm não é conferência executiva | preservar abertura integral e acesso; posições/fontes só após coordenação, sem limitar porta/varal para caber luz |
| R07/alta | luz no rosto | 300 lx verticais é meta residencial, faixa255–493 lx do cenário; barras inferior/superior e torneira exigem acesso, sem refletância especular modelada | confirmar geometriaB09, IRC do lote, conforto e incidência no rosto; não tomar render com barras verticais como detalhe executivo |
| R08/média | reflexos em telas | difusor/âmbar/linhaLED podem aparecer diretamente ou no reflexo; posição/tilt das telas/olhos e luminância ausentes; janela atrás dos monitores cria contraste | manter luz fora da reflexão especular para observadores; cortina/blackout; teste com tela apagada e acesa; não prometer ausência de reflexo |
| R09/alta | circuitos e consumo | símbolo de iluminação visível no quadro da outra unidade; amperagem/curva/condutor/retornos e correspondência à unidade sem comprovação | RT identifica circuito real e FP/inrush; correnteP/127 é equivalente ativa, não correnteRMS de LED |
| R10/média | fonte documental | EVO2329lm35,65W em2021 versus2300lm30W atual; WiZ800lm127V versus oferta806lmbivolt; Brilia cabeçalho12V versus tabela314450127V | pedir ficha/etiqueta do lote, fotometria e transmissão do conjunto; não transferir dados entre variantes |

UGR em leitura/TV/escritório fica **indeterminado**, com campos necessários listados em R02; um número assumindo área/índice de posição/fundo seria precisão fabricada. Reflexos especulares e contraste de telas são riscos separados de UGR. Não foi feito ensaio de segurança elétrica, dissipação, dimerização ou desempenho no imóvel.

## Confronto com as imagens dia/noite

Doze WebP atuais inspecionados visualmente em29/10, sem regeneração. [Tabela reproduzida](Coerencia_imagens_luz.csv). Não converter pixels em lux ou temperatura Kelvin: exposição, emissão gerada e balanço de branco são desconhecidos.

| Ambiente | Situação | Evidência observada |
|---|---|---|
| sala | coerência parcial | 1 plafon e3 globos nas duas imagens; noite quente e indireta acima do painel; sombras/reflexos ilustrativos; cápsulas aparentam filamento, não MiniG9 real; S03/S04/S05;P1 |
| cozinha | divergência de trecho | 1 plafon cozinha+1 lavanderia coerentes; render mostra linha contínua incluindo zona de cocção; C14 técnico são dois trechos sob apoios, não fita comum junto ao cooktop; C13/C14/L11;P5/P6 |
| lavanderia | coerência qualitativa | 1 plafon como única fonte, sem fita sob aéreo; corpo/posição e intensidade não medem fluxo real; varal está vazio; L11;S2;V1 |
| banho | divergência de geometria/cor | 1 plafon real+reflexo no espelho, não2 plafons; duas linhas verticais luminosas no render versus propostas R54 horizontais;4000K não verificável em imagem com balanço de branco; indireta inferior não prova B10 separado; B09/B10/B11;P5;Peca188/189 |
| quarto | coerência parcial | 1 plafon,2 arandelas e linha de cabeceira; luminária smart/modelo/3000K não verificáveis só por imagem; representa queen futura, não viúva atual; Q01/Q02/Q05/Q06;P1 |
| escritorio | divergência de escopo | noite mostra linha quente sob prateleira e halo TV; E06/prateleira adiada, só E05/TV nesta etapa; produtos são aproximações; luz da tarefa não comprovada pelo brilho do render; E04/E05;E06 adiada por D06-B27/10 |

## Perguntas objetivas

1. **Elias:** manter500 lx como meta de leitura/jogos na mesa aberta, ou comparar também uma meta residencial menos exigente de300 lx? Não alterada automaticamente. Para o escritório, a referência de500 lx na tarefa laboral permanece.
2. **Elias:** caso a confirmação fotométrica mantenha o déficit, aceita comparar reforço local de tarefa ou prefere preservar somente luminárias gerais? Não é autorização de compra/novo ponto.
3. **Elias:** para o espelho, prefere avaliar barras horizontais da proposta técnica ou a composição vertical da imagem? Ambas precisam de validação; nenhuma foi escolhida neste estudo.
4. **Fornecedores, dentro das IL existentes:** qual IES/LDT/transmissão do conjunto exato por SKU, branco e difusor? O IES2021 representa o EVO30W atual? Confirmar corrente Cristallux e tensão/cabeçalho G9, PWM/curva térmica da fonte e uso WiZ em plafon fechado.
5. **RT/instalador após documentação/levantamento:** quais circuito/disjuntor/FP/inrush/condutores e retornos efetivos, coordenadas/altura do emissor, rebaixos/vigas, volumes/IP/DR e sombras de uso? Não pedir agora ao morador medidas que ele não possui.

Sem produto escolhido, envio a fornecedor, mudança de cota/preço/orçamento, modificação de item do site, publicação ou CAD salvo.

[Rastreio das entradas por SHA](Rastreio_fotometrico.json): inclui curva, código, lista comercial, geometria, coordenadas e manifesto das imagens; textos normalizados paraLF, CAD/IES originais por bytes.

## Fontes

- **N1:** [ABNT NBR ISO/CIE 8995-1:2013, §§4.2–4.4, 4.8, 4.10 e tabela 5/22; texto primário em cópia pública; edição aplicável a confirmar](https://drb-assessoria.com.br/drbr/nbrisocie8995.pdf).
- **N2:** [ABNT NBR 5413:1992, §5.3.65; referência histórica secundária, não declaração de vigência](http://ftp.demec.ufpr.br/disciplinas/TM802/NBR5413.pdf).
- **N3:** [ABNT NBR 5410:2004 corrigida 2008, §§5.1.3.2.2 e 9.1; edição aplicável pelo RT](https://universidadeniltonlins.com.br/wp-content/uploads/2019/04/NBR-5410.pdf).
- **S1:** [Stella: anexos IES /30 e fator de utilização; consulta 29/10](https://conhecimento.stella.com.br/hc/pt-br/articles/11888873996311-PLAFON-DE-SOBREPOR-EVO-30W-STH21967-XX).
- **S2:** [Galaxy, loja oficial: 9608, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10](https://galaxyshop.com.br/plafon-firefly-com-led-integrado-quadrado-ip44-25w-3000k-branco.html).
- **S3:** [Galaxy, loja oficial: 9605, 2000 lm/25 W/110°/IRC80/IP44; consulta técnica 29/10, preço não transportado](https://galaxyshop.com.br/plafon-firefly-com-led-integrado-redondo-ip44-25w-3000k-branco.html).
- **S4:** [WiZ oficial 929002424712: 800 lm/8,8 W/127 V; não identifica automaticamente a oferta 806 lm/bivolt](https://www.wizconnected.com/pt-br/p/lampada-moderna-lampada-60w-a60-e27/8718699787370).
- **S5:** [Elgin 48D18WSRWIFI: referência comercial 1440 lm/18 W; curva e fluxo por branco ausentes](https://www.avantistore.com.br/luminaria-de-sobrepor-redonda-inteligente-18w-3000-6500k-wifi-48d18wsrwifi-elgin).
- **S6:** [Nordecor EVY2054: 270 lm/3 W/30°/IP20; consulta fabricante 29/10](https://nordecor.com.br/produto/arandela-led-pix/).
- **S7:** [Brilia 314450: 320 lm/3,5 W/3000 K/127 V na tabela, IRC>80; cabeçalho 12 V/0,015 A inconsistente, não usado](https://brilia.com/produtos/residencial-e-comercial/mini-g9-35w).
- **S8:** [Cristallux 221506: 1200 lm/m,12 W/m,12 V,IRC>90; campo0,1 A/m inconsistente, cálculo usa1 A/m](https://www.cristallux.com.br/produto/fita-led-cristall-pro-dry-cob-5mt-12v-12w-m-3000k-1200lm-m-ip65-480led-m-irc-90).
- **S9:** [3R, COB4000K:1200 lm/m,12 W/m,IRC>90; dado comercial, confirmar CLX-FT331240/lote](https://www.3reletrica.com.br/fita-de-led-cob-480led/m-ip65-4000k-12v-5-metros-dimerizavel-cristallux).
- **S10:** [Brilia318939:530 lm/m,4,8 W/m,12 V,3000K,IRC80,IP65; valor comercial já registrado](https://www.belluce.com.br/bll604418-fita-de-led-4-8wm-3000k-irc-80-530lmm-12v-angulo-120-brilia-318939).
- **S11:** [WiZ Pro Kit-C929002681171:1600 lm/20 W/2 m,IRC80,IP20; E05, E06 adiada](https://assets.wizconnected.com/datasheets/WiZ_Pro_LED_Strip_RGBTW_2M_Kit-C_929002681171_DS1022.pdf).
- **S12:** [Shelly Plus RGBW PM:12/24 V CC,<1,2 W,4 A/canal,10 A total,PWM833 Hz/22 kHz; consulta29/10](https://kb.shelly.cloud/knowledge-base/shelly-plus-rgbw-pm).
- **P1:** [Seleção e preços27/10 prevalecem; sem recotação, frete ou instalação](Lista_curta_luminarias_e_madeira.md).
- **P2:** [Alturas nominais2,60/2,50 m; rebaixos e vigas sem cotas verticais confirmadas](../../01_Programa_e_decisoes/Pesquisa_pe_direito.md).
- **P3:** [Planta oficial, 1 folha, conferida visualmente29/10; não localiza luminárias](../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf).
- **P4:** [PR-PONTO e contornos nominais, não levantamento da unidade](../../07_Imovel/Medidas_e_impactos.csv).
- **P5:** [Comandos funcionais não identificam circuitos/disjuntores/condutores](../Planta_pontos/README.md).
- **P6:** [Perfis e fontes; comprimentos existentes C2=1,1 m,S3=1 m,Q06=2 m, não cortes executivos](Fechamento_custo_beneficio/Revisao_quarto_CB02.md).
- **P7:** [Berlin110/170×80 cm, tampo nominal79 cm na R54; fonte vigente29/10](../Sala_e_jantar/README.md).
- **P8:** [Cama viúva atual128×188×64 cm; queen só futura](../Quarto_e_portas/README.md).
- **P9:** [Cozinha: materiais, aéreos, passagem e bancada nominais](../Cozinha/README.md).
- **P10:** [Lavanderia: varal100×50 cm; texto de bancada75 cm diverge da caixa CAD92 cm, não corrigido neste estudo](../Lavanderia/README.md).
- **V1:** [Outra unidade espelhada: quatro saídas de teto; foto07:26 conferida29/10](../../07_Imovel/Complemento/Fotos/AD-0446.jpg).
- **V2:** [Outra unidade: duas teclas junto ao interfone; função não testada](../../07_Imovel/Complemento/Fotos/AD-0334.jpg).
- **V3:** [Outra unidade: três teclas junto à circulação, mão encobre parte](../../07_Imovel/Complemento/Fotos/AD-0430.jpg).
- **V4:** [Outra unidade: tomada e interruptor junto ao lavatório/porta](../../07_Imovel/Complemento/Fotos/AD-0486.jpg).
- **V5:** [Correspondência corrigida: quartoA→escritório; B→quarto principal; provável](../../07_Imovel/Complemento/Complemento_da_visita_R02.md).
- **V6:** [Outra unidade: saída de teto visível no quartoA,09:30; região central, sem escala](../../07_Imovel/Fotos/dormitorio_A/DRA-01_09m30s.jpg).
- **V7:** [Outra unidade: saída de teto visível no quartoB,11:30; região central, sem escala](../../07_Imovel/Fotos/dormitorio_B/DRB-02_11m30s.jpg).
