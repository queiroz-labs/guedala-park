# Southco E6 — conferência independente da geometria do fabricante

23/10/2026. Pesquisa de fixação; não altera o modelo e não libera fabricação.

## O que a documentação efetivamente fecha

O desenho oficial [J-E6-10-6-0, revisão D](https://files.southco.com/static/JDrawing/j-e6-10-6-0.pdf) e a [página 377 do catálogo](https://media.southco.com/media/static/Literature/e6-ct.en.pdf) foram conferidos visualmente nas cópias arquivadas na R45. A ferragem possui quatro furos de passagem para M6: dois em cada folha. O espaçamento longitudinal entre os dois furos de uma folha é 46 ± 0,2 mm; cada linha está a 25 mm da referência da articulação na posição plana. A preparação do painel no desenho é Ø6,7 +0,1 mm. Os 50 mm entre linhas são da posição plana, não são uma distância que se possa aplicar diretamente a duas faces perpendiculares.

As folhas têm 4,5 mm, a largura máxima do conjunto é 91,6 mm e sua projeção total a partir da face de montagem é 20,3 mm. A projeção de 20,3 mm **não é a distância ao eixo**. O desenho não fornece cota explícita eixo–plano de apoio. Portanto, não é válido tomar metade de 20,3 mm, nem obter a coordenada por escala de pixels, para fabricar o suporte.

O [ensaio TD-E6-10-6-0-J](https://files.southco.com/static/TestDataSheet/td-e6-10-6-0-j.pdf) mostra expressamente uma montagem perpendicular: folha fixa para cima em apoio vertical e móvel horizontal, apoiada sobre o painel. Essa configuração é fisicamente coerente com um suporte no encosto e folha móvel acima da tampa. O ensaio demonstra a configuração da dobradiça; não fornece dimensões do suporte nem certifica madeira, insertos ou parafusos do banco.

## Consequências no banco

- Colocar a folha móvel diretamente na face superior Z420 produz aço/alumínio em Z420–424,5, pelo menos. As cabeças M6 aumentam o ressalto, a menos que uma solução específica as acomode. Não há como chamar esse ressalto de zero.
- A almofada modelada inicia em Z420. Portanto, onde o envelope em planta da almofada coincide com a folha, existe interferência volumétrica real. O fato de ser espuma não constitui verificação de apoio nem autorização para ignorar esse volume.
- Embutir a folha 4,5 mm na tampa eliminaria parte do ressalto, mas usinaria a tampa: não atende à hipótese de preservar sua geometria. Fixar tudo por baixo coloca material no baú e requer uma nova verificação de eixo e giro.
- O suporte fixo pode ser contido na reserva X0–100 do encosto; isso não reduz o baú. Entretanto, essa reserva não prova que haja estrutura portante ali. O caminho de carga até a estrutura do banco continua necessário.
- A montagem direta sobre a frente X100 do encosto desloca o corpo/eixo à frente dessa face. Não se pode aprová-la usando o ensaio abstrato X100/Z430 da R45. A R45 já encontrou interferências com eixo X110; somente um suporte recuado, dimensionado com o CAD real, pode potencialmente recuperar o eixo próximo de X100–102.

## Sentido F0 e R0

F0 fornece torque alto no sentido denominado forward e giro livre no reverse. R0 faz o inverso. O sufixo inclui o zero; E6-10-6110F-50 sem zero é outra ferragem, com resistência também na abertura.

Na vista do catálogo que mostra a folha fixa abaixo, barrel à esquerda e móvel acima, o sentido forward é horário e reverse anti-horário. Ao girar essa configuração em 180° no plano da vista para pôr a fixa acima e usar a móvel horizontal para a direita, a abertura horizontal→vertical corresponde ao sentido reverse; nessa leitura **F0 é a pré-seleção** para abertura livre e fechamento resistido. Esta é uma inferência de orientação, não uma indicação de mão de montagem fornecida especificamente para o banco.

O desenho J mostra a seção pelo outro arranjo visual e não fornece uma transformação 3D entre a vista e a instalação do banco. Antes de fixar os códigos na lista de compra, o STEP ou uma peça deve identificar inequivocamente a folha fixa e demonstrar o sentido. Um teste simples deve confirmar que levantar a tampa exige só o peso e a pequena resistência livre, enquanto o fechamento encontra o torque nominal. Não substituir esse teste por uma identificação de esquerda/direita sem referencial.

## Resultado geométrico

A Southco permite a configuração perpendicular pretendida e pode deixar o armazenamento livre. **A fixação não está fechada só com os PDFs disponíveis:** faltam a coordenada real do eixo, o envelope montado e o tratamento do ressalto acima de Z420. A solução tem de preservar simultaneamente tampa, almofada e baú; validar somente o sólido da tampa em giro não satisfaz essas três condições.

Fontes adicionais: [produto oficial F0](https://shop.southco.com/en_eu/e6-10-6110f0-50), [catálogo em português](https://files.southco.com/static/Literature/e6-ct.pt.pdf). A página do produto confirma família one-way, montagem frontal e fixação por parafuso/rebite; não contém aprovação de inserto para madeira. Nenhuma compra ou contato externo foi efetuado.
