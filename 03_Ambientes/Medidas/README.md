# Medidas e instalações

Origem das medidas usadas no projeto. A convenção (p. 4) confirma 40,180 m² privativos; o memorial não informa pé-direito, sancas, janelas nem posições cotadas dos pontos. As cotas das plantas são de face a face com acabamento, não levantamento da unidade.

A base é a planta oficial, complementada por imagens de outra unidade espelhada. Não há medidas acabadas conferidas na unidade de Elias. Cozinha: 352 × 155 cm; lavanderia: 129 cm paralelos à bancada × 154 cm transversais.

## Documentos

| Abrir | Conteúdo |
|---|---|
| [Origem das medidas](Origem_das_medidas.md) | Método, cotas, instalações identificadas e limites da leitura. |
| [Plantas e instalações](Plantas_e_instalacoes_R00.pdf) | Seis pranchas de referência dimensional. |
| [Dados das medidas](Dados_das_medidas_R00.json) | Registros e rastreabilidade da base dimensional. |
| Pesquisa comparativa Cury | Pesquisa de 12/09/2026: planta oficial adicional, finais equivalentes e comparações com outros empreendimentos; pé-direito permanece pendente. |

Consultar estudos anteriores. Os estudos não liberam fabricação ou instalação.

## Fonte das pranchas R02

O CSV [Medidas e impactos](../../07_Imovel/Medidas_e_impactos.csv) concentra as entradas de campo e nominais das pranchas: pé-direito PD por ambiente, incluindo circulação, contornos PR, vãos/peitoris e posições dos 53 pontos R01. `valor_medido` preenchido vence `valor_nominal_atual`; usar número com unidade (mm, cm ou m). Coordenadas e aberturas reconstituídas são nominais, não levantamento. Cotas.json contém os vínculos; Geometria.json registra os envelopes e SHA da R53.

Regenerar: `python ferramentas/pranchas/gerar.py`. [Guia em três passos e limites](../../06_Entregas/Caderno_pranchas/README.md). O PDF R02 distingue N/M e informa cotas nominais por folha; alturas de estudo e fechamento dependem do pé-direito do ambiente. Alteração não salva o CAD.

Teste externo de 27/10/2026: seis PD medidos fictícios de 2470 mm prevaleceram sobre os nominais de 2600 mm; 99 cotas mudaram e quatro conflitos ao teto foram avisados. Foi apenas ensaio em cópia apagada: **nenhuma medição real incorporada**; esse teste histórico usou nominal de 2,60 m. Desde 27/10/2026, o nominal é 2,60 m nos cômodos e 2,50 m no banheiro, a confirmar.

## Dependências dos móveis

[Regras da R53](../../04_Moveis/Dependencias/README.md) vinculam envelopes, teto, vãos e instalações ao CSV. DEP-COZ-PRUMO registra o desvio base/topo da parede da cozinha; zero nominal não comprova prumo.
