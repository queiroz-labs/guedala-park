# Ensaios de oficina

Pacote preparado em 28/10/2026 a pedido de Elias nesta conversa. **Todos os ensaios: pendente de execução.** Nenhum valor medido, foto de ensaio, compra ou contato externo foi produzido. Modelo FreeCAD preservado.

[Caderno único: procedimentos, compras e mensagem](Caderno.md) · [Registro único de medições](Registro.csv) · [Verificador](../../ferramentas/estudos/verificar_ensaios_oficina.py).

Entregar esta pasta com os documentos de origem abaixo, mantendo os caminhos relativos. O caderno é a ordem de serviço para preparação e orçamento. Onde faltam produto, corte, furação ou protocolo, ele identifica o bloqueio: não é possível prometer execução integral imediata sem essas definições. “Não depende do apartamento” não significa que já tenha ferragens e protocolo fechados.

## Levantamento e decisão que cada ensaio atende

| Ensaio | Móvel | O que decide | Documento de origem | Depende de medida do apartamento? |
|---|---|---|---|---|
| E01 — identificação e pesagem | Todos os protótipos | Material, espessuras e componentes reais que serão ensaiados | [Dados para fornecedor/oficina](../Cargas_e_ligacoes/Dados_para_fornecedor_e_oficina.md), BC01/BC02 do [banco/cesto](../P20/Assento_fechado/Roteiro_banco_cesto.md) | Não |
| E02 — acesso T0 | P04 | Se a chave entra, gira e sai nos quatro Minifix | [Retalhos](../Aereos_suspensao/P04_retalhos_T0.csv), [roteiro](../Aereos_suspensao/P04_roteiro_validacao.txt), [registro original](../Aereos_suspensao/P04_registro_laboratorio.csv) | Não |
| E03 — juntas T1 | P04/P15 | Comportamento das ligações reais, sem presumir rigidez | [Roteiro de juntas](../Ligacoes_sem_tubos/Roteiro_ensaios_e_requisitos.md), [P04](../Aereos_suspensao/P04_roteiro_validacao.txt) | Não |
| E04 — suporte T2 e caixa T3 | P04 | Montagem, retenção e caminho entre caixa e suspensores | [Suspensão P04/P15](../P04/Suspensao_P04_P15/README.md), [casos T2](../Aereos_suspensao/P04_casos_qualificacao.csv) | Não, em dispositivo de oficina |
| E05 — qualificação de suspensão | P12 | Montagem do suporte, acesso e caixa completa | [Qualificação P12](../Aereos_suspensao/P12_qualificacao_suspensao.txt) e [seis casos](../Aereos_suspensao/P12_qualificacao_suspensao.csv) | Não, em dispositivo de oficina |
| E06 — qualificação de suspensão | P17 | Montagem do suporte, acesso e fundo inteiro proposto | [Qualificação P17](../Aereos_suspensao/P17_qualificacao_suspensao.txt) e [seis casos](../Aereos_suspensao/P17_qualificacao_suspensao.csv) | Não, em dispositivo de oficina |
| E07 — composição e caixa | P15 | Processo de união das duas chapas e comportamento da base | [Roteiro comparativo](../Ligacoes_sem_tubos/Roteiro_ensaios_e_requisitos.md), [composição](../P15/Composicao_parcial/README.md) | Não |
| E08 — banco | P20 | Apoios, piano, trava, manutenção e assento fechado | B01–B06 do [kit existente](../P20/Assento_fechado/Roteiro_banco_cesto.md), [montagem](../P20/Assento_fechado/Montagem_prototipo.svg) | Não, em piso de ensaio |
| E09 — cesto | P14 | Pivô, trava, abertura e retirada do saco/armação | C01–C04 do [kit](../P20/Assento_fechado/Roteiro_banco_cesto.md), [sequência](../P14/Reacoes_e_operacao/README.md), [oito registros](../P14/Reacoes_e_operacao/Registro_montagem.csv) | Não, com gabarito hidráulico |
| E10 — rodas, curso e retirada | P08 | Contato das seis rodas, guia e batente removível | [P08](../P08/README.md), [kit escolhido](../../03_Ambientes/Cozinha/Rodizios_gaveta/Selecao.md) | Não, em piso de ensaio |
| E11 — gavetas e estabilidade | P16 | Engates, interferências, massa do tampo e união da bancada | [Estabilidade](../P16/Gavetas_estabilidade/README.md), [guia/fundo](../P16/Interface_guia_fundo/README.md) | Não, em dispositivo de oficina |
| E12 — gavetas e frentes | P01/P06 | Caixa 500, engates, ajuste e manutenção das sete gavetas | [Inventário](../Inventario_dimensional/Gavetas/README.md), [frentes](../Inventario_dimensional/Gavetas/Fixacao_frentes.md) | Não |
| E13 — juntas e apoios complementares | P01/P09/P11/P15 | Fixação representativa e retenção, sem generalizar resultado de outro móvel | [Dados de oficina](../Cargas_e_ligacoes/Dados_para_fornecedor_e_oficina.md), [apoio da caixa](../Aereos_suspensao/Roteiro_apoio_caixa.txt), [corpos de prova](../Aereos_suspensao/Corpos_prova_fundo_laterais.csv) | Não |
| A01 — instalação final | Todos | Piso, parede, ancoragens, teto, instalações e folgas reais | [P04/P15](../P04/Suspensao_P04_P15/README.md), [P08](../P08/README.md), [P16](../P16/Gavetas_estabilidade/README.md), [banco/cesto](../P20/Assento_fechado/Roteiro_banco_cesto.md) | **Sim — após as chaves** |

Preparar agora E01–E13; a oficina executa somente a etapa cujos pré-requisitos estiverem fechados. A01 fica separado. “Executar agora” neste pacote significa preparar documentos e verificar o registro por software; não houve execução física.

## Uma única entrada de resultados

O preenchimento corrente deste pacote é somente em `Registro.csv`. Os formulários `Registro_ensaio.csv` do P20, `Registro_montagem.csv` do P14 e `P04_registro_laboratorio.csv` ficam como fontes de rastreabilidade, sem preenchimento paralelo. Os roteiros antigos conservam detalhes técnicos; sua função de agenda e entrada de resultados é substituída por este caderno. Não foram apagados porque continuam referenciados por desenhos e verificadores do projeto.

Rodar na raiz: `python -B ferramentas/estudos/verificar_ensaios_oficina.py`. Para uma cópia preenchida: `python -B ferramentas/estudos/verificar_ensaios_oficina.py CAMINHO_DO_CSV`.

O programa só confere integridade e completude documental: **sem dados**, **dados incompletos** ou **dados completos — revisar com RT** por ensaio. Não avalia resistência ou autenticidade da medição. Códigos de saída: 0 leitura válida; 1 dados incompletos; 2 arquivo/esquema inválido. “Sem dados” não é erro de formato.

## Entrega e privacidade

Usar cópia privada para dados da oficina, laudos assinados e fotos. No repositório público, manter o modelo vazio; qualquer incorporação futura exige retirar dados pessoais e metadados identificáveis. Registrar operador por código, sem telefone/e-mail. Não incluir arquivo G2 personalizado no pacote público.
