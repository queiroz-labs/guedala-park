# Ensaios de oficina — pacote para envio

[Caderno em PDF](Caderno_ensaios_oficina.pdf) · [ZIP completo](Pacote_ensaios_oficina.zip) · [Fontes e integridade](Manifesto.json) · [Caderno-fonte](../../04_Moveis/Ensaios_oficina/Caderno.md).

Todos os ensaios permanecem **pendentes de execução**. O pacote contém o caderno, o CSV vazio, o verificador e uma seleção explícita de documentos, mapas e desenhos de origem. Não inclui o modelo FreeCAD nem documentos personalizados.

Extraia todo o ZIP e abra `Ensaios_oficina/COMECE_AQUI.html`. O registro corrente é `Registro.csv`; formulários das fontes servem apenas para consulta. As versões HTML das fontes permitem leitura offline e apontam somente para arquivos incluídos. Referências complementares fora da seleção estão relacionadas no manifesto; endereços de fabricantes exigem internet. Os originais Markdown são preservados para rastreabilidade.

As fontes registram hipóteses e estudos; o caderno informa as etapas e os bloqueios para cada prova. Nenhuma medida ou resultado foi preenchido. Fotos, laudos e identificação pessoal da oficina devem ficar na cópia privada.

Gerar com `python -B ferramentas/estudos/empacotar_ensaios_oficina.py`, usando ReportLab/pypdf e fontes Arial do Windows. O script confere CSV sem dados, CRC/SHA256 das entradas e links locais das versões HTML. O PDF deve ser renderizado e revisado após mudança de conteúdo. O ZIP inclui manifesto com hashes; o manifesto externo tem os mesmos bytes.

Publicação solicitada por Elias em 28/10/2026 nesta conversa: “pode fazer o push e atualizar o site com essas infos”. A biblioteca do site apresenta os downloads e a situação dos ensaios, sem diário de alterações.
