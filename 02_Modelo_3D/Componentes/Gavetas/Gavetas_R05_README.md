# Gavetas — conferência dimensional R05

Apartamento editável · [Gavetas do escritório abertas](Escritorio_gavetas_400_R05.png) · [Dimensões](Caixas_dimensoes_R05.json) · [Percursos](Conferencia_caixas_R05.json) · [Alturas](Alturas_R05.json)

A R05 preserva o canto simples da R04 e desenvolve nove caixas de gaveta com uma referência comum de corrediça oculta. MOVENTO 760H foi usada como candidata para conferir dimensões; marca e amortecimento não estão aprovados para compra. A gaveta baixa de limpeza permanece com seu mecanismo próprio pendente.

## Dimensões propostas

| Grupo | Quantidade | Vão entre apoios | Largura interna da caixa | Largura externa, laterais15 | Lateral da caixa |
|---|---:|---:|---:|---:|---:|
| Roupeiro | 4 | 355 mm | 313 mm | 343 mm | 490 mm, NL500 candidato |
| Cozinha G1/G2/G3 | 3 | 583 mm | 541 mm | 571 mm | 490 mm, NL500 candidato |
| Escritório | 2 | 364 mm | 322 mm | 352 mm | 390 mm, NL400 candidato |

O requisito **LW−42 se refere à largura interna**, não externa. Com laterais15 mm, a largura externa é LW−12. As caixas antigas de estudo estavam14 mm mais estreitas. Comprimento da lateral: NL−10. Fundo recuado12 mm, espessura15 como hipótese construtiva; ligação/encaixe do fundo e furação de gancho/travas ainda pendentes. [Planejamento oficial MOVENTO](https://publications.blum.com/2024/catalogue/en/413/) e [guia de construção da Blum](https://ea.blum.com/en/building-a-movento-drawer/).

A margem em profundidade, usando NL+3 e a referência adotada do início da caixa, é42 mm no roupeiro,64 na cozinha e somente4 no escritório. Confirmar calços, fundo real, montagem e regulagens antes de fechar essa última condição.

## Correções da representação CAD

- **Escritório:** o arquivo anterior abria as gavetas para a parede, contrariando R10. A R05 mantém o mesmo envelope x2700..3100/y250..700 e muda a orientação para que a frente fique em y700 e avance para+Y. A antiga representação interceptava a parede em845.352 mm³ no curso300. Frente em y1100 com curso400, conforme o ensaio documental aceito.
- **Folha direita inferior do roupeiro:** `App::PropertyLength` não aceitou o deslocamento negativo usado no teste. Corrigida a expressão para `985 mm − Deslocamento`; abrir para a esquerda agora usa985 mm positivos. Isso é uma correção do controle CAD, não validação de trilhos.
- Fontes do gerador geral corrigidas para conservar ambos os sentidos em gerações futuras. R01/R04 salvas não foram reconstruídas nem sobrescritas.

## Conferência realizada e limites

Nove gavetas, **181 posições de translação rígida**, em passos25 mm até500/400 conforme a candidata. Sem interseções relevantes (>0,1 mm³) entre as peças móveis e estrutura considerada, outras gavetas, paredes, bancada e referências de móveis do cenário diário. As54 peças individuais das nove gavetas são válidas e não se interpenetram na montagem da caixa. Portas inferiores do roupeiro deslocadas idealmente para liberar o lado em ensaio.

O escritório chega exatamente à linha y1100 adotada para a cama preparada: **não há margem de uso comprovada nesse modo**. A verificação cobre o cenário diário; altura real da cama e roupa de cama continuam pendentes.

NL500 do roupeiro foi testado apenas como candidato. O `CursoNominal` anterior de400 está preservado. A ausência de colisão rígida não resolve alcance, passagem de uma pessoa ou a instalação real das portas de correr.

As corrediças STEP ainda não estão montadas no apartamento. `Fontes_MOVENTO.FCStd` e JSON contêm pares esquerdo/direito de400/500, com sólidos válidos. Cada perfil principal chega como um único sólido, sem separação das etapas telescópicas; não tratar o STEP estático como mecanismo animável homologado.

## Alturas e conteúdo

A parede da caixa não é o limite superior para objetos: o vão até o primeiro obstáculo é o que governa. G2 tem parede73 mm acima do fundo, mas o planejamento estima **116,5 mm até a corrediça superior**, usando o requisito de28,5 mm abaixo do fundo. São5,5 mm acima dos111 exigidos pelo programa de utensílios/ frigideira; confirmar com a geometria instalada e regulagens. Não é uma folga real garantida.

Estimativas: G3 340,5 mm; G1 112; roupas inferiores106,5/superiores85; escritório inferior60,5/superior54. Detalhes e primeiro obstáculo em `Alturas_R05.json`.

Os organizadores de G2 anteriormente propostos com460 mm de profundidade coincidem com o fundo interno disponível de460: falta folga de fabricação/retirada. Próximo passo: encurtar as bandejas removíveis como proposta e reconferir os gabaritos, preservando composição e frentes16/16/40 aprovadas.

## Continuação

Confirmar posição dos perfis e travas comuns, furação traseira, carga e encaixe do fundo; depois conferir conteúdo e demais portas. Evitar acrescentar mecanismos ou perder inventário para forçar encaixe. As medidas são propostas de projeto, não lista de corte ou compra.

Reprodução: `../../../ferramentas/componentes/Gavetas/ajustar_caixas.py`, `../../../ferramentas/componentes/Gavetas/conferir_caixas.py` e `../../../ferramentas/componentes/Gavetas/conferir_alturas.py`, nessa ordem. O gerador preserva R04 e gera outra revisão se R05 já existir. Os auditores selecionam a R05 canônica pelo arquivo; adaptar explicitamente o destino se estiver trabalhando numa revisão com timestamp.
