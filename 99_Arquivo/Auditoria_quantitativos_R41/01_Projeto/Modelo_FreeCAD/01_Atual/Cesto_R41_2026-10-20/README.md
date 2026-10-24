**21/10/2026 — documentação conciliada:** [resumo vigente](../../../Resumo.md), [painel de pendências](../../../Painel_de_decisoes.md) e [complemento de orçamento](../../../Complemento_orcamento_vigente_R41.md). Links incorporados ao FreeCAD, na mesma R41; [conferência do salvamento](Conferencia_documental_R41.json).

**Consulta enviada:** Häfele e FGVTN receberam mensagens separadas pelo Outlook. [Texto e confirmação dos envios](Envios_fabricantes_R41.md). A confirmação é de execução do envio; resposta técnica ainda pendente.

**Continuidade na mesma R41:** busca de mecanismos mais fortes e estudo de esforços para8kg de roupa. [Resultado e próximos dados necessários](Pesquisa_ferragem_forte_R41.md). [Conferência do arquivo atual](Conferencia_atual_R41.json). O registroSalvamento_R41.json documenta a primeira gravação; o hash vigente está na conferência atual.

# Frente de500mm com FGVTN BV0 — estudo R41

20/10/2026. **Diminuir a frente para500mm resolve o enquadramento de altura, mas não permite aprovar o BV0 para8kg de roupa.** O saco pode ser preservado geometricamente; a aplicação física depende também de carga, montagem, dobradiças e retenção.

[Modelo R41](Guedala_Park_R41_Estudo_Frente500.FCStd) · [Cálculos](Calculo_R41.json) · [Conferência](Salvamento_R41.json)

## Peso: a redução é pequena

Mantidos550mm de largura e18mm de espessura, a altura cai de521para500mm: menos21mm, ou4,03% do volume da frente. Os valores abaixo usam os cenários históricos de densidade750/900kg/m³; não são pesagens nem propriedades confirmadas da chapa definitiva.

| Grandeza | Frente521mm | Frente500mm |
|---|---:|---:|
| Massa da frente, cenário750kg/m³ |3,868kg|3,713kg|
| Massa da frente, cenário900kg/m³ |4,642kg|4,455kg|
| Frente + requisito de8kg de roupa |11,868–12,642kg|11,713–12,455kg|

Economia:156–187g. Ainda falta somar armação, saco, ferragens, pega e fixações. A massa total não determina sozinha a ferragem: é necessário considerar a posição do centro de massa, o braço do esforço durante o giro, a carga variável e a ação de retirar o saco. Não foi convertido o subtotal em carga admissível do mecanismo.

## O que a tabela FGVTN permite concluir

A [ficha técnica atual do BV0](https://www.fgvtn.com.br/site/novopdf/Braco_de_abertura_variavel_BV0.pdf), também arquivada emFontes e inspecionada visualmente naR40, informa portas até6kg. A tabela de quantidade indica1braço para altura200–400mm e2braços para200–500mm. A proposta500mm entra nesse intervalo com2braços.

Isso **não significa2×6=12kg de roupa ou de conjunto**. O documento não certifica a aplicação em uma frente que carrega uma armação com8kg de roupa fora do plano da porta. A tabela orientativa de dimensões/massa de porta não representa aprovação dessa carga deslocada. Não há confirmação de limite mecânico/retentor positivo55° para a retirada diária do saco, nem definição de dobradiça real e suas fixações.

Portanto, mesmo enquadrando a altura, permanecem pendentes a carga e os momentos admissíveis para a montagem inferior completa. Não se pode concluir que é impossível usar BV0 em qualquer cesto; pode-se concluir que **a documentação disponível não valida este cesto com8kg**.

## Duas formas de reduzir a frente

As duas alternativas foram criadas no FreeCAD como peças de estudo **ocultas**, sem substituir a frente instalada:

| Alternativa | Base/topo da frente | Consequência |
|---|---|---|
| Manter base atual |150–650mm|Junta ao painel superior675 cresce de4para25mm; exigiria rever acabamento/fechamento desse vão.|
| Manter topo atual |171–671mm|Junta superior4mm preservada; borda inferior sobe21mm, exigindo rever relação com base, apoios e fixações.|

Essas alternativas são recortes da peça atual: ambas550×500×18mm, formas válidas e volume4.950.000mm³. Não representam furação de fabricação ou ferragem instalada. As ligações à armação e a montagem do BV0 não foram reposicionadas por presunção.

O saco400×200×400mm e a armação atual permanecem iguais. Reduzir apenas a frente não obriga a diminuir o saco. Contudo, ocupar as laterais com braços e mudar o eixo para uma dobradiça comercial pode alterar o caminho de extração; por isso não foi declarada retirada real validada.

## Decisão

**Não adotar BV0 para8kg apenas com essa mudança.** A frente500mm fica como alternativa dimensional possível, condicionada a uma ferragem aprovada para o conjunto carregado. Para avançar comBV0, é necessária confirmação técnica do fabricante para frente550×500×18mm, roupa8kg mais peso próprio, posição real do cesto, abertura inferior, retenção55° e montagem/fixações. Consulta posteriormente enviada a Häfele e FGVTN; ver o registro de envios no início deste documento. Resposta técnica pendente.

R39 eR40 preservadas. A R41 acrescenta estudo, planilha, duas alternativas ocultas e conclusões. As1239 formas originais permaneceram idênticas às daR40; nenhum erro de objeto foi encontrado. A geometria operacional do apartamento e seus controles permanecem na configuração anterior.
