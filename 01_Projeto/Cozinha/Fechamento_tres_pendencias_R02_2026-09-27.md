# Gaveta baixa e cocção — três pendências, R02

27/09/2026. Continuidade solicitada por Elias: “vamos resolver essas 3 pendencias agr”. Conferência documental e geométrica; não medição física. Este estudo complementa a [conferência lateral R01](Coccao_60cm_conferencia_R01_2026-09-27.md).

## Decisões desta rodada

- Elias prefere **cabos fixos, sem ajustar o comprimento**. Cabo retrátil pesquisado e não adotado.
- Elias aceita retirar a cabeça da vassoura para guardar e, em resposta posterior, aceita o mesmo para o rodo: **“Sim, para os dois”**.
- Logo, deixa de ser requisito guardar vassoura e rodo montados. Não exigir nova confirmação disso nem encurtar/cortar cabos automaticamente.
- A transferência de 5 cm da cocção continua direção preferida de estudo: gaveteiro 61,9 + pia 65 + cocção 60 = 186,9 cm. Não equivale à validação completa do forno.

## Resultado das três frentes

| Frente | Resultado desta rodada | Limite restante |
|---|---|---|
| Forno/cooktop | Largura de 60 cm favorável; exigências de altura e profundidade verificadas; corte condicional calculado | Instalação ainda não fechada: falta cota inferior do KE4GC e corrigir/confirmar profundidade livre do nicho |
| Rodas, guias e caixa | Rodízio real com altura total de 39 mm confirmado em desenho primário; envelope de estudo 118,7 × 40,6 × 8,8 cm | Guias propostas, material/carga do rodízio e estrutura independente ainda precisam de especificação executiva |
| Vassoura e rodo | Forma de guardar aprovada; conjunto de referência desmontado cabe geometricamente, com cabos retos e cabeças sem empilhar | Conferir SKU comprado, medidas acabadas e manuseio; não estender conclusão a mop/pá não dimensionados |

**Não registrar as três frentes como integralmente encerradas para fabricação.** A escolha funcional dos utensílios está encerrada; a compatibilização dos aparelhos tem informação indispensável ausente.

## 1. Forno e cooktop: o que o corte precisa atender

### Documentos e atualização

Forno Venax Totale Nero GIII 50 L e cooktop Electrolux KE4GC, conforme seleção vigente. O pacote de manuais ligado à página oficial Venax em 27/09/2026 foi baixado e seu PDF comparado com o arquivo local: SHA-256 idêntico, `116C425CE605D51C27C55B50350A9D5842E58246839AF8DF4EAAD7A1580F5C24`. Portanto, os 20 cm não são uma exigência antiga superada por um manual novo encontrado nesta pesquisa.

Manual Venax, página 11: módulo de 60 cm, recorte frontal 49 × 60 cm, profundidade mínima de nicho 61 cm, ventilação na base 38 × 45 cm e **20 cm mínimos entre fundo do cooktop e topo do forno**. Tabela p. 6: frente/envelope externo 61 A × 51,7 L × 61,5 P cm; corpo de embutimento 57 A × 48,5 L × 56 P cm.

Manual Electrolux, páginas impressas 8–9: recorte 52 × 39 cm, requisitos de afastamento e passagem de ar com forno abaixo. Os 3 cm indicados em sua ilustração de ventilação não substituem os 20 cm da Venax. A altura total publicada de 13,1 cm inclui partes acima da bancada: **não é a cota de embutimento abaixo da pedra**. Página oficial e ficha BIM do fabricante repetem a altura total, sem esclarecer a cota inferior procurada.

### Altura: limite calculado

Manter por enquanto a bancada de referência a 92 cm. Definir `d` como distância vertical da superfície acabada da bancada ao ponto inferior relevante da caixa do cooktop, incluindo o que o fabricante exigir considerar. Não atribuir valor a `d` a partir de fotografia ou altura total.

Para um teste conservador usando o topo do envelope externo do forno:

- topo máximo do forno = 92 − d − 20 = **72 − d cm**;
- borda inferior máxima da frente de 61 cm = **11 − d cm**.

| d, apenas cenário | Topo máximo do forno | Borda inferior máxima da frente |
|---:|---:|---:|
| 5 cm | 67 cm | 6 cm |
| 6 cm | 66 cm | 5 cm |
| 7 cm | 65 cm | 4 cm |
| 8 cm | 64 cm | 3 cm |

**Teste concreto para desenvolvimento:** frente entre 5 e 66 cm do piso; manter 20 cm acima dela requer fundo do cooktop a pelo menos 86 cm, isto é, `d ≤ 6 cm`. É condição geométrica suficiente desse teste, não medida comprovada do KE4GC nem instalação liberada. Diferenças entre corpo, abas e frente do forno precisam ser desenhadas para posicionar a base vazada e a entrada inferior de ar; a tabela não as resolve.

Consequência já fechada: **não repetir o rodapé/base de 18 cm dos gabinetes sob o forno**. A gaveta acaba antes dele. Não elevar bancada, trocar aparelho ou remover ventilação automaticamente para resolver o corte.

### Profundidade: conflito explícito e alternativa

No estudo dos demais móveis, tampo de 61 cm com avanço frontal de 2 cm coloca as portas em 59 cm da parede. Isso não demonstra um nicho com 61 cm livres. Se o plano frontal do nicho do forno acompanhar os 59 cm, haverá **déficit de pelo menos 2 cm**, antes de acabamentos e interferências.

Alternativa concreta para avaliar, sem adotá-la automaticamente: levar o plano frontal do nicho a pelo menos 61 cm da parede acabada e prever tampo de referência de 63 cm se for mantido avanço frontal de 2 cm. Preservar a continuidade pode exigir revisar a profundidade da bancada/cozinha e sua ligação com a lavanderia; circulação e encontros não foram medidos. Avançar somente o módulo também altera o alinhamento escolhido. As cotas 61/63 são referências mínimas condicionais, não desenho executivo.

Não usar os 61,5 cm externos do forno como profundidade de nicho: incluem projeções frontais e não substituem os 61 cm livres do manual. A posição real do puxador, conexões e fundo precisa aparecer no corte.

### Informação necessária para encerrar esta frente

Obter desenho técnico ou confirmação dimensional do **KE4GC com a distância da superfície da bancada ao ponto mais baixo da caixa instalada**, e cruzar esse dado com o apoio/abas do Venax. No desenho da marcenaria, cotar explicitamente 61 cm livres de profundidade, ventilação 38 × 45 cm na base e percurso de ar, além dos 20 cm entre aparelhos. Conferir interface térmica junto à máquina e acessibilidade das instalações conforme manuais específicos.

Nenhum fabricante foi contatado e nenhuma mensagem foi enviada. Não pedir novamente ao usuário medidas de obra/aparelho que ele já informou não possuir. A ausência dessa cota é limite da documentação disponível, não decisão estética pendente.

## 2. Rodas, guias e espaço útil

### Rodízio dimensional de referência

**Quadrilátero Rodízio Fixo 30 Cristal, código 1372.** Desenho publicado pelo fabricante e inspecionado visualmente no navegador:

- diâmetro da roda: 30 mm;
- altura total: **39 mm**;
- dimensões principais da chapa: 40 × 21 mm;
- largura indicada da roda: 13,5 mm.

O varejo o anuncia como silicone, mas a página/desenho primários consultados não declaram composição nem capacidade de carga. **Geometria confirmada; material silicone e carga ainda não certificados pela fonte primária.** Não substituir silenciosamente silicone por outro polímero nem encomendar com base apenas na palavra “cristal”. Existe erro de unidade na tabela comercial (“39 cm”), em conflito com a descrição de 39 mm; prevalece o desenho primário de 39 mm.

Proposta de implantação: seis rodízios fixos, em duas fileiras com três apoios cada, orientados no sentido de abertura. Quantidade é proposta para distribuir o fundo largo, não cálculo certificado de carga. Conferir peso próprio, carga de uso, fixação e piso; não multiplicar seis vezes a carga individual como garantia de capacidade do conjunto.

### Reserva de guias

Proposta dimensionada para o estudo: guias laterais simples de deslizamento, removíveis, sem sustentar verticalmente a gaveta. Reservar **5 mm por lado**, por exemplo 3 mm para faixa de desgaste e 2 mm de folga de corrida. Material, fixação, desgaste, tolerância e batente desmontável ainda a especificar. Esta reserva não é uma ferragem industrial selecionada e não garante funcionamento em piso irregular.

Preservar retirada completa para limpeza. O caminho de cargas dos gabinetes e da pedra deve ser independente da caixa e das rodas, sem pés/divisórias bloqueando o vão. A faixa superior de 3,5 cm não foi dimensionada como viga nem liberada para corte de apoios.

### Cálculo proposto, em centímetros

| Dimensão | Conta | Útil geométrico |
|---|---|---:|
| Comprimento | 126,9 − 3,6 de laterais estruturais − 1,0 de guias/folgas − 3,6 de laterais da caixa | **118,7** |
| Profundidade | 51,0 de posição da frente recuada − 5,0 de reserva posterior − 1,8 de frente aplicada − 3,6 de frente/fundo da caixa | **40,6** |
| Altura | 14,5 de cota do bordo da caixa − 3,9 de roda/suporte − 1,8 de fundo | **8,8** |

Preservados recuo frontal de 8 cm, base total de 18 cm e reserva acima da caixa de 3,5 cm. A mudança de rodas recupera **0,6 cm de altura**, não 2 ou 3 cm. Se houver forro removível de 2 mm sobre o fundo, a altura livre cai para **8,6 cm**; não incluí-lo sem descontar sua espessura.

As cotas são o envelope do estudo. Guias mais espessas, reforços, piso, montagem e manuseio podem reduzi-lo. Não registrar 118,7 × 40,6 × 8,8 como medida de fabricação já aprovada.

## 3. Vassoura e rodo com cabeças retiradas

Referências reais que atendem ao estudo, sem compra ou aprovação automática de marca:

| Item | Referência consultada | Dimensão publicada |
|---|---|---|
| Vassoura | Noviça Original BT167215 | Cabeça 31,5 × 19 × 6,5 cm; cabo fixo 112,5 × 2,1 × 2,1 cm |
| Rodo | Noviça Máxima Aderência P, ref. 1292 | Cabeça 32,5 × 9,5 × 3,5 cm; cabo fixo 112,5 × 2,1 × 2,1 cm |

**Atenção ao código:** fichas de outras versões/linhas da Bettanin informam cabos de 120 cm. Não comprar apenas pelo nome da linha. Cabo de 120 cm ultrapassa os 118,7 cm úteis no arranjo reto adotado e não está validado por este estudo.

### Disposição sem empilhar

Origem no canto interno esquerdo, medidas da planta em centímetros. Os retângulos são envelopes dos produtos, não desenho de suas formas exatas.

- Cabo 1: x = 3,1..115,6; y = 3,0..5,1.
- Cabo 2: x = 3,1..115,6; y = 6,5..8,6.
- Cabeça da vassoura deitada: x = 5,0..36,5; y = 14,0..33,0; altura 6,5.
- Cabeça do rodo deitada: x = 43,0..75,5; y = 17,0..26,5; altura 3,5.

Todos os envelopes ficam dentro de 118,7 × 40,6 cm, sem interseção em planta. O item mais alto tem 6,5 cm, deixando 2,3 cm dentro dos 8,8 cm; com forro de 2 mm restam 2,1 cm. Cabos de 112,5 deixam **6,2 cm de saldo total**, ou 3,1 cm por extremidade no arranjo centrado. A pega real deve ser ensaiada; o saldo não é tolerância toda disponível para construção.

Sem ganhar os 5 cm da cocção, com as mesmas guias o comprimento seria 113,7 cm: apenas 1,2 cm a mais que o cabo. A ampliação continua útil para manuseio e margem de montagem, embora a desmontagem resolva a maior parte do problema.

Guardar peças limpas e secas. Não contar a área restante como capacidade comprovada para mop, pá ou todos os itens de limpeza ainda não dimensionados.

## Fontes verificadas em 27/09/2026

- [Manual Venax local, p. 6 e 11](../../02_Plantas_e_manuais/Manuais/Venax_Forno_embutir_gas_50_90L_26019.pdf), idêntico ao PDF do pacote oficial atual.
- [Venax, página oficial e downloads](https://venax.com.br/categoria-produto/fornos/fornos-de-embutir-a-gas/forno-a-gas-de-embutir-50-l-totale-nero/forno-de-embutir-a-gas-50l-totale-nero-giii-gas-glp/).
- [Manual Electrolux 250405XATF](https://api.electrolux-medialibrary.com/asset/1fc5d741-d94e-4db1-b564-bde514cdb7f8/E4RM3Q/250405XATF/PDF/250405XATF.pdf) e [ficha publicada pela Electrolux no BIMobject](https://www.bimobject.com/en/electroluxbrasil/product/ke4gc).
- [Quadrilátero, produto 1372](https://www.quadrilatero.ind.br/produtos/rodizio-fixo-30-cristal-250) e [desenho técnico](https://www.quadrilatero.ind.br/img/ecommerce/250-1.jpg).
- [Anúncio comercial de silicone, confirmação de material ainda necessária](https://www.madeiramadeira.com.br/rodizio-de-silicone-fixo-30mm-quadrilatero-4-unidades-155137746.html).
- [Bettanin, Noviça Original BT167215](https://www.bettanin.com.br/produto/bt167215-novica-original/) e [rodo 1292](https://www.bettanin.com.br/produto/1292-novica-rodo-maxima-aderencia-p/).
- [Cabo retrátil BTN45H, pesquisado e não adotado](https://www.bettanin.com.br/produto/btn45h-novica-concept-cabo-extensor/).

Respostas de pesquisa arquivadas em `.firecrawl/2026-09-27-fechamento-tres-pendencias.json`, na raiz do workspace. Nenhuma compra, fabricação, mudança no modelo geral ou publicação realizada.
