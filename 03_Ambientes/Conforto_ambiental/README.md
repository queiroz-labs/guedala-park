# Conforto ambiental — sol, luz, umidade e temperatura anual

**30/10/2026. Estudo integrado A–D, condicional.** Controlar o sol SW e aproveitar noites frescas são as primeiras frentes. No inverno, conservar o sol da tarde e controlar frestas sem acumular vapor. Nenhuma decisão, compra, cota real, CAD, orçamento ou cronograma foi alterado. Temperaturas internas são resultados de hipóteses, ainda sem calibração no apartamento.

[Hipóteses editáveis](../../ferramentas/estudos/modelos/Conforto_hipoteses.json) · [parâmetros](Premissas.csv) · [fontes e SHA256](Fontes.csv) · [rastreio das entradas/código](Rastreio.csv) · [prioridades](Prioridades.csv).

## Orientação e geometria

A seta vetorial da [planta oficial](../../09_Referencias/Plantas_e_manuais/Planta_oficial.pdf) dá alto242,85°±2° de leitura, coerente com243° preliminares; [coordenadas exatas](Orientacao.json) e [extração/método](Metodo_e_limites.md).

Adotado245°±4°, sensibilidade240/245/250°. Diagramas06/ACESSO e situação são coerentes: quarto e escritório(dorm02)+sala SW; banho/AS SSE155°; direita335°/baixo65°; cozinha sem janela própria. Vídeo espelhado excluído; satélite é conferência de Elias30/10/2026, sem nova medição independente.

Ponto climático−23,60/−46,72; pin público do endereço−23,583937/−46,7159814 não localiza a janela. Piso23,2m(21–25), hipótese de entrepisos; pé-direito2,60m/banho2,50m. [Georreferenciamento e altura](Metodo_e_limites.md).

Vãos gráficos R54 e vidro estão nas [hipóteses](../../ferramentas/estudos/modelos/Conforto_hipoteses.json). Cotas2,45/2,30m são cômodos, não janelas. Memorial não fornece propriedades térmicas/área livre. Confirmar persiana também na sala.

## Sol e obstruções — A1–A3

NOAA, altura geométrica sem refração, UTC−3 fixo. Testes: meio-dia solar≈89,8° dezembro/43° junho/66,4° equinócios; poente≈244°/296°. [Sol mensal por janela](Sol_mensal.csv), passo6min, já recorta o vão com parede hipotética140mm. Horários abaixo: cenário livre, alguma área da janela recebe feixe; nuvens não consideradas.

| Janela |21/12|21/03|21/06|23/09|
|---|---|---|---|---|
|Quarto J-Q|12:42–18:48|13:24–18:12|14:00–17:24|13:12–18:00|
|Escritório J-E|12:42–18:48|13:24–18:12|14:00–17:24|13:12–18:00|
|Sala J-S|12:42–18:48|13:24–18:12|13:54–17:24|13:12–18:00|
|AS J-AS|05:18–11:00|06:12–08:48|sem feixe|06:00–08:30|
|Banho J-B|05:18–11:00|06:12–07:12|sem feixe|06:00–06:54|

**SSE tem sol de manhã no verão.** Oclusão do próprio vão explica diferenças banho/AS. ±5° desloca janelas de horário e ganhos, sem mudar a necessidade de proteção SW nem a escassez de sol SSE no inverno. Não atribuir minuto exato ao imóvel sem medir vãos/orientação.

[Manchas3D nas quatro datas](Manchas_referencia.csv): primeiro impacto em piso/parede/móveis. Sala21/12: profundidade recortada1,47m às15h/4,42m às17h/5,15m às18h; projeção infinita11,38m às18h não cabe no piso. Atinge sofá, painel/TV em algumas tardes e cama viúva no quarto. Ofuscamento depende do olho/BRDF, sem DGP/UGR. Tapete sem posição confirmada; UV/desbotamento e aquecimento do vinílico sem dose/temperatura calculadas. [Detalhes](Metodo_e_limites.md).

[Obstruções](Obstrucoes.csv): hospital249°±10°, alturas0/10/20° hipotéticas. Cenário20° em dezembro antecipa fim SW18:48→17:12; junho sem efeito. Altura/distância do hospital não obtidas; cobertura do tênis/casas abaixo da janela não confirmadas. Foto nivelada deve substituir o cenário. [Pesquisa e limites](Metodo_e_limites.md).

Torres: aproximação da situação SEM ESCALA, altura/escala incertas. T03 cobre direções aproximadamente120–165°, além do cenário alternativo155°; AS em dezembro cai de5,7h para1,2h no cenário geométrico. NNW335° é rasante à SW: edifício largo pode bloquear céu/feixe. [Hipóteses e limites](Metodo_e_limites.md).

[Ganhos solares](Ganhos_solares.csv): área×SHGC×irradiância vertical, recorte do vão no feixe. Céu claro Haurwitz e partição Erbs para ERA5 sem DNI/DHI; [equações e limites](Metodo_e_limites.md).

Três SW≈75% do ganho solar anual: pico simultâneo1,80kW, janeiro203/julho105/setembro158/outubro180kWh térmicos por mês médio ERA5. Fatores usuais não verificados: ripas0,45/persiana0,15/blackout claro0,45/tecido0,65/película0,55/combinações0,10–0,36. [Editáveis](../../ferramentas/estudos/modelos/Conforto_hipoteses.json); CSV solar supõe proteção contínua, RC usa horários. Não são kWh elétricos nem ensaios de produto.

## Luz natural e luminárias — A4–A5

CIE encoberto, Eext10000lux, plano0,75m: componente do céu pelos vãos/oclusores R54 + cavidade difusa aproximada. Refletâncias piso0,25/parede0,65/teto0,80 hipotéticas. Radiance indisponível, sem validação cruzada; [método](Metodo_e_limites.md).

|Ambiente|DF médio %|lux mínimo|h/dia ≥150lux em80% da grade, janeiro|
|---|---:|---:|---:|
|Sala|3,155|69,9|9,06|
|Quarto|3,515|75,7|9,39|
|Escritório/dorm02|1,122|23,1|5,26|
|Cozinha|0,688|13,5|0,00|
|AS|7,123|106,8|12,77|
|Banho|1,460|24,3|5,68|
|Circulação|0,201|2,4|0,00|

[Cenários](Luz_natural.csv)/[integração artificial](Luz_artificial_integracao.csv): metas150/300/500lux de estudo. Suficiência anual só difusaTMY; artificial reaproveitada por interpolação, sem refazer luminárias. NBR15575-1 pendente de conferir texto; horários não equivalem a economia sem ocupação/comandos.

Receptores comuns: escritório sem móveis passa deDF1,122% a1,945%; fechamento superior não mudou céu nessa grade, sem validar qualquer móvel futuro. Cortinas escurecem. [Céu claro](Luz_ceu_claro.csv), [horizontes](Luz_obstrucoes.csv), [grade](Luz_grade.csv).

## Clima, calor e frio — C–D

[Clima mensal](Clima_mensal.csv), [ciclo diário](Clima_diurno.csv), [resumo](Clima_resumo.json). ERA5 fornecido:87.672h/2015–2024, célula−23,5/−46,75,746m,≈25km; suaviza microclima/picos urbanos. TMYx Congonhas2011–2025:8.760h sintéticas,7,4–36°C; não representa os mesmos anos nem seus extremos. ERA5:2,4°C em30/07/2021 e37,1°C em02/10/2020,37–85dias/ano comTmax≥30°C;1.397h/ano<16°C,2.564<18°C,5.035entre18–26°C;75,1% das<16°C entre0–12h. São externos; outubro tem31,9h>30°C, menos que janeiro39,7h; setembro50,7h.

RC implícito de dois nós/sete zonas: ar e massa efetiva180kJ/m²K(100–300), Top≈(Tar+Tmassa)/2. Vizinhos adiabáticos, hall22°C e áreas externas parciais são hipóteses; caso alternativo vizinhos22°C. Pessoas/luz/ASUS reaproveitados; demais ganhos explicitamente hipotéticos. [Zonas](Zonas_termicas.csv), [ganhos](Ganhos_internos.csv), [parcelas](Parcelas_ERA5.csv), [método/limites](Metodo_e_limites.md). Sem dimensionar AC ou certificar ASHRAE55/ISO7730/NBR15575.

Resultados centrais ERA5, horas médias/ano, todas as horas; **não previsão calibrada**:

|Cenário|Sala>28°C|Quarto>28°C|Escritório>28°C|Quarto<18°C|
|---|---:|---:|---:|---:|
|Fechado, sem proteção|5479|2441|3615|306|
|Persiana13–18h|4747|1779|2893|374|
|+ventilação noturna|2287|1024|2034|381|
|Sazonal+vedação|4199|1382|2726|187|
|+isolamento interno|7198|3605|5751|0|

[ERA5 mensal](Conforto_ERA5.csv)/[TMY](Conforto_TMYx.csv):<18/20 e>26/28/30/32°C, quarto22–6h, proteções e sensibilidades. [Efeitos anuais](Efeito_anual.csv). Combinações de hipóteses, sem intervalo probabilístico; vizinhos22°C reduzem sala>28°C de5479 para3605h/ano.

Referência adaptativa0,31Tm7dias+17,8+3,5 conferida no código CBE, sem alegar norma/aplicabilidade ao sono/AC. Ventilador30W,0,5m/s/alívio2°C hipotéticos: não baixa Tar; CSV separa temperatura e alívio durante ocupação/Top≥25°C. [Limites](Metodo_e_limites.md).

### Ventilação e operação sazonal

[Vento por setor](Vento_setores.csv): SE≈35% anual/39% tardes de verão; NW≈17%/23%. V10p10/p50/p90=1,22/2,63/4,68m/s; interpolação10–100m dá alfa mediano0,199 eV23m≈1,48/3,18/5,41m/s. É cota de escoamento livre, atenuada por fatores urbanos0,25/0,50/1,00, sem garantia de vento na janela.

Ventilação por duas fachadas/gargalo em série; Cd0,60/Cp hipotéticos, correr50%/maxim-ar35% não confirmados; abertura100%/50% e portas/obstáculos/frestas. SE entra SSE/sai SW; NW inverte. Sem rede3D, tiragem ou pressão real. [Cenários](Ventilacao_cenarios.csv), [potencial](Ventilacao_potencial_ERA5.csv), [equações](Metodo_e_limites.md).

Janeiro/fator urbano0,5: ACHp50≈13,4 no caminho aberto, ainda sem vazão medida. Noturna remove≈213kWh térmicos/mês; massa20h/6h≈30,4/26,1°C: esfria, mas nem sempre o suficiente. [Resultados/limites](Remocao_noite_ERA5.csv).

Verão/picos set–out: sombrear13–18h, abrir à noite quandoTe<Tar−0,5K eTe>18°C, ventilador quando ocupado. Inverno: abrir proteção à tarde, fechar ao anoitecer, ventilar por eventos de vapor; infiltração0,2–1ACH é faixa não medida. Caso sem sol SW no período frio eleva quarto<18°C de187 para323h/ano na estratégia sazonal: ganho solar útil. Vedação exige preservar admissão/exaustão de aparelhos a gás.

### Aquecimento e isolamento

[Madrugadas5/10°C, alvos18/20°C](Aquecimento_madrugada.csv): UA de parede/vidro+infiltração, sem ganhos internos, sem perdas por vizinho/hall nesse ensaio. Para20°C comTe5°C: quarto≈628–716W; escritório410–480W; sala344–444W, ACH0,2–1. Não são cargas dimensionantes medidas.

[Aquecimento/custos](Aquecimento_opcoes.csv): quarto ideal20°C≈51kWh úteis/ano, resistência≈51kWh/splitCOP3≈17kWh elétricos, sem previsão de fatura. Portátil1500W no quarto/noite é caso separado;127V≈11,81A sem dimensionar circuito. EnelB1 baseR$0,78938/kWh vigente04/07/2026/consulta30/10, sem tributos/bandeiras/CIP; R$1,05 é hipótese total. Split quente/frio/capacidade/COP/tensão pendentes. [Detalhes](Metodo_e_limites.md).

[Piso radiante](Piso_radiante_hipoteses.csv):100W/m² em70% da área, não executivo; com base27°C eTi20°C, entrega hipotética≈56W/m² pode ser insuficiente. Tarkett limita base/sistema a27°C, SKUOlmo/adesivo pendentes. Manta sob vinílico colado não é automaticamente compatível; acréscimo hipotético10–30mm consome pé-direito. RT deve verificar carga/circuitos127V, sem tomar os6740W parciais existentes como capacidade. Tapete/manta pessoal: alívio de contato, não horas deTop evitadas. [Fontes e limites](Metodo_e_limites.md).

Isolamento40mm+gesso12,5mm reduz perda do quarto≈361W no ensaio5→20°C, mas piora calor no RC. Perde≈0,73m² nominais antes dos encontros. [Glaser](Isolamento_Glaser.csv) indica condensação potencial em alguns casos de lã; EPS sem garantia real. Sem chuva/sorção/pontes2D/água anual ou ganho acústico certificado. **Não priorizar antes de medir/revisar com RT.** [Método](Metodo_e_limites.md).

## Umidade, condensação e marcenaria — B

Tetens/FAO:20°C/65% dá orvalho≈13,2°C. Parede equivalente20+140+15mm; materiais/λ/graute/cor e resistências superficiais não verificados, hipóteses vinculadas ao memorial§3.1/4.14. [Composição/método](Metodo_e_limites.md).

[Superfícies](Superficies_mensais.csv): regime estacionárioTe mensalp05 e volumes finitos implícitos1D horários, `Tsa=Te+αI/he`. Ti26°C dez–mar/20°C demais, independente do RC; estudo de risco condicional, sem acoplamento térmico-hígrico completo. Julho parede média SW19,52/SSE19,38°C: diferença pequena≈0,14K, não prova de parede SSE permanentemente fria. Vidro U5,7 e perfil fRsi0,3–0,7 hipotéticos; sem ganho por absorção solar no vidro.

[UR superficial75/80/90%](Umidade_superficial.csv): URin65%, parede≥80% por4hSW/5hSSE anuais TMY; a80%,4663/4911h. Julho vidro aURin65%:254h≥80%,24h com condensação potencial. Contagem de exposição, não diagnóstico/índice biológico; material/duração/secagem importam. fRsi crítico por pressão de vapor, indefinido seTe≥Ti. [Método](Metodo_e_limites.md).

[Balanço de vapor](Balanco_umidade.csv),5min/48h, dias TMY06/jan e14/jul: fontes e renovação hipotéticas, conservação de massa com dreno ao saturar; sem sorção/secagem do condensado. Banho<70% no verão: fechado395min/janela4ACH25min/exaustores15–40L/s15–5min; no inverno235/15/10–5min. Não é tempo para secar revestimento. Roupa aberta≈28h verão/21h inverno; fechada não seca em48h. Quarto2pessoas/0,2ACH chega a100% no modelo: alerta de renovação, não previsão medida. [Fontes/condições](Metodo_e_limites.md).

[Fundos/grelhas](Fundos_armarios.csv):6/15mm, vãos0/10/20/30mm, duas grelhas0/20/50/100cm² eΔp0,05–0,5Pa. Fundo15mm/SSE/UR65%: vão0 sem fluxo327h≥80%; vão20mm parado761h; com2×100cm²/0,2Pa448h. Vão parado pode esfriar a parede; não há solução universal a65%. CSV informa UR ambiente máxima condicional; fluxo/pressão/caminho exigem medida/RT/oficina. [Modelo](Metodo_e_limites.md).

[Contatos por móvel](Moveis_contatos.csv): P04 junto à lateralSSE do quarto; P01/P02 e P14 têm contatos laterais candidatos. **Fundos de P01/P03, P15 e P18/P19 não são automaticamente SSE/SW**: banho P18/P19 estão do lado oposto à janela; P15 fundo emy7. P17 está adiado, excluído. Não criar uma nova implantação de armários pelo estudo.

[AC/orvalho externo20–22°C](AC_ponto_orvalho.csv): tubulação/ponte exposta abaixo do orvalho pode condensar; rodapé aquecido não condensa apenas por haver AC. Isolar/drenar tubulação conforme projeto. Desumidificador pode controlar vapor, mas aquece o recinto; potência/capacidade não dimensionadas. Banho: ensaiar15–40L/s com duto, admissão, retorno, ruído e instalação verificados, não escolher pelo número de catálogo.

## Medir, perguntar e reproduzir

[12 propostas AMB-01–12](Medidas_propostas.csv), **sem editar Medidas_e_impactos.csv/pipeline**: bússola245/155±5°, vidro/vãos/peitoril, persiana na sala/tipo/área livre, bloco/graute/laje/cor, duto/shaft/vazão do banho, horizonte nivelado, loggersT/UR5min por7dias no verão e inverno, fotos15h/17h, vento com fita/anemômetro e portas/roupa, IR de paredes manhã/tarde, frestas de janela/caixa com fita/teste apropriado. Não usar leitura IR de vidro refletivo como temperatura real sem corrigir emissividade/reflexão.

Nenhum novo PQ criado; vínculos existentes nas propostas. PQ-017 preserva [memorial§5.9 × convençãoart58](../../01_Programa_e_decisoes/Convencao_e_ata_impactos.md): proibição x instalação condicionada de AC, viabilidade pendente. [Prioridades/custos hipotéticos](Prioridades.csv), sem mudar decisões.

Na raiz, ativar `..\ferramentas_locais\ativar.ps1`; executar:

```powershell
python -B ferramentas/estudos/test_sol_luz_umidade.py
python -B ferramentas/estudos/sol_luz_umidade.py
python -B ferramentas/verificar_tudo.py
```

`--dados` escolhe pasta externa com os dois climas; `--hipoteses` escolhe JSON; `--somente solar|luz|umidade|termico` permite refazer parte. SHA divergente/entrada ausente interrompe. NumPy/Pillow/pdfplumber já locais; matplotlib3.11.2 acrescentado aos requisitos locais. Gráficos PNG, séries NPZ/CSV.gz e resumo de uma página em `..\outputs\Codex_sol_e_umidade\`, fora do Git. Testes físicos não exigem downloads. Arquivos gerados compactos no repo não certificam desempenho.

Fontes científicas/técnicas e hipóteses detalhadas em [Método e limites](Metodo_e_limites.md); URLs, acesso30/10/2026, SHA256 e falhas em [Fontes.csv](Fontes.csv).

SHA256 dos dados principais (demais downloads, acesso e falhas em[Fontes.csv](Fontes.csv)): ERA5 `f75cc1f245064b2e74c261e960fa2bcff94f8d9db4c3e6e8e2b2d91662d9a876`; EPW `e3fc5a807387948e1b69145df8677c2a51bbc2556b00ab98ca6da69ecb4208b5`; ZIPTMYx `78ff773c63739fa7034468c2b43dbcf60d5671110d9833b106ef168850b7fd99`. TMY baixado29/10/reutilizado e conferido30/10; ERA5 entregue por Elias30/10, requisição original não arquivada. Fontes brutas preservadas somente na pasta externa; PDF do folder/manual Tarkett indisponíveis por403, sem SHA inventado.
