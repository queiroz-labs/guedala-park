// Textos atuais de apresentação. IDs, medidas e escolhas técnicas permanecem nos dados.
const MODULE_NAMES={P01:'Guarda-roupa',P02:'Armário de canto do quarto',P03:'Armário sobre o guarda-roupa',P04:'Armário sobre a cabeceira',P05:'Gabinete da pia',P06:'Três gavetas da cozinha',P07:'Móvel do forno e cooktop',P08:'Gaveta de limpeza',P09:'Armário superior D · depurador',P10:'Armário superior C · pia',P11:'Armário superior B · micro-ondas',P12:'Armário superior A · geladeira',P13:'Prateleira do micro-ondas',P14:'Tanque e cesto de roupas',P15:'Armário superior da lavanderia',P16:'Gavetas do escritório',P17:'Armário superior do escritório',P18:'Gabinete do banheiro',P19:'Armário com espelho',P20:'Banco com baú'};
CAD_DATA.modules.forEach(m=>{m.name=MODULE_NAMES[m.code]||m.name;});

const ITEM_COPY={
 bonnie:['Sofá com baú Bonnie','Sofá retrátil e reclinável, com baú. Confira o espaço para abrir, dormir e acessar o baú. A altura no desenho é aproximada.'],
 panel:['Painel da TV','Painel liso para a TV. Confira a parede, a passagem, a cortina e o espaço para a luz da TV antes de instalar.'],
 racks:['Prateleiras da TV','Uma prateleira acima e outra abaixo da TV. Falta definir as alturas, o peso suportado e a fixação.'],
 power:['Compartimento de tomadas e cabos','Espaço ao lado do videogame para a régua de tomadas e as fontes. Deve ter ventilação e acesso fácil.'],
 tv50:['TV Philips Ambilight de 50 polegadas','Escolhida em 29/10/2026. Aplicativos direto na TV. Logo após a compra, teste o Stremio com a sua conta dentro do prazo de troca.'],
 soundbar:['Caixa de som Philips TAB4000','Escolhida em 29/10/2026. Liga na TV por um cabo HDMI, e o controle da TV comanda o volume. Fica sob a TV, com as saídas de som livres.'],
 ps5:['PS5 da sala e do escritório','Um único PS5 para usar nos dois ambientes. Confira os apoios, os cabos e o espaço de ventilação.'],
 table:['Mesa extensível Berlin','Mesa pronta que abre de 110 para 170 cm. Confira as cadeiras e a passagem perto do sofá. A cor do desenho é aproximada.'],
 bench:['Banco com baú','Banco com duas tampas e duas almofadas removíveis em suede areia escolhido. Retire as almofadas antes de abrir. Falta testar as dobradiças, as travas e o peso suportado.'],
 diningchairs:['Três cadeiras de jantar','Na mesa fechada, duas cadeiras ficam nas pontas e uma na lateral. Confira a disposição e a passagem com a mesa aberta.'],
 bed:['Cama viúva com baú · atual','A cama que você já tem, 128 × 188 cm, vai na mudança. O baú tem 25 cm de profundidade útil: confira se a mala grande cabe deitada.'],
 queen:['Cama queen com baú · troca futura','Troca para bem depois da mudança. O desenho mostra a reserva da queen, translúcida, no mesmo eixo da cama atual.'],
 wardrobe:['Guarda-roupa','Uma metade para cada pessoa, com quatro gavetas e espaço para sapatos e roupas longas. Confira as portas, os cabideiros e as medidas antes de fabricar.'],
 headboard:['Cabeceira em suede areia','Dois painéis lisos em suede areia escolhido. No quarto, brilho em três níveis pelo interruptor comum; arandelas e indireta com comandos separados. Confira amostra, medidas e fixação.'],
 bedcabinet:['Armários sobre a cama e o guarda-roupa','Armários alinhados, com duas portas independentes no canto. Confira o teto, os materiais e a abertura de cada porta.'],
 desk:['Bancada de trabalho','Profundidade de 70 cm e altura de 75 cm escolhidas em 29/10/2026. O vão de 72 cm sob o tampo deve acomodar os braços da cadeira abaixados. Falta confirmar a largura e os apoios.'],
 drawers:['Duas gavetas no escritório','Gavetas à esquerda, com abertura total e puxador discreto. Confira se abrem com o sofá-cama em uso.'],
 setup:['Notebook, dois monitores e computador','Notebook à esquerda, monitor AOC de 24 polegadas que você já tem e monitor ASUS de 27 polegadas a comprar, computador à direita. Braços ELG F80N, um por monitor. Confira na etiqueta do AOC se o encaixe é VESA 100 × 100.'],
 daiane:['Sofá-cama Daiane','Versão suede cinza, escolhida em 29/10/2026. Abre em direção à janela. Confira o espaço para girar e abrir a cama, e o tamanho do baú.'],
 officechair:['Cadeira Ercathe A01','Escolhida em 29/10/2026, fora do orçamento. Os braços devem passar sob a bancada só na posição mais baixa, com pouca folga: confirme a altura com a loja ou meça na entrega.'],
 officecab:['Armário sobre o sofá-cama','Aéreo em marfim claro, liso e fosco escolhido para deixar o teto mais leve. Prateleiras ajustáveis para capacete, sapatilha e ferramentas. Confira amostra, alcance, peso e folga até o teto.'],
 officeshelf:['Prateleira dos videogames','Prateleira alta para os videogames. Confira o acesso, a posição e o peso suportado.'],
 tv43:['TV Samsung de 43 polegadas','TV que você já tem (modelo UN43CU7700GXZD): 96,4 × 55,9 cm e 6 cm de espessura, sem a base. Fica na parede oposta ao sofá. O suporte de parede escolhido é o ELG FIX200, que deixa a TV a 2,7 cm da parede. Use cabos com conector em L e confira a abertura da porta.'],
 kitchenbase:['Gavetas e base da cozinha','Três gavetas com abertura total e fechamento suave. Confira os apoios do forno, os recortes da bancada e a ligação com a lavanderia.'],
 sinkstorage:['Gabinete da pia','Duas portas, com espaço para panelas e utensílios. A prateleira precisa permitir acesso ao sifão. Defina os recortes após escolher a cuba e as conexões.'],
 lowdrawer:['Gaveta para vassoura e rodo','Guarde os cabos fixos separados das cabeças da vassoura e do rodo. A gaveta usa seis rodas. Confira os apoios, as guias e o peso suportado.'],
 kitchenupper:['Armários superiores da cozinha','Quatro armários em azul-petróleo, com portas de fechamento suave. Confira as divisórias, a ventilação dos aparelhos e a abertura perto da luminária.'],
 fridge:['Geladeira Electrolux IB6S','Acabamento com aparência de inox escolhido. Confira as medidas, a abertura das portas e os espaços de ventilação antes de comprar.'],
 cooktop:['Cooktop Electrolux KE4GC','Modelo escolhido para gás natural. Confira o recorte da pedra, as conexões, a ventilação e o espaço até o forno.'],
 oven:['Forno Fischer Infinity 50 litros','Forno elétrico de 127 V, com grill e sem turbo. Ainda não comprado. Confira os apoios, a ventilação, o circuito elétrico e a distância até o cooktop.'],
 microwave:['Micro-ondas Electrolux ME23P','O projeto reserva 10 cm acima do aparelho, mas o manual pede 30 cm. Resolva essa diferença antes de instalar.'],
 hood:['Depurador Suggar DE61IX','Aparelho de 127 V, usado como depurador. Confira o espaço mínimo de instalação e mantenha acesso aos filtros e à saída de ar.'],
 airfryer:['Air fryer Philips Walita','Pode ser usada na lavanderia quando o varal estiver sem roupas. Com roupas, leve para a bancada da cozinha. Confira as tomadas e as distâncias de segurança.'],
 coffeemaker:['Cafeteira Mondial · espaço a definir','Cafeteira já existente, ainda sem medidas. O desenho não reserva o aparelho nem comprova o encaixe junto à air fryer. Use sem roupas no varal; confira espaço e circuito.'],
 sink:['Cuba e torneira da cozinha','Cuba Dora, torneira preta extensível e tábua parcial. Preveja apoio para o pano e espaço para usar o escorredor junto à pia.'],
 filter:['Purificador Electrolux PE12G','Modelo escolhido, com água natural, fria e gelada. Confira a tomada, o ponto de água e o acesso para trocar o filtro.'],
 washer:['Lava e seca LG VC4','Modelo de 127 V. Confira o nivelamento, as conexões e o espaço para abrir a porta. A bancada precisa de apoios próprios.'],
 laundrybase:['Tanque integrado à bancada','Pedra contínua com a cozinha e torneira preta com ponta extraível. Falta conferir a válvula, o sifão e a mangueira reais.'],
 laundryupper:['Armários superiores da lavanderia','Acabamento amadeirado Arenza. Preserve o espaço do aquecedor e do varal. Falta detalhar a ventilação e a saída de gases.'],
 heater:['Aquecedor Rinnai E21 · opção em estudo','Modelo para gás natural, ainda não comprado. A instalação depende da ventilação, da saída de gases e das condições de água do apartamento.'],
 drying:['Varal que sobe e desce','Varal manual, acionado por manivela. Falta conferir a altura, a trava, o peso suportado e a distância da janela e do aquecedor.'],
 bathvanity:['Gabinete do banheiro','Duas portas de correr e uma frente removível para manutenção. Confira os trilhos, as fixações e o acesso à tubulação.'],
 basin:['Cuba Deca Slim branca','Cuba de apoio retangular. Confira o espaço para limpar e o encaixe com a torneira e o armário.'],
 'bath tap':['Torneira alta Addra Arion','Torneira preta, com água quente e fria, atrás da cuba. Confira o alcance da água e o espaço para abrir a alavanca.'],
 bathmirror:['Armário com espelho','Duas portas espelhadas e duas prateleiras removíveis. Falta testar a montagem e definir a fixação dos espelhos e do armário na parede.'],
 bathlight:['Luzes do banheiro','Três luzes com comandos separados: teto e luz indireta mais quentes, espelho com luz neutra. Confira os perfis, as fontes e a instalação.'],
 shower:['Box e chuveiro do banheiro','Vidro transparente, perfis pretos e ducha Addra Livo escolhidos. A parede do chuveiro será verde. Falta conferir as medidas e a abertura do box.'],
 'bath shelf':['Prateleira do box','Prateleira de pedra para shampoo e sabonete. A escolha dispensa fazer um nicho na parede.'],
 bathshaft:['Fechamento das tubulações','Fechamento existente em gesso. Confira onde passam os tubos antes de abrir ou remover qualquer parte.'],
 toilet:['Vaso sanitário Celite VIP','Modelo branco com caixa acoplada e assento de fechamento suave. Confira a saída de esgoto e as distâncias de instalação.'],
 hygiene:['Ducha higiênica quente e fria','Falta escolher o modelo e a posição. Confira a vazão necessária para acionar o aquecedor e manter a temperatura estável.'],
 hotwater:['Água quente · 13 opções em estudo','Compare soluções discretas, tubulação com acesso fácil e aquecimento local. Calha com tampa, forro e rodapé são alternativas condicionais; nenhuma foi escolhida. Vazão, passagem, elétrica e reforma dependem de avaliação técnica.'],
 bathfinish:['Cores e revestimentos do banheiro','Paredes em Algodão Egípcio e teto branco. Verde apenas na parede do chuveiro. Confira as amostras e a adequação do piso ao box.'],
 mirror:['Espelho de corpo inteiro','Espelho sem moldura, na lateral do guarda-roupa. Bordas polidas e cantos levemente arredondados. Confira o painel e a fixação.'],
 dishrack:['Escorredor Tramontina Mini Plurale','Modelo compacto para usar junto à cuba. Guarde limpo e seco no gabinete inferior.'],
 pressurecooker:['Panela de pressão Tramontina','Guarda prevista no gabinete da pia. Confira o espaço para retirar a panela. Respeite o limite de enchimento ao cozinhar.'],
 trash:['Lixeira comum Biovis de 15 litros','Lixeira com pedal e balde removível. Ficará fora do banheiro, voltada para a mesa. Confira a passagem e o espaço para abrir a tampa.'],
 recycling:['Lixeira de recicláveis de 20 litros','Modelo Tramontina com pedal e balde removível. Ficará no chão da lavanderia. Confira a passagem e o espaço para abrir a tampa.'],
 kitchenfinish:['Pedra, pintura e puxadores da cozinha','Granito Branco Itaúnas e pintura fosca resistente à limpeza. Puxadores discretos de alumínio preto. Confira as amostras, as fixações e os recortes.'],
 tower:['Torre de tomadas da cozinha','Abre ao pressionar e ficará na área seca. Confira a potência de todo o conjunto antes de usar a air fryer. Falta definir a posição e o recorte.'],
 kitchenlight:['Luz do teto da cozinha','Luminária quadrada branca, ainda a escolher. Confira se as portas dos armários abrem livremente e se a luz atende ao ambiente.'],
 counterlight:['Luz da bancada','Luz com intensidade ajustável sob os armários. Falta definir os comprimentos. Mantenha livres a ventilação dos aparelhos e a área quente do depurador.'],
 laundrybasket:['Cesto de roupas inclinável','Frente lisa, com saco removível e lavável. A estrutura também deve sair para dar acesso ao sifão. Falta testar a abertura e as conexões.'],
 laundrypower:['Tomada da lavanderia','Tomada discreta e acessível. Confira o alcance dos cabos e a distância do tanque e do varal. Use os aparelhos sem roupas no varal.'],
 laundrylight:['Luz do teto da lavanderia','Luminária branca, combinando com a cozinha. Falta escolher o modelo e a posição. Confira sombras e espaço para portas, varal e aquecedor.'],
 laundryfinish:['Materiais da lavanderia','Mesma pedra e pintura da cozinha. Armários e cesto em padrão amadeirado Arenza, com puxadores pretos foscos.']
};
for(const it of ITEMS){
 const copy=ITEM_COPY[it.id];
 if(!copy)throw Error('Texto de apresentação ausente: '+it.id);
 // O texto completo continua disponível para conferência, sem alongar o resumo.
 it.detailNotes=it.notes;
 [it.name,it.notes]=copy;
}

const MATERIAL_COPY={
 chairFabric:'Estofado claro e estrutura amadeirada. Confira o tecido e o acabamento da cadeira real.',
 whiteTX:'Branco texturizado na parte interna dos armários. Falta definir o fabricante e o código da chapa.',
 mirror:'Espelho na frente do armário do banheiro. O desenho não simula reflexos.',
 finishPending:'O cinza marca partes sem acabamento escolhido. Ele não indica uma cor de compra.',
 wood:'Padrão amadeirado Arenza. Confira nas fichas onde será aplicado e compare a amostra real.',
 petrol:'Azul-petróleo nos armários superiores da cozinha. Confira a amostra antes de comprar.',
 altblue:'Outra opção de azul, ainda não escolhida.',
 stone:'Pedra natural. A cor e o desenho variam entre as chapas.',
 paint:'Cor escolhida para as paredes. Na cozinha e lavanderia, use acabamento fosco resistente à limpeza. Confira uma amostra.',
 offwhite:'Tom claro e fosco para as frentes indicadas nas fichas. Falta definir o código da chapa.',
 inox:'Acabamento com aparência de inox na geladeira e na lava e seca. Compare os tons dos produtos reais.',
 beige:'Tecido bege-claro do sofá Bonnie. Confira a versão e o tecido com o vendedor.',
 grey:'Cinza-claro escolhido para o sofá-cama Daiane. Confira o tecido da versão à venda.',
 head:'Suede areia escolhido para a cabeceira e o banco de jantar. Compare amostra e lote; o desenho é uma aproximação de cor.',
 sage:'Revestimento verde da parede do chuveiro. Confira a amostra.',
 greige:'Piso em tom bege-acinzentado. Confira a versão indicada para cada área do banheiro.',
 ivory:'Piso marfim previsto para a reforma da lavanderia.',
 black:'Preto e grafite nos metais, equipamentos e detalhes.',
 vinyl:'Piso vinílico para a casa, exceto banheiro e lavanderia. Olmo é a opção preferida. Compare amostras e defina o sentido das réguas.',
 bathbeige:'Bege fosco nas frentes do banheiro. Confira a amostra e a combinação com o branco interno.',
 lightwood:'Padrão de madeira clara nas laterais visíveis do banheiro. Confira a amostra e o leve brilho do acabamento.'
};
for(const m of PROJECT.materials)if(MATERIAL_COPY[m.id])m.note=MATERIAL_COPY[m.id];
PROJECT.note='O desenho mostra o projeto. Confira as medidas e a montagem antes de fabricar.';
Object.assign(ROOM_NOTES,{
 all:'Escolha um ambiente para ver os móveis e as medidas.',
 sala:'Mesa extensível, três cadeiras e banco com baú. Confira as passagens e a abertura dos móveis.',
 quarto:'A cama viúva com baú, 128 × 188 × 64 cm, vai na mudança; a queen fica para bem depois. Luz geral smart Elgin escolhida em 27/10/2026; manual, comando físico e instalação a conferir.',
 escritorio:'Espaço de trabalho que também recebe hóspedes. Confira a abertura do sofá-cama e das gavetas.',
 cozinha:'Confira os recortes da bancada, a ventilação e o acesso às conexões dos aparelhos.',
 lavanderia:'Confira o varal, o aquecedor e o acesso ao sifão. Use os aparelhos de bancada sem roupas no varal.',
 banho:'Confira as medidas, as tubulações e a fixação dos armários. Compare amostras dos revestimentos.'
});
