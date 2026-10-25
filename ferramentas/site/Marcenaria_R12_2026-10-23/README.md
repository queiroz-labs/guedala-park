# Consulta de marcenaria R12

Site: https://queiroz-labs.github.io/guedala-park/
Figma: https://www.figma.com/design/ChOvYeL6ULhHR3GEGgcukZ?node-id=2-2

Consulta por seis ambientes e 20 módulos, visualização 3D/2,5D, isolamento e seleção de peças, medidas em milímetros, ferragens, acabamentos, impressão e CSV. Biblioteca com fontes explícitas e arquivos FreeCAD. O dossiê está em `06_Entregas/Dossie_marcenaria_R45.html`.

## Dados e limites

383 formas visíveis extraídas da R45; 249 linhas de painéis, sendo 121 com material rastreável e 128 com acabamento não especificado. Quantitativos não constituem plano de corte. Dimensões são envolventes nominais; não substituem cotas acabadas, recortes, veios, bordas, folgas, furação e fixações. Estudos R47 e torneiras são complementares, não substituem a R45.

## Reprodução

Execute `python ferramentas/site/preparar_pages.py` na raiz. A saída `.site` é publicada pelo workflow Pages. Para regenerar a geometria, execute `export_cad.py` desta pasta com o Python distribuído com FreeCAD 1.1.4; o exportador abre o FCStd sem salvar e verifica o SHA256. Depois regenere o site.

## Verificação

Inspeção visual em desktop e celular (412 px), seleção dos 20 módulos, isolamento, busca documental e download CSV. Verificação estática de JavaScript, links e allowlist documental; relatórios anexos. Os documentos disponíveis não incluem liberação executiva de fabricação: as pendências permanecem explícitas nas fichas.
