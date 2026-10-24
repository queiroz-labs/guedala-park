# Roteiro para projeto oficial de arquitetura de interiores

24/10/2026. Diagnóstico documental: compara o material existente com as etapas de um projeto de interiores assinado (NBR 13532 e fluxo usual CAU). Nenhum CAD, ficha ou orçamento foi alterado.

## Situação geral

- **Conteúdo técnico de marcenaria:** cerca de 55–60% do caminho até um executivo completo. Detalhamento acima da média: 20 módulos com peças, furações e ferragens selecionadas.
- **Camada oficial** (responsável técnico, pranchas normatizadas, complementares, aprovação do condomínio): cerca de 0–10%.
- **Bloqueio principal:** as medidas reais do apartamento. Todas as cotas continuam nominais e o pacote não libera fabricação.

## Situação por etapa

| Etapa | % estimado | Evidência | Falta |
|---|---|---|---|
| Programa de necessidades | 100% | [Programa de necessidades R01](Programa_de_necessidades_R01.md) | Validar uso no local após as chaves |
| Levantamento do imóvel | 25% | [Medidas](Medidas/README.md), [visita](../04_Visita_ao_apartamento/README.md) (unidade espelhada) | Vistoria completa após as chaves |
| Estudo preliminar | 100% | [Planta mobiliada R02 e vistas](Planta_mobiliada/README.md), site 3D | Corrigir 4 textos desatualizados do site |
| Anteprojeto | 75% | Modelo R45, [acabamentos](Estudo_interativo/fabrication/Decisao_acabamentos_R13.md) | Códigos de chapa, madeira do banheiro, bege/off-white exatos, amostras |
| Executivo de marcenaria | 45–55% | [Fichas R14](../05_Entregas/Fichas_fabricacao_R13/index.html), [Pendências](../05_Entregas/Fichas_fabricacao_R13/Pendencias.html) | Ver item 4 |
| Complementares | 30% | [Planta de pontos preliminar R00](Planta_pontos_R00/README.md): 50 pontos de elétrica, luz, água, esgoto e gás | Circuitos, traçados e assinatura do RT |
| Pranchas formais | 30% | [PDFs R28/R30](../05_Entregas/README.md), históricos | Ver item 5 |
| Memorial e especificações | 70% | [Caderno de especificações R01](Caderno_de_especificacoes_R01.md), gerado a partir dos dados do site | Códigos de chapa e itens parciais; revisão do(a) RT |
| Orçamento | 60% | [Orçamento R43](Orcamento_R43_2026-10-22/Orcamento_R43.md): estimativa R$137,8 mil contra teto de R$120 mil | Cotações reais |
| Responsabilidade técnica e aprovação | 10% | [Rascunho do plano de reforma NBR 16280](Plano_de_reforma_NBR16280_rascunho.md) e perguntas à administração | Contratar RT; protocolar após as chaves |

## O que falta, em ordem de dependência

### 1. Formal e legal — bloqueia o "oficial"
- [ ] Contratar arquiteto(a) (CAU) ou engenheiro(a) (CREA) para revisar, assinar e emitir RRT/ART de projeto (e de execução, se for o caso).
- [ ] Elaborar o plano de reforma conforme a NBR 16280.
- [ ] Submeter projeto, memorial e cronograma ao síndico e ao conselho. A Convenção (p. 21, art. 7º, alínea i) exige aprovação prévia para hidráulica, pisos e paredes.
- [ ] Pedir à administração o rito e os documentos exigidos (p. 33, art. 57, alínea g: termo de responsabilidade e laudo técnico).

### 2. Levantamento físico — após as chaves
- [ ] Preencher a [folha de levantamento](../05_Entregas/Fichas_fabricacao_R13/Levantamento.html):
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
- [ ] Paginação de piso e revestimentos, a partir da [análise de pisos](Orcamento_R43_2026-10-22/Pisos_e_revestimentos/Analise_pisos.md).
- [ ] Forro/sanca e faixa de LED do banheiro, com o percurso da tubulação validado.

### 4. Fechar o executivo de marcenaria
- [ ] Desenhar a distribuição de conectores nas "ligações sem mapa" de cada módulo.
- [ ] Incorporar as definições das fichas R14 ao modelo FreeCAD. Hoje modelo e fichas divergem.
- [ ] Fechar as montagens pendentes, conforme a [continuidade pré-entrega](Continuidade_pre_entrega_2026-10-23.md):
  - banco P20;
  - cesto P14;
  - gavetas P01/P06 (FGVTN 500) e P16 (MOVENTO);
  - gaveta de limpeza P08.
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
- [ ] Reconciliar a geometria R45, o pacote R16, as fichas R14 e o orçamento R43 numa só revisão.
- [ ] Atualizar o [README de entregas](../05_Entregas/README.md), que ainda cita o modelo R41 como vigente.

### 7. Orçamento com preços reais
- [ ] Cotar marcenaria e obra com escopo comparável. A marcenaria está estimada em R$46,5 mil, contra a meta de R$35 mil.
- [x] Reconciliar as ferragens ([reconciliação](Orcamento_R43_2026-10-22/Marcenaria_35mil/Reconciliacao_ferragens_fichas_R14_2026-10-24.md)); [pacote de cotação pronto](Orcamento_R43_2026-10-22/Marcenaria_35mil/Pacote_cotacao_marcenaria_R01.md). As fichas usam Blum, e o orçamento usa referências FGVTN. Os Minifix somam 40 nas fichas e 20 no orçamento.

### 8. Organização para revisão externa (não bloqueia)
- [ ] Separar a pasta de entrega do histórico. Hoje há `tmp` com cerca de 476 MB, várias cópias `antes_*` e revisões FCStd de 20–47 MB cada.

## Esforço estimado

- **Partindo deste material, com o profissional que vai assinar:** 3–6 semanas de escritório para complementares, pranchas e memorial.
- **Depois da vistoria:** mais 1–2 semanas para as cotas executivas finais.
