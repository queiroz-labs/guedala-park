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

H3: fatores de manutenção0,70/0,80/0,90 (baixo/central/alto); N1§4.8 exige justificar manutenção real, não usar estes fatores como garantia. H4 substituída por radiosidade H13; não se usa FU assumido nem se multiplica a direta por um fator de utilização.

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

IES EVO obtido diretamente do anexo oficial S1 em29/10: teste31/08/2021,2329 lm/35,65 W; catálogo2300 lm/30 W. A curva original é cenário histórico, não fotometria certificada do lote30 W. UGR H16 usa a curva original; lux H13 usa comparação normalizada2300/2329; normalizar fluxo não resolve diferença construtiva. Curva numérica pequena preservada em `Fotometria_fontes.json`, com SHA do IES original.

## Geometria e evidências do vídeo

Planta oficial P3 conferida com a skill PDF; projeções PR-FLOORS e PR-PONTO de P4 fixam o sistema global da prancha em mm. Exportação R54 e modelo são vinculados por SHA. O FreeCAD não é aberto. Os `bounds` do site incluem margens de câmera e não são áreas dos cômodos. Usar união dos retângulos PR-FLOORS sem duplicar sobreposições; excluir footprints de caixas que atravessam o plano apenas na malha útil, mantendo a área bruta separada.

Elias,29/10/2026, nesta conversa: “tem imagens de um video de um apartamento semelhante ao meu (só q espelhado)”. V1–V5 foram conferidos: quatro saídas no conjunto social/cozinha/serviço; duas teclas junto ao interfone; três junto à circulação; tomada+interruptor junto ao lavatório. A→Dormitório02/escritório e B→Dormitório01/quarto é a correspondência provável corrigida pela R02. Orientação transferida pelas paredes e vãos da planta, não por inverter coordenadas de pixels. O vídeo sustenta quantidade e região, não centímetros, retorno, neutro ou circuito.

Para o cálculo: centros nominais dos pontos existentes; altura do teto2,60 m (banho2,50) menos corpo/hipótese do emissor. Não deduzir novamente forro de uma altura já acabada. Jurerê10 cm de corpo; EVO3,8 cm; Elgin/Firefly5 cm como hipótese, sem dimensão exata comprovada. Rebaixos/vigas sem cotas ficam como perguntas, sem inventar seção. Deslocamento de±25 cm é ensaio de sensibilidade, não precisão atribuída ao vídeo.

Planos pedidos0,75/0,85/0,45 m são comparadores; bancadas atuais chegam a0,92 m na cozinha e0,765 no banho; cama atual tem0,64 m. Registrar as duas referências, sem alterar móveis. Plano vertical do rosto separado da horizontal. Portas/varal e armários são envelopes de oclusão, não simulação contínua de interferências.

## Método

Interreflexão calculada por radiosidade H13 abaixo. Direta: E=ΣI(θ,φ)×cos(incidência)/r²×FM, com visibilidade por segmento×caixa; todas as coordenadas convertidas para metros. Não multiplicar a direta por FU novamente. Emed ponderada pela área das células; Emin por amostra e U0=Emin/Emed. Refinar malha só para testar erro numérico, sem redimensionar instalação condicionada.

UGR real requer luminância direcional, área luminosa aparente, luminância de fundo e índice de posição. Curva só da lâmpada/alegaçãoUGR<19 não comprova o ambiente. Sem esses dados, registrar indeterminado e risco/reflexo geométrico, sem fabricar um UGR numérico. Luz natural, Ambilight, telas acesas e iluminação do depurador não entram como fluxo conhecido.

## Método e resultados por cômodo

**H13: interreflexão difusa nominal, não medida.** FU fixo H4 foi retirado. As três faixas abaixo variam somente ρ (H2); manutenção/transmissão ficam centrais H3/H5, para isolar a contribuição refletida. Direta baixo/alto no CSV ainda varia manutenção/transmissão. Nenhuma faixa é intervalo estatístico nem cobre todas as curvas ausentes.

Radiosidade: patches retangulares ≤0,45 m; Fij estimado por 512 raios por patch, origem uniforme na área e direção cossenoidal, semente291026. Potências refletidas p=ρ(q+Fᵀp), em lm; B=p/A e L=B/π. Sensor usa1024 direções cossenoidais e Eref=π×média(L); fontes8192 raios/emissor. A direta continua analítica com visibilidade. Perdas pelas aberturas e resíduo iterativo são explícitos em [Energia_luz.csv](Energia_luz.csv). A conservação não prova precisão espacial; reciprocidade é estatística e o erro Monte Carlo depende da malha. NumPy e Pillow nas ferramentas locais.

H13/material: paredes Algodão Egípcio0,50/0,625/0,75; teto e topo branco0,70/0,775/0,85; piso Olmo/greige0,15/0,25/0,35; Arenza/Beige/Louro representados por0,35/0,475/0,60; P09–P12 azul e parede Sauge do box0,10/0,20/0,30; tecido0,20/0,35/0,50; eletros/telas0,02/0,06/0,10; pedra0,45/0,575/0,70. São as faixas H2 atribuídas aos acabamentos vigentes, não refletâncias reais medidas. P19 espelho frontal temρdifusa=0: componente especular excluída, energia não devolvida ao campo difuso. Vidro/janela e porta exterior: aberturaρ=0 e fuga integral como limite conservador; sem luz natural. Portas interiores abertas deixam luz atravessar; caso fechado usa parede clara como envelope conservador.

H13/geometria: faces expostas dos envelopes R54, paredes com vãos, pisos e tetos por união exata; recorte por sólidos e limite interior. Mesma sombra em direta/refletida. P17/E06 adiado excluído. Cama viúva128×188×64 colocada nominalmente no eixo da reserva, cabeceira x0,05 e centro y2,00 m; não é medida de instalação. Mesa Berlin aberta H9. Caixa de roupa conservadora separada. Sem vidro especular, formas curvas, pessoas móveis ou luz de grupos ainda sem implantação.

Malhas: geral0,75 m exclui projeções de móveis/equipamentos baixos e paredes; piso da circulação idem. Tarefas usam somente superfície útil, sem purificador/escorredor/PC. Planos0,85 m dentro das bases foram retirados: cozinha/tanque somente tampo0,92 m. Livro passa a0,85 m, acima da cama real0,64 m; foco das EVY permanece nominal H8 e deve ser ajustado no uso. Não comparar esse resultado com a antiga leitura0,45 m como se apenas ρ tivesse mudado. Lux zero remanescente pode ser sombra física, nunca é removido por ser baixo.

### sala

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| sala_geral (0.75 m) | 5.36 | 49.3 / 0.0 / 0.00 | 61.9 / 67.2 / 74.6 | 7.0 / 0.10 | 17.9 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| sala_mesa (0.79 m) | 1.36 | 78.3 / 35.1 / 0.45 | 96.8 / 103.8 / 113.3 | 56.6 / 0.55 | 25.6 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

### cozinha

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| cozinha_geral (0.75 m) | 3.87 | 163.7 / 0.0 / 0.00 | 176.9 / 184.9 / 196.1 | 2.6 / 0.01 | 21.2 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| cozinha_preparo_tampo92 (0.92 m) | 0.26 | 358.0 / 22.1 / 0.06 | 394.8 / 415.7 / 443.6 | 40.2 / 0.10 | 57.7 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| cozinha_pia_tampo92 (0.92 m) | 0.40 | 490.4 / 245.8 / 0.50 | 539.0 / 563.0 / 594.7 | 374.7 / 0.67 | 72.6 | direta: não atende no cenário; reflexão: marginal no cenário com interreflexão H13; três faixas rho |
| cozinha_preparo_tampo92_pessoa (0.92 m) | 0.26 | 290.4 / 15.7 / 0.05 | 332.7 / 360.2 / 397.4 | 41.1 / 0.11 | 69.7 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| cozinha_pia_tampo92_pessoa (0.92 m) | 0.40 | 423.9 / 213.1 / 0.50 | 475.3 / 505.8 / 547.0 | 265.5 / 0.52 | 81.9 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

### lavanderia

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| lavanderia_geral (0.75 m) | 1.24 | 144.3 / 0.0 / 0.00 | 173.7 / 186.6 / 203.2 | 14.8 / 0.08 | 42.3 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| lavanderia_tanque_tampo92 (0.92 m) | 0.37 | 132.1 / 86.2 / 0.65 | 162.5 / 176.4 / 195.0 | 149.8 / 0.85 | 44.3 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| lavanderia_tanque_roupa_tampo92 (0.92 m) | 0.37 | 0.0 / 0.0 / 0.00 | 7.1 / 14.6 / 26.4 | 10.4 / 0.71 | 14.6 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

### banho

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| banho_geral (0.75 m) | 2.38 | 139.0 / 62.8 / 0.45 | 181.1 / 201.8 / 231.4 | 109.0 / 0.54 | 62.7 | direta: marginal no cenário; reflexão: atende no cenário com interreflexão H13; três faixas rho |
| banho_rosto (vertical1,35–1,75 m) | 0.16 | 365.0 / 318.1 / 0.87 | 450.2 / 483.1 / 526.8 | 424.0 / 0.88 | 118.1 | direta: marginal no cenário; reflexão: atende no cenário com interreflexão H13; três faixas rho |

### quarto

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| quarto_geral (0.75 m) | 4.68 | 47.6 / 0.0 / 0.00 | 61.7 / 69.7 / 81.8 | 0.0 / 0.00 | 22.1 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| quarto_leitura (0.85 m) | 0.24 | 166.7 / 102.9 / 0.62 | 188.8 / 203.3 / 225.7 | 133.8 / 0.66 | 36.6 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

### escritorio

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| escritorio_geral (0.75 m) | 4.08 | 53.2 / 0.0 / 0.00 | 64.8 / 70.7 / 79.5 | 4.6 / 0.06 | 17.6 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| escritorio_mesa (0.75 m) | 0.51 | 44.1 / 0.0 / 0.00 | 53.7 / 58.9 / 66.5 | 10.4 / 0.18 | 14.8 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

### circulacao

| Plano/caso | Área m² | Direta Emed / Emin / U0 | Com reflexão Emed baixo / central / alto | Emin central / U0 | Ganho central lx | Veredito por cenário |
|---|---:|---|---|---|---:|---|
| circulacao_geral (0 m) | 0.92 | 26.3 / 0.0 / 0.00 | 32.2 / 36.0 / 42.1 | 2.2 / 0.06 | 9.7 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |
| circulacao_geral_portas_fechadas (0 m) | 0.92 | 26.3 / 0.0 / 0.00 | 32.2 / 36.0 / 42.1 | 2.2 / 0.06 | 9.7 | direta: não atende no cenário; reflexão: não atende no cenário com interreflexão H13; três faixas rho |

[Resumo completo](Resumo_lux.csv): mínimos/U0 nas três faixas. [Malha resumida](Grades_lux.csv), [superfícies por material](Superficies_luz.csv), [validação](Validacao_luz.json). Mapas: total direto+refletido central, mesma legenda0–500 lx para todos; branco é fora da malha. Não há luz natural.




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

H14: [fluxo necessário por padrão/posição](Fluxo_necessario_luz.csv) resolve exatamente as inequações Emed≥meta e cada Ei≥Umeta×Emed para base+a×resposta. É mínimo entre escalas de um padrão fixo, não mínimo global instalado. Se a resposta piora U0, há também limite superior; distribuição inviável não vira promessa de mais lúmens. Lúmens são adicionais nus, antes de H3/H5. Posições amostradas em −0,15/0/+0,15 m no eixo transversal; não representam intervalo contínuo validado nem tolerância de obra.

[Opções comparáveis](Alternativas_luz.csv) usa somente produtos P1/S1–S9: gerais adicionais do mesmo tipo e perfis COB locais independentes. Local não reativa E06 nem supõe prateleira. Compra de rolos/fontes/perfis inteiros, sem ratear sobra: fonte por no máximo2,7 m/32,4 W nominais; capacidade térmica ainda pendente. Não são uma solução executiva nem novos itens da lista de compra. FP/inrush desconhecidos; corrente é P/127, não RMS. W das fitas usa eficiência85% hipotética; faixa80–90% dá W×85/90 a W×85/80.

Sóρ varia nas colunas baixo/central/alto; fluxo branco/transmissão/curva ausentes permanecem limitações fora dessa faixa. Sem fotometria do conjunto, cumprir o cenário não comprova produto instalado. Os preços são materiais parciais P1, não custo entregue: instalação/comandos/frete/acessórios sem cotação. WiZ usa preço da oferta sem SKU conciliado; não atribuir preço ao SKU técnico. Troca por lâmpada de maior fluxo no mesmo soquete e refletor de parede: dado ausente no catálogo permitido, sem opção comercial fabricada.

| Cômodo/tarefa/meta | Até três menores materiais parciais que cumprem cenárioρcentral | Posições testadas que cumprem |
|---|---|---|
| banho_geral / 150 lx | vigente sem acréscimo: R$0.00, 202 lx/U0 0.54; geral 1 × B11: R$129.00, 420 lx/U0 0.68; geral 2 × B11: R$258.00, 632 lx/U0 0.67 | vigente sem acréscimo: 0 m; geral 1 × B11: -0.15,0,0.15 m; geral 2 × B11: -0.15,0,0.15 m |
| circulacao_geral / 100 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| cozinha_geral / 150 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| cozinha_pia_tampo92 / 300 lx | local 3 perfil COB 0.65m: R$297.25, 1457 lx/U0 0.76; local 2 perfil COB 0.65m: R$297.25, 1181 lx/U0 0.74; local 1 perfil COB 0.65m: R$297.25, 879 lx/U0 0.71 | local 3 perfil COB 0.65m: 0 m; local 2 perfil COB 0.65m: 0 m; local 1 perfil COB 0.65m: 0,0.15 m |
| cozinha_preparo_tampo92 / 500 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| escritorio_geral / 150 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| escritorio_mesa / 300 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| escritorio_mesa / 500 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| lavanderia_geral / 150 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| lavanderia_tanque_tampo92 / 300 lx | local 1 perfil COB 0.59m: R$297.25, 495 lx/U0 0.79; local 3 perfil COB 0.59m: R$297.25, 1081 lx/U0 0.76; local 2 perfil COB 0.59m: R$297.25, 802 lx/U0 0.76 | local 1 perfil COB 0.59m: -0.15,0 m; local 3 perfil COB 0.59m: -0.15,0 m; local 2 perfil COB 0.59m: 0 m |
| quarto_geral / 150 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| quarto_leitura / 300 lx | geral 1 × Q05: R$134.83, 351 lx/U0 0.79; geral 2 × Q05: R$269.66, 493 lx/U0 0.84; local 2 perfil COB 1.00m: R$297.25, 908 lx/U0 0.87 | geral 1 × Q05: -0.15,0,0.15 m; geral 2 × Q05: -0.15,0,0.15 m; local 2 perfil COB 1.00m: 0,0.15 m |
| sala_geral / 150 lx | nenhuma das opções testadas fecha média e U0; não há três para ranquear | nenhuma |
| sala_mesa / 300 lx | local 3 perfil COB 1.70m: R$628.04, 672 lx/U0 0.71; local 4 perfil COB 1.70m: R$760.49, 850 lx/U0 0.72; geral 4 × S03: R$1034.36, 441 lx/U0 0.76 | local 3 perfil COB 1.70m: 0 m; local 4 perfil COB 1.70m: 0 m; geral 4 × S03: -0.15,0,0.15 m |
| sala_mesa / 500 lx | local 3 perfil COB 1.70m: R$628.04, 672 lx/U0 0.71; local 4 perfil COB 1.70m: R$760.49, 850 lx/U0 0.72 | local 3 perfil COB 1.70m: 0 m; local 4 perfil COB 1.70m: 0 m |

As alternativas que falham também permanecem no CSV. Nenhuma é selecionada; limites por interferência/pontos reais ficam com RT. Metas300/500 lx para sala/escritório coexistem: escolher uma não está implícito no cálculo.

## Camada de tarefa e espelho

H15: comparação finita de reforço local e geral; [todos os valores e três faixasρ](Camadas_tarefa_luz.csv). Pessoa tem ombros até1,50 m e cabeça até1,75 m; na pia desloca-se0,65 m em X para ficar diante da pia, sem reutilizar a posição do preparo. Não representa anatomia medida. Roupa permanece envelope totalmente opaco; seu resultado não prevê o tecido real.

| Caso | Camada/opção | Emed central lx (baixo–alto) | Emin central / U0 |
|---|---|---:|---|
| cozinha_preparo_tampo92 | vigente | 416 (395–444) | 40 / 0.10 |
| cozinha_preparo_tampo92 | local 2 perfil COB 0.62m | 856 (811–915) | 134 / 0.16 |
| cozinha_preparo_tampo92 | geral 2 × C13 | 430 (404–469) | 41 / 0.10 |
| cozinha_preparo_tampo92_pessoa | vigente | 360 (333–397) | 41 / 0.11 |
| cozinha_preparo_tampo92_pessoa | local 2 perfil COB 0.62m | 817 (756–897) | 71 / 0.09 |
| cozinha_preparo_tampo92_pessoa | geral 2 × C13 | 377 (342–428) | 43 / 0.11 |
| cozinha_pia_tampo92 | vigente | 563 (539–595) | 375 / 0.67 |
| cozinha_pia_tampo92 | local 2 perfil COB 0.65m | 1181 (1132–1244) | 877 / 0.74 |
| cozinha_pia_tampo92 | geral 2 × C13 | 605 (566–664) | 381 / 0.63 |
| cozinha_pia_tampo92_pessoa | vigente | 506 (475–547) | 265 / 0.53 |
| cozinha_pia_tampo92_pessoa | local 2 perfil COB 0.65m | 1152 (1082–1245) | 749 / 0.65 |
| cozinha_pia_tampo92_pessoa | geral 2 × C13 | 546 (501–614) | 339 / 0.62 |
| lavanderia_tanque_tampo92 | vigente | 176 (162–195) | 150 / 0.85 |
| lavanderia_tanque_tampo92 | local 2 perfil COB 0.59m | 802 (760–854) | 608 / 0.76 |
| lavanderia_tanque_roupa_tampo92 | vigente | 15 (7–26) | 10 / 0.71 |
| lavanderia_tanque_roupa_tampo92 | local 2 perfil COB 0.59m | 646 (607–697) | 454 / 0.70 |
| escritorio_mesa | vigente | 59 (54–66) | 10 / 0.18 |
| escritorio_mesa | local 2 perfil COB 2.00m | 909 (884–944) | 84 / 0.09 |
| escritorio_mesa | geral 2 × E04 | 232 (216–255) | 40 / 0.17 |
| sala_mesa | vigente | 104 (97–113) | 57 / 0.55 |
| sala_mesa | local 2 perfil COB 1.70m | 487 (465–515) | 339 / 0.70 |
| sala_mesa | geral 2 × S03 | 285 (268–308) | 199 / 0.70 |
| banho_rosto | horizontal R54 | 483 (450–527) | 424 / 0.88 |
| banho_rosto | vertical imagem | 715 (676–765) | 651 / 0.91 |
| banho_rosto | horizontal + geral adicional | 520 (474–583) | 466 / 0.90 |
| quarto_leitura | EVY apontadas ao livro0,85m | 452 (437–474) | 298 / 0.66 |

Espelho: horizontais R54 e verticais H15 usam o mesmo1,10 m de COB4000K,13,2 W e1320 lm nus, com mesma hipótese de difusor. Vertical: x4,065/4,615 m,y5,139 m,z1,25–1,80 m; não é cota inferida dos pixels. Material nominal reutilizável, custo de remanejamento/terminações sem cotação (não zero). Variante com segundo plafon acrescenta25 W/2000 lm/R$129,00 parciais; composição vigente tem somente um. A escolha estética não está feita.

EVY reorientadas ao livro é outra hipótese de orientação, não troca de luminária nem promessa sobre seu curso mecânico. Reforços locais podem introduzir fonte no campo visual/reflexos; cálculos de lux não autorizam montagem sobre aquecedor, passagem, móveis, varal ou área molhada.

## UGR e reflexos geométricos

H16: UGR=8 log10[(0,25/Lb)Σ(L²ω/p²)], com índice Guth S13 e fundo Lb=Evertical_refletida/π S14. Observador em(5,215;5,000;1,600)m, olhar horizontal+Y, apenas EVO aceso. IES2021 original2329 lm, abertura luminosa0,354×0,354 m do cabeçalho LM63, manutenção0,80. L=I/Aprojetada, área uniforme em cada direção como hipótese de cálculo; ω calculado pelas duas faces triangulares do retângulo aparente. Não se copiou UGR<19 do catálogo. Não é a cena cozinha completa, pois C14 não tem IES/área luminosa conciliados.

| ρ | Lb cd/m² | L EVO cd/m² | ω sr | Guth | UGR no cenário EVO |
|---|---:|---:|---:|---:|---:|
| baixo | 5.51 | 5551 | 0.05207 | 7.690 | 24.7 |
| central | 8.63 | 5551 | 0.05207 | 7.690 | 23.2 |
| alto | 12.56 | 5551 | 0.05207 | 7.690 | 21.9 |

[Entradas e resultado UGR](UGR_luz.csv). Abertura2021 e luminância média não demonstram distribuição de luminância do difusor/lote30W atual; UGR desse lote continua pendente. Demais luminárias: **indeterminado** até IES/LDT do conjunto, dimensões luminosas/área aparente, luminância direcional por branco e condições de montagem. Fundo/observador acima são H13/H16, não medidos.

H17: para telas apagadas, reflete-se a fonte no plano da tela e intersecta-se a reta olho→fonte virtual. Incidência=reflexão; só conta se o ponto fica dentro do envelope da tela e os dois segmentos estão visíveis. [Todas as coordenadas/ângulos](Reflexos_telas_luz.csv). Olhos sentados são hipóteses explícitas; orientação sem inclinação é do envelope R54. Monitor27/24 atual pode divergir dos envelopes R54: não é medição da área ativa dos novos SKUs. Não se calculou intensidade do reflexo, porque faltam BRDF/haze/revestimento. Centro fora não exclui reflexo parcial de um difusor finito.

| Tela / olho nominal m | Centros de fontes que aparecem | Incidência=reflexão |
|---|---|---|
| TV_sala / 6.75,2.65,1.1 | nenhum dos centros testados | ver interseções fora da tela no CSV |
| TV_escritorio / 3.1,2.05,1.1 | nenhum dos centros testados | ver interseções fora da tela no CSV |
| monitor_esquerdo / 3.7,1.0,1.2 | nenhum dos centros testados | ver interseções fora da tela no CSV |
| monitor_direito / 3.7,1.0,1.2 | nenhum dos centros testados | ver interseções fora da tela no CSV |

S05/E05/Q06 e Ambilight: implantação/área luminosa ausentes, reflexo indeterminado. Janela, tela acesa e luz natural não estão nesta cena; ausência de um centro testado não promete tela sem reflexos no uso.

## Riscos e lacunas

| ID/gravidade | Frente | Evidência | O que resolve |
|---|---|---|---|
| R01/alta | mesa escritório/jantar | malhas centrais abaixo da meta de tarefa; indireta/TV não é reforço direto quantificado | fotometria do conjunto e distribuição de tarefa; opções em Alternativas_luz.csv |
| R02/alta | UGR leitura/TV/escritório | UGR dos conjuntos atuais indeterminado; EVO histórico tem cenário H16, sem comprovar o lote30W; demais produtos sem IES/área luminosa | obter IES/LDT e tabelaUGR do conjunto; simular observadores e medir instalação; não inventar índice |
| R03/alta | compatibilidade elétrica | Opus36 W/3 A e Shelly4 A/canal não validam PWM/regulação/térmica nem contatoTramontina; G9/D1 ainda sem ensaio do trio10,5 W | respostasIL04–IL07/IL09;12VCC no controlador, nunca127V em I1; ensaio do trio antes de compra |
| R04/alta | fitas/dissipação | C14/S05/Q06 nominais13,2/12/24 W, mais<1,2 W/controlador;5m de fita=60 W excedem fonte36 W; perfilMOV4329 com fita12 W/m sem capacidade térmica confirmada | manter grupos e confirmar dissipação, área útil, terminais, proteção e temperatura; não alojar fonte no fluxo do depurador/micro |
| R05/alta | banheiro/IP | IP44 do plafon não valida todas as posições; IP65 da fita/IP67 da fonte não protegem cortes/emendas | N3§9.1:volumes pelo RT;IPX7/0,IPX4/1,IPX3/2,IPX1/3 na edição consultada;DR≤30mA§5.1.3.2.2; equipotencialização e classes; confirmar revisão aplicável |
| R06/média | sombra e giro | caixas de aéreos e roupa produzem sombras; cozinha EVO41cm em teto260cm ainda cruza altura do giro nominal; folga histórica13cm não é conferência executiva | preservar abertura integral e acesso; posições/fontes só após coordenação, sem limitar porta/varal para caber luz |
| R07/alta | luz no rosto | 300 lx verticais é meta residencial; comparações H15 não comprovam luz instalada; barras inferior/superior e torneira exigem acesso, sem refletância especular modelada | confirmar geometriaB09, IRC do lote, conforto e incidência no rosto; não tomar render com barras verticais como detalhe executivo |
| R08/média | reflexos em telas | difusor/âmbar/linhaLED podem aparecer diretamente ou no reflexo; posição/tilt das telas/olhos e luminância ausentes; janela atrás dos monitores cria contraste | manter luz fora da reflexão especular para observadores; cortina/blackout; teste com tela apagada e acesa; não prometer ausência de reflexo |
| R09/alta | circuitos e consumo | símbolo de iluminação visível no quadro da outra unidade; amperagem/curva/condutor/retornos e correspondência à unidade sem comprovação | RT identifica circuito real e FP/inrush; correnteP/127 é equivalente ativa, não correnteRMS de LED |
| R10/média | fonte documental | EVO2329lm35,65W em2021 versus2300lm30W atual; WiZ800lm127V versus oferta806lmbivolt; Brilia cabeçalho12V versus tabela314450127V | pedir ficha/etiqueta do lote, fotometria e transmissão do conjunto; não transferir dados entre variantes |

UGR em leitura/TV/escritório fica **indeterminado**, com campos necessários em R02. EVO tem cálculo do cenário histórico H16 acima, sem comprovar o lote atual. Reflexos especulares e contraste de telas são riscos separados de UGR. Não foi feito ensaio de segurança elétrica, dissipação, dimerização ou desempenho no imóvel.

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

## Perguntas objetivas e consequências numéricas



**Cenários, não escolhas.** As faixas completas estão nos CSV; números abaixo usamρcentral/H13 e preços parciais P1, sem instalação/frete/comando novo. A menor opção do catálogo testado não é o mínimo de mercado nem solução de obra.



1. **Mesa da sala:300 ou500 lx?** Para300: local 3 perfil COB 1.70m: 672 lx/U0 0.71, material parcial R$628.04. Para500: local 3 perfil COB 1.70m: 672 lx/U0 0.71, material parcial R$628.04. A exigência de U0 mantém o mesmo menor pacote testado nas duas metas; não há economia demonstrada só por baixar a média.

2. **Escritório:300 residencial ou500 lx laboral; aceita reforço local?** nenhuma opção testada cumpre média e U0 no cenário central, em nenhuma das duas metas. Confirmar área efetiva de trabalho e sombras dos equipamentos antes de compra; não descartar pontos escuros apenas para subir U0.

3. **Sala:reforço local ou somente geral?** Local500: local 3 perfil COB 1.70m: 672 lx/U0 0.71, material parcial R$628.04. Somente geral300: geral 4 × S03: 433 lx/U0 0.75, material parcial R$1034.36. Somente geral500: nenhuma opção testada cumpre média e U0 no cenário central.

4. **Espelho:horizontal ou vertical?** horizontal R54: 483 lx/U0 0.88; vertical imagem: 715 lx/U0 0.91; horizontal + geral adicional: 520 lx/U0 0.90. Mesmo1,10 m de fita nas duas orientações; relocalização/terminações ainda sem cotação.



**Dados faltantes e destinatários:** WiZ/Taschibra:SKU, branco e conjunto fechado/difusor; Stella:IES do lote30W/abertura; Galaxy/Elgin/Nordecor:curva, abertura e fluxo por branco; Cristallux:corrente/fluxo/curva; Brilia:tensãoG9; Opus/Shelly:PWM, perdas e corrente; fornecedores nos [rascunhos IL02–IL09](Fechamento_custo_beneficio/Revisao_quarto_CB02.md#consultas-aos-fornecedores--rascunhos-não-enviados), sem envio. RT/instalador:posição, área de tarefa, circuito, retornos, teto e interferências após levantamento. Não transformar resposta estética em autorização de compra.



[Prompts de correção por cômodo](../../09_Referencias/README.md#prompts-de-correção-da-luz--rascunhos29102026): apenas rascunhos; nenhuma imagem gerada/substituída.

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
- **S13:** [Radiance/EPFL: implementação primária get_posindex/get_ugr; equações Guth/UGR, consulta29/10](https://github.com/LBNL-ETA/Radiance/blob/master/src/util/evalglare.c).
- **S14:** [Radiance evalglare: fundo CIE Lb=(Ev−Edir)/π; documentação primária](https://www.radiance-online.org/learning/documentation/manual-pages/pdfs/evalglare.pdf).
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
