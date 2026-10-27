# Detalhamento documental R28

Pedido humano: executar os quatro itens propostos — pranchas cotadas, lista de ferragens, sequências de montagem/uso/manutenção e reconciliação documental.

Abra [o índice das entregas](Indice_entregas_R28.html). Os dois PDFs estão em `06_Entregas/pdf` na raiz do repositório. O primeiro contém capa e 20 pranchas A3; o segundo reúne ferragens, 54 referências de calços, dez sequências e nove itens de conferência em 20 páginas A4. Os CSVs permitem consultar ferragens e os 774 componentes dos módulos sem contar sólidos internos de um conjunto como itens de compra.

## Escopo e limites

A fonte é a R28, preservada sem mudança de hash. Foram lidas apenas geometrias e propriedades atuais; nenhuma abertura ou simulação antiga foi refeita. As projeções mostram posições fechadas, com orientação frontal local espelhada. A planta do canto normaliza sua origem Y para apresentação; o CSV mantém as coordenadas locais originais, inclusive negativas.

As cotas são de compatibilização, não de fabricação. H01 e seguintes marcam centros das envoltórias de calços, não centros de furos. Quantidades de ferragens são candidatas ou reservas conforme indicado; não constituem lista liberada de compra. As sequências dependentes de ferragens, retenção, carga, manuseio ou levantamento real estão identificadas como propostas. Não houve alteração do programa, adoção de mecanismo ou liberação executiva.

## Verificação

[Verificacao_entregas.json](Verificacao_entregas.json) registra páginas, links, contagens, unicidade dos objetos e hash da R28. Todas as 41 páginas foram renderizadas e inspecionadas; ajustes de apresentação do canto e distribuição das tabelas foram incorporados. Os relatórios anteriores de colisões mantêm seus escopos e limites.

`../../../ferramentas/componentes/Detalhamento_documental/exportar_pranchas.py` já foi executado uma vez para obter `Base_pranchas_R28.json`; não deve ser tratado como rotina recorrente. `../../../ferramentas/componentes/Detalhamento_documental/gerar_entregas.py` usa essa base para produzir os documentos. `../../../ferramentas/componentes/Detalhamento_documental/verificar_entregas.py` confere os artefatos finais. A execução desta entrega não reinicia o agendamento encerrado nem comprova a revisão Astra.
