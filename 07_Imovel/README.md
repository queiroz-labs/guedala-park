# Visita ao apartamento — fotos e relatórios

**Pé-direito de projeto: 2,60 m = 260 cm = 2600 mm em todos os cômodos, incluindo escritório e circulação; banheiro: 2,50 m = 250 cm = 2500 mm. Medida a confirmar.** Elias, 27/10/2026, nesta conversa: “altera a altura de todos os comodos para 2,6 e o banheiro para 2,5”. Substitui o cenário anterior de 2,47 m do escritório. Alturas nominais acabadas; levantamento, forros e instalações continuam a conferir. Não autoriza fabricação nem altera automaticamente as dimensões dos móveis.

## Levantamento e impactos — T08, 26/10/2026

[Roteiro do dia das chaves](Roteiro_dia_das_chaves_R01.md) · [Medidas e arquivos afetados — CSV](Medidas_e_impactos.csv).

São **530 registros**: 173 do roteiro e verificações complementares, mais 357 entradas escalares PR da geração A3 R02. Não representam medições feitas: incluem preparação, vistoria, documentos, referências e coordenadas nominais. **Nenhum valor de campo preenchido.**

| Grupo | Cobertura |
|---|---|
| LOG, A1–A6 e POS | 38 itens originais de preparação, vistoria/documentos e pós-visita; logística marcada como não afeta o projeto |
| PD, B e DIM, GER-ID | 20 registros de alturas, prioridades, croqui e cotas oficiais com escopo preservado |
| MOV-P01…P20 | 20 móveis: vão, três alturas, prumo, rodapé, substrato e interferências |
| COMP, LAV-TEC, COZ-FAIXA/ACESSO, SAL-COND | 10 verificações de interfaces e infraestrutura |
| ANC e PISO | 8 paredes/ancoragens e 4 verificações de piso/nivelamento |
| PTO-* | 50 códigos da planta de pontos; coordenadas reais a definir pelo RT |
| OBS-* | 23 observações de outra unidade, sem correspondência presumida com PTO-* |
| PR-* | Contornos, vãos, peitoris e eixos XYZ dos pontos para as pranchas R02; nominal/planta com fonte |

Cada linha traz código, ambiente, valor nominal e sua natureza/fonte, tolerância e quem a define, Pxx, arquivos de ficha/prancha/README/orçamento e quem valida. Caminhos são relativos à raiz do repositório; `|` separa vários arquivos ou móveis. “a definir” é ausência de dado, nunca zero. Papéis de Elias, RT e oficina são indicações de validação, não contratação. `valor_medido` e `evidencia_campo` ficam vazios até a visita.

**Origens e limites:** cotas oficiais em [Cotas.json](../06_Entregas/Planta_cotada/Cotas.json) e [Medidas](../03_Ambientes/Medidas/README.md). Pé-direito 2600 mm é hipótese vigente, não cota oficial; 2470 mm do escritório é cenário separado. Roteiros R30/R41/R42 e planta de pontos baseada na R45 são referências históricas; não preencher medidas R52 a partir deles. Sensibilidade gráfica, folga nominal e resultados de estudo não viram tolerância. A lavanderia tem cota oficial 1540 mm, divergente do desenho histórico 1610 mm; conferir no local.

Os arquivos indicados são **alvos de revisão após validar o levantamento**, não mudanças já executadas. Alterar fontes e regenerar fichas/pranchas; não editar HTML/PDF à mão. O custo só muda após demonstrar efeito no escopo; reserva permanece separada.

**Retomada exata:** com acesso à unidade, preencher PD-*, DIM-*, MOV-* e os pontos PTO/OBS usando piso acabado e faces identificadas, anexando fotos/croqui. RT define tolerâncias ainda ausentes e valida infraestrutura, piso e ancoragens; oficina valida encaixe/acesso. Só depois atualizar os arquivos afetados. Sem chaves, preparar documentação do RT e instrumentos; T08 não encerra medição, aprovação profissional ou fabricação.

## Conferência pendente — iluminação de sala/jantar (20/09/2026)

- Conferir se existe conduíte aproveitável entre a caixa de comandos na entrada e a região do painel da TV. Elias não sabe se existe; não tratar como infraestrutura entregue.
- Identificar pontos do teto, alimentação disponível no painel, neutro/retornos e espaço das caixas com o eletricista; verificar viabilidade do comando escolhido antes de especificar ligações.
- Medir pé-direito, posição/altura da prateleira superior e relação com a TV para ocultar a indireta e evitar reflexos.
- Se não houver caminho viável, comparar comando sem fio na entrada; respeitar restrições de estrutura e orçamento. Estudo: [iluminação da sala](../03_Ambientes/Sala_e_jantar/Iluminacao.md).

[Voltar ao início](../README.md)

O levantamento vem do vídeo de **outra unidade, espelhada**. Registra evidências visuais e não medidas acabadas da unidade de Elias.

## Abrir os relatórios

1. [Complemento da visita — R02 (HTML)](Complemento/Complemento_da_visita_R02.html): inclui a correção de identificação dos quartos. Leia suas correções junto do relatório principal.
2. [Relatório principal — R01 (HTML)](Relatorio_da_visita_R01.html): álbum por ambiente, com legendas.
3. [Resumo visual](Resumo_visual.jpg): visão rápida das imagens selecionadas.

Os HTMLs podem ser abertos no navegador e contêm as imagens incorporadas. Versões em texto: [relatório R01](Relatorio_da_visita_R01.md) e [complemento R02](Complemento/Complemento_da_visita_R02.md).

## Fotos e apoio

- [Fotos por ambiente](Fotos/): códigos como COZ-01 e LAV-02 relacionam foto, legenda e instante do vídeo.
- [Fotos complementares](Complemento/Fotos/): imagens usadas no complemento R02.
- [Planta de referência](referencias/P01_planta_oficial.png).
- [Índice das fotos](indice_frames.json): relação entre arquivos, ambientes e horários.
- [Transcrição com horários](Complemento/Transcricao_automatica_com_horarios.txt): transcrição automática, sujeita a erros.
- `triagem/` e as pastas de apoio do complemento guardam quadros e imagens de seleção.

**Histórico:** relatório R00 em HTML e texto R00. Use R01 com as correções de R02 para continuar. Os códigos dos quartos nas fotos foram mantidos para rastreabilidade; a identificação corrigida está no complemento.

O vídeo original do apartamento espelhado (`Video_Apartamento_Espelhado.mp4`, somente no PC, fora do Git/site) foi recuperado da pasta antiga na unificação de 25/09/2026. Os pacotes originais dos levantamentos também foram preservados. Vídeos e ZIPs continuam fora do Git e estão disponíveis nesta pasta local.

**Uso no caderno R02:** PD-* alimenta o teto por ambiente; DIM-* fornece as cotas compostas oficiais (exemplo de preenchimento: `2450 × 2950 mm`), sem segunda linha numérica para a mesma cota. PR-* fornece as coordenadas escalares. [Guia de regeneração e teste](../06_Entregas/Caderno_pranchas/README.md). Os campos de vistoria PTO/OBS não substituem as coordenadas PR-PONTO.
