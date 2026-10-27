# Gerador de pranchas

Fonte de campo: `07_Imovel/Medidas_e_impactos.csv`. Topologia e vínculos: `06_Entregas/Planta_cotada/Cotas.json`. O campo `valor_medido` vence o nominal; números exigem unidade. Vazio significa pendência, nunca zero.

`exportar.py` abre o FCStd oculto, lê envelopes globais e fecha sem salvar ou recalcular. Exportação em `06_Entregas/Caderno_pranchas/Geometria.json`, com SHA256. Grupos agregados não duplicam as peças. A montagem BC43 integra P18. O comando de exportação é separado da regeneração de desenhos: atualizar uma medida não abre o CAD.

As coordenadas R53 são espelhadas em X em relação à planta do site; a referência de conversão está no CSV. A geometria exportada é nominal e não substitui medidas de campo. As caixas são envelopes, não desenhos de usinagem ou perfis exatos das ferragens.

Gerar tudo: `python ferramentas/pranchas/gerar.py`. Saídas vetoriais SVG/HTML/PDF compartilham coordenadas em mm de papel. [Uso, folhas, fontes e limites](../../06_Entregas/Caderno_pranchas/README.md). O gerador antigo que apenas juntava imagens foi removido.

Teste integrado: `python ferramentas/pranchas/testar.py --temporarios CAMINHO_FORA_DO_REPOSITORIO`. Copia apenas fontes necessárias, executa o comando real, verifica variação de 130 mm, conflitos, origem, escala, idempotência e recusa de entrada inválida; apaga a própria cópia. Resultado de 27/10: 12 elevações, 99 cotas alteradas, quatro conflitos de 80 mm; originais preservados.
