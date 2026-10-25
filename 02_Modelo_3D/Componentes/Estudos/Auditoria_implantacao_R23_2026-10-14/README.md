# Implantação estática R23 contra arquitetura vigente

A auditoria global da implantação **salva** encontrou duas interpenetrações volumétricas do sofá-cama do escritório com uma parede inteira. Também identificou um volume histórico do tanque exibido por um vínculo ativo. Nenhuma peça CAD foi alterada; os achados foram encaminhados ao responsável para revisão da correção. O apartamento auditado continua sendo a R23 com SHA-256 `cf515686f48057c3b9e025bee28f3ddac735ea73608e401133e5fc842a972eea` antes e depois.

## Seleção e cobertura

O manifesto usa a composição nativa App::Link da R20, realmente salva na R23, e a visibilidade de seus filhos em `GuiDocument.xml`, reconciliada com as exclusões explícitas da R22. Uma raiz-fonte oculta não é descartada quando seu vínculo espelhado está ativo. Dentro dos módulos, foram selecionados os resultados finais e assemblies vigentes visíveis; históricos nomeados, canto articulado R03, operandos booleanos e referências duplicadas ocultas foram excluídos. Trinta e dois eixos referenciais RO62, visíveis mas sem volume/sólidos, ficaram fora do teste volumétrico.

Foram selecionados **20 módulos**, 173 raízes gráficas e **927 resultados sólidos exibidos**. Uma revisão da atualidade separou essa contagem em **926 resultados vigentes e um volume histórico exibido indevidamente**, `Peca358`. Esse último permaneceu apenas como extra conservador no cruzamento original; não teve interpenetração arquitetônica e os testes não foram repetidos para retirá-lo da contagem atual.

Arquitetura: **27 paredes inteiras e nove pisos**. Não existe sólido de teto na composição selecionada; **não foi feita comprovação de colisão com teto**. A classificação arquitetônica utiliza o grupo fonte `ParedesInteiras` e os pisos explicitamente identificados como `Arquitetura de estudo`, não a palavra “parede” em componentes de bandejas, perfis ou reservas hidráulicas.

O [manifesto](Manifesto_implantacao_R23.json) registra nomes, rótulos, raiz proprietária, ambiente, vínculo, BBox global no referencial-fonte, matrizes e volumes. O espelhamento comum `Xnovo=7400−Xbase` conserva as interseções e permitiu conferir as fontes sem fazer novos sólidos refletidos.

## Resultado efetivamente calculado

| Etapa | Quantidade |
|---|---:|
| Pares resultado × arquitetura | 33.372 |
| Separados pelo BBox | 33.210 |
| BBox apenas na fronteira | 160 |
| Candidatos volumétricos / booleanos calculados | 2 / 2 |
| Interpenetrações acima de 0,1 mm³ | 2 |
| Erros booleanos | 0 |

Tempo da auditoria: **7,218 s**. Processo `FreeCADCmd.exe` 1.1.4 em modo seguro, sem interface, pose nova, salvamento, reparentamento ou mudança de geometria/parâmetros. O limiar de 0,1 mm³ é triagem CAD e não tolerância certificada. BBox com epsilon de 0,000001 mm serve para filtrar candidatos; os dois candidatos positivos foram confirmados por `Shape.common()`.

Os 160 pares de BBox na fronteira são **possíveis contatos de implantação/apoio**, incluindo peças no piso ou junto à parede. Não são chamados de penetração volumétrica nem de contato físico/fixação comprovados. Não houve novo ensaio de movimentos ou colisão interna de ferragens.

## Achados positivos

| Peça atual | Parede | Volume comum (mm³) | BBox do contato no apartamento espelhado: X / Y / Z (mm) |
|---|---|---:|---|
| Peca122 — corpo do sofá-cama Daiane | Peca017 — parede Quarto004 | 39.200.000 | 4850–4950 / 1520–2920 / 80–360 |
| Peca124 — parte traseira do sofá-cama Daiane | Peca017 — parede Quarto004 | 63.920.000 | 4850–4950 / 1540–2900 / 350–820 |

As sete primitivas vigentes do sofá são `Peca122` até `Peca128`, vinculadas por `EspelhoPecaR036` até `EspelhoPecaR042`, todas exibidas. O envelope do corpo no referencial-fonte vai de X1670 a2570, enquanto o interior do escritório começa emX2550. Portanto o sofá está majoritariamente no lado do quarto, não apenas encostado na face da parede.

[Diagnostico_sofa_historico.json](Diagnostico_sofa_historico.json) preserva os BBox e matrizes, as propriedades XML das sete peças e as oito entradas Daiane da `Base_interativa.json`. O programa aprovado é 140×90 cm fechado / 140×182 cm aberto, com braço junto à parede da porta no cotidiano e cama girando rumo à janela. O documento informa posições finais, não trajetória validada.

A origem documental tem `rootX=257`, `rootZ=222`, `yaw=−π/2`, em coordenadas XZ com eixo vertical Y. A fonte CAD usa rotação Rz−90° em XY. **Há uma hipótese concreta de inversão de sinal na conversão entre essas convenções**, encaminhada ao responsável para conferir o gerador. Não foi executada translação, rotação, espelhamento local ou redução de sofá por esta auditoria.

## Histórico do tanque exibido

`Peca358` está rotulada “Histórico oculto - volume útil aproximado anterior do tanque”. Sua visibilidade-fonte é falsa, mas `EspelhoPecaR123` está visível no arquivo salvo. Portanto existe um erro de exibição real: não foi simples seleção acidental de uma peça oculta. O manifesto marca `adoption_scope=historical_display_error` e a lista `retired_visible_roots`; esse objeto não pode ser apresentado como geometria vigente do tanque. O responsável também está verificando seus encontros com o cesto em entrega separada.

## Limites

Este resultado cobre apenas o estado salvo dos sólidos selecionados contra as paredes inteiras e pisos existentes. Não cobre todas as posições de movimento, superfícies inexistentes do teto, medidas reais, revestimentos, tolerâncias, cargas, fixações, pessoas, manutenção ou ventilação. Equipamentos e volumes de conteúdo continuam gabaritos com os limites documentados nas respectivas revisões. Não transforma fontes simplificadas em produtos homologados.

As colisões entre módulos/móveis distintos são trabalho separado do responsável, reutilizando o mesmo manifesto. Não foram duplicadas aqui. Nenhum contato foi apagado, histórico excluído do CAD ou programa alterado para chamar o conjunto pronto.

## Arquivos da entrega

- `inventariar_implantacao.py` / `Manifesto_implantacao_R23.json`: seleção explícita e classificação dos resultados atuais/extras históricos.
- `auditar_arquitetura.py` / `Auditoria_arquitetura_R23.json`: pares, BBox, candidatos, volumes comuns, coordenadas dos achados, contatos de fronteira e hashes.
- `Diagnostico_sofa_historico.json`: propriedades salvas e correspondência documental dos dois achados.

Não há corte, furação, compra, instalação de dependências, contato com fornecedores ou liberação de fabricação.
