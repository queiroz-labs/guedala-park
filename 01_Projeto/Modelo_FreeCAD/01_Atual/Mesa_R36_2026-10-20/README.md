# R36 — transferência da folha e ferragens da mesa

[Modelo FreeCAD R36](Guedala_Park_R36_Extensao_Mesa.FCStd) · [Teste do percurso](Teste_percurso_R36.json) · [Reabertura e controles](Reabertura_R36.json) · [Ferragens oficiais baixadas](../../../Sala_e_jantar/Ferragens_mesa_2026-10-20/README.md)

R35 preservada byte a byte. Apartamento único na orientação correta, placa do varal removida e controles anteriores mantidos. Revisão salva com mesa e bandeja fechadas. O pedido posterior de Elias foi usar somente mecanismos com medidas confirmadas; nenhum eixo de sofá/aparelho foi inventado.

## Mesa

Em CONTROLES ATUAIS / Sala, TransferenciaMesaR36.Progresso0–100 coordena a mesma BancoFolhaR31: abre vão300; extrai bandeja723; desliza folha120; eleva; recolhe bandeja e transporta longitudinalmente; desloca transversalmente; gira90°; assenta a folha. É percurso manual ilustrativo sobre a geometria existente, não mecanismo automático ou ferragem homologada. A preferência de revisar o banco para baú convencional está preservada; o acesso lateral não foi reaprovado.

Progresso0 mantém os controles independentes da R35 operantes. Progresso100 coloca a folha única em X500–1250, Y4500–4800, Z720–750 mm, fechando o vão nominal entre metades, com bandeja recolhida. A mesa tem1800x750, sem alterar a base. Retornar100→0 inverte a sequência. Operar partindo dos controles independentes zerados; o ciclo assumirá as poses coordenadas ao iniciar.

Foram conferidas101 posições da folha contra1126 outras peças do modelo, sem interseção volumétrica nas amostras e com retorno à posição inicial. Foi corrigida a pequena invasão da referência gráfica da junta no vão. Reabertura testa as principais fases na ida e volta e4 controles independentes afetados. A verificação é amostral, não certifica todo o contínuo, operação humana, peso, tolerâncias, cargas ou componentes ausentes. Folha nominal sem pinos e folga de inserção ainda não dimensionada.

## Fechamento dos demais mecanismos

| Item | Situação | Dado que falta |
| --- | --- | --- |
| Mesa: folha única | Percurso manual CAD implementado e testado | Ferragem sincronizada, folga de inserção, apoios e travas ainda sem seleção final |
| Mesa: corrediças reais | 7 STEP oficiais Hettich baixados e válidos; desenhos Pöttker baixados | Confirmar código, sincronismo, curso útil para folha300, furação e ligação ao pedestal |
| Bonnie: retrátil/reclinação/baú | Fabricante confirma envelopes1100/1360 e encosto180 graus | Eixos cotados, cursos de cada parte, mecanismo do baú e recuo real |
| Daiane: retrátil/reclinação/baú | Fornecedor confirma1400x900 fechado e1400x1820 aberto | Desenho da articulação, eixos, fases intermediárias e implantação real; não deduzir curso do assento da diferença de envelopes |
| Portas dos aparelhos | LG confirma620 fechada/1100 aberta90; forno tem instrução de retirada da porta | Geometria cotada de cada folha/eixo; geladeira, forno e micro não são portas de marcenaria genéricas |
| Box | Aparência definida; documento local não define giro ou correr | Desenho do vidraceiro: tipo, folhas, sobreposição, ferragens, puxador e vão útil |
| Janelas e portas arquitetônicas restantes | Planta contém vãos, sem todos os eixos e folhas cotados | Quadro de esquadrias, eixos, sentido, cursos e ferragens do projeto original |
| Varal: cabos/manivela/roupas | Grelha1000x500 e descida de estudo existentes; chapa removida | Produto e desenho cotado do mecanismo, roldanas, curso, retenção, fixações e envelopes de roupa |

As fontes consultadas não trazem todas as coordenadas de eixos necessárias. Não se considera concluída a totalidade das articulações. O quadro também fica dentro do FreeCAD em Documentação / R36 - mecanismos e dados confirmados.

Fontes adicionais:
- [Bonnie, fabricante](https://www.camainbox.com.br/products/sofa-bau-sem-caixa-retratil-softgel-bonnie-boucle-cama-inbox).
- [Daiane, fornecedor do produto escolhido](https://www.mobly.com.br/sofacama-daiane-veludo-light-cinza-974920.html).
- [LG CV5012PC4, fabricante](https://www.lg.com/br/lavanderia/lava-e-seca/cv5012pc4/).
- [Box: tipo de abertura ainda indefinido](../../../Banheiro/Medidas_e_encaixe_2026-09-18.md).

A documentação não constitui liberação de fabricação. Nenhuma mensagem foi enviada a fabricantes.
