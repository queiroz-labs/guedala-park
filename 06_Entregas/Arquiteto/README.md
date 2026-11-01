# Pacote para revisão do arquiteto

Preparado em 01/11/2026; **não enviado**. Anteprojeto nominal, com levantamento e revisão técnica pendentes.

| Abrir | Conteúdo e limite |
|---|---|
| [Caderno do arquiteto](Caderno_arquiteto.pdf) | Revisão, layout R03/cena R54, comparação de níveis, materiais, 13 questões de arquitetura, 10 interfaces, roteiro de campo e 20 pranchas A3 originais R02/R54. |
| [Manifesto](Manifesto.csv) | Caminhos, bytes, SHA256 e limites dos 17 arquivos de conteúdo incluídos no ZIP. |
| [CAD nativo](../../02_Modelo_3D/Guedala_Park_R55_Berlin.FCStd) | R55 vigente; o ZIP inclui os mesmos bytes. Não convertido ou alterado. |
| [Pontos R01](../../03_Ambientes/Planta_pontos/README.md) | 53 funções/E06 adiada; SVG e fontes incluídos. |
| [Especificações R01](../../01_Programa_e_decisoes/Caderno_de_especificacoes.md) | Fonte completa; quadro de materiais no caderno. Produtos/amostras/SKUs condicionados. |
| [Levantamento](../../07_Imovel/Roteiro_dia_das_chaves_R01.md) | Roteiro completo e índice de 532 registros sem medidas reais incluídos. |

ZIP local fora do Git: ../../../outputs/Arquiteto/Guedala_Park_Arquiteto.zip. Extrair inteiro e ler LEIA_PRIMEIRO.txt; inclui 19 arquivos, sendo 17 conteúdos, manifesto e instruções. Os documentos-fonte mantêm referências ao repositório completo; o recorte não inclui todo estudo citado.

O FCStd é R55, mas as pranchas anexas mantêm a referência R54. A composição não reexporta paredes, vãos, pisos ou esquadrias nem altera escala: anexos A3 a 100%, barra de 50 mm. O quadro de níveis é comparativo, não corte construtivo. Não representa pacote executivo compatibilizado. IFC/DWG/DXF/STEP dependem de formato/finalidade definidos com o destinatário; não foram gerados.

## Regenerar

Usar Python com ReportLab e pypdf (runtime local do Codex disponível), na raiz:

    python -B ferramentas/estudos/pacote_arquiteto.py --zip CAMINHO_EXTERNO_NOVO.zip

O destino ZIP precisa ser novo e externo ao repositório. O gerador confere SHA/revisão do CAD, índices de revisão e ausência de medidas; gera PDF/manifesto aqui, prepara ZIP e confere CRC/hashes. Não abre o FreeCAD, não envia e não publica. Fontes/cotas preservadas. Após atualizar as fontes, revisar o conteúdo e a emissão antes de regenerar.

Validação: páginas renderizadas e inspecionadas; anexos com conteúdo vetorial e tamanho de página idênticos ao PDF R02; CRC e hashes do ZIP conferidos. Isso verifica montagem/integridade, não levantamento ou compatibilização profissional.
