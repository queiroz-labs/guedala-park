# R37 — banco com entrada superior e ferragens no Brasil

Modelo FreeCAD · [Seleção de ferragens](Ferragens_Brasil_R37.md) · [Percurso](Verificacao_percurso_R37.json) · [Reabertura](Reabertura_R37.json)

R36 preservada byte a byte. A extensão única750x300x30 agora fica sobre a prateleira do banco, com entrada pelo alto. Foram removidos bandeja, guias e peças do acesso lateral; lateral fechada e prateleira contínua restauradas. Apartamento único, orientação correta preservada.

Em CONTROLES ATUAIS / Sala, usar **Mesa e banco — acesso superior (0 a100)**, propriedade Progresso do controle TransferenciaMesaR37. Começar com os controles manuais zerados. O percurso retira a almofada, abre a tampa, eleva a extensão e a leva à mesa.100→0 guarda a mesma extensão por cima e fecha o banco. Em0 os controles manuais da mesa e do banco permanecem disponíveis. Salvo em0, banco e mesa fechados.

A sequência representa transporte manual, não mecanismo automático. A tampa usa o eixo ideal existente: dobradiças e retenção comercial ainda precisam dimensionamento. Não acessar outros setores enquanto a almofada estiver estacionada sobre eles.

Foram testadas101 posições de6peças móveis contra a geometria fixa e entre si, sem novas interseções volumétricas acima da tolerância0,1mm³ sobre os contatos preexistentes. Todas retornaram à posição inicial. Verificação amostral, sem certificação do percurso contínuo, cargas, tolerâncias de inserção, mãos ou peças ainda ausentes. O teste global isValid identificou compostos preexistentes: comparação separada com R36 e validade das peças modificadas ficam em Reabertura_R37.json. Não se declara o documento inteiro geometricamente válido por esse indicador.

## Os300mm

O desenho Pöttker47085103 B-SB/850.4/280.4/W260/KK3, página1, informa abertura aproximada605mm. Há alcance para vão total300mm, nominalmente150mm por metade em sistema simétrico. Isso não confirma travamento nessa posição, fixação ao pedestal ou tolerâncias de montagem. O desenho e a consulta anterior não comprovam compra fácil no Brasil.

A candidata brasileira Häfele642.59.902 é tratada separadamente: não se transferem para ela os605mm da Pöttker. Conferir o desenho exato e estoque antes da seleção final. As guias simplificadas atuais continuam gabaritos, sem homologação para fabricação.

[Desenho Pöttker consultado](https://form32.com/media/b0/ee/81/1708069799/B-SB_850.4_280.4_W260_KK3_(47085103).pdf?ts=1708069799)

Sofás, portas de aparelhos, box, esquadrias e ferragem do varal seguem com pendências de dados reais; nenhuma articulação foi inventada para aparentar conclusão. A pesquisa brasileira está incorporada na documentação do FreeCAD.
