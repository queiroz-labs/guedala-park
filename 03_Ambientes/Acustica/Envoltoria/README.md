# Envoltória: paredes, porta e teto

**Estudo NOMINAL, não é projeto acústico nem laudo — 29/10/2026.** Cotas de projeto, não medições. As faixas abaixo são sensibilidades analíticas; não são previsão do isolamento entregue. Nenhuma compra ou solução adotada.

| Parte | Resultado calculável | Resultado real / decisão |
|---|---|---|
| Paredes | 256 valores de R por incidência normal, 100–3150 Hz, para 16 massas condicionais | Rw e coincidência desconhecidos; não escolher contraparede pela lei da massa |
| Porta | Folha H=30 dB: conjunto com fresta inferior 0/1/3/10 mm = 30/28,24/26,02/22,22 dB | Conferir frestas antes de cotar troca; não é Rw da porta Cury |
| Pontos fracos | Parede H=50 dB, 0,1–5% de área com R=0/10/20: composto 13,01–46,99 dB | Identificar caixas, visitas e selagens; não vedar ventilação ou acesso técnico |
| Flancos | Energia marginal H=0/25/100/300% da direta: perda 0/0,97/3,01/6,02 dB | Sensibilidade arbitrária, **não ISO 12354**; DnT,w não determinado |
| Laje H maciça 10–14 cm | 230–350 kg/m²; base de impacto equivalente 74,96–81,34 dB | **Não L'nT,w**; composição/piso superior desconhecidos; ganho de forro não calculável |
| Contraparede/forro | Ressonância ideal H: 43,48–112,76 Hz; cavidade 3–10 cm | Não é ΔRw; cavidade rasa pode colocar ressonância na faixa relevante |
| Cobertura | 29 faces, 407 linhas de sensibilidade; áreas reconciliadas | Adjacências de unidades/hall/escada/elevador ainda sem mapa seguro |

## O que a documentação realmente sustenta

- [Memorial Cury](../../../01_Programa_e_decisoes/Memorial_Cury_impactos.md), §§2.1 e 3.1, pp.12–15 do PDF: alvenaria estrutural; não identifica concreto/cerâmica, espessura, graute ou massa superficial. A informação do usuário em 29/10/2026 (“paredes são feitas de bloco estrutural”) confirma o sistema, não esses parâmetros. Fechamentos não estruturais podem ser bloco de concreto e/ou drywall; não atribuir a todos os shafts a mesma composição.
- Paredes secas: pintura sobre gesso. Cozinha/lavanderia: cerâmica nas posições especificadas, pintura nas demais. Gesso de enchimento e paredes de shaft exigem projeto executivo: um revestimento de gesso não identifica uma parede inteira de gesso.
- **A planta do pavimento tipo é a p.14 da convenção**, não do memorial. O PDF comprimido não permitiu associar com segurança cada face ao outro apartamento, escada ou elevador. Não se deduz proximidade pelo número do final. [Convenção e referência à planta](../../../01_Programa_e_decisoes/Convencao_e_ata_impactos.md).
- A planta oficial da unidade mostra **entrada pela cozinha**, na extremidade direita inferior do desenho, abrindo para dentro. A porta do dormitório 02 abre para circulação interna. Isso corrige a localização descrita no pedido. A face nominal correspondente é `cozinha_x740`, não parede do escritório. [Plantas originais](../../../09_Referencias/Plantas_e_manuais/README.md).
- Memorial §4.3: portas/batentes de madeira e/ou MDF, acabamento liso; não especifica núcleo maciço/semioco, Rw ou vedação. O vão H de 0,75 × 2,05 m do levantamento de acabamentos **não é dimensão oficial confirmada**. O exercício de fresta usa outra dimensão H explícita, 0,80 × 2,00 m.
- [Quadro de cargas](../../Planta_pontos/Quadro_cargas.md): falta origem/rota do quadro para comprimentos elétricos; não confirma quadro ao lado da entrada. Caixas de costas e rasgos não estão inventariados: não se inventou perda real por caixa.
- [Reforma](../../../01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md): parede estrutural não recebe remoção/rasgos por este estudo; furos, fixações e interferências dependem de RT. Convenção arts.4/7/57 restringe intervenções; não foi encontrada autorização específica para trocar a porta. Troca de folha/conjunto, acabamento voltado ao hall e requisitos de incêndio precisam de confirmação; vedação também não pode bloquear ventilação necessária.
- **Laje maciça é hipótese**, não informação comprovada pelo memorial consultado. O acabamento sobre laje não prova seu tipo ou espessura. Quarto/sala/circulação: pintura/textura sobre laje; cozinha/lavanderia: laje e sanca; banheiro: forro de gesso. Não confundir item tipo com PCD.
- Alturas vigentes: **2,60 m**, banheiro **2,50 m**, ambas a confirmar; escritório 2,47 m é histórico substituído. [Fonte](../../../01_Programa_e_decisoes/Pesquisa_pe_direito.md). Forro novo H de 10/15 cm deixaria 2,50/2,45 m; no banheiro 2,40/2,35 m somente se fosse adicional ao teto acabado atual. Não descontar duas vezes o forro existente.
- [Dependências](../../../04_Moveis/Dependencias/README.md): 34 folgas nominais ≤15 mm, quatro negativas, algumas contra limites de referência. Contraparede de 63 mm não cabe automaticamente nessas folgas; perda de espaço precisa de nova compatibilização antes de mudar móveis. Armários previstos até o teto, luminárias, elétrica, acessos e varal não podem ser sustentados pelo novo forro sem detalhe próprio. [Iluminação](../../Iluminacao/README.md) e [móveis](../../../04_Moveis/README.md).

## Fronteiras e áreas

[Fronteiras.csv](Fronteiras.csv) inventaria cada face do modelo: cômodo, eixo/coordenada, comprimento somado dos segmentos, área bruta, vãos, área líquida, outro lado e linhas de origem. Não é planta executiva nem inventário confirmado de paredes compartilhadas. Faces com janela identificam exterior **na abertura**, sem presumir que o restante seja todo fachada. As demais ficam a confirmar; faces internas também estão incluídas para não descartar silenciosamente nenhuma parede.

| Recinto | Área líquida de todas as faces nominais, m² | Teto nominal, m² | Prioridade |
|---|---:|---:|---|
| Quarto | 30,9425 | 8,3825 | **Alta: descanso** |
| Escritório/dormitório 02 | 24,4975 | 6,7850 | **Alta: trabalho; conferir classificação original como dormitório** |
| Sala | 21,6110 | 9,1800 | Normal |
| Cozinha | 14,2705 | 5,5176 | Normal; entrada |
| Lavanderia | 9,5460 | 1,9866 | Normal; shaft a conferir |
| Banheiro | 14,7750 | 2,6616 | Normal; shaft/forro a conferir |
| Circulação | 3,2900 | 0,9450 | Acesso interno |

Fonte: [quantitativos nominais](../../Acabamentos/Quantidades_por_ambiente.csv). As alturas/vãos já contêm hipóteses desse levantamento. A soma é de faces por recinto, não área única de paredes do edifício; não somar duas faces de uma divisória como duas paredes físicas. O teste reconcilia com esta base nominal, **não verifica área real ainda desconhecida**. [Diagrama](Fronteiras.svg): cinza = déficit desconhecido, roxo = prioridade; sem falsa cor de conformidade.

## Cálculos e parâmetros explícitos

[407 cenários](Cenarios_envoltoria.csv), gerados pelo [script](../../../ferramentas/estudos/acustica_envoltoria.py). Reutiliza `base_homogenea` e `somar_niveis` do estudo anterior.

**Paredes:** quatro bases comerciais documentais, não seleção para a obra: cerâmico 14 cm Ermida 7,124 kg × 12,5 = 89,05 kg/m²; cerâmico 19 cm, índice do catálogo Ermida, 8 × 12,5 = 100 kg/m² (conferência visual da ficha pendente); concreto Tatu 14 cm/4,5 MPa: 9,53/(0,30 × 0,20) = 158,83 kg/m²; concreto 19 cm/14 MPa: 17,97/(0,40 × 0,20) = 224,625 kg/m². Junta de 10 mm é H nos dois últimos. Os produtos têm resistências/morfologias distintas: a comparação não isola efeito de espessura. Fontes BR12–BR15 em [registro](../Fontes_brasileiras.csv). Normas de produto NBR 6136 e série NBR 15270 não fornecem Rw do conjunto; edição aplicável e certificado do bloco continuam a solicitar, sem alegar confirmação atual integral dessas normas.

H-P1: acréscimo total de revestimento/assentamento **20 ou 60 kg/m²**, sem presumir gesso ou reboco real. H-P2: acréscimo de graute **0 ou 100 kg/m²**, varredura arbitrária; 100 não significa células totalmente preenchidas. Não converter esses acréscimos em espessuras reais. Assim, a massa total ensaiada analiticamente é 109,05–384,625 kg/m². O CSV identifica cada combinação.

Modelo analítico de folha flácida infinita: `R_normal=10log10[1+(π f m'/(ρ c))²]`, derivado da impedância superficial `iωm'` entre meios iguais. H-ar: ρ=1,2 kg/m³ e c=343 m/s. Não há rigidez ou amortecimento: **não é curva de bloco vazado, lei difusa nem Rw**. Frequências de terço de oitava 100 a 3150 Hz; não se deslocou curva ISO 717 para obter um índice artificial. Sharp/coincidência exige rigidez à flexão, E, ν, perdas e geometria de vazios, que faltam. Essas curvas e Rw por composição permanecem não calculados, em vez de inventados.

**Flancos:** H-F é a razão de energia marginal/direta q=0/0,25/1/3; perda `10log10(1+q)`. Não é faixa típica nem entrada ISO 12354-1. Para DnT por banda seriam necessários R' com todas as vias e geometria/reverberação; não se converteu uma curva fictícia em DnT,w. A [ISO 12354-1:2017](https://www.iso.org/standard/70242.html) requer caracterização direta/marginal; faltam Kij, comprimentos de junção e propriedades de elementos. Junções rígidas não autorizam descontar universalmente 3 ou 5 dB.

**Pontos fracos/porta:** `R_composto=−10log10[Σ(Si 10^(−Ri/10))/ΣSi]`, por banda. H-R: parede 50 dB, trechos fracos 0/10/20 dB em 0,1/1/5% da área. Não são medições de caixa, shaft ou visita. H-D: folha 20/30/40 dB constantes por banda, área 1,6 m², fresta inferior 0/1/3/10 mm com transmissão unitária. As classes H não correspondem automaticamente a semioca/maciça/segurança. Parede+porta usa área total H=10 m² e restante 50 dB, dando 26,20–46,13 dB. Essa área **não substitui os 2,4925 m² líquidos nominais da face de entrada**. Não compor Rw de catálogo pela fórmula como se fosse espectro.

Referências comerciais separadas: Multidoor publica classes Rw 21–24 até 37–40 dB; Vibrasom declara MDF 32 dB, segurança aço 30 dB e profissional aço 43/50 dB. Isso mostra que “segurança” ou “maciça” não garante maior isolamento. Falta laudo do conjunto exato com batente, guarnição, soleira e montagem. Não foram encontradas faixas comprovadas universais para porta comum maciça/semioca. Nenhum ΔR próprio atribuído a borracha, guarnição ou soleira: o ganho depende da fresta que realmente eliminam.

**Laje/teto:** H-L é laje homogênea 100/120/140 mm, densidade H 2300/2500 kg/m³. As curvas de massa usam as mesmas limitações. A equação de impacto do estudo anterior dá apenas base equivalente homogênea; não inclui piso superior, flancos ou receptor. **Rw e L'nT,w da laje do Guedala permanecem indeterminados**. Não se subtrai ΔLw de manta do ganho de forro. Pintura/textura não recebem ganho de isolamento calculável; não são opção acústica demonstrada. [Impacto do nosso piso para baixo](../Piso_e_equipamentos/README.md) permanece no estudo anterior.

**Massa-mola-massa:** `f0=(1/2π)√[(ρc²/d)(1/m1+1/m2)]`. H-M: m1=150/350 kg/m², m2=10/20 kg/m², d=0,03/0,05/0,10 m. Ar ideal e folhas desacopladas, sem amortecimento/ponte estrutural. Cavidade quadruplicada reduz f0 à metade; não é promessa de melhoria. O forro real exige suspensões e perímetro, não só lã. Knauf W625/W626 documenta contraparedes autoportantes com limite de altura; acima dele pode exigir ligação à base. O exemplo português W625 63 mm anuncia **ΔRA=14 dB(A)** e W626 ΔRA=15 dB(A), não ΔRw. PET Trisoft 50/75/100 mm é opção de absorvente, não parede/forro ensaiado. Não há ΔRw/ganho de impacto verificável para o conjunto local.

## Comparação normativa e matriz de decisão

O catálogo ABNT identifica **15575-4:2025 e 15575-3:2021**. Não houve acesso às tabelas integrais atuais nem confirmação da edição contratual. Referência histórica separada: [ProAcústica 2013, p.18](https://labeee.ufsc.br/sites/default/files/disciplinas/proacustica_manualnorma_nov_2013.pdf) reproduz DnT,w M/I/S: sem dormitório 40/45/50; ao menos um dormitório 45/50/55; dormitório versus circulação comum eventual 40/45/50; sala/cozinha versus circulação comum 30/35/40; área comum de permanência 45/50/55; entre unidades através do hall, conjunto paredes+portas 40/45/50 dB. **Não são limites de Rw de uma porta isolada nem confirmação da tabela2025.** Para impacto, referências e limites de consulta ficam no estudo anterior; valores atuais por receptor permanecem a conferir. Nenhuma folga/déficit normativo foi calculado.

| Cômodo / fronteira | Rw / DnT,w / L'nT,w real | M/I/S vigente e folga | Opção do nosso lado / espaço | Custo e responsável | Decisão que isto muda |
|---|---|---|---|---|---|
| **Quarto**, parede com unidade ou comum a localizar | Não determinados | A conferir; déficit desconhecido | Contraparede só após diagnóstico; exemplo63 mm | Cotação ausente; construtora/RT/oficina | Não reduzir roupeiro nem comprar lã agora |
| **Escritório**, parede com unidade/comum a localizar | Não determinados | A conferir como dormitório original | Mesmo critério; exemplo63 mm | Cotação ausente; construtora/RT | Proteger uso de trabalho sem alterar bancada por hipótese |
| Sala, parede com unidade/hall a localizar | Não determinados | A conferir conforme receptor | Vedação de falha comprovada; depois contraparede | Cotação ausente; RT | Nada muda na marcenaria neste estágio |
| Cozinha, entrada e demais faces | Não determinados | Conjunto via hall, não porta isolada | Conferir frestas; vedação compatível sem reduzir área útil | Vedador82 cm: oferta R$359,91, sem instalação/frete; condomínio/RT | Cotar conjunto de vedação após conferir dimensão/regras |
| Banheiro/lavanderia, shaft e faces a localizar | Não determinados | Critério depende da transmissão/receptor | Selagem técnica mantendo inspeção/ventilação | Cotação ausente; construtora/RT | Não fechar visitas ou comprar revestimento acústico genérico |
| Todos, teto e unidade superior | Não determinados | Impacto e aéreo: a conferir; déficit desconhecido | Forro desacoplado condicionado; H10/15 cm | Cotação ausente; construtora/RT/oficina | Não rebaixar armários/luminárias sem diagnóstico |
| Circulação interna | Não determinados | Não presumir parede de hall comum | Conferir continuidade de vedação | Sem compra definida | Nada muda agora |

Não existe ranking quantitativo de dB/R$ ou dB/cm sustentado. **Ordem nominal de investigação/compra condicionada:** (1) frestas da entrada — pequena ocupação e intervenção potencialmente localizada; (2) falhas documentadas de vedação/visitas — corrigir apenas com detalhe compatível; (3) contraparede apenas na fronteira comprovadamente dominante de quarto/escritório. Forro completo fica depois de identificar ruído aéreo versus impacto e caminhos estruturais. Não compensa comprar espuma/textura por promessa de bloquear vizinho, nem gastar espaço com cavidade rasa sem projeto do sistema. A verba histórica R$1.500 já inclui adaptação do piso; não foi reutilizada como saldo disponível para a envoltória. Custos ausentes não são zero.

## Pendências

[Sete perguntas exatas e destinatários](Pendencias_e_perguntas.md): construtora, condomínio, RT e fornecedores. Nenhum contato realizado.

## Arquivos, reprodução e cobertura

[Protocolo indicativo nas chaves](Protocolo_medicao.md). Sugestão apenas: linká-lo futuramente no roteiro das chaves e expor este README na biblioteca; site/roteiro não editados.

`python -B ferramentas/estudos/acustica_envoltoria.py`

`python -B -m unittest discover -s ferramentas/estudos -p test_acustica_envoltoria.py`

11 testes: impedância, massa, composição, fresta, energia marginal, ressonância, fundo, domínios, reconciliação nominal de áreas, segmentos disjuntos e exportação. Não validam a obra.

SHA256 Cenarios_envoltoria.csv: `1e0ddce829a0c6db88edc0ba8066d543c7e806e60218f389f0a68546d2b66318`.

SHA256 Fronteiras.csv: `70e60e8d7af6d58ccbe02ae61615585fe0438cc6a69473e9f943770d75b90dbb`.

[Cobertura e cálculos impedidos por dados ausentes](Pendencias_e_perguntas.md).
