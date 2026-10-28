# Guedala Park — conferência dimensional R54 e histórico R45

## Conferência documental R54 — 28/10/2026

[Tabela R44 → R54](Inventario/Comparacao_R44_R54.md): 3.420 medidas (dimensões e posições) de 380 IDs comuns, mais 37 vãos entre faces. Comparação independente das medidas textuais copiadas em `fabrication-data.js`; utiliza coordenadas e IDs de `cad-data.js`. Mudanças relevantes: divisor P09 +194 mm (já refletido na matriz), quatro painéis superiores P16 −6 mm em altura e correção do envelope histórico G2 −1,196152 mm. Banco: envelopes comparados sem mudança.

Matriz e dois relatórios HTML distinguem cotas atuais de variantes, catálogo e simulações históricas. Não se revalidaram resistência, massas, áreas de contato BRep ou interferências de ferragens. A lacuna exata é documentada na comparação, sem transformar igualdade de envelope em confirmação técnica. O CSV completo fica fora do git; comando e SHA256 estão no resumo. Testes: `python -B -m unittest discover -s ferramentas/estudos -p test_reconciliar_documentos_dimensionais.py`.

Para integrar ao site, após as outras frentes: `python -B ferramentas/site/construir.py`, `python -B ferramentas/site/build_workshop_docs.py --sources-only` e `python -B ferramentas/verificar_site.py`. Nenhum desses comandos publica. O restante deste README é o registro da consolidação R45, não uma afirmação de revisão atual.

> **Southco — aprofundamento posterior:** [fixação proposta no banco e limites](../Banco_e_cesto/Fixacao_Southco/Relatorio.html). Contraplatinas e suporte recuado estudados sem alterar dimensões das tampas ou gabaritos de armazenamento. Instalação ainda não fechada: almofadas, eixo real, batente e ligações pendentes. Modelo principal R45 preservado.

23/10/2026. [Relatório completo](Relatorio.html) · [FreeCAD R45](Guedala_Park_R45_Consolidado.FCStd) · [Verificação](Verificacao_entrega.json).

Revisão dos 20 módulos, 171 interfaces, gavetas, portas, banco, equipamentos e ferragens. A R44 permanece intacta. A R45 incorpora registros de revisão e grupos ocultos dos estudos, preservando a geometria principal e o armazenamento. Não representa todos os mecanismos aprovados para fabricação.

As propostas de bancada, Minifix e pinos do espelheiro são alternativas separadas. Rockler traseira e abertura frontal do banco foram rejeitadas. Southco com eixo superior permanece candidata sem fixação executiva. MOVENTO400 preserva o útil do escritório, mas requer fechamento dos pequenos conflitos e retirada. O quantitativo vigente é52dobradiças, não56; FGVTN tem35kg de capacidade, não40kg.

Cada relatório contém as fontes e os dados que ainda faltam. Medidas reais do apartamento, substratos de ancoragem e instalações não foram inventados. A cobertura dos20módulos não significa20aprovações.

## Frentes

- [Inventário, vãos, ligações e ferragens fixas](Inventario/README.md)
- [Gavetas e rodízios](Gavetas/Resultado.html)
- [Alternativa MOVENTO no escritório](Gavetas/Alternativas_escritorio/Resultado.html)
- [Portas, banco, cesto, mesa e varal](Portas_e_articulacoes/Relatorio.html)
- [Banco: estrutura e interferência das fixações](Banco_estrutura/Resultado.html)
- Rockler no projeto

Pesquisa e ensaios realizados em frentes paralelas até o prazo solicitado; consolidação e verificação final concluídas após as6h por atraso de comunicação na abertura da cópia FreeCAD. Consulte a hora de verificação noJSON. Nenhuma compra, publicação ou comunicação com fornecedores foi realizada.
