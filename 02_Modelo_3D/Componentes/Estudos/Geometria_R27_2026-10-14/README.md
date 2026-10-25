# R27 — representação oficial de dois perfis G2

Apartamento atual · [Alteração](Restauracao_R27.json) · [Conferência salva](Verificacao_R27.json). R26 e anteriores preservadas. Não mudou programa, ferragens, cursos, posição habitual da lixeira ou envelopes dos armários.

## Erro digital corrigido

A conferência adicional das cotas superiores revelou que **dois perfis fixos G2 tinham Shape nativa inválida**, embora o documento não apresentasse objetos com estado `Invalid`. Eram `MontagemG2R007` e `MontagemG2R014`, artigos48346342/49027541. O relatório original R07 já registrava `valid:false`; a montagem antiga fazia duas chamadas `transformGeometry`, convertendo a geometria em superfícies B-spline.

As peças correspondentes da fonte oficial `Fonte_G2_BlUM.FCStd`, obtida do STEP configurado já arquivado, são válidas. A R27 restaura essas formas **com a transformação rígida original preservada emPlacement**, evitando a conversão de superfícies. Não usou reparo automático, alteração de tolerância, corte, rebaixo, deslocamento físico ou substituição de produto. As guias continuam referências estáticas; não são telescópio animável.

## Evidência e alcance

[Diagnóstico](../Pendencias_autonomas_2026-10-14/Diagnostico_perfis_G2.json): fontes oficiais válidas, montagens spline antigas inválidas; limites locais concordam dentro de0,0000001 mm e1.096 vértices correspondentes concordam dentro de0,000000000001 mm.

[Comparação amostrada de superfícies](../Pendencias_autonomas_2026-10-14/Equivalencia_perfis_G2.json):10.188 pontos em arestas e3.508 em faces, em ambos os sentidos; maior distância4,56×10⁻¹³ mm. Isso é comparação numérica amostrada, não tolerância física nem prova de movimento. A forma adotada é a própria fonte oficial sob o mesmo mapeamento rígido, não uma forma reconstruída pelas amostras.

A integral de volume da representação oficial difere da antiga inválida em8,284 e8,212 mm³, respectivamente. Essa diferença foi registrada, não escondida nem usada para afirmar remoção/adição física de material. A ocupação nominal e as superfícies amostradas coincidem; não apagou os contatos de perfil/fundo anteriormente registrados, cuja causa continua desconhecida.

Foram comparados os5.899 objetos anteriores: somente a Shape/Placement local dos dois perfis e seus textosStatus mudaram; pais, expressões, vínculos, visibilidades e demais Placements preservados. As coordenadas globais dos vértices concordam dentro de9,38×10⁻¹³ mm. Os novos Placements locais representam a orientação que antes estava incorporada às superfícies, mantendo a posição física no apartamento.

Na versão salva, **925 formas nativas atuais válidas**, nenhum objetoInvalid e lixeira emAfastamento0. Essa checagem não inclui históricos ou cópias auxiliares transformadas. Algumas dessas cópias auxiliares usadas para diagnóstico de outras ferragens retornam validação negativa após reposicionamento; as formas nativas correspondentes são válidas, e não foram alteradas para apagar esse resultado. Os arquivos de diagnóstico preservam essa distinção.

Não repetiu movimentos, varreduras gerais, bandejas, galerias ou auditorias de contatos internos. Novos scripts executados somente nos dois perfis e na validade nativa da versão salva. Scripts impedem sobrescrever revisões existentes.

## Limites vigentes

Fixação, carga, tolerâncias físicas, contatos internosSTEP/fundo, batentes, 70T3553, ferragens do correr/cesto/rodas e instalações continuam pendentes. [Complemento de alturas e fontes](../Pendencias_autonomas_2026-10-14/README.md). Sem liberação de corte, furação, compra ou fabricação. Última revisão Astra nesta mesma conversa permanece reservada para18h30.
