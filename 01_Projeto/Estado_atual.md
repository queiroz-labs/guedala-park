# Guedala Park — estado atual

**25/10/2026.** Uma página para entender o projeto. Detalhes e histórico estão nos links; em caso de divergência, vale esta página e os documentos marcados como vigentes.

Janela noturna encerrada às07h de25/10; automação pausada. [Registro e confirmação](Execucao_ate_07h_2026-10-25.md). As propostas estruturais continuam separadas e condicionadas.

[Entrada curta de retomada25/10](Retomada_25_10_2026.md) · [matriz dos20 móveis](Cargas_e_ligacoes_R50_2026-10-25/Andamento_20_moveis.md) · [conferência leve dos arquivos](Conferencia_entrega_25_10_2026/README.md). Reúnem entregas, limites e a primeira ação de cada frente sem precisar refazer o bloco noturno.

**Publicação autorizada R52/R18:** modelo corrente R52, pacote R18 em `05_Entregas/Publicacao` e fichas R14. Consulte a execução em [GitHub Actions](https://github.com/queiroz-labs/guedala-park/actions/workflows/pages.yml) e a versão entregue no [site](https://queiroz-labs.github.io/guedala-park/) para confirmar o envio e o deploy. R49/R16 identificam a entrega anterior; R17 selado preservado. Nenhuma proposta estrutural foi incorporada por esta publicação.

**Continuidade após R52:** [avanços e pendências por dependência](Continuidade_pos_R52_2026-10-25/README.md). Concluídos54 cenários/12 equilíbrios nominais P01/P03, triagem de249 painéis e36 propostas, arranjos de210 painéis, alternativa separada300mm do micro e cinemática daR52. Restam juntas e produtos reais,39 painéis sem definição suficiente, protótipos e levantamento final; o modelo R52 permanece preservado.

## O projeto

Projeto de interiores e marcenaria de um apartamento Cury Guedala Park III (Torre 2, final 06, 8º andar, 40,18 m², dois dormitórios). **O apartamento ainda não foi entregue**, então todas as medidas são da planta oficial e ainda precisam ser conferidas no local.

**Objetivo:** mudar com tudo pronto, com dois meses de obra depois das chaves e mudança no terceiro mês.

**Verba:** R$120 mil de execução + R$10 mil de reserva intocada.

## Versões vigentes

| O quê | Versão | Abrir |
|---|---|---|
| Modelo 3D | FreeCAD R52: correções da revisão integral | [Modelo completo](Correcao_integral_R52_2026-10-25/Guedala_Park_R52_Corrigido.FCStd) · [correções e conferências](Correcao_integral_R52_2026-10-25/README.md) |
| Cargas e ligações | Estudos separados; P01/P03 com equilíbrio por painel e caminhos compartilhados | [Avanços e pendências](Continuidade_pos_R52_2026-10-25/README.md) · [P01/P03](Continuidade_pos_R52_2026-10-25/P01_P03/README.md) |
| Fichas dos 20 móveis | R14 | [Fichas](../05_Entregas/Fichas_fabricacao_R13/index.html) · [Pendências](../05_Entregas/Fichas_fabricacao_R13/Pendencias.html) |
| Programa | R01 | [Programa de necessidades](Programa_de_necessidades_R01.md) |
| Planta mobiliada e vistas | R02 | [Planta mobiliada](Planta_mobiliada/README.md) |
| Especificações | R01 | [Caderno de especificações](Caderno_de_especificacoes_R01.md) |
| Pontos (elétrica, água, gás) | R00, preliminar | [Planta de pontos](Planta_pontos_R00/README.md) |
| Cronograma de obra e compras | R00 | [Cronograma](Cronograma_obra_e_compras_R00.md) |
| Pranchas (A3, com carimbo) | R00 | [Caderno de pranchas](../05_Entregas/Caderno_pranchas_R00/index.html) · [PDF](../05_Entregas/Caderno_pranchas_R00/Guedala_Park_Pranchas_R00.pdf) |
| Conectores (P01, P04, P12, P17) | R00, proposta | [Mapa de conectores](Mapa_conectores_R00/README.md) |
| Orçamento | R43 | [Orçamento R43](Orcamento_R43_2026-10-22/Orcamento_R43.md) |
| Site e pacote | Publicação autorizada R52/R18; envio/deploy conferíveis no GitHub Actions | [Site interativo](Estudo_interativo/Guedala_Park_Interativo.html) · [pacote R18](../05_Entregas/Publicacao/Guedala_Park_R18.zip) · [versão online](https://queiroz-labs.github.io/guedala-park/) |

A R49 ([detalhes](Gavetas_escritorio_R49_2026-10-24/README.md)) corrige as gavetas do escritório sobre a R48 ([detalhes](Depurador_sem_canal_R48_2026-10-24/README.md)), que mantém tudo da R46. Na R46 o modelo traz as ferragens das fichas por móvel, a especificação de cada peça e os 52 Minifix como marcadores. Continuam fora da geometria: os furos, a forma da FGVTN 500 (sem STEP oficial) e a dobradiça piano do banco.

A R50 mantém essa geometria completa e todos os controles; muda a gravação para BREP binário. A integração local passou a ignorar eventos de restauração, preservando as edições interativas. A entrega anterior R49/R16 fica no histórico; a publicação corrente usa R52/R18 e fichas R14, preservando as condições técnicas de fabricação.

A [cinemática offline da R52](Continuidade_pos_R52_2026-10-25/Cinematica_R52/README.md) já está extraída e conferida:4 planilhas,867 células,24 folhas,66 poses nativas adicionais e528 referências preservadas;1.914 matrizes testadas. Usar a consulta numérica corrente; nova extração só se a geometria ou a cinemática-fonte mudar.

Na conferência de 25/10, foram ocultados oito objetos de referência do grupo `BC43_Referencias`, que estavam visíveis sobre o gabinete do banheiro. Fundo original, caixa e portas de correr preservados; volumes de teste continuam disponíveis no arquivo. [Registro](Otimizacao_FreeCAD_R50_2026-10-24/Banheiro_referencias_ocultas.json).

## Onde estamos

| Etapa | % | Situação |
|---|---:|---|
| Programa e estudo preliminar | 100% | Fechados; falta só validar no local |
| Anteprojeto | 75% | Faltam códigos de chapa, tons exatos e luminárias |
| Executivo de marcenaria | 45–55% | Fichas prontas; faltam montagens do banco, cesto e gavetas, furação dos conectores (proposta no [mapa R00](Mapa_conectores_R00/README.md)) e medidas reais |
| Complementares | 30% | Planta de pontos preliminar; circuitos e traçados com o responsável técnico |
| Especificações | 70% | Caderno gerado a partir dos dados do site |
| Orçamento | 60% | Cenário de R$137,8 mil para teto de R$120 mil; pacote de marcenaria pronto, **em espera** |
| Responsável técnico e aprovação | 10% | Rascunho do plano de reforma; RT ainda não contratado |
| Levantamento no imóvel | 25% | Roteiro pronto; depende das chaves |

Detalhes no [roteiro para projeto oficial](Roteiro_para_projeto_oficial.md).

## Principais decisões tomadas

- **Sustentação das chapas:** Elias não quer tubos sustentando madeira. Qualquer proposta futura exige autorização prévia. Alternativas tubulares P11/P15/bancada canceladas; priorizar apoios e ligações de marcenaria. [Decisão e inventário](Cargas_e_ligacoes_R50_2026-10-25/Decisao_sem_tubos.md).

- **Cores:** interiores Branco TX; Arenza na cozinha, lavanderia, escritório e quarto; Azul Petróleo nos aéreos da cozinha; off-white e bege foscos; Granito Branco Itaúnas; piso vinílico Olmo.
- **Sala:** sofá Bonnie; mesa Berlin pronta com três cadeiras; banco baú com duas tampas presas por dobradiça piano e articuladores com trava (nas fichas R14; protótipo pendente).
- **Quarto:** roupeiro de 65 cm de profundidade com portas de correr; queen futura; apoios de celular retirados. Luz geral com três níveis de brilho pelo interruptor; Liny caro retirado e conjunto Jurerê/SceneSwitch candidato a cerca de R$110 ([CB02](Iluminacao/Fechamento_custo_beneficio_2026-10-24/Revisao_quarto_CB02.md)).
- **Tecidos e marcenaria:** cortina da sala C2 Areia, suede areia no banco e na cabeceira, aéreo do escritório marfim claro. Códigos comerciais ainda dependem de amostra. [Imagens das luminárias](../03_Referencias/Iluminacao_CB02_2026-10-24/Galeria.md).
- **Cozinha:** forno Fischer 127 V, cooktop KE4GC a gás natural, gaveta de limpeza sobre rodízios Leão Aço.
- **Banheiro:** gabinete com portas de correr e frente removível; uma parede verde no box. Luz: teto/indireta 3000 K e espelho 4000 K, três comandos. [Componentes L02: R$612,64 à vista](Banheiro/Fechamento_pre_entrega_2026-10-24/Luminarias_selecao_L02.html); conjunto montado e instalação condicionados.
- **Ferragens:** dobradiças Blum, corrediças FGVTN 500 e MOVENTO 400 no escritório; 52 conjuntos Minifix definidos (P10, P11, P15, P19).

**P16, avanço25/10:** [curso das gavetas e estabilidade da bancada de estudo](P16_gavetas_estabilidade_2026-10-25/README.md) conferidos nominalmente: sem interseção nas caixas varridas do escopo testado;1296 cenários de equilíbrio. Ferragens telescópicas reais, juntas e massa/constituição do tampo permanecem condições de fechamento. R51 intacta.

**P04/P15, avanço25/10:** [demanda global de suspensão](P04_P15_suspensao_2026-10-25/README.md) calculada com caixas, reforços, conteúdo e portas abertas;660 casos e72 envelopes paramétricos. Produto, juntas e parede real ainda condicionam o fechamento; não há bucha ou capacidade liberada.

**P09/P11/P12/P17, avanço25/10:** [suspensão global ampliada](Aereos_suspensao_P09_P11_P12_P17_2026-10-25/README.md),1404 casos e48 envelopes. O manual do depurador60 cm informa6,00 kg e fixação à parede+gabinete; no CAD há42 mm entre o gabarito e a baseP09. Transferência de esforços e adaptação ainda não demonstradas, com posições/ventilação preservadas. O relatório contém desenho e pergunta exata de montagem; não tratar o peso como já transmitido ao aéreo.

## O que falta, em ordem

**Corte e formatos:** [249 painéis atuais e36 propostas separados](Continuidade_pos_R52_2026-10-25/Corte_e_formatos/README.md) já triados. Arranjos preliminares cobrem210 painéis;39 ainda exigem definição de produto/faces/composição. FundoP01 atual/proposto não cabe em2750×1850; a orientação útil no formato2750×2100 e os refilos foram calculados. Produto, fornecimento e direção permitida continuam pendentes; não há plano executivo ou compra liberada.

**P16, interface25/10:** [regiões guia–fundo localizadas](P16_interface_guia_fundo_2026-10-25/README.md),18 componentes positivos e quatro furos nominais conferidos. O padrão também aparece na referênciaG2 configurada. Causa funcional/regulagem e montagem individual400 continuam para confirmar, com mapa/pergunta exata; sem cortes ou alterações de movimento.

**P04, auditoria25/10:** eixos nativos conferidos e [referências esclarecidas](Solucoes_marcenaria_sem_tubos_2026-10-25/P04_auditoria_referencias.json). O estudo que mantém as chapas separadas usa agora869,5/300=2,898mm; a flecha permanece1,523mm. Rigidez1000 inicial refere-se a cada posição, e o grupo de dois corresponde a2000; o texto foi corrigido para corresponder à matriz. Caixa/fundo e caminhos compartilhados continuam condicionados.

**P15, composição25/10:** [deslizamento contínuo entre camadas](P15_composicao_parcial_2026-10-25/README.md),16 respostas e cinco conferências principais, incluindo dois limites e montagem independente dos três campos. Colagem continua sem produto/processo selecionados; TitebondMelamine foi excluída desta sustentação pela limitação expressa do fabricante. Não incorporar a base36 sem comprovar composição/juntas e revisar aparência externa.

**P01/P03:** [caixa superior e caminhos compartilhados](Continuidade_pos_R52_2026-10-25/P01_P03/README.md) já modelados nominalmente por topo/fundo/laterais/portas:54 cenários e12 equilíbrios por painel. Apoio traseiro não garante alívio da travessa; ligaçãoP02↔P03 muda a partilha. Faltam topologia/curvas/capacidades reais das juntas, chapa e detalhamento internoP02 para calcular deformação/resistência. A modelagem nominal não deve voltar como tarefa ainda não iniciada.

**P01, massas25/10:** [inventário e equilíbrio simultâneo](P01_massas_equilibrio_2026-10-25/README.md),47/7/10 madeirasP01/P03/P02, oito contatos superiores e4608 combinações aritméticas. P01+P03+soco+723 dá315,9kg a800 antes de conteúdo/acessórios; cenário mais carregado exemplificado648kg é hipótese, não uso aprovado. Área total nominal0,270720m² inclui as duas laterais originais além do soco. O equilíbrio dos caminhos superiores foi ampliado na continuidadeP01/P03; resistência/deformação das juntas, retenção e piso real continuam por demonstrar. Este inventário preserva a baseR51 de sua etapa.

**P17, avanço25/10:** [base/fundo e ligações positivas](P17_base_fundo_ligacoes_2026-10-25/README.md), estudo parcial com fundo514→550,16 contatos e58 eixos nominais. Placa18 preservada:20kg totais distribuídos dá0,863mm e frontal1,336mm com reserva, sob hipóteses explícitas de juntas/referência superior; reduzir a rigidez das juntas faz exceder a referência. Seis convergências e11 casos conferidos. Produto/caixa completa/suspensão e acabamento ainda condicionam adoção; R51 intacta.

1. **Antes das chaves** (dá para fazer agora):
   - continuar os [cálculos e ligações sem tubos](Solucoes_marcenaria_sem_tubos_2026-10-25/README.md): composição/juntas P15, tração/apoio traseiro P04, juntas reais P01/P03 a partir do modelo nominal concluído, e mecanismos/assento P20. P01 recebeu [estudo do caminho até o piso](P01_apoios_ao_piso_2026-10-25/README.md), com soco,21 contatos de face e submodelo da caixa. A [bancada recebeu estudo de apoios de marcenaria](Bancada_marcenaria_2026-10-25/README.md), sete contatos e14 verificações; constituição do tampo30, retenção e estabilidade ainda por resolver. P20 recebeu [análise do assento fechado](P20_assento_fechado_2026-10-25/README.md),18 contatos reconciliados, cinco convergências e roteiroP20/P14; painel real, juntas, massa global e protótipo seguem condicionados. Estudos separados, aparência e uso ainda por rever; sem liberação de carga de uso;
   - concluir as luminárias dos demais ambientes na [lista curta](Lista_curta_luminarias_e_madeira_R00.md); no banheiro os componentes estão selecionados e precificados em L02, faltando prova do perfil, terminações e montagem. Chapas do banheiro: Arauco Beige Matt e Louro Freijó Poro;
   - banco: provar o apoio da piano na junta do encosto e os terminais dos articuladores no protótipo; cesto: [reações3D e operação nominal calculadas](P14_reacoes_e_operacao_2026-10-25/README.md), com270 cenários e retenção vertical dos suportes identificada; fechar pivôs/buchas, juntas, limitadores a55° e retenção com componentes efetivos;
   - pedir orçamentos de marcenaria quando o pacote sair da espera;
   - contratar o responsável técnico e enviar os [e-mails preparados](Rascunhos_emails_R00.md);
   - comprar 1 dobradiça piano e 2 pares de articuladores (~R$150) para o protótipo do banco ([preços](Banco_cesto_simples_2026-10-23/Precos_e_conjunto_R01.md)).
2. **No dia das chaves:** seguir o [roteiro do dia das chaves](../04_Visita_ao_apartamento/Roteiro_dia_das_chaves_R01.md), com vistoria da Cury e medição.
3. **Depois das chaves:**
   - ajustar modelo, fichas e orçamento às medidas reais;
   - protocolar o [plano de reforma](Plano_de_reforma_NBR16280_rascunho.md);
   - contratar e executar.

Para conferir se os documentos continuam batendo entre si, rode `python 01_Projeto/verificar_consistencia.py` ([último resultado](Verificacao_consistencia.md)).

## Onde está o histórico

- [Resumo](Resumo.md) e [Painel de decisões](Painel_de_decisoes.md): registros por revisão, do mais recente ao mais antigo.
- [Registro de decisões](Registro_de_decisoes.md): histórico completo.
- **Modelos FreeCAD antigos** (R30–R44, estudos e arquivo) foram para fora do projeto em `Documents\PROJETOS\Guedala_Park_FreeCAD_antigos.zip`. Também estão no commit `1b4aeaa` do git. A lista está em `99_Arquivo/_manifesto_fcstd_zip.json`. [Como recuperar os modelos e identificar backups não localizados](../99_Arquivo/Recuperacao_modelos_FreeCAD.md).
