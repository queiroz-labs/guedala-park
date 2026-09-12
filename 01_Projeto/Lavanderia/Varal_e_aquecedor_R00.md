# Varal e aquecedor

[Voltar ao assunto](README.md) · [Resumo do projeto](../Resumo.md)

Referência original: A04.5. As capas dos PDFs conservam esse código.

**R00 · 10/09/2026 · Estudo preliminar e especificação de desempenho — sem liberação para fabricar ou instalar**

O pedido de Elias é ampliar a robustez do varal ocasional, que sai de um compartimento tipo gaveta e desce. O aquecedor deve permanecer escondido por armário ripado. A alternativa de varal em módulo aéreo vizinho já foi aceita caso a posição acima do aquecedor não seja viável.

**Resultado:** propor **30 kg de roupa molhada como capacidade útil nominal mínima a comprovar**, com grelha de estudo de **100 × 50 cm**. A implantação lateral é a recomendação preliminar por permitir separar roupa, movimento e gotejamento da área técnica. A posição acima permanece uma intenção, sem cabimento demonstrado. Não foi localizado, nas fontes consultadas, um conjunto pronto que comprove simultaneamente essa carga, extração tipo gaveta, descida e instalação oculta em móvel.

## 1. Requisitos propostos para o varal

| Item | Valor / solução de estudo | Significado |
|---|---|---|
| Capacidade útil | 30 kg de roupa já molhada, distribuída | Meta proposta nesta revisão; não capacidade instalada ou aprovação de produto. |
| Grelha inicial | 100 cm de largura × 50 cm de profundidade | Geometria para ensaio de layout, não medida da unidade ou ordem de fabricação. |
| Opção maior | 120 × 50 cm | Somente se houver espaço para mecanismo e movimentos. Maior largura não aumenta a carga automaticamente. |
| Retração e descida | Extração completa com trava, seguida de descida controlada | Mecanismo específico a selecionar ou desenvolver; não combinar ferragens sem validação do conjunto. |
| Acionamento | Assistido e controlado, com retenção contra queda | Avaliar força de operação para carga cheia, parcial e varal vazio; motor é alternativa, não escolha fechada. |
| Altura de uso | A definir pelo alcance e obstáculos | Não fixar altura sem bancada, pé-direito e curso do mecanismo. |
| Compartimento fechado | A definir pelo envelope real do mecanismo | 100 × 50 cm é a grelha, não o nicho: articulações, trilhos, folgas e acesso aumentam o volume. |
| Apoio de cobertor | Distribuído entre barras apropriadas | Carga total não garante resistência de uma vareta isolada; exigir carga admissível local e distribuição permitida. |

O peso da roupa deve ser o peso molhado após o processo de lavagem/centrifugação que será utilizado. Não adotar multiplicador fixo do peso seco nem equiparar os 12 kg nominais de lavagem da VC4 a 12 kg de roupa molhada. Cobertor dobrado pode caber em largura menor que a peça aberta, mas ocupa volume, perde ventilação entre dobras e pode tocar os móveis; seu comprimento pendurado ainda precisa ser conferido.

## 2. Fixação: caminho das cargas

**Roupa → barras → quadro móvel → articulações/cabos/trilhos → chassi fixo → ancoragens → suporte resistente verificado.**

A marcenaria serve para acabamento e ocultação. A proposta é um chassi metálico próprio, sem transferir carga ao aquecedor, às conexões, ao duto, à máquina ou apenas ao fundo do armário. Material resistente à corrosão, extremidades protegidas e componentes substituíveis são requisitos de projeto; perfis, espessuras e soldas dependem de cálculo e do mecanismo.

| Suporte encontrado futuramente | Encaminhamento |
|---|---|
| Concreto ou alvenaria apta, identificados | Selecionar ancoragem pela base, tração/cisalhamento, bordas, espaçamentos, profundidade disponível e instalações ocultas. |
| Parede em drywall | Verificar composição e reforço dedicado ligado à estrutura adequada. Não considerar uma bucha na chapa como solução já suficiente para este varal móvel. |
| Forro de gesso/drywall | Como diretriz deste estudo, levar a carga ao suporte resistente por estrutura projetada; não suspender este conjunto apenas no acabamento do forro. |
| Shaft, fechamento técnico ou parede com tubulações não mapeadas | Não especificar furos até identificar o suporte e as interferências. |

A Knauf orienta considerar geometria, tipo de uso, vibração e forma de aplicação da carga; no teto, a extração dos fixadores merece atenção específica. Isso impede escolher fixação apenas pelo peso anunciado de uma bucha. [Fonte: Knauf](https://knauf.com/pt-BR/performance/resistencia-e-seguranca).

Os HTMLs registram um aviso de limite de profundidade de furação de 3 cm na região do aquecedor da unidade filmada. Esse aviso **não é autorização para furar 3 cm na unidade de Elias**, nem demonstra existência de reforço disponível para o varal. A base oficial também representa alvenaria estrutural: não pressupor que rasgos ou aberturas para embutir mecanismos sejam permitidos.

### Cálculo preliminar de solicitação — não é cálculo final de resistência

Para tornar o pedido de cotação verificável, adota-se um **cenário ilustrativo** com massa do quadro/mecanismo de 15 kg, além dos 30 kg úteis. Os 15 kg não foram medidos nem correspondem a um produto selecionado; substituir pela massa real. Peso de portas, revestimentos e outros componentes carregados pelo suporte também entra no cálculo final.

| Cenário estático | Massa total ilustrativa | Força vertical, g = 9,81 m/s² | Momento com centro de carga a 0,60 m do suporte |
|---|---:|---:|---:|
| 20 kg de roupa + 15 kg de conjunto | 35 kg | 343,35 N | 206,01 N·m |
| **30 kg de roupa + 15 kg de conjunto** | **45 kg** | **441,45 N** | **264,87 N·m** |
| 35 kg de roupa + 15 kg de conjunto | 50 kg | 490,50 N | 294,30 N·m |

Fórmulas: **F = m × g**; **M = F × e**. O braço de 0,60 m é uma hipótese para mostrar o efeito da extração e não a profundidade da grelha. A distância real será medida do suporte ao centro de gravidade em cada posição; a posição mais desfavorável pode ocorrer durante o movimento.

Exemplo adicional: com o momento de 264,87 N·m e duas linhas de reação separadas verticalmente por 0,30 m, o binário idealizado exige **882,9 N** de reação de tração na linha superior, antes de fatores e demais efeitos. Isso **não é carga por parafuso**, nem capacidade requerida final de uma bucha. Distribuição desigual, flexão da placa e efeito de alavanca podem alterar as reações.

O cálculo final precisa incluir peso próprio real, carga parcial e assimétrica, cobertor concentrado em poucas barras, aceleração/frenagem, esforço manual, torção, fadiga de ciclos e deformação. Coeficientes de segurança e combinações devem ser definidos pelo responsável pelo conjunto e pelas normas aplicáveis; esta memória não os substitui. Não usar ensaio doméstico com pessoas ou sobrecarga improvisada.

**Não especificados por falta de base verificável:** quantidade/diâmetro/profundidade dos fixadores, perfil e espessura do chassi, cabo, mola, pistão, motor ou corrediça. Uma corrediça anunciada para 45 kg em gaveta não comprova capacidade de 30 kg neste mecanismo suspenso e articulado.

## 3. Aquecedor: verificação do candidato E15

O REU-E150 FEH continua candidato, sem escolha final. No manual oficial consultado, as páginas 3–4 admitem compartimento exclusivo sujeito à NBR 13103, exigem base incombustível e vedam fixação sobre madeira mesmo isolada. Registram **20 cm laterais recomendados, 30 cm acima, 20 cm ao redor da chaminé e 60 cm livres à frente**. Ventilação deve ser permanente, sem obstrução, e manutenção acessível; materiais/produtos inflamáveis devem ficar afastados. [Manual Rinnai E15](https://www.rinnai.com.br/uploads/manual/201.pdf).

**Aplicação ao projeto — inferências preliminares:**

- A frente ripada próxima ao aparelho não está validada só porque abre: o manual apresenta o espaço frontal como condição de funcionamento, não apenas de manutenção. Exigir solução documentada para o fechamento antes de definir a profundidade do armário.
- Não colocar prateleira, gaveta ou roupa nos volumes livres. Verificar o envelope do tecido em todos os estados, incluindo deslocamento e gotejamento; testar somente o varal vazio no desenho é insuficiente.
- O ripado decorativo não substitui a ventilação permanente do ambiente. A área livre efetiva depende de ripas, inclinação, telas, percurso e ligação ao ambiente/exterior; não adotar uma porcentagem visual como aprovação.
- Não compartilhar o compartimento técnico com estoque de limpeza. Uma chapa separadora improvisada não comprova afastamento térmico ou adequação do fechamento.
- Não utilizar o aquecedor ou sua exaustão para secar roupa, nem basear a solução na promessa de mantê-lo desligado enquanto o varal estiver aberto.

O E21/REU-E211 FEH também foi consultado apenas para comparação: o fabricante o identifica como equipamento de circuito aberto; seu manual prevê ventilação, base incombustível e restrições a combustíveis próximos. Não constitui solução automaticamente compatível com armário ripado. As dimensões atuais publicadas são **48,3 × 35 × 15,7 cm (A × L × P)**; não transferir os afastamentos do E15 como se fossem especificação do E21. [Ficha E21](https://www.rinnai.com.br/aquecedores-a-gas/nova-geracao/e21-1/) · [Manual E21](https://www.rinnai.com.br/uploads/manual/176.pdf).

Este estudo não escolhe capacidade térmica do aquecedor. Permanecem a demanda da Addra Livo, pressão/vazão, temperatura de entrada, exaustão e orçamento. As normas são referenciadas pelos fabricantes; não foi realizada leitura integral da NBR 13103 ou validação normativa da instalação.

## 4. Teste geométrico com a base existente

Base documental: 129 cm no trecho longitudinal de serviço e 154 cm transversais. Pé-direito, rebaixos, shaft e eixos do duto não medidos.

| Alternativa | Teste preliminar | Resultado |
|---|---|---|
| Acima do aquecedor | Compartimento e percurso do tecido precisam ficar fora de afastamentos e duto | Sem volume livre demonstrado; não liberar a posição preferida. |
| Módulo vizinho | Usando largura do E15 de 35 cm registrada no projeto e reservando 20 cm de cada lado, a faixa resulta em 75 cm. Somada a grelha de 100 cm, resulta em 175 cm, antes de painéis/mecanismos. | Excede 129 cm em 46 cm neste ensaio de volumes separados na mesma linha. Não prova impossibilidade em outro arranjo, mas impede desenhar ambos lado a lado dentro desse trecho como resolvidos. |
| Varal maior de 120 cm | 129 − 120 = 9 cm antes de laterais, mecanismo e demais interferências | Não há folga comprovada para embutimento; 120 cm fica como alternativa. |
| Varal de teto comercial de 122 cm | Corpo quase ocupa o trecho longitudinal e desce sobre a zona de uso | Precisa de outra implantação e solução de ocultação aprovada; não é substituição direta da gaveta. |

**Recomendação de desenvolvimento:** estudar o módulo vizinho fora da área técnica, eventualmente na transição com a cozinha, mantendo a janela livre. Essa posição ainda precisa ser compatibilizada com micro-ondas, depurador, aéreos e circulação; nenhum módulo aprovado foi deslocado nesta revisão. Se não houver espaço, será necessária uma escolha explícita entre mecanismo, ocultação e capacidade; não reduzir silenciosamente a carga ou trocar por varal visível.

O teste final deve representar quatro estados: recolhido, extraído, descido e carregado. Incluir roupas penduradas, porta da VC4, tampas/portas do móvel, acesso ao tanque, janela, aquecedor e manutenção. Uma toalha ou cobertor não pode formar uma cortina diante da ventilação ou do aparelho.

## 5. Referências reais de produto

| Referência | Evidência do fabricante | Limite para este projeto |
|---|---|---|
| Mad Varais, linha de embutir | Até 20 kg, inox 304, tamanhos anunciados 50 cm, 1 m e 1,2 m | Abaixo da meta de 30 kg; descida não comprovada. Modelo oculto é descrito para embutir em alvenaria, não autorização para rasgar paredes do apartamento. |
| Foxydry Air, versão de 122 cm | Até 35 kg de roupa distribuída; corpo aproximadamente 122 × 57 × 30 cm; descida até 180 cm | Modelo de teto com alimentação elétrica, sem extração de gaveta. Instalação em caixa de marcenaria não demonstrada; importação, suporte local e compatibilidade elétrica não verificados. |

Fontes primárias: [Mad Varais](https://www.madvarais.com.br/) e [Foxydry Air](https://www.foxydry.com/products/foxydry-air), consultadas em 10/09/2026. Nenhum produto escolhido ou comprado. Não é necessário adotar ventiladores, iluminação integrada ou motorização por aparecerem em uma referência. Um elevador avulso com capacidade anunciada não valida grelha, fixação ou sistema completo.

## 6. Especificação para futura proposta técnica

Solicitar um conjunto ocultável, extraível e com descida controlada, para **30 kg úteis de roupa molhada**, inicialmente estudado com grelha **100 × 50 cm**. A proposta deve informar:

1. Carga total e por barra, distribuição admitida, massa própria, envelope aberto/fechado e curso completo.
2. Travamento na extração, retenção contra queda, comportamento com carga assimétrica e força de operação vazio/cheio.
3. Desenho do chassi e caminho das cargas; cálculo de ancoragens conforme suporte identificado e mapa de instalações.
4. Critérios de resistência, deformação, fadiga/ciclos e manutenção; validação do conjunto na aplicação proposta, não somente de componentes avulsos.
5. Condições de teste e aceitação definidas pelo fabricante/responsável técnico, com capacidade final identificada no equipamento.
6. Desenho conjunto com aquecedor, duto, ripado e envelope de roupa, conferido pelo responsável pela instalação de gás.

Não foi enviado pedido a fornecedores. Os documentos indisponíveis ficam como condição da execução futura, sem nova solicitação imediata a Elias.

**Concluído nesta etapa:** meta de carga, geometria para estudo, memória de esforços ilustrativa, estratégia de fixação, análise das interferências e critérios para selecionar/validar o mecanismo. **Ainda não concluído:** dimensionamento estrutural executivo, produto que atenda integralmente à gaveta com descida, ancoragem específica e cabimento definitivo do fechamento do aquecedor.
