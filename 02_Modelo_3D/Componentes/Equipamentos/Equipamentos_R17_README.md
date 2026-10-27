# Equipamentos, nichos e reservas — R17

14/10/2026. Apartamento atual, incorporando integralmente R16 e anteriores. Duas correções geométricas documentadas; soluções simples preservadas. **Estudo: sem corte, furação ou compra liberados.** Medidas de parede/pedra/equipamentos continuam referências, não levantamento da unidade.

## Correções aplicadas

**ME23P:** `Peca351` tinha 452 mm de profundidade, incorporando a folga traseira de 100 no corpo preto. O guia oficial, página PDF 5, informa corpo **461 L × 290 A × 352 P**. Corrigido para 352, mantendo frente Y6548 e base Z1550. Corpo termina em Y6900; os 100 até parede Y7000 passam a ser uma reserva separada. O apoio continua 697 × 470, com 18 mm à frente do envelope. Pés, porta aberta, suporte/carga e cabos não foram validados.

**PE12G:** modelo vigente preservado; PE11X e seu manual são históricos. O [manual PE12 arquivado](Fontes/Electrolux_PE12_Manual_251021JAXM.pdf), página PDF 5/impresso 4, pede 50 mm em cada lado, 100 atrás e 220 acima. Dimensões 160 × 350 × 420 constam na página PDF 10/impresso 9.

A R16 tinha traseira Y6950: apenas 50 até a parede e **30 até a rodabanca Y6980**. A primeira proposta de avançar50 dava100 até parede, mas a reserva de ar ainda intersectava a rodabanca `Peca141`; resultado preservado em [Conferencia_pre_rodabanca.json](Conferencia_pre_rodabanca.json). Proposta final: **avançar70 no total**, frente Y6460/traseira Y6880, deixando **100 até rodabanca e120 até parede**. O aparelho termina540 da parede,90 antes da borda da pedra630. X, altura920 e modelo preservados. Reserva superior termina1490,42 abaixo do apoio do micro em1532; iluminação/suportes reais não foram acrescentados. Conexões, estabilidade, enchimento, calor e exemplar real pendentes.

Uma envoltória contínua da translação proposta do PE12G e os dois corpos corrigidos ficaram sem interpenetração no subconjunto de255 obstáculos explicitamente registrado. A posição não foi escolhida removendo obstáculos. Somente essas duas geometrias herdadas mudaram.

## Resultado dos equipamentos e aéreos

| Conjunto | Conferência desta revisão | Pendência que permanece |
|---|---|---|
| ME23P / B / apoio aberto | Corpo corrigido352;100 traseiros separados;24 reservas globais incluem o micro. Os100 superiores escolhidos permanecem; a reserva300 do manual intersecta baseB e suas duas frentes | Divergência100/300 não resolvida; não compensar com laterais abertas, nem alterar B/C ou modelo automaticamente. Pés, porta, carga, fixação, tomada/circuito e alcance reais |
| PE12G | Manual exato arquivado/inspecionado; proposta70 para deixar100 atrás até rodabanca; quatro reservas livres no subconjunto estacionário | Água/pressão, tomadas/cabos, mão/garrafa, proteção das superfícies, proximidade do calor e tolerâncias reais |
| IB6S / A | Reservas100 dos lados/traseira/topo sem hits no subconjunto; topo do aparelho1866 e baseA1966 dão100 nominais | Portas/gavetas e retirada reais, acabamentos, nivelamento/pontos e parede real. Os100 exatos não incluem tolerância extra. A largura801 do módulo não autoriza painéis invadindo a reserva inferior |
| LG CV5012PC4 | Corpo600×850 e envelope até porta fechada620, rearY6900/reserva100. Reservas laterais20/topo5 sem hits no subconjunto. Pedra inferior900 deixa50 sobre aparelho850,45 além do mínimo5 antes de nivelamento | Pedra com apoio independente, pés/mangueiras/manutenção/vibração e abertura real. Manual exige isolamento850×600 com alumínio voltado ao forno se proximidade inevitável; material/espessura/implantação não definidos. Lateral de MDF não foi homologada como isolamento |
| Venax / KE4GC | Mantido módulo600/pedra630/topo920. Relida precedência em Corte_coccao: corpo485×560×570 versus envelope517×615×610, Venax3cm laterais/5 atrás versus10 em toda volta; condição conservadora b+d≤110mm | O volume único do forno tem traseira15 da parede, não os50 do cenário documental. Não representa corpo/frente instalados. d inferior real do KE4GC, grampos, datums/apoio, GN, ventilação inferior380×450 e passagens30 pendentes. Não modificar posição/rodapé para fingir atendimento |
| Suggar DE61IX / D | Manual REV.0025 inspecionado: nicho603×137×305; produto600×176×300,488 aberto. D externo650 deixa614 entre laterais. Eixos de cooktop/depurador/D coincidem em4180 no gabarito | Vão favorável em largura não fecha montagem. Topo do aparelho1916/baseD1958 têm42 sem conexão definida. Base/tampoD inteiros; canal196×178 não atravessa esses painéis nem mostra entrada/saída. Retorno20 por largura, fixação/abertura de filtro e distância real à superfície de cocção ainda não projetados |
| RI9252/91 | Guarda cotidiana na lavanderia mantida; reservas100 atrás/lados/acima sem hits no subconjunto | Uso temporário no preparo conforme programa, sem nova decisão ou movimento aplicado aqui. Vapor/gaveta/cabo/tomada/água/pessoa e distância do calor não provados; ausência de interpenetração não autoriza operar em nicho |
| E21 / aéreo lavanderia / varal | Reserva lateral200 recomendada intersecta parede `Peca043` à esquerda e lateral/base do aéreo `Peca359`/`Peca362` à direita. Corpo350 ocupaX2620–2970; parede livre começa2550/aéreo3020:70 e50, insuficientes para referência200 | Faixa470 não acomoda envelope lateral750 nessa mesma altura. Posição/pontos reais, apoio incombustível, duto/terminação/ventilação, roupa/varal e manutenção precisam implantação conjunta. Não deslocar instalações desconhecidas ou avançar varal à cozinha |

E21: manual informa corpo483 alto e chaminé Ø60. O CAD herdado usa envelope530 e duto quadrado80. Foram identificados como **gabaritos com datums/conexões indefinidos**, mantidos para não encurtar reservas sem informação. Não são aparelho/duto reais. A referência frontal600 usada no estudo é apenas limite inferior da distância ideal **maior que600** da figura3; não define caixa permitida. O manual proíbe montagem sobre madeira mesmo isolada. Ripado decorativo não resolve essas condições.

## Escopo e limites da conferência

[Conferencia_R17.json](Conferencia_R17.json) registra24 caixas documentais de ar/acesso contra255 obstáculos: paredes inteiras, volumes importados, painéis atuais dos módulos selecionados e frentesR10 fechadas. O grupo `ReferenciasEquipamentosR17` inicia oculto; mostrar caixas individualmente. Referências não são peças de compra/corte ou capacidade de ar demonstrada.

Há três reservas com conflito no resultado final: acima300 do micro e as duas laterais200 do E21. Outros21 volumes sem hits neste subconjunto **não homologam aparelhos**. Os equipamentos foram excluídos da lista de obstáculos desta auditoria de marcenaria; ela não testa interação térmica entre equipamentos, ferragens detalhadas, todos os novos componentes do cesto, dutos/conexões reais, molduras/pessoas, portas/gavetas dos aparelhos ou fluxo de ar. Corpos e percurso do PE12G foram verificados separadamente. Não contar contato de apoio na pedra como interpenetração.

R17 salva/reaberta: correções persistiram, caixas novas válidas, nenhuma expressão inválida. Comparação com R16 identifica somente `Peca351.Width` e `Peca140.Placement` diferentes nas geometrias herdadas; hash do arquivoR16 permaneceu igual. Controles anteriores foram apenas lidos no estado salvo, sem reexecutar seus movimentos. [Reabertura_R17.json](Reabertura_R17.json).

Vistas estáticas inspecionadas: [micro/purificador](MicroPurificador_R17.png), [E21/lavanderia](E21Lavanderia_R17.png), com arquivosFCStd correspondentes. Laranja representa reservas documentais; transparência só nas vistas, para enxergar obstáculos. As vistas não acrescentam dimensionamento de instalação.

## Fontes e sequência

Decisões cruzadas antes das alterações: Aparelhos_R03, corte de cocção, micro/C2, E21/varal, incluindo F108/F109 e [organização da bancada](../../../03_Ambientes/Cozinha/Detalhamento_dimensional.md). Documentos iniciais de PE11X, E15 e LG branca não substituem escolhas posteriores. Correspondência dos manuaisIB6/LG com variantes inox foi registrada em27/09, não repetida como nova consulta do suporte nesta rodada.

[Referencias_documentais.json](Fontes/Referencias_documentais.json) contém caminhos, hashes e páginas consultadas dos PDFs. PE12 foi obtido da [fonte oficial](https://api.electrolux-medialibrary.com/asset/2766b234-544a-4587-b0e8-7545af48356c/E4RM3Q/251021JAXM/PDF/251021JAXM.pdf); páginas de instalação de PE12, Suggar, LG e E21 e tabelaME23P renderizadas/inspecionadas. Manuais locais têm versões identificadas; não se alega que todos são a edição comercial mais recente.

Scripts desta pasta são etapas executadas, não instalador único: conferir_equipamentos → corrigir_rodabanca → reabrir_e_conferir → criar_vistas → renderizar_vistas. Preservam primeira falha eR16. Não reconstruir R17 nem repetir testes prontos sem mudança.

Próximo trabalho: [fechamento preparado](Fechamento_manha_R17.md) e [pendências dos20 módulos](Pendencias_apartamento_R17.md). Prioridade continua ferragem comum/manutenção simples. Restam dados documentais/comerciais/estruturais/físicos descritos nesses arquivos; não substituir informação ausente por repetição de poses. Nada foi enviado a fornecedores, comprado ou liberado para execução.
