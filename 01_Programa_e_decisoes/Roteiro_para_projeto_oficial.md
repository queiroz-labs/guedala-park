# Roteiro para projeto oficial de arquitetura de interiores

24/10/2026. Diagnóstico documental: compara o material existente com as etapas de um projeto de interiores assinado (NBR 13532 e fluxo usual CAU). Nenhum CAD, ficha ou orçamento foi alterado. Revisão de coerência em 24/10/2026: marcados os itens já feitos (site corrigido e publicado, README de entregas, códigos do banheiro, P08, P20 e Minifix).

## Situação geral

- **Conteúdo técnico de marcenaria:** cerca de 55–60% do caminho até um executivo completo. Detalhamento acima da média: 20 módulos com peças, furações e ferragens selecionadas.
- **Camada oficial** (responsável técnico, pranchas normatizadas, complementares, aprovação do condomínio): cerca de 0–10%.
- **Bloqueio principal:** as medidas reais do apartamento. Todas as cotas continuam nominais e o pacote não libera fabricação.

## Situação por etapa

| Etapa | % estimado | Evidência | Falta |
|---|---|---|---|
| Programa de necessidades | 100% | [Programa de necessidades R01](Programa_de_necessidades.md) | Validar uso no local após as chaves |
| Levantamento do imóvel | 25% | [Medidas](../03_Ambientes/Medidas/README.md), [visita](../07_Imovel/README.md) (unidade espelhada) | Vistoria completa após as chaves |
| Estudo preliminar | 100% | [Planta mobiliada R02 e vistas](../03_Ambientes/Planta_mobiliada/README.md), site 3D | Validar no local (os 4 textos desatualizados do site foram corrigidos e publicados em 24/10) |
| Anteprojeto | 75% | [Modelo vigente R52](../02_Modelo_3D/Guedala_Park_R53_Decisoes.FCStd), [acabamentos](../ferramentas/site/fabrication/Decisao_acabamentos_R13.md) | Códigos de chapa (o banheiro já tem Arauco Beige Matt e Louro Freijó Poro, 24/10), off-white exato, amostras |
| Executivo de marcenaria | 45–55% | [Fichas R15](../06_Entregas/Fichas_fabricacao/index.html), [Pendências](../06_Entregas/Fichas_fabricacao/Pendencias.html) | Ver item 4 |
| Complementares | 30% | [Planta de pontos preliminar R00](../03_Ambientes/Planta_pontos/README.md): 50 pontos de elétrica, luz, água, esgoto e gás | Circuitos, traçados e assinatura do RT |
| Pranchas formais | 45% | [Caderno de pranchas R00](../06_Entregas/Caderno_pranchas/Guedala_Park_Pranchas_R00.pdf): 7 pranchas A3 com carimbo (planta cotada, layout, pontos, vistas) | Elevações cotadas, detalhes da marcenaria e cotas finais após a medição |
| Memorial e especificações | 70% | [Caderno de especificações R01](Caderno_de_especificacoes.md), gerado a partir dos dados do site | Códigos de chapa e itens parciais; revisão do(a) RT |
| Orçamento | 60% | [Orçamento R44](../05_Orcamento_e_cronograma/Orcamento/Orcamento_R43.md): execução R$ 137.748,11 contra teto de R$ 120 mil; reserva R$ 10 mil intocada | Cotações reais e divergências listadas no consolidado |
| Responsabilidade técnica e aprovação | 10% | [Rascunho do plano de reforma NBR 16280](Plano_de_reforma_NBR16280.md) e perguntas à administração | Contratar RT; protocolar após as chaves |

## O que falta, em ordem de dependência

### 1. Formal e legal — bloqueia o "oficial"
- [ ] Contratar arquiteto(a) (CAU) ou engenheiro(a) (CREA) para revisar, assinar e emitir RRT/ART de projeto (e de execução, se for o caso).
- [ ] Elaborar o plano de reforma conforme a NBR 16280.
- [ ] Submeter projeto, memorial e cronograma ao síndico e ao conselho. A Convenção (p. 21, art. 7º, alínea i) exige aprovação prévia para hidráulica, pisos e paredes.
- [ ] Pedir à administração o rito e os documentos exigidos (p. 33, art. 57, alínea g: termo de responsabilidade e laudo técnico).

### 2. Levantamento físico — após as chaves
- [ ] Preencher a [folha de levantamento](../06_Entregas/Fichas_fabricacao/Levantamento.html):
  - larguras e alturas em vários pontos;
  - pé-direito, prumo, esquadro, piso acabado e rodapés.
- [ ] Localizar os pontos reais de água, esgoto, gás, tomadas e saídas técnicas.
- [ ] Conferir material e resistência de paredes e teto e as instalações ocultas.
- [ ] Medir portas, janelas e peitoris reais. Isso fecha a interferência da porta do gabinete do banheiro com a porta de entrada.

### 3. Projetos complementares mínimos
- [ ] Planta de pontos elétricos e de iluminação com circuitos e comandos, incluindo o ponto de 20 A da torre e as definições em 127 V.
- [ ] Hidráulica e gás:
  - cuba e tanque;
  - aquecedor E21;
  - cooktop (conversão GN).
- [ ] Paginação de piso e revestimentos, a partir da [análise de pisos](../05_Orcamento_e_cronograma/Orcamento/Pisos_e_revestimentos/Analise_pisos.md).
- [ ] Forro/sanca e faixa de LED do banheiro, com o percurso da tubulação validado.

### 4. Fechar o executivo de marcenaria
- [ ] Desenhar a distribuição de conectores nas "ligações sem mapa" de cada módulo.
- [ ] Incorporar as definições das fichas R14 ao modelo FreeCAD. **Feito em grande parte na [R46](../02_Modelo_3D/Historico/Fichas_no_CAD/README.md)** (24/10): ferragens por móvel, especificação por peça e 52 Minifix como marcadores. Faltam os furos executivos após a prova em retalho, a geometria da FGVTN 500 (pedir o STEP ao fabricante) e a piano do banco após o protótipo.
- [ ] Fechar as montagens pendentes, conforme a continuidade pré-entrega:
  - banco P20: dobradiça piano + articuladores com trava já nas fichas; faltam apoio da piano, terminais e protótipo;
  - cesto P14;
  - gavetas P01/P06 (FGVTN 500) e P16 (MOVENTO selecionada; corrigir interferências);
  - gaveta de limpeza P08: rodízios Leão Aço + espaçadores de 1 mm selecionados e modelados; faltam fixação, guias e batente.
- [ ] Dimensionar suspensão, cargas e reforços dos aéreos e do roupeiro.
- [ ] Definir substrato, códigos de chapa, bordas e veios por peça.
- [ ] Fazer caixas-piloto e ensaios em oficina antes do corte em série.

### 5. Pacote documental unificado
- [ ] Montar um conjunto único de pranchas numeradas:
  - layout;
  - demolir/construir, se houver;
  - pontos;
  - forro;
  - piso;
  - elevações por ambiente;
  - detalhamento dos 20 módulos.
- [ ] Incluir em cada prancha: carimbo, escala, cotas finais, legenda e tabela de revisões.
- [ ] Escrever um memorial descritivo e um caderno de especificações únicos (materiais, ferragens, louças, metais, eletros).
- [ ] Exportar em PDF e DWG/DXF para o profissional e os fornecedores.

### 6. Uma revisão vigente única
- [ ] Reconciliar modelo R52, fichas R14, orçamento R44 e as versões divergentes de pacote no [manifesto](../06_Entregas/README.md#manifesto-de-versões--conferência-t09-em-26102026); conferir as vistas ainda baseadas na R45 sem presumir que foram regeneradas.
- [x] Atualizar o [README de entregas](../06_Entregas/README.md): desde 24/10 ele abre com "o que vale hoje"; o R41 ficou só na parte histórica.

### 7. Orçamento com preços reais
- [ ] Cotar marcenaria e obra com escopo comparável. A marcenaria está estimada em R$46,5 mil, contra a meta de R$35 mil.
- [x] Reconciliar as ferragens ([reconciliação](../05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Reconciliacao_ferragens_fichas_R14_2026-10-24.md)); [pacote de cotação pronto](../05_Orcamento_e_cronograma/Orcamento/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md). As fichas usam Blum, e o orçamento usa referências FGVTN. Os Minifix somam 52 nas fichas (40 dos aéreos + 12 do espelheiro P19) e 20 no orçamento.

### 8. Organização para revisão externa (não bloqueia)
- [ ] Separar a pasta de entrega do histórico. Hoje há `tmp` com cerca de 2 GB (fora do git), várias cópias `antes_*` e revisões FCStd de 20–47 MB cada.

## Esforço estimado

- **Partindo deste material, com o profissional que vai assinar:** 3–6 semanas de escritório para complementares, pranchas e memorial.
- **Depois da vistoria:** mais 1–2 semanas para as cotas executivas finais.
