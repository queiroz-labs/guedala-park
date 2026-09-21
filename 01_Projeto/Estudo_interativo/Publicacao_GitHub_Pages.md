# Publicação do estudo — 13/09/2026

## Envio completo autorizado — 21/09/2026

Após aprovar a referência R03 do quarto, Elias solicitou explicitamente commit e push de tudo feito até agora. Esta autorização amplia o escopo anterior restrito ao site/moodboard para incluir o histórico completo de documentos, estudos e referências do projeto. Os registros anteriores descrevem o escopo daqueles envios, não impedem o envio completo agora solicitado. O artefato do Pages continua restrito aos arquivos definidos em preparar_pages.py; as imagens aprovadas ficam no repositório e nos registros do projeto.

## Parede do banheiro e porta do quarto — 20/09/2026 · publicado

Corrigida a omissão da divisória entre banheiro e acesso do dormitório, recuperando P01/F120. Porta do quarto reorientada para abrir para dentro junto à divisória, com arco na planta, batentes e trecho sobre o vão quando as paredes completas estão visíveis. O piso e o enquadramento do quarto incluem o acesso; paredes compartilhadas aparecem nas vistas dos ambientes correspondentes. Dimensões de vãos permanecem gráficas, sem mudança física proposta.

Commit `549c749997e6455118e9b2583621418e6afa8fa4` publicado pela cópia `tmp/pages-r03`, limitado a quatro arquivos públicos. Verificadas continuidade da parede, existência de um único vão para o banheiro, vão e folha do quarto sem interseção com paredes/móveis, vistas superior/3D e celular, com e sem paredes completas; sem erros JavaScript. Prévia em `tmp/wall-quarto-top.png` e conferência em `tmp/check-bedroom-wall.cjs`.

Após autorização explícita de Elias, publicação concluída: https://github.com/queiroz-labs/guedala-park/actions/runs/35533247115. Confirmados no endereço público o commit exato, o HTML do moodboard e os testes da geometria nas vistas de computador e celular. Demais documentos locais não foram enviados.

## Piso mais próximo da referência — 20/09/2026 · publicado

Preparada e verificada a aproximação visual do piso Olmo, com réguas proporcionais, juntas em terços, variação suave de cor e veios. Banheiro e lavanderia têm módulos ilustrativos de 90 × 90 cm. A ficha de material distingue a representação da amostra física e da paginação final.

Após autorização explícita de Elias, publicado o commit `3ac30dac0a80ec72a70f043ddd5af3d4b4a97ed2` pela cópia `tmp/pages-r03`. Somente cinco arquivos públicos do site/moodboard foram incluídos. Testes de continuidade do desenho entre superfícies, juntas, renderização sem WebGL, profundidade, seleção, animações e telas de computador/celular passaram sem erros JavaScript.

Publicação concluída: https://github.com/queiroz-labs/guedala-park/actions/runs/35532186899. Commit exato e conteúdo do moodboard confirmados no endereço público. Conferência pública de acabamento, continuidade, juntas, giro, alternativa sem WebGL e telas de computador/celular aprovada. Demais documentos locais não foram enviados.

## Correção do forno no 3D — 20/09/2026

Após autorização explícita de Elias, publicada a correção do nicho sob o cooktop: o bloco sólido do módulo foi substituído por volumes ao redor do forno, preservando a posição e o tamanho do equipamento. Enviados somente `src/app.js` e os dois HTML gerados, pela cópia `tmp/pages-r03`, no commit `f35e6b4088e65e33428c853803c462c6ba8c4c05`.

Publicação concluída: https://github.com/queiroz-labs/guedala-park/actions/runs/35531539166. Versão exata confirmada no site público; forno visível e selecionável em quatro ângulos, com e sem interiores em corte, sem interseção com o módulo. Conferidas telas de computador e celular, ausência de erros JavaScript e correção no HTML do moodboard. Demais documentos locais não foram enviados.

## Revisão vigente R05 — 18/09/2026

Atualização solicitada por Elias: correção de oclusão no giro 3D com profundidade por pixel e seleção correspondente; animações entre estados das cadeiras, Bonnie e Daiane, também aplicadas aos demais seletores. Movimento reduzido respeitado. As trajetórias são ilustrativas, sem validação de colisões ou mecanismos.

Incluídas 59 fichas de decisões e 12 consultas de interiores, com desenhos dos aéreos A/B/C/D, gabinete da pia, gaveteiro e guarda-roupa R02. Corte 3D disponível para os armários detalhados. Banheiro atualizado com VIP, Slim como primeira opção, Arion atrás da cuba, gabinete fechado, espelho raso e luz frontal, parede verde única, Livo e estudos de água quente. Vinílico Olmo registrado como preferência. Divisões e medidas não aprovadas permanecem identificadas.

Publicados somente nove arquivos do site/moodboard pela cópia `tmp/pages-r03`, nos commits `d60e3c3` e `b45bf3d31c185338e87a4ebc4c2c6a2f3303d1c7`. Fluxo final: https://github.com/queiroz-labs/guedala-park/actions/runs/35401780662 — sucesso. Versão pública, commit exato e funcionamento confirmados. Sem envio de documentos privados adicionais.

Verificação: faces cruzadas e seleção pela profundidade, órbita completa, sete ambientes nas três vistas, animações intermediárias/finais/reversas, movimento reduzido, interiores, exportação HTML autônoma e larguras 1440/412/340 px. Página e moodboard públicos HTTP 200, sem erros JavaScript ou transbordamento na conferência móvel. Registro local em `Verificacao_R05.json`.

## Revisão R04 — 15/09/2026

Atualização autorizada por Elias: site e aba Decisões incorporam PE12G grafite, espelho Cebrace 50 × 180 cm, escorredor Mini Plurale, pressão Vancouver Effect 3 L, lixeira comum Biovis 15 L e recicláveis Loop 20 L. Planta com espelho e lixeiras nos locais aprovados; fichas da pia e lavanderia atualizadas. Decisões abre com escolhas aprovadas selecionadas. Mantidas as conferências de instalação e medidas.

Publicados apenas seis arquivos do site/moodboard a partir de `tmp/pages-r03`, commit `52e3e4cf6c0e1c4bdd331a9f0bc1ec1a641a18b4`. Fluxo https://github.com/queiroz-labs/guedala-park/actions/runs/35035985134 concluído com sucesso. Endereço público respondeu HTTP 200; versão R04 e conteúdo novo confirmados. Verificadas sintaxe JavaScript, 50 fichas sem IDs duplicados, estados das escolhas e geometria finita. Demais documentos locais não foram enviados.

- Site: https://queiroz-labs.github.io/guedala-park/
- Moodboard: https://queiroz-labs.github.io/guedala-park/moodboard/
- Commit publicado: `bb23813cae8e28142a32da5721e61d04e5e904d7`.
- Publicação concluída: https://github.com/queiroz-labs/guedala-park/actions/runs/34777056246.

Elias escolheu explicitamente publicar apenas o site e o moodboard, preservando os demais documentos novos localmente. O commit completo `8f0a2ae` foi salvo, mas não foi enviado. A publicação usa um commit separado com 14 arquivos de HTML, fontes, imagem, SVG do interior incorporado, instruções e configuração. Nenhum novo PDF, áudio, pesquisa ou registro do apartamento foi incluído nesse envio. Arquivos que já estavam no repositório remoto antes desta solicitação não foram removidos.

## Continuidade

A cópia principal do projeto mantém o histórico completo local. A branch `codex/pages-publication`, no diretório de trabalho `tmp/pages-publication`, contém a versão pública e foi enviada a `origin/main`. As duas linhas de histórico têm escopos diferentes: não enviar nem mesclar o histórico completo local para o remoto sem nova autorização explícita para os documentos.

Para atualizar o site, transferir somente as mudanças pertinentes aos arquivos públicos para a branch de publicação, reconstruir e conferir o artefato `.site`, criar o commit e enviar a `origin/main`. O fluxo do GitHub publica automaticamente os dois HTML e a imagem. A pasta `.site` local e auxiliares em `tmp` são ignorados pelo Git.

Verificação final no endereço público: página principal e moodboard abriram; estados e conta de circulação funcionaram; imagem de materiais respondeu; layouts de computador e celular sem transbordamento horizontal nem erro JavaScript nos testes. Validação em emulação de 1440 × 1000 e 412 × 915 pixels lógicos.

## Revisão R02 publicada — F158

Após autorização explícita de Elias, publicados somente os seis arquivos do site e moodboard com correções dos aéreos, tanque/lava e seca e ducha. Commit bb23813; fluxo 34777056246 concluído com sucesso. Versão pública R02 confirmada por versao.json e testes de página principal/moodboard em computador e celular emulados, sem erros ou transbordamento.

## Revisão R03 publicada — 15/09/2026

Após autorização explícita de Elias, publicados seis arquivos do site e moodboard com as decisões até 15/09: prateleiras acima/abaixo da TV, acabamentos Inox Look, posição dos aparelhos, purificador compacto candidato, organização dos aéreos A/B/C/D, gabinete da pia e gaveta baixa com rodas. Commit `f3723c0bf7a91273729f553dd703e96fc7fa8514`, na branch local `codex/pages-r03` em `tmp/pages-r03`, enviado a `origin/main`. Fluxo `35029516857` concluído com sucesso. Página principal e moodboard responderam HTTP 200 e exibiram R03; `versao.json` confirmou o mesmo commit. Validação visual local realizada em computador e celular emulado. Medidas e instalações pendentes continuam identificadas nas fichas.
