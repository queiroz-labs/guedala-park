# Cesto — seleção de mecanismo e complemento de esforço

23/10/2026. Preservar frente550×521×18, saco removível400×200×400 e operação até55°. Não foi adotada frente500 nem alterado gabinete. A resposta FGVTN já excluiu fornecimento de mecanismo para esta aplicação; não manter essa consulta como se ainda aguardasse resposta positiva.

## Peso completo do gabarito

O cálculo R41 omitia a armação. `cesto_calculos_completos.py` acrescenta as13peças móveis PecaCestoR004–016 ao eixo ideal em Y6440/Z120. Volume2,769192 L; massa hipotética1,800/2,077/2,492 kg para densidades650/750/900kg/m³. Material ainda não especificado; não usar esse peso como peso real de uma estrutura metálica futura.

Aρ900, frente4,642 kg + armação2,492 kg + roupa8 kg = **15,134kg** antes de saco, pivôs, ferragens e pega. A carga de roupa de8 kg não deve ser comparada isoladamente à capacidade de uma dobradiça para porta.

| Posição | Momento com roupa central, Nm | Limites teóricos pela posição da roupa, Nm |
|---|---:|---:|
|0°|−10,00|−17,84 a−2,15|
|15°|−1,09|−12,73 a10,55|
|30°|7,89|−6,75 a22,53|
|45°|16,33|−0,31 a32,97|
|55°|21,37|4,02 a38,73|

Sinal positivo tende a abrir, negativo a fechar. O limite é sensibilidade ao centro de massa dentro do saco, não fator de segurança. A base baixa da armação contrabalança parte das outras peças: por isso o acréscimo de massa quase não aumenta o torque a55°, mas aumenta a solicitação dos pivôs. O peso estático total de referência é148,42 N, aproximadamente74,21 N por pivô somente em distribuição simétrica; esforços de retenção, mãos e impacto se somam.

Fonte reproduzível: `Cesto_com_armacao.json`. Pequenas diferenças para R41 vêm do uso de g=9,80665 em vez de9,81. Centros usados são os centros dos paralelepípedos do gabarito, não de ferragens reais.

## Triagem de produtos reais

| Ferragem/conjunto | Evidência | Compatibilidade com escopo atual |
|---|---|---|
|Sugatsune HDS-10H|[Fabricante](https://global.sugatsune.com/global/en/tech/products/21577_t), par24,5–29,4 Nm, montagem publicada90°.|Não fecha a aplicação55° carregada: torque instantâneo21,37não basta para escolher; limite38,73supera a faixa e o manual trata porta, não saco variável.|
|Häfele K12,372.05.110/111|[Produto oficial](https://www.hafele.com.br/pt/product/articulador-k12-com-abertura-para-baixo-com-movimento-de-abertura-suave/P-01539543/), abertura inferior e164/244 mm.|Ainda falta curva/faixa de carga e trajetória. Comprimento fechado sozinho não prova encaixe.|
|Marathon04-LHF450-35-W|[Catálogo oficial, p98](https://marathonhardware.com/brochures/catalogues/4.kitchen/2020/web/pdf/kitchen-accessories-catalogue-2020-final.pdf): conjunto basculante35 L, braços e amortecedor, capacidade10 kg, mínimo interno400×552×261 mm; duas dobradiças inferiores adicionais.|Mais próximo da aplicação cesto, mas sistema completo diferente. Não autoriza usar apenas seus braços com a frente550×521 e o saco existente. Catálogo não fornece peso máximo da frente, curso55°, furação ou disponibilidade Brasil.|
|Marathon04-LHF450-48-W|Mesmo catálogo:48 L, mínimo400×530×346 mm.|Profundidade346 excede a reserva anterior à hidráulica em uma implantação começandoY6388: terminaY6734,14 mm além da reserva posterior iniciandoY6720. Não aplicar.|
|Rev-A-ShelfCTOHBSL-FS-1|[Fabricante](https://rev-a-shelf.com/laundry): braço de reposição específico para cestos basculantes CTOHSL/CTOHBSL; catálogo oficial reproduzido por distribuidor dá43×43×267 mm.|SKU concreto, mas sem capacidade por momento publicada encontrada;43 mm não garantem folga nos52 mm laterais porque há pivôs/apoios/curso. Não aprovar apenas pelo nome “hamper”.|
|Hailo Laundry Carrier4503270811|[Fabricante](https://www.hailo.de/de/einbautechnik/p/hailo-laundry-carrier-450-3270811):412–418×528×545 mm, corrediças.|Excluído: extração horizontal, profundidade528, muda operação e conflita com reservas hidráulicas.|
|Sige010 L|[Fabricante](https://www.sige-spa.it/en/cataloghi/010l-3/):560×410×560, módulo600,60 L.|Excluído: largura560 supera vão554 e profundidade410 ultrapassa reserva anterior à hidráulica. Não reduzir o módulo atual para adaptar.|

Catálogo Marathon salvo como`Fontes/Marathon_catalogo.pdf`; página98 renderizada e conferida em`Fontes/Marathon_cesto.png`. Os35 L são volume do fabricante e os32 L atuais são envelope retangular do saco: não são prova de equivalência de capacidade útil ou acesso.

### Por que o35 L merece só estudo separado

Uma caixa de planejamento400×552×261 começando emY6388/Z98 terminaria emY6649/Z650; não intersectaria a reserva posteriorY6720nem o tanqueZ700 apenas nessa posição fechada. Porém a frente atual começaZ150, o pivô ideal estáZ120 e o kit pede dobradiças inferiores de porta. Logo essa colocação de caixa não define a cinemática de instalação. Começar a altura útil na frenteZ150leva o topo aZ702e invade a região do painel superior/tanque. O desenho real de montagem precisa resolver essa referência antes de chamar o produto compatível.

## Caminho técnico preservando o saco

Separar três funções no dimensionamento: pivôs suportam o conjunto; batentes/limitadores recebem o esforço no55°; amortecimento ou retenção controla a transição entre cheio e vazio. Uma mola escolhida só para8 kg pode empurrar o conjunto vazio de modo indesejado. Um limitador que apenas para em55° não controla a queda até lá. Usar catálogo de “porta até6kg” ou somar duas capacidades não resolve essas funções.

Consulta técnica preparada a partir destes dados deve exigir: mecanismo ensaiado com15,13 kg móveis de referência e momento variável até38,73 Nm; espessura18; frente550×521; curso55°; laterais52mmcom apoios existentes; saco retirável sem reduzir400×200×400; desenhos completo/aberto e carga das fixações. Nenhuma comunicação nova enviada neste estudo.
