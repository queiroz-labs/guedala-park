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

Resultados espaciais, cenas/consumo e alternativas serão gerados nas próximas etapas deste mesmo arquivo.

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
- **V1:** [Outra unidade espelhada: quatro saídas de teto; foto07:26 conferida29/10](../../07_Imovel/Complemento/Fotos/AD-0446.jpg).
- **V2:** [Outra unidade: duas teclas junto ao interfone; função não testada](../../07_Imovel/Complemento/Fotos/AD-0334.jpg).
- **V3:** [Outra unidade: três teclas junto à circulação, mão encobre parte](../../07_Imovel/Complemento/Fotos/AD-0430.jpg).
- **V4:** [Outra unidade: tomada e interruptor junto ao lavatório/porta](../../07_Imovel/Complemento/Fotos/AD-0486.jpg).
- **V5:** [Correspondência corrigida: quartoA→escritório; B→quarto principal; provável](../../07_Imovel/Complemento/Complemento_da_visita_R02.md).
