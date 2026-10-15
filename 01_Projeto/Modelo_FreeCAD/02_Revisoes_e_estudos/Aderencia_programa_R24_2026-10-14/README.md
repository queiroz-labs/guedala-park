# Aderência do programa - R24

Auditoria independente de dados locais. Nenhum CAD, controle, automação ou documento fora desta pasta foi alterado. Não houve pesquisa pública, contato, booleanos, poses ou testes de fabricação. A leitura indexou73 raízes standalone de sala/escritório/quarto e comparou13 conjuntos selecionados com documentos; não equivale a conferir todos os bens reais ou toda decoração.

## Duas correções digitais localizadas para revisão do responsável

**Espelho lateral: desvio nominal de15mm na centralização.** A escolha de15/09 registrada em `Portas_e_quarto/README.md` determina Cebrace prata50×180cm/5mm, base20cm e centralização na lateral. A profundidade total do roupeiro passou a65cm em12/10. A R24 tem espelho `Peca275` emY3350..3850, centro3600, mantendo tamanho/base corretos.

O corpo temY3290..3940. Para evitar centralizar numa dimensão abstrata, foi identificada a face lateral efetivamente modelada na altura do espelho:

- `Peca207`: X1992..2010/Y3372..3940/Z0..2132. Painel568mm, centroY3656.
- `ReferenciaCorrerR001`: X1992..2010/Y3290..3372/Z62..2132. Apoio frontal82mm. O arquivo BREP salvo contém os oito vértices da caixa, conferidos por leitura textual sem runtime CAD; Placement do feature é identidade e pai é `Modulo`.
- As duas peças se encontram emY3372 e formam o mesmo plano externoX2010, contínuo emY3290..3940 na alturaZ200..2000 do espelho. Centro da lateral composta: **3615**. Centrar só no painel568 levaria a3656 e não refletiria a lateral composta.

Restaurar a centralização do espelho na lateral proposta, sem mudar dimensões, resulta emY3365..3865. A entrega contém evidência e limites para o responsável integrar; nenhuma alteração foi feita aqui. Os apoios/ligação do conjunto e fixação do vidro continuam propostas, sem capacidade ou instalação comprovadas.

**Cabeceira: divisão visual aprovada ausente.** `Portas_e_quarto/README.md`29 e `Cabeceira_e_armario_superior_R00.md` registram a escolha21/09: cabeceira estofada lisa em dois painéis lado a lado. O CAD mantém um bloco único `Peca107`, Length50/Width1600/Height950, Placement(0,1200,200), envelopeX0..50/Y1200..2800/Z200..1150. A lacuna é de representação, não de envelope. Pode-se mostrar a divisão central preservando esse volume; não transformar a linha ilustrativa em junta, cota ou corte aprovado.

## Conferências aderentes

| Conjunto | Geometria R24 | Situação documental |
|---|---|---|
| Bancada escritório | 2000×700, topo750; centrada emX2700..4700/Y0..700 | Profundidade70 aceita; largura/altura/apoios continuam de estudo |
| Prateleira consoles | 1100 longitudinal×350 profundo, topo1950 | Superfície e topo195 compatíveis com F154/F155; fixação/carga pendentes |
| Setup | Notebook, dois monitores620×350 e um CH360215×428×431 | Envelopes do R10; modelos exatos de telas/notebook/braços indisponíveis. Ordem da base acompanha a reflexão geral mais recente; não fixar direita/esquerda físicas antigas como nova decisão |
| Queen | Reserva2000×1600 | Documento distingue padrão de colchão1580×1980 da reserva de base não medida; não reduzir para fazer caber |
| Dois apoios da cabeceira | 150×200, dois objetos | Base20×15 presente, dentro do contorno da cama; conforto/postura reais pendentes |
| Mesa compacta | Duas metades750×750; conjunto1500×750/topo750 | Direção150/180 preservada; coluna/sapata/quadro são gabaritos, sem mecanismo ou resistência aprovados |
| Três Lina | 440×470×940 na lateral; central85mm mais externa | Posições exatas do documento23/09, inclusive centros e inserções propostas |
| TV escritório | Reserva970×560×50 | Samsung43 existente, modelo desconhecido; não atribuir essas cotas ao aparelho real |
| Painel/TV sala | Painel1150/prateleiras1100; TV1111×649 e soundbar futura900×70 | A proposta1120/1070/projeção40 e cortina7cm declara explicitamente que não foi aplicada ao3D; manter diferença como proposta pendente, não erro automático |
| Bonnie | Envelope fechado1800 longitudinal×1100 profundo/altura1000 | Referência comercial escolhida preservada; pose fechada não comprova uso aberto cotidiano/mecanismo real |

Os rótulos automáticos do setup terminam em CH361..CH368 porque o FreeCAD incrementou o sufixo de um rótulo composto. São partes do mesmo setup, não evidência de novos gabinetes escolhidos. O corpo do CH360 é `Peca119`.

## Contatos comunicados pelo responsável

O responsável comunicou13 comuns da auditoria externa standalone:10mesa/cadeiras e3enchimento/perfis do box. Nenhuma interseção foi recalculada nesta entrega.

**Mesa/cadeiras:** `Mesa_circulacao_entrada_2026-09-23.md` lista exatamente as posições atuais: lateraisX606..653cm, central597,5..644,5; faixasY393..437/443..487/493..537. O documento explicita que pés, encosto, sapata, guias e altura livre ainda dependem da cadeira real. Caixas cheias até940mm ocupam os vazios que permitem inserir cadeiras sob tampo. Os comuns não justificam deslocar a guarda aceita ou reduzir pedestal para chamá-la aprovada.

**Enchimento/box:** `Banheiro/Medidas_e_encaixe_2026-09-18.md`13/26 reserva hipoteticamente30cm de enchimento, com altura/forma não medidas, e faixa80×124cm de box. A modelagem tem enchimento800×300×180 emZ20..200 e perfis/planos simplificados atravessando essa faixa posterior. O documento35 exige desenho de vidro/perfis/abertura; o estudo de água quente não prova acesso ou redes no enchimento. Esses três comuns precisam de detalhe físico/profissional, não de alteração arbitrária da posição do box ou remoção do enchimento.

## Limites da representação

Fonte gráfica e busca de rótulos não identificam sólidos específicos para espelho70×120 da sala, quadro2×2, tapeteAlmeidas140×200, duas almofadas greige/azul e fruteira. São escolhas/intenções no programa, com diversos tamanhos/peças ainda propostos. Ausência no CAD estrutural não significa cancelamento dessas escolhas nem permite inventar cotas a partir dos renders. Não foi iniciada modelagem decorativa.

[Comparacao_programa.json](Comparacao_programa.json) separa aderência, hipóteses, lacunas e desvio. [Standalone_R24.json](Standalone_R24.json) contém propriedades e coordenadas das73 raízes. [Espelho_lateral_evidencia.json](Espelho_lateral_evidencia.json) registra quatro apoios R14, XPaths, arquivos BREP e vértices, matriz do pai e centros.

Medidas derivadas do CAD são de estudo; nenhuma lista de corte, furação, compra, estrutura ou instalação foi liberada. Sofá Daiane/tanque já corrigidos na R24 não foram novamente auditados ou propostos para alteração.
