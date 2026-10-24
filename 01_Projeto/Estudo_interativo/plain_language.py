"""Textos de apresentação do site. Medidas, códigos e arquivos de origem são preservados.

A revisão acontece no build, antes de gerar fichas e páginas. Não traduz chaves,
identificadores, URLs, fórmulas ou referências comerciais dos dados técnicos.
"""
from html import escape, unescape
import re


SUMMARIES = {
    'P01': 'Guarda-roupa com duas portas de correr e quatro gavetas. Confira os trilhos, os cabideiros e a montagem antes de fabricar.',
    'P02': 'Armário de canto com duas portas independentes e dobradiças da marca Blum. Falta detalhar como as peças do canto serão unidas.',
    'P03': 'Armário sobre o guarda-roupa com duas portas de correr. Confira os apoios e a união com o móvel de baixo.',
    'P04': 'Armário com quatro portas e dobradiças da marca Blum. A porta junto ao canto tem um recuo diferente. Falta definir o reforço e a fixação na parede.',
    'P05': 'Gabinete com duas portas e dobradiças da marca Blum. O recorte da prateleira depende da cuba e do sifão escolhidos.',
    'P06': 'Três gavetas com corrediças da marca FGVTN. Confira os encaixes e as posições de montagem antes de fabricar.',
    'P07': 'Grelhas removíveis para acesso ao forno. Falta detalhar as peças de fixação. Mantenha os espaços de ventilação livres.',
    'P08': 'Gaveta baixa com seis rodas. Confira os furos, o peso suportado e as peças que guiam e limitam o movimento.',
    'P09': 'Armário com duas portas e dobradiças da marca Blum. As peças de montagem devem deixar livre a passagem do duto.',
    'P10': 'Armário com três prateleiras e dobradiças da marca Blum nas portas. As prateleiras ficam presas ao armário e podem ser retiradas ao desmontá-lo. Confira os furos antes de fabricar.',
    'P11': 'Portas com dobradiças da marca Blum. O projeto indica os furos de montagem. Falta confirmar o peso suportado e a fixação na parede.',
    'P12': 'Portas com dobradiças da marca Blum. Falta detalhar a união da divisória central e a fixação na parede.',
    'P13': 'Prateleira aberta para o micro-ondas. Falta definir o suporte e conferir o espaço de ventilação exigido pelo aparelho.',
    'P14': 'Cesto que inclina para abrir. A estrutura e o cesto têm fixações próprias. Falta testar o mecanismo de abertura.',
    'P15': 'Portas com dobradiças da marca Blum. O espaço entre apoios precisa de reforço. Falta definir o peso suportado.',
    'P16': 'Duas gavetas com corrediças MOVENTO, da marca Blum. Corrija os pontos de colisão antes de fabricar.',
    'P17': 'Armário com quatro portas e dobradiças da marca Blum. Falta detalhar as uniões internas e a fixação na parede.',
    'P18': 'Gabinete com portas de correr e frente removível para manutenção. Confira os trilhos, as uniões e os parafusos de fixação.',
    'P19': 'Armário com espelho e portas com dobradiças da marca Blum. O projeto prevê apoios e conectores para unir as peças. Falta conferir a montagem, o espelho e a fixação na parede.',
    'P20': 'Banco com duas tampas. Cada tampa terá uma dobradiça contínua e suportes com trava. Teste a montagem antes de definir os furos.',
}

NAMES = {
    'Roupeiro': 'Guarda-roupa',
    'Canto L do quarto': 'Armário de canto do quarto',
    'Aéreo C': 'Armário superior C · pia',
    'Aéreo D': 'Armário superior D · depurador',
    'Aéreo A': 'Armário superior A · geladeira',
    'Aéreo B': 'Armário superior B · micro-ondas',
}
NAMES.update(dict(zip(SUMMARIES, [
    'Guarda-roupa', 'Armário de canto do quarto', 'Armário sobre o guarda-roupa',
    'Armário sobre a cabeceira', 'Gabinete da pia', 'Três gavetas da cozinha',
    'Móvel do forno e cooktop', 'Gaveta de limpeza', 'Armário superior D · depurador',
    'Armário superior C · pia', 'Armário superior B · micro-ondas',
    'Armário superior A · geladeira', 'Prateleira do micro-ondas', 'Tanque e cesto de roupas',
    'Armário superior da lavanderia', 'Gavetas do escritório',
    'Armário superior do escritório', 'Gabinete do banheiro', 'Armário com espelho', 'Banco com baú'
])))

DOCUMENT_COPY = {
    'dossie': ('Guia de montagem', 'Consulte as medidas, os materiais e o que falta conferir em cada móvel.'),
    'pacote-compartilhar': ('Baixar arquivos do projeto', 'Modelo 3D editável, fichas dos móveis, planta com medidas e instruções em um arquivo ZIP.'),
    'matriz': ('Medidas dos 20 móveis', 'Veja os espaços internos e as medidas que ainda precisam de confirmação.'),
    'interfaces': ('Como unir as peças', 'Encontros entre chapas. Falta definir as peças de união e o peso suportado.'),
    'fixas': ('Conectores e suportes dos armários', 'Opções para unir as peças e prender os móveis na parede. Confira a aplicação antes de comprar.'),
    'varoes': ('Cabideiros do guarda-roupa', 'Quatro cabideiros previstos. Confira os suportes antes de cortar os tubos.'),
    'bancada': ('Apoios da bancada do escritório', 'Veja as medidas da bancada e o reforço que ainda está em estudo.'),
    'minifix': ('Conectores do armário sobre a pia', 'Proposta de 20 conjuntos Minifix, que unem as peças e permitem desmontar o armário.'),
    'espelheiro': ('Prateleiras do armário com espelho', 'Opções de apoios. Falta confirmar o peso suportado e a fixação na parede.'),
    'gavetas': ('Montagem das gavetas', 'Confira as corrediças, as rodas e o peso suportado. Veja também como retirar cada gaveta.'),
    'rodizios-p08': ('Rodas da gaveta de limpeza', 'Seis rodas de 38 mm e espaçadores de 1 mm. Veja a escolha e o link de compra.'),
    'banheiro-fechamento': ('Escolhas do banheiro', 'Materiais e luzes escolhidos. Veja o que falta conferir na montagem e nas tubulações.'),
    'cad-p19': ('Modelo de estudo do armário com espelho', 'Proposta de união entre as peças. A montagem ainda precisa de teste.'),
    'luz-banho': ('Luzes do banheiro e preços', 'Veja os componentes escolhidos e os links de compra. O valor não inclui frete nem instalação.'),
    'movento': ('Corrediças MOVENTO para as gavetas', 'Peças que guiam as gavetas do escritório. Confira os encaixes e os pontos de colisão.'),
    'portas': ('Abertura de portas e tampas', 'Estudos dos mecanismos. Teste a montagem antes de fabricar.'),
    'cesto': ('Abertura do cesto de roupas', 'Frente que inclina para abrir, com saco removível. Falta testar o mecanismo.'),
    'mesa-varal': ('Mesa extensível e varal', 'Mesa pronta e varal que sobe e desce. Veja as medidas e o que falta conferir.'),
    'banco': ('Estrutura do banco com baú', 'Duas tampas e espaço para guardar objetos. Falta detalhar os apoios e as uniões.'),
    'southco': ('Alternativa de dobradiça para o banco', 'Estudo anterior com dobradiças Southco. Consulte a ficha do banco para ver a solução atual.'),
    'batente': ('Limite de abertura do banco', 'Estudo de uma peça para limitar a abertura. A posição depende da dobradiça real.'),
    'torneiras': ('Encaixe das cubas e torneiras', 'Confira as medidas dos produtos e o espaço para abrir as torneiras.'),
    'purangi': ('Torneira Purangi · opção em estudo', 'A vedação e a abertura ainda precisam de confirmação. A troca não foi aprovada.'),
    'forno': ('Apoios e ventilação do forno', 'Grelhas removíveis para manutenção. Confira os apoios e a passagem de ar antes de montar.'),
    'cad': ('Baixar modelo 3D editável', 'Arquivo para abrir no FreeCAD. Confira as fichas antes de fabricar.'),
    'cad-cores': ('Cores do modelo 3D', 'Veja os acabamentos representados. Compare as cores com amostras reais.'),
    'cad-southco': ('Modelo da alternativa Southco', 'Estudo anterior da fixação do banco. Veja a solução atual na ficha do móvel.'),
    'cad-purangi': ('Modelo de estudo da torneira Purangi', 'Desenho aproximado para conferir a abertura. Confirme as medidas no produto real.'),
    'executivo': ('Desenhos e medidas antes de fabricar', 'Falta concluir os detalhes de corte, furos, bordas, folgas e montagem.'),
    'planta': ('Planta oficial do apartamento', 'Documento de origem. Confira as medidas reais depois dos acabamentos.'),
    'pisos': ('Pisos e rodapés', 'Veja as escolhas de acabamento e o que falta conferir na instalação.'),
    'luz-quarto': ('Luzes do quarto', 'Posições e comandos em estudo. Confira o espaço junto à cabeceira e aos armários.'),
    'instalacoes': ('Água, gás, tomadas e ventilação', 'Confira os pontos reais no apartamento antes de finalizar os desenhos de instalação.'),
    'levantamento': ('O que medir antes de fabricar', 'Confira as paredes, o piso pronto, os revestimentos e os pontos de fixação.'),
    'acabamentos-r13': ('Acabamento interno dos armários', 'Branco texturizado por dentro e os padrões escolhidos nas partes visíveis.'),
    'planta-cotada': ('Planta com medidas', 'Veja as distâncias entre paredes e as diferenças entre a planta e o desenho do site.'),
    'fichas': ('Fichas dos 20 móveis', 'Medidas, materiais, peças de montagem e furos de cada móvel.'),
    'pendencias-r14': ('O que falta conferir', 'Veja o que falta definir, testar na oficina e medir no apartamento.'),
    'campo': ('Folha para medir o apartamento', 'Anote as medidas reais de cada móvel. Imprima ou salve em PDF para guardar.'),
}

# Frases recorrentes, reescritas por inteiro para manter o sentido.
EXACT = {
    'Kits de correr RO62 para uma folha': 'Kit de trilhos e guias para uma porta de correr',
    'Calços das dobradiças': 'Bases de fixação das dobradiças',
    'Horizontais fixos desmontáveis e fundo permanente': 'Base, tampo e prateleiras presos ao armário',
    'Uniões dos horizontais às laterais externas': 'Uniões da base, do tampo e das prateleiras com as laterais',
    'Ligações dos painéis da carcaça': 'Uniões das chapas do armário',
    'Caixas Minifix': 'Conectores Minifix · peças de encaixe',
    'Pinos Minifix': 'Pinos dos conectores Minifix',
    'Selecionado como ligação fixa desmontável nas peças abaixo, mantendo geometria nominal. Não é prateleira regulável nem aprovação de carga.': 'Os conectores prendem as peças e permitem desmontar o armário. A altura das prateleiras é fixa. Falta confirmar o peso suportado.',
    'Selecionado no projeto; validar em oficina': 'Escolhido no projeto. Testar na oficina.',
    'Selecionado no projeto. Validar em oficina': 'Escolhido no projeto. Testar na oficina.',
    'Estratégia selecionada; componente e seção pendentes de projeto': 'Solução escolhida. Falta definir a peça e suas medidas.',
    'Estratégia selecionada. Componente e seção pendentes de projeto': 'Solução escolhida. Falta definir a peça e suas medidas.',
    'Estudo proporcional. Escolha aprovada não significa medida acabada ou fabricação liberada.': 'O desenho mostra o projeto. Confira as medidas e a montagem antes de fabricar.',
    'Interiores identificados': 'Parte interna',
    'Faces aparentes': 'Partes visíveis',
    'Escolhido pelo usuário em 23/10/2026; fabricante/código e substrato ainda técnicos': 'Escolhido em 23/10/2026. Falta definir o fabricante, o código e o material da chapa.',
    'Escolha documental preservada; distinguir cada face da mesma peça': 'Acabamento escolhido. Confira o lado de aplicação em cada peça.',
    'Aplicação por face ainda não individualizada': 'Falta indicar o acabamento de cada lado da peça.',
    'A decisão documental vigente prevalece sobre cores antigas do CAD. A lista de peças distingue as duas referências.': 'Siga o acabamento indicado na ficha. As cores do desenho são aproximadas.',
    'A especificação documental vigente prevalece sobre cores antigas do modelo. Código comercial não informado permanece a definir.': 'Siga o acabamento da ficha. Falta definir os códigos comerciais que não aparecem na lista.',
    'Itens candidatos ainda exigem compatibilização. Quantidade nominal não é ordem de compra.': 'Confira se as peças servem neste móvel antes de comprar. As quantidades ainda precisam de confirmação.',
    'Quantidade de referência não equivale a compra liberada. Itens candidatos conservam seu status até fechar compatibilidade.': 'Confirme as quantidades e a compatibilidade antes de comprar.',
    'Cotas em mm. A situação de cada operação distingue catálogo, mapa nominal e detalhe bloqueado. Conferir a ferragem e provar em retalho antes de usinar.': 'Medidas em milímetros. Veja o que já está definido e o que falta conferir. Teste os furos em uma sobra da chapa antes de furar a peça.',
    'Valores em milímetros. Cada operação informa sua situação: parâmetro de catálogo, mapa nominal ou detalhe ainda bloqueado. Coordenadas nominais exigem conferência da ferragem e prova em retalho antes de usinar a peça.': 'Medidas em milímetros. Cada item mostra o que já está definido e o que falta conferir. Confira a peça de montagem e teste os furos em uma sobra da chapa.',
    'Peças equivalentes na mesma linha, com quantidade total. Toque no grupo para destacá-lo no 3D; abra os IDs para selecionar uma peça.': 'Peças iguais aparecem juntas. Toque no grupo para vê-lo no 3D. Abra a lista de códigos para escolher uma peça.',
    'As fichas usam milímetros. A caixa envolvente mostra o espaço ocupado no modelo; as peças mostram dimensões locais. Recortes, veios, bordas e tolerâncias precisam de detalhamento antes do corte.': 'As fichas usam milímetros. As medidas gerais mostram o espaço ocupado pelo móvel. Antes de cortar, confira os recortes, o sentido da madeira, as bordas e as folgas.',
    'Envelope nominal do conjunto no eixo do móvel. Peças, vãos úteis e reservas são discriminados nos documentos.': 'Medidas gerais do móvel no desenho. Consulte abaixo as medidas das peças e dos espaços internos.',
    'Envelope nominal do conjunto, incluindo componentes e reservas. Peças abaixo têm medidas próprias.': 'Medidas gerais do móvel no desenho. Cada peça tem suas medidas na lista abaixo.',
    'Dimensões do modelo, sujeitas à conferência de campo. Vãos internos e ligações estão nos documentos da ficha.': 'Confira estas medidas no apartamento. Os espaços internos e as uniões estão na ficha.',
    '¹ Menor dimensão do envelope local. Para recortes, uniões e formas especiais, é uma referência geométrica; confirmar espessura e orientação na peça. Não inclui fita de borda, sobremetal ou folga de corte.': '¹ A espessura vem do desenho. Confira a chapa real antes de cortar. As medidas ainda não descontam bordas, recortes ou folgas.',
    'Referências e candidatas: quantidades de compra e usinagens dependem da compatibilização.': 'Confirme as peças, as quantidades e os furos antes de comprar ou fabricar.',
    'C e L são as duas maiores dimensões do envelope local, sem indicar sentido do veio. Espessura é a menor dimensão geométrica. Recortes e furação não podem ser recuperados destas três medidas. Fita de borda e folgas não foram descontadas; lista nominal, não plano de corte.': 'C = comprimento. L = largura. Confira a espessura e o sentido da madeira na peça real. A lista não mostra todos os recortes e furos. Bordas e folgas ainda precisam de ajuste antes do corte.',
    'Dimensões do envelope local; C e L não indicam veio. Bordas, recortes, furos e folgas não descontados. Não é plano de corte.': 'C = comprimento. L = largura. Confira o sentido da madeira. Ajuste bordas, recortes, furos e folgas antes de cortar.',
    'Pronta para consulta e compatibilização. Liberação de fabricação exige resolver os fechamentos técnicos e as cotas de campo aplicáveis.': 'Use esta ficha para consultar o projeto. Resolva as pendências e confira as medidas no apartamento antes de fabricar.',
    'As escolhas de ferragens e os parâmetros disponíveis estão nas fichas. Aqui, cada móvel distingue compatibilização de projeto, conferência em oficina e levantamento físico no apartamento.': 'Veja o que falta definir no projeto, testar na oficina e medir no apartamento. Os detalhes de cada móvel estão na ficha.',
    'Preencher em milímetros, com data, responsável e referência de piso acabado. Anexar fotos com régua e marcar cada ponto na planta. Estes campos são uma folha de coleta: preencher no navegador não salva os valores; imprima ou salve em PDF.': 'Anote as medidas em milímetros, a data e o responsável. Meça a partir do piso acabado. Tire fotos com uma régua e marque os pontos na planta. O navegador não salva suas anotações. Imprima ou salve em PDF.',
    'Material, ferragens, cargas, folgas de mecanismos e usinagem são decisões técnicas das fichas. Aqui entram apenas condições físicas existentes no apartamento.': 'Use esta folha para registrar as medidas e as condições do apartamento. Consulte os materiais e a montagem nas fichas dos móveis.',
    'Encontros identificados na amostra de painéis retangulares. Cada par ainda exige distribuição de conectores; o número de contatos não é quantidade de parafusos. Ausência na amostra não elimina uma ligação necessária.': 'Estas uniões ainda precisam de um desenho de montagem. A quantidade de encontros não indica quantos parafusos comprar. Outras uniões também podem ser necessárias.',
    'Contatos da amostra retangular; não são quantidades de parafusos.': 'A lista mostra encontros entre peças. Ela não indica a quantidade de parafusos.',
    'Fechar substrato e códigos de chapa, composição Branco TX/padrão aparente, bordas e veios por peça. As faces ainda parciais estão marcadas na lista de peças.': 'Defina o material e o código de cada chapa. Indique onde aplicar o branco interno e o acabamento externo. Confira as bordas e o sentido da madeira. A lista marca o que falta definir.',
    'Distribuição/quantidade final de conectores ainda deve ser desenhada nas interfaces listadas em “Ligações ainda sem mapa”; seleção da família não é programa de furação. Contagem de contato não é quantidade de parafuso.': 'Desenhe a posição e a quantidade dos conectores nas uniões ainda sem detalhe. Escolher o conector não define os furos. O número de encontros não indica quantos parafusos comprar.',
    'Em chapa real: conferir espessura, prova de pré-furo/torque e fita de borda; travar origem/face e sentido de montagem antes de gerar programa de usinagem.': 'Confira a espessura e a fita de borda na chapa real. Teste o pré-furo e o aperto do parafuso. Marque o lado e o ponto de referência antes de preparar os cortes e furos.',
    'Oficina: pesar uma folha acabada de cada família (incluindo pegas/espelho) e confrontar a quantidade nominal com a orientação Blum; a contagem não é uma carga admitida.': 'Pese uma porta pronta de cada tipo, incluindo puxador e espelho. Confira a quantidade de dobradiças no manual da marca Blum. A quantidade prevista não confirma o peso suportado.',
    'Família selecionada para conservar a cinemática estudada e usar limitador comercial compatível. Quantidade nominal mantida; peso acabado e retenção da chapa são conferências da oficina.': 'Dobradiça escolhida para manter a abertura prevista e usar um limitador compatível. Confira o peso da porta pronta e a firmeza dos parafusos na chapa.',
    'Diretriz R14: limitar todas as 24 folhas de abrir a 86°, preservando o curso verificado no projeto. Por esta decisão explícita, equipar todas as dobradiças de cada folha; não é multiplicação automática de uma opção indefinida.': 'As 24 portas de abrir terão abertura limitada a 86°. Instale o limitador em todas as dobradiças de cada porta.',
    'As três prateleiras ficam fixas desmontáveis. Não comprar quatro apoios soltos para a mesma união. Fundo e suspensão são interfaces adicionais.': 'As três prateleiras ficam presas e saem ao desmontar o armário. Não compre apoios soltos para essas uniões. Defina também a montagem do fundo e a fixação na parede.',
    'Montar as três prateleiras fixas desmontáveis com os 20 conjuntos Minifix do módulo; não usar pinos soltos para as mesmas ligações.': 'Prenda as três prateleiras com os 20 conjuntos de conectores Minifix previstos. Eles unem as peças e permitem desmontar o armário. Não substitua essas uniões por pinos soltos.',
    'Suspensão: dimensionar ferragem/placa interna, distribuição de carga, parafusos no móvel e acesso; isto é projeto/oficina. Tipo e resistência real da parede e pontos ocultos são levantamento do apartamento.': 'Defina os suportes, a placa interna, os parafusos e o peso suportado na fixação à parede. Preveja acesso para montar. No apartamento, confira a resistência da parede e a passagem de tubos e fios.',
    'Abertura das portas, ferramenta de aperto, montagem e carga não foram ensaiadas pelo teste dos cilindros.': 'O teste do desenho dos furos não confirma a abertura das portas, o acesso da ferramenta, a montagem ou o peso suportado. Confira esses pontos separadamente.',
    'O projeto, peça por peça.': 'Conheça o projeto do apartamento.',
    'Da visão geral': 'Escolha um móvel',
    'ao detalhe.': 'para ver os detalhes.',
    'Marcenaria': 'Móveis',
    'deste ambiente.': 'deste ambiente.',
    'Cada informação,': 'Documentos',
    'no seu lugar.': 'do projeto.',
    'A casa que estamos escolhendo.': 'Cores e materiais.',
    'Madeira, luz': 'Materiais',
    'e espaço para viver.': 'do apartamento.',
    'Uma medida por vez.': 'Medidas por ambiente.',
    'O que falta, no lugar certo.': 'O que falta conferir.',
    'Uma ficha para cada móvel.': 'Fichas dos móveis.',
    'Escolhas de materiais e soluções. As fichas distinguem direção escolhida de conferência técnica; a documentação R45 reúne os detalhes mais recentes.': 'Veja as escolhas e o que falta conferir. Abra a ficha do móvel para ver os detalhes.',
    'Explore cada ambiente em 3D. Abra uma ficha para consultar medidas, madeira e ferragens.': 'Escolha um ambiente. Toque em um móvel para ver medidas, materiais e montagem.',
    'Explore os ambientes em 3D. Cada móvel tem sua ficha; as medições do apartamento ficam em uma folha separada.': 'Escolha um ambiente e toque em um móvel. A ficha mostra medidas, materiais e o que falta conferir.',
    'Desenhos, ferragens e decisões organizados para consulta. Abra apenas a disciplina ou o ambiente que precisa.': 'Encontre desenhos, materiais e orientações de montagem. Busque pelo assunto ou pelo ambiente.',
    'As fichas completas reúnem medidas, esquemas dimensionais, peças, acabamentos, ferragens e orientações de montagem.': 'Consulte as medidas, os materiais e a montagem de cada móvel.',
    'Movimentos ilustrativos entre estados de uso; mecanismos e trajetórias reais ainda precisam de conferência.': 'Os movimentos são uma simulação. Confira a abertura e o funcionamento dos móveis reais.',
    'Este ambiente tem um layout fixo no estudo. Toque nos móveis para conhecer as escolhas.': 'Toque nos móveis para ver os detalhes deste ambiente.',
    'Paletas por ambiente, móveis e proporções atuais. Cores digitais aproximadas; as amostras físicas continuam necessárias. Medidas de móveis em largura × profundidade × altura, salvo indicação diferente.': 'Veja as cores e os materiais de cada ambiente. Confira amostras reais antes de escolher. As medidas seguem largura × profundidade × altura, salvo indicação.',
    'Os desenhos são volumes proporcionais, não fotografias dos produtos. O painel de materiais anterior fica como histórico: sofá, rack, cabeceira e armários foram atualizados; ar-condicionado e módulo da caixa foram retirados.': 'Os desenhos e as cores são aproximados. Consulte as fichas para ver as escolhas atuais.',
    'Estes controles simulam alternativas; não alteram as decisões salvas. Profundidade menor pode deixar de atender ao console. Recarregar restaura o projeto.': 'Teste outras medidas no desenho. Confira se o videogame cabe. Recarregue a página para voltar ao projeto salvo.',
    '3D · 2,5D': '3D',
    'Geometria R45 · cores aproximadas': 'Desenho do projeto · cores aproximadas',
    'Medida geométrica R45': 'Medida do desenho',
    'Ficha R14 · definições técnicas': 'Confira antes de fabricar',
    'Envelope nominal · L × P × A': 'Medidas gerais · largura × profundidade × altura',
    'Planta cotada': 'Planta com medidas',
    'Interiores em corte': 'Ver dentro dos armários',
    'Ajustar hipóteses de circulação': 'Testar o espaço de passagem',
    'Medidas e ferragens ↓': 'Ver ficha do móvel ↓',
    'Cotas do módulo · mm': 'Medidas do móvel · mm',
    'Ferragens · quantidades e referências': 'Peças de montagem e quantidades',
    'Ferragens e ligações': 'Peças e uniões de montagem',
    'Furação · medidas e referências': 'Furos de montagem',
    'Furação e fixação': 'Furos e fixação',
    'Acabamentos · por aplicação': 'Onde aplicar cada acabamento',
    'O que falta · projeto, oficina e apartamento': 'O que falta conferir',
    'Projeto · compatibilizar': 'Definir no projeto',
    'Oficina · conferir e provar': 'Testar na oficina',
    'Apartamento · medir': 'Medir no apartamento',
    'Medidas internas e encontros': 'Espaços internos e uniões',
    'Roteiro de montagem e compatibilização': 'Como montar e o que conferir',
    'Montagem e compatibilização': 'Montagem e conferências',
    'Fechamentos técnicos deste móvel': 'O que falta conferir neste móvel',
    'Rastreabilidade documental': 'Documentos de origem',
    'Levantamento separado': 'Medidas do apartamento',
    'Levantamento no apartamento': 'Medidas do apartamento',
    'Origem / referência': 'Ponto de referência para medir',
    'Origem': 'Ponto de referência',
    'Todas as operações': 'Todos os furos',
    'Fixador': 'Peça de fixação',
    'Referências gerais': 'Orientações gerais',
    'Medidas dos 20 módulos': 'Medidas dos 20 móveis',
    'Levantamento para fabricação': 'Medidas antes de fabricar',
    'Peça / grupo': 'Peça ou grupo',
    'Esp. mm': 'Espessura · mm',
    'Esp. · mm': 'Espessura · mm',
    'C × L · mm': 'Comprimento × largura · mm',
    'Documento vigente': 'Acabamento escolhido',
    'Referência CAD · ver acabamento': 'Cor do desenho · confira o acabamento',
    'Definições técnicas': 'Escolhas e montagem',
    'Definido para este móvel': 'Escolhas deste móvel',
    'Definições': 'Escolhas',
    'Buscar documentos': 'Buscar no projeto',
    'Todas as disciplinas': 'Todos os assuntos',
    'Filtrar disciplina': 'Filtrar assunto',
    'Compatibilização': 'Conferências de montagem',
    'Executivo': 'Antes de fabricar',
    'Nominal': 'Medida do projeto',
    'Candidatas': 'Opções a conferir',
    'Não liberado': 'Ainda não aprovado para fabricar',
    'Parcial / hipótese': 'Medida a confirmar',
    'Referência comercial': 'Medida informada pelo fabricante',
    'Direção aprovada': 'Escolha para o projeto',
    'Direção / proposta': 'Proposta a conferir',
    'Envelope a conferir': 'Medidas a conferir',
    'Preferência aprovada': 'Opção preferida',
    'Fechamentos técnicos na ficha; condições físicas do apartamento na folha de levantamento.': 'Veja as pendências na ficha. Anote as medidas reais na folha do apartamento.',
    'Ligações ainda sem mapa': 'Uniões ainda sem desenho de montagem',
}


def plain_text(value):
    """Reescreve somente prosa. Chamadores protegem códigos, URLs e coordenadas."""
    if not isinstance(value, str) or not value.strip():
        return value
    leading = value[:len(value)-len(value.lstrip())]
    trailing = value[len(value.rstrip()):]
    s = value.strip()
    if s in EXACT:
        return leading + EXACT[s] + trailing
    # Arquivos e links exibidos como fontes devem continuar copiáveis.
    if re.match(r'^(?:https?://|data:|[A-Za-z]:[\\/]|(?:\d\d_|src/|fabrication/))', s):
        return value
    replacements = [
        (r'\b[Ff]uração nominal\b', 'furos previstos no projeto'),
        (r'\b[Mm]apa nominal\b', 'desenho de montagem do projeto'),
        (r'\b[Mm]edidas nominais\b', 'medidas do projeto'),
        (r'\b[Cc]otas nominais\b', 'medidas do projeto'),
        (r'\b[Cc]oordenadas nominais\b', 'posições previstas no projeto'),
        (r'\b[Ee]nvelope nominal\b', 'medidas gerais do desenho'),
        (r'\b[Ee]nvelopes\b', 'volumes do desenho'),
        (r'\b[Ee]nvelope\b', 'volume do desenho'),
        (r'\b[Cc]inemática\b', 'forma de abertura'),
        (r'\b[Dd]atum\b', 'ponto de referência para medir'),
        (r'\b[Cc]anecos\b', 'encaixes circulares das dobradiças'),
        (r'\b[Cc]aneco\b', 'encaixe circular da dobradiça'),
        (r'\b[Uu]sinagens\b', 'operações de corte e furação'),
        (r'\b[Uu]sinagem\b', 'preparação das peças'),
        (r'\b[Uu]sinar\b', 'preparar os cortes e furos'),
        (r'\b[Cc]ompatibilização fabril\b', 'conferir a montagem na oficina'),
        (r'\b[Cc]ompatibilização\b', 'conferência de encaixe e montagem'),
        (r'\b[Cc]ompatibilizar\b', 'conferir'),
        (r'\b[Ll]evantamento de campo\b', 'medição no apartamento'),
        (r'\b[Cc]otas de campo\b', 'medidas reais do apartamento'),
        (r'\b[Cc]otas acabadas\b', 'medidas com os acabamentos prontos'),
        (r'\b[Mm]edidas de campo\b', 'medidas no apartamento'),
        (r'\b[Ss]ubstratos\b', 'materiais da base'),
        (r'\b[Ss]ubstrato\b', 'material da base'),
        (r'\b[Ss]uspensão\b', 'fixação na parede'),
        (r'\b[Cc]arga admissível\b', 'peso suportado'),
        (r'\b[Cc]argas admissíveis\b', 'pesos suportados'),
        (r'\b[Cc]arga útil\b', 'peso do conteúdo'),
        (r'\b[Ii]nterfaces\b', 'uniões entre peças'),
        (r'\b[Ii]nterface\b', 'união entre peças'),
        (r'\b[Ff]aces aparentes\b', 'partes visíveis'),
        (r'\b[Pp]or face\b', 'em cada lado da peça'),
        (r'\b[Cc]ota documental\b', 'medida da planta'),
        (r'\b[Cc]otas oficiais\b', 'medidas da planta oficial'),
        (r'\b[Cc]ota oficial\b', 'medida da planta oficial'),
        (r'\b[Cc]otas\b', 'medidas'),
        (r'\b[Cc]ota\b', 'medida'),
        (r'\b[Pp]ranchas executivas\b', 'desenhos para fabricação'),
        (r'\b[Ll]iberação executiva\b', 'aprovação para fabricar'),
        (r'\b[Rr]astreável\b', 'com fonte indicada'),
        (r'\b[Rr]astreabilidade\b', 'documentos de origem'),
        (r'\b[Rr]ecotar\b', 'pedir novo orçamento para'),
        (r'\b[Ss]em Comfort\b', 'sem o sistema Comfort de fechamento suave'),
        (r'\b[Gg]eometria nominal\b', 'medidas do projeto'),
        (r'\b[Cc]arcaça\b', 'estrutura do armário'),
        (r'\b[Cc]alços\b', 'bases de fixação'),
        (r'\b[Cc]alço\b', 'base de fixação'),
        (r'\b[Vv]alidar\b', 'conferir'),
        (r'\b[Aa]éreos\b', 'armários superiores'),
        (r'\b[Aa]éreo\b', 'armário superior'),
        (r'\b[Rr]oupeiro\b', 'guarda-roupa'),
        (r'\b[Mm]aleiro\b', 'armário sobre o guarda-roupa'),
    ]
    for pattern, replacement in replacements:
        s = re.sub(pattern, replacement, s)
    # Mantém o nome comercial, explicando a função quando ela não está próxima.
    def explain(match):
        before = s[max(0, match.start()-65):match.start()].lower()
        if re.search(r'conector(?:es)?|uni(?:ão|ões)', before):
            return match[0]
        return 'conectores ' + match[0]
    s = re.sub(r'\bMinifix\b', explain, s)
    s = re.sub(r'(?i)(\d+) conjuntos (?!de )conectores', r'\1 conjuntos de conectores', s)
    # Ponto e vírgula em prosa vira uma nova frase; medidas e fórmulas ficam intactas.
    s = re.sub(r';\s+(?=[A-Za-zÀ-ÿ])', '. ', s)
    s = re.sub(r'(?<=[.!?])\s+([a-zà-ÿ])', lambda m: ' '+m[1].upper(), s)
    s = re.sub(r'\b(em|até|com|de|teto|espelho|indireta|curso|folga|profundidade)(?=\d)', r'\1 ', s)
    for wrong, right in [('pelo base de fixação','pela base de fixação'),('do base de fixação','da base de fixação'),('no base de fixação','na base de fixação'),('o base de fixação','a base de fixação'),('um base de fixação','uma base de fixação'),('dos bases de fixação','das bases de fixação'),('nos bases de fixação','nas bases de fixação'),('os bases de fixação','as bases de fixação')]:
        s = re.sub(r'\b'+wrong+r'\b', right, s)
    if value.strip()[0].isupper():
        s = s[0].upper() + s[1:]
    return leading + s + trailing


# Chaves descritivas. Referências comerciais, fórmulas, coordenadas e fontes não passam aqui.
PROSE_KEYS = {
    'summary', 'technicalSummary', 'finishSummary', 'finish', 'pending', 'hardware',
    'notes', 'note', 'reason', 'assembly', 'assemblyStatus', 'status', 'area',
    'technicalChecks', 'projectChecks', 'workshopChecks', 'resolvedChecks',
    'unmappedInterfaces', 'remainingFinish', 'remainingFinishQuestion',
    'measure', 'method', 'affects', 'acceptance', 'releaseCondition', 'scope', 'match',
    'title', 'category', 'description', 'item',
}
PROTECTED_KEYS = {'sources', 'sourcePaths', 'source', 'path', 'url', 'local', 'evidence',
                  'reference', 'pattern', 'datum', 'diameter', 'depth', 'fastener',
                  'partIds', 'ids', 'id', 'code', 'drawings', 'materialEvidence', 'unit'}


def plain_data(value, key=''):
    if key in PROTECTED_KEYS:
        return value
    if isinstance(value, dict):
        return {k: plain_data(v, k) for k, v in value.items()}
    if isinstance(value, list):
        return [plain_data(v, key) for v in value]
    if isinstance(value, str) and key in PROSE_KEYS:
        return plain_text(value)
    return value


def plain_module(g):
    g.update(plain_data(g))
    g['technicalSummary'] = SUMMARIES[g['code']]
    g['name'] = NAMES.get(g['code'], NAMES.get(g['name'], g['name']))
    old = g['finishSummary']
    if old.startswith('Interiores Branco TX. '):
        old = old.replace('Interiores Branco TX.', 'Parte interna em branco texturizado (Branco TX).', 1)
        old = old.replace('Faces aparentes:', 'Partes visíveis:').replace('partes visíveis:', 'Partes visíveis:')
        old = old.replace('Faces registradas separadamente. Não implica chapa dupla pronta.', 'Defina o acabamento de cada lado da chapa antes de comprar.')
    g['finishSummary'] = old
    for field in ['decisions', 'hardwareRows']:
        for row in g.get(field, []):
            row['explanation'] = hardware_hint(row)
    return g


def hardware_hint(row):
    item = (row.get('item') or '').lower()
    ref = (row.get('reference') or '').lower()
    if 'minifix' in ref or 'minifix' in item:
        return 'Conectores que unem as chapas e permitem desmontar o móvel.'
    if 'movento' in ref or 'fgvtn' in ref and ('corredi' in item or 'guias' in item):
        return 'Corrediças: peças que guiam a abertura e o fechamento das gavetas.'
    if 'ro-62' in ref or 'ro62' in ref or 'ro25' in ref:
        return 'Sistema para as portas deslizarem nos trilhos.'
    if 'blum' in ref:
        if 'parafuso' in item:
            return 'Parafusos para prender as dobradiças e suas bases.'
        if 'base' in item or 'calço' in item:
            return 'Bases que prendem as dobradiças ao armário.'
        if 'limitador' in item:
            return 'Peças que limitam o quanto a porta pode abrir.'
        return 'Dobradiças da marca Blum para abrir e fechar as portas.'
    if 'confirmat' in ref:
        return 'Parafusos próprios para unir chapas de madeira.'
    if 'häfele' in ref and ('apoio' in item or 'prateleira' in item):
        return 'Apoios que seguram as prateleiras.'
    if 'piano' in item:
        return 'Dobradiça contínua, instalada ao longo da borda da tampa.'
    if 'articulador' in item:
        return 'Suportes com trava para manter a tampa aberta.'
    return ''


def plain_html(html):
    """Só altera texto visível. Atributos, scripts, CSS e código ficam intactos."""
    tokens = re.split(r'(<[^>]*>)', html)
    protected = []
    for i, token in enumerate(tokens):
        if token.startswith('<'):
            tag = re.match(r'<\s*(/?)\s*(script|style|code|pre)\b', token, re.I)
            if tag:
                if tag[1]:
                    if protected and protected[-1] == tag[2].lower():
                        protected.pop()
                elif not token.endswith('/>'):
                    protected.append(tag[2].lower())
        elif not protected and token.strip():
            original = unescape(token)
            rewritten = plain_text(original)
            if rewritten != original:
                tokens[i] = escape(rewritten, quote=False)
    result = ''.join(tokens)
    # Parágrafos técnicos extensos ficam em frases separadas, sem perder valores.
    def paragraphs(match):
        text = match[2]
        if len(text.split()) <= 45:
            return match[0]
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-ZÀ-Ý])', text)
        if len(sentences) < 2:
            return match[0]
        groups = []
        for sentence in sentences:
            if groups and len((groups[-1]+' '+sentence).split()) <= 35:
                groups[-1] += ' '+sentence
            else:
                groups.append(sentence)
        return ''.join('<p'+match[1]+'>'+group+'</p>' for group in groups)
    return re.sub(r'<p([^>]*)>([^<>]+)</p>', paragraphs, result)


def document_intro(content, document):
    """Uma entrada simples para relatórios de oficina que continuam disponíveis na íntegra."""
    if document['id'] not in DOCUMENT_COPY:
        return content
    title, summary = DOCUMENT_COPY[document['id']]
    intro = '<h1>'+escape(title)+'</h1><p>'+escape(summary)+'</p>'
    intro += '<p>Confira os detalhes e as pendências antes de comprar, cortar ou instalar.</p>'
    intro += '<details class="project-report"><summary>Ver detalhes e documentos de origem</summary>'
    intro += '<p>As medidas e os códigos abaixo servem para conferir a montagem.</p>'
    # Mantém o estilo do relatório, seus links, tabelas e referências.
    main = re.search(r'(<main\b[^>]*>)([\s\S]*?)(</main>)', content, flags=re.I)
    if main:
        original = re.sub(r'<(/?)h1\b', r'<\1h2', main[2], flags=re.I)
        content = content[:main.start()] + main[1]+intro+original+'</details>'+main[3]+content[main.end():]
    else:
        body = re.search(r'(<body\b[^>]*>)([\s\S]*?)(</body>)', content, flags=re.I)
        if not body:
            return content
        original = re.sub(r'<(/?)h1\b', r'<\1h2', body[2], flags=re.I)
        content = content[:body.start()] + body[1]+intro+original+'</details>'+body[3]+content[body.end():]
    content = re.sub(r'<title>[^<]*</title>', '<title>'+escape(title)+'</title>', content, count=1, flags=re.I)
    style = '<style>.project-report{margin-top:24px}.project-report>summary{cursor:pointer;font-weight:600;padding:12px 0}@media print{.project-report::details-content{content-visibility:visible!important;display:block!important}}</style>'
    return content.replace('</head>', style+'</head>') if '</head>' in content else content.replace('<main',style+'<main',1)
