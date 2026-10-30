# Visita ao apartamento — fotos e relatórios

**Pé-direito de projeto: 2,60 m = 260 cm = 2600 mm em todos os cômodos, incluindo escritório e circulação; banheiro: 2,50 m = 250 cm = 2500 mm. Medida a confirmar.** Elias, 27/10/2026, nesta conversa: “altera a altura de todos os comodos para 2,6 e o banheiro para 2,5”. Substitui o cenário anterior de 2,47 m do escritório. Alturas nominais acabadas; levantamento, forros e instalações continuam a conferir. Não autoriza fabricação nem altera automaticamente as dimensões dos móveis.

## Levantamento e impactos — T08, 26/10/2026

[Checklist de vistoria](Checklist_vistoria_dia_das_chaves.md) · [Folha de medidas](Roteiro_dia_das_chaves_R01.md) · [Medidas e arquivos afetados — CSV](Medidas_e_impactos.csv).

São **532 registros** no índice atual de levantamento, incluindo verificações e coordenadas PR da geração A3 R02. Não representam medições feitas: incluem preparação, vistoria, documentos, referências e coordenadas nominais. **Nenhum valor de campo preenchido.**

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

O CSV vincula código, ambiente, fonte, tolerância, móveis e arquivos a revisar; caminhos relativos à raiz, `|` separa vínculos. “a definir” não é zero. Papéis de RT/oficina não indicam contratação. Campos reais continuam vazios.

**Origens e limites:** cotas oficiais em [Cotas.json](../06_Entregas/Planta_cotada/Cotas.json) e [Medidas](../03_Ambientes/Medidas/README.md). Pé-direito 2600 mm é hipótese vigente, não cota oficial; 2470 mm do escritório é cenário separado. Roteiros R30/R41/R42 e planta de pontos baseada na R45 são referências históricas; não preencher medidas R52 a partir deles. Sensibilidade gráfica, folga nominal e resultados de estudo não viram tolerância. A lavanderia tem cota oficial 1540 mm, divergente do desenho histórico 1610 mm; conferir no local.

Os arquivos indicados são **alvos de revisão após validar o levantamento**, não mudanças já executadas. Alterar fontes e regenerar fichas/pranchas; não editar HTML/PDF à mão. O custo só muda após demonstrar efeito no escopo; reserva permanece separada.

**Retomada exata:** com acesso à unidade, preencher PD-*, DIM-*, MOV-* e os pontos PTO/OBS usando piso acabado e faces identificadas, anexando fotos/croqui. RT define tolerâncias ainda ausentes e valida infraestrutura, piso e ancoragens; oficina valida encaixe/acesso. Só depois atualizar os arquivos afetados. Sem chaves, preparar documentação do RT e instrumentos; T08 não encerra medição, aprovação profissional ou fabricação.

## Pipeline de medidas no dia das chaves

### Importar o JSON do celular

Exportar `Medidas_reais.json` para fora do git e executar, na raiz:

```powershell
python -B ferramentas/estudos/medidas_do_celular.py --entrada C:/Temp/Medidas_reais.json --saida C:/Temp/Impactos
```

Saída nova/vazia e externa: `Importacao.md`, `campo.csv` (só cotas preenchidas com unidade e DIM completo) e `Cadeia/` com `Cadeia.md`, `Impacto.md`, `Pecas_diferencas.csv` e `Pendencias_propagacao.csv`. O resumo mostra peças, folgas e pendências. PR-* só passa com datum confirmado por seção; sem vínculo, cota vazia e evidência preservada. Só as duas colunas de campo do índice são importadas; CAD, fichas e orçamento vigentes permanecem. Pontos/panos PR ficam recolhidos por cômodo; MOV/ANC/PISO/COMP são anotações.

Para teste fictício, fornecer `--csv C:/Temp/Copia_medidas.csv`, cópia externa do índice; a trava impede fixture no CSV real. Importador isolado: `importar_medidas_site.py --entrada <json> --csv <copia> --relatorio <md> --campo <csv externo>`. Teste integrado: `python -B ferramentas/estudos/test_importar_medidas_site.py`, incluído em `verificar_site.py`.

**Preparado, sem levantamento real.** O [script](../ferramentas/estudos/medidas_chaves.py) gera diferenças, semáforo, vínculos com cotação e perguntas. O [modelo CSV](../ferramentas/estudos/modelos/medidas_reais_modelo.csv) contém **562 códigos vazios**: 532 do índice fonte, 15 parâmetros da folha prioritária, 14 auxiliares de piso/esquadro do motor existente e BOX-VERDE, suplemento para a divergência documentada em [Acabamentos](../03_Ambientes/Acabamentos/README.md). Não são medições realizadas.

Os **15 primeiros seguem exatamente a ordem do roteiro vigente/Ranking_15**, por variância explicada; o restante conserva a ordem do índice fonte e depois os complementos. O roteiro atual não documenta uma caminhada espacial completa: não foi inventada. Descrições físicas pendentes continuam indicadas; não converter leitura absoluta do laser em deslocamento da parede sem marcos comuns.

### Uso no dia

Ativar o Python local com `. ..\ferramentas_locais\ativar.ps1`, na raiz. Guardar medidas e fotos **fora do git**, na saída externa. O comando sem entrada produz o diagnóstico de ausência; não preenche zero nem usa a fixture como visita real.

```powershell
python -B ferramentas/estudos/medidas_chaves.py --gerar-modelo
Copy-Item ../outputs/Codex_cotacao_e_chaves/medidas_reais_modelo.csv ../outputs/Codex_cotacao_e_chaves/Medidas_reais.csv
# Preencher a cópia externa, sem alterar o modelo do repositório.
python -B ferramentas/estudos/medidas_chaves.py --entrada ../outputs/Codex_cotacao_e_chaves/Medidas_reais.csv
python -B ferramentas/estudos/test_medidas_chaves.py
```

Não repetir `Copy-Item` sobre a cópia já preenchida. Saída padrão: `../outputs/Codex_cotacao_e_chaves/`. `--saida` aceita outra pasta externa e rejeita o repositório. Usar `-B`; em sandbox com temporário bloqueado, apontar TEMP/TMP para uma pasta externa autorizada antes dos testes.

CSV UTF-8 com separador `;`: **codigo_medida, descricao, valor_nominal, unidade, valor_medido, data_hora, foto/arquivo, obs**. Só preencher as últimas quatro colunas; pode trocar unidade mm/cm/m junto com o número. O nominal da análise vem da fonte, nunca da coluna editável. Ex.: 2598 em mm, ou `2,598` em m; cotas compostas: `1290 x 1540` em mm, na ordem da fonte. Data/hora ISO, exemplo `2026-10-29T10:00:00`; preservar a data real da visita. Códigos desconhecidos/duplicados, eixos incompletos, unidades incompatíveis, negativo em dimensões, não finitos e data inválida são rejeitados. Vazio é sem medida; não é zero. Zero é válido para deslocamento, piso e desvio angular, não para altura/largura.

Linhas `texto` são verificações compostas/qualitativas: descrever em valor_medido/obs e anexar evidência; o motor não extrai cotas de texto livre. Use PD/DIM/PR para os valores numéricos relacionados. Fotografar e identificar os pontos/posições; as várias alturas de um móvel ou leituras de teto precisam de croqui/fotos, não de média automática. A entrada aceita subconjunto dos códigos: os omitidos ficam sem medida.

### Tolerâncias e datum

[Tabela editável de trabalho](../ferramentas/estudos/modelos/Tolerancias_trabalho.csv): **hipótese de trabalho — a confirmar com RT/oficina**. Fonte: **referência usual, não verificada**, sem norma invocada. A tabela é triagem de diferença absoluta em relação ao nominal, não aceitação de obra nem tolerância de fabricação.

| Família | Ok até | Atenção até | Acima |
|---|---:|---:|---|
| PD | 0 mm | 5 mm | revisar |
| DIM, PR e deslocamento de parede | 2 mm | 5 mm | revisar |
| Ângulo de parede/desvio absoluto de esquadro | 0,1° | 0,3° | revisar |
| Piso/prumo da cozinha | 1 mm | 3 mm | revisar |

**Qualquer diferença de teto exige rever encontro/arremate**, mesmo em atenção. Para diferença bruta sem hipótese: acrescentar `--modo bruto`; sem tolerância nunca vira ok, mesmo delta zero. Para tolerâncias próprias: `--tolerancias caminho_externo.csv`, com as colunas do modelo (codigo_medida, unidade, ok_ate, atencao_ate, natureza, fonte, quem_confirma). A tabela própria **substitui integralmente** a hipótese; códigos omitidos ficam sem tolerância. Código exato prevalece sobre padrão com `*`; manter uma única regra por família. Unidade da tabela deve corresponder à unidade interna mm/grau, não à unidade escolhida no formulário.

PR/PAREDE sem `--datum arquivo_externo.txt` só têm diferença bruta e alerta; suas coordenadas não são aplicadas na geometria. O arquivo deve documentar M0/M1/E1/E2, direção, faces e transformação para o datum nominal; o script registra seu hash, **não valida a transformação**. Descrição física pendente continua alerta. PAREDE-DESLOCAMENTO é avanço normal assinado já convertido, não distância absoluta; PAREDE-ANGULO é rotação derivada. CAMPO-*-ESQUADRO é desvio absoluto de 90°, não o ângulo total. CAMPO-*-PISO é elevação desde o piso de referência; não descontar novamente se PD já usa o ponto alto.

### Resultados e limites

- `Relatorio_medidas.md`: semáforo por ambiente, o que muda em obra/marcenaria/compra, perguntas e códigos sem medida. `Relatorio_medidas_celular.md`: consulta compacta de uma página, com remissão ao detalhe.
- `Impactos_medidas.csv`: delta em mm/grau, classificação, móveis/fichas/pranchas, origem, evidência e responsável a consultar. Sem nominal numérico fica atenção. BOX-VERDE compara 800×2250 mm e registra também delta contra 1240×2470 mm; calcula área do retângulo, sem escolher parede, altura ou descontar a compra. O teto vigente do banheiro continua 2500 mm.
- `Impactos_geometria.json`: reaproveita `04_Moveis/Dependencias/orquestrar.py` e `ferramentas/medidas/recalcular.py`. Só lista relações tocadas pelas entradas; mostra folgas remanescentes e quais bases continuam nominais. Caixas fixas permanecem fixas; referências e nove fechamentos não são peças de corte. Conflito geométrico agrava o semáforo para revisar, inclusive se uma base nominal participar. Ausência de conflito não comprova tolerância nem carga.
- `Pecas_afetadas.csv`: lista somente painéis dos móveis atingidos por diferença numérica, com C/L atuais, C/L revisados vazios e indicação **reabrir corte do móvel Pxx**. Falta vínculo executivo medida→eixo/ID para deduzir novo blank: não inventar dimensões nem regenerar plano vigente. Juntas, ferragens, recortes, fitas e compras continuam sujeitos à revisão indicada.
- `Linhas_dependentes_medidas.csv`: cruzamento das 101 linhas da cotação com móveis e códigos de medida. Usa inventários de painéis, fita e ferragens para agregados; quando o vínculo não é suficiente, marca precaução sem ratear preço. **42.469 vínculos** externos não significam 42.469 compras ou novas medidas. Campos logísticos/pós-visita não entram. Condiciona preço à medida real, sem alterar orçamento.
- `Perguntas_RT.csv`: lavanderia 1540/1610, box/forro, porta sem largura documental, teto/arremates, prumo/esquadro, TV/conduíte, tampas cegas do quadro e datum/regras do condomínio. `Manifesto_medidas.json` guarda hashes de fontes, entrada, datum, tolerâncias e resultados.

Integração com o [comparador](../05_Orcamento_e_cronograma/Orcamento/Cotacoes/README.md):

```powershell
python -B ferramentas/estudos/comparador_cotacoes.py --data 2026-10-29 --dependencias ../outputs/Codex_cotacao_e_chaves/Linhas_dependentes_medidas.csv
```

No uso real, acrescentar `--entrada` da proposta normalizada e atualizar a data. As fontes de campo, decisões, CAD, base, fichas, corte e orçamento permanecem preservadas. Oito testes **FICTÍCIOS** passaram; cobrem tolerância dentro/fora, sem tolerância, ausência, unidade, decimal, código/duplicação, propagação ao P01, lavanderia e box. Nenhum teste representa visita real.

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

HTMLs com imagens incorporadas. Textos: [relatório R01](Relatorio_da_visita_R01.md) e [complemento R02](Complemento/Complemento_da_visita_R02.md).

## Fotos e apoio

- [Fotos por ambiente](Fotos/): códigos como COZ-01 e LAV-02 relacionam foto, legenda e instante do vídeo.
- [Fotos complementares](Complemento/Fotos/): imagens usadas no complemento R02.
- [Planta de referência](referencias/P01_planta_oficial.png).
- [Índice das fotos](indice_frames.json): relação entre arquivos, ambientes e horários.
- [Transcrição com horários](Complemento/Transcricao_automatica_com_horarios.txt): transcrição automática, sujeita a erros.
- `triagem/` e as pastas de apoio do complemento guardam quadros e imagens de seleção.
- [Vídeo do apartamento mobiliado](Mobiliado/README.md): 51 quadros catalogados (códigos M-…), medidas relatadas pelo morador e o que ele responde das lacunas do vazio.

**Histórico:** relatório R00 em HTML e texto R00. Use R01 com as correções de R02 para continuar. Os códigos dos quartos nas fotos foram mantidos para rastreabilidade; a identificação corrigida está no complemento.

Vídeos/ZIPs originais ficam apenas no PC, fora do Git/site.

**Uso no caderno R02:** PD-* alimenta o teto por ambiente; DIM-* fornece as cotas compostas oficiais (exemplo de preenchimento: `2450 × 2950 mm`), sem segunda linha numérica para a mesma cota. PR-* fornece as coordenadas escalares. [Guia de regeneração e teste](../06_Entregas/Caderno_pranchas/README.md). Os campos de vistoria PTO/OBS não substituem as coordenadas PR-PONTO.

Folha: 15 prioridades; [546 códigos e descrições pendentes](../04_Moveis/Dependencias/Descricao_fisica.csv).

Levantamento dos panos no roteiro: duas visadas com distância e azimute desde M0/M0→M1, a1m do piso; não são duas perpendiculares a partir do mesmo ponto. Identificar M0/M1/E1/E2 e vinculá-los ao datum nominal antes de converter a reta para deslocamento normal assinado/ângulo no CSV da cadeia. Vínculo pendente.

**Datum proposto:** [folha de uma página](Roteiro_dia_das_chaves_R01.md#protocolo-de-datum--proposto), antes das prioridades. **Pergunta exata:** quais faces/marcos físicos correspondem à origem (0,0), ao sentido +X da planta e ao PR-EIXO-X nominal de 7400 mm, e que transformação leva M0 junto à entrada/M0→M1 paralelo à fachada a esse referencial? Até demonstrar o vínculo, PR-* não deve alimentar a cadeia.
