# Banco — candidato Southco E6 unidirecional

Estudo separado, 23/10/2026. Não incorpora ferragem ao CAD nem aprova compra/fabricação. Preserva as duas tampas e procura não ocupar o baú. A instalação sobre a tampa é uma hipótese de adaptação da fixação, ainda sem detalhamento estrutural.

## Evidência do fabricante

- [Desenho J-E6-10-6-0, revisão D, 12/08/2021](https://files.southco.com/static/JDrawing/j-e6-10-6-0.pdf): família E6-10-6110R0/F0, torque 12,4 ± 2,5 N·m por unidade; resistência no sentido livre até 0,5 N·m. Montagem M6, furos da ferragem Ø6,52 com tolerância −0,2; preparação do suporte Ø6,7 +0,1; padrão 46 × 50 mm, 25 mm de cada linha à linha de referência da articulação. Abas 4,5 mm, projeção total 20,3 mm, largura máxima 91,6 mm. Não extrair a coordenada exata do eixo medindo pixels do desenho.
- [Ficha TD-E6-10-6-0-J, revisão A, 03/10/2019](https://files.southco.com/static/TestDataSheet/td-e6-10-6-0-j.pdf): 20.000 ciclos, eixo horizontal, movimento de 180° ida/volta; torque dentro de 20% do nominal. Ensaio térmico dividido entre −20 °C, ambiente e 65 °C. Dados de resistência não certificam a fixação na madeira; o fabricante recomenda ensaio da aplicação.
- [Catálogo oficial, página 377](https://media.southco.com/media/static/Literature/e6-ct.en.pdf): confirmação dos códigos unidirecionais e montagem. A versão R0 oferece resistência no sentido reverso; F0 no adiante. A orientação exata deve fazer a abertura trabalhar no sentido livre e o fechamento no sentido resistido.

Os PDFs e imagens estão em `Fontes/Southco_E6_*` e foram inspecionados visualmente.

## Pré-seleção mecânica

Duas unidades de 12,4 N·m por tampa: torque nominal 24,8 N·m; mínimo conservador do desenho 19,8 N·m; máximo 29,8 N·m. O máximo de abertura livre do par é 1,0 N·m, adicional ao peso da tampa. É retenção por atrito, não mola de assistência e não amortecimento de fechamento.

Tampas 971 × 448 × 20 e 825 × 448 × 20 mm. A densidade hipotética de 900 kg/m³ produz 7,830 e 6,653 kg; momentos de peso com braço 224 mm de aproximadamente 17,20 e 14,61 N·m. O par supera esses momentos nus, mas revestimento, ferragem móvel, tolerância, posição final do eixo e margem de aplicação ainda precisam entrar na conta. Nenhum ocupante ou objeto deve permanecer sobre a tampa ao abrir.

## Geometria a validar

A folha móvel pode, em princípio, ficar sobre a face superior da tampa; a folha fixa, em suporte vertical acima do plano da tampa, junto à frente do encosto. Isso desloca o eixo para acima de Z420, evitando a condição de eixo inferior que inviabilizou a Rockler. A ficha do fabricante mostra montagem perpendicular como situação de ensaio, mas não é uma instalação específica para este banco.

O encosto atual é apenas reserva geométrica de X0–100, Z400–900; não há estrutura interna comprovada para receber o torque. A solução precisaria de ligação estrutural à traseira/estrutura do banco, contida na região do encosto, sem braços no baú. Não se pode parafusar a ferragem numa espuma ou assumir resistência do volume de reserva.

A projeção da ferragem sobre o tampo interfere com a almofada de 50 mm e deve ser avaliada sem assumir que a espuma absorve o ressalto. M6 pede contraparte/insertos dimensionados; uma porca saliente no interior conflitaria com o requisito de preservar armazenamento. Não aprovar insertos cegos de comprimento arbitrário em tampa de 20 mm.

Pendências específicas, independentes de medidas do apartamento: CAD real ou coordenada do eixo fornecida pela Southco, envelope em 90° de montagem, sentido R0/F0, suporte do encosto, transferência de torque, retenção dos M6 no painel, compatibilidade com almofada e limite de abertura. O objetivo é avançar para uma solução verificável, não afirmar compatibilidade apenas pela capacidade nominal.

## Ensaio de eixo superior — resultado novo

`banco_eixo_superior.py` e `Banco_eixo_superior.json` ensaiam 18 combinações × 901 poses de 0–90° em incrementos de 0,1°. Eixos abstratos em X100 ou X102, com Z425/430/435, não intersectam os AABB ativos nem a superfície física Berlin nas duas tampas. A faixa passa na triagem da tampa, não constitui CAD validado da ferragem. Almofadas foram retiradas para o ensaio; ferragem, suporte, usuário e tolerâncias não estão nele.

Em X110, mesmo com o eixo acima da tampa, a quina inferior traseira desce e colide com traseira/laterais. Portanto, montar diretamente a folha fixa na face X100 do encosto e deixar o cilindro avançar pode ser incompatível. O suporte precisa posicionar o eixo até X102, preferencialmente próximo de X100 para folga. Isso provavelmente exige um alojamento localizado dentro da reserva do encosto; não assumir que uma fixação aparente simples resolve.

Para eixo hipotético X100/Z430, o centro de massa nu fica a (226,−20) mm do eixo. O máximo de torque em 0–90° é m·g·√(0,226²+0,020²), em cerca de 5,06°. A tampa maior a ρ900 exige aproximadamente **17,42 N·m**, e a menor **14,80 N·m**. O cálculo anterior de braço224 é referência do eixo na borda, não deve ser transplantado à implantação superior.

Pré-seleção a estudar: par12,4±2,5 N·m na tampa maior (mínimo19,8) e par10,7±2,1 N·m na menor (mínimo17,2). São quatro ferragens no total, não quatro de12,4 obrigatórias. A margem nua até o mínimo é cerca de2,38/2,40 N·m, antes de acabamento, ferragem móvel, margem de aplicação e fixação. A peça12,4 é código6110R0/F0; a10,7 é695R0/F0. Orientação ainda não escolhida.

Atrito não alivia a elevação: a força tangencial inicial aproximada na borda dianteira da tampa maior fica em torno de41 N (4,2 kgf), incluindo até1 N·m de atrito livre do par. Perto de90°, forçar fechamento contra o torque máximo do par pode pedir aproximadamente63 N (6,4 kgf), dependendo do ponto e direção de pega. Não chamar de abertura assistida ou fechamento suave. Essas forças também precisam ser transferidas pela fixação M6 e suporte; a capacidade da dobradiça não é capacidade da madeira.
