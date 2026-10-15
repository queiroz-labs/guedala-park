# Montagem comum de G2 — R07

[Apartamento atual](Guedala_Park_R07_Montagem_G2.FCStd) · [Detalhe isolado](Detalhe_G2_R07.FCStd) · [Vista CAD](G2_montagem_R07.png) · [Auditoria da montagem](Montagem_G2_R07.json)

A R07 incorpora o apartamento R06 e aplica a G2 a montagem oficial configurada MOVENTO500/40 kg, BLUMOTION e travas T51.7600. São candidatos de ferragem e construção; não há liberação de corte, furação ou compra. R06 e anteriores preservadas. Demais gavetas continuam na representação R05.

As duas bandejas455 mm e os nove gabaritos permanecem. A frente externa continua617×156×18 mm, no mesmo lugar; frentes aprovadas16/16/40 cm preservadas. A caixa passa a apoiar diretamente na frente, avançando7 mm em relação à hipótese anterior. Peça dianteira16 mm, traseira/laterais15, fundo15/recuo12; fundo físico551×490 inclui encaixes em rasgos laterais5 mm e passagem sob travessas. O espaço superior interno disponível é541×459, com2 mm à frente e atrás das bandejas. Abertura e retirada dos gabaritos foram reconferidas após a alteração, sem interferências no cenário considerado.

As seis peças de madeira e duas travas têm formas individuais válidas. Madeira, bandejas e gabaritos não se interpenetram. Caixa e travas passaram21 posições rígidas0–500 mm contra estrutura, outras gavetas e bancada consideradas. `Percurso_caixa_G2_R07.json` e `Percursos_G2_R07.json` registram o escopo. Não se trata de animação homologada das etapas telescópicas: o perfil principal STEP continua sendo um único sólido estático. As guias ficam no módulo; as travas acompanham a caixa. A representação aberta com esses perfis estáticos não demonstra o mecanismo real.

Há sobreposições nominais pequenas entre perfis oficiais e fundo oficial:52,14 e54,04 mm³. Ambos vieram da mesma montagem configurada, aplicada por transformação rígida. Causa ainda não determinada; não ampliar furações/rebaixos nem deslocar peças para apagá-las. `Sobreposicao_G2_R07.json` registra o diagnóstico inicial; sua BoundBox também abrange contatos de superfície e não identifica isoladamente cada região volumétrica. Os dez cilindros EURO são referências de fixação, com penetração prevista nos apoios, não ferragens detalhadas de rosca nem confirmação de quantidade executiva.

O limite nominal40 kg precisa ser confrontado com peso da caixa, frente e conteúdo, ainda não medidos. Fixação dos apoios, material, tolerâncias, regulagens, pega/rigidez das bandejas e altura até a guia da G1 continuam pendentes. A estimativa anterior116,5 mm de altura não é prova da montagem superior, ainda não instalada.

## Fontes e reprodução

Conta Blum existente, configurador de produtos detalhado em14/10/2026. Sem estabilização lateral, sem acionamento elétrico. Parâmetros aceitos: LW583, NL500,40 kg, EURO, caixa100/16/15/15/recuo12; frente617/156/18, recobrimentos17/17/**3,5**. O campo inferior usa referência própria da instalação, não o afastamento até a base da lateral. O valor inicial20 produziu frente16,5 mm mais baixa e foi corrigido antes de montar a R07.

STEP aplicado: `../G2_R06_2026-10-13/Blum_configurado/G2_MOVENTO_500_40kg_Recobrimento3_5.STEP`; importação nativa preservada em `Fonte_G2_BlUM.FCStd`. Desenho atual PDF/DXF em `Fabricacao_corrigida/productionDrawings/`; a página5 foi inspecionada e tem cota72,5 até os furos da frente. PDF anterior na R06, com89 mm, é histórico e não deve ser usado para a R07. Situação de instalação com GIF/DXF oficiais em `../G2_R06_2026-10-13/Blum_configurado/Instalacao/`.

`montar_g2.py` aplica a montagem; preserva a caixa R06 em grupo histórico oculto. `conferir_percursos.py` confere as bandejas após a mudança. Selecionar documentos pelo caminho resolvido, porque FileName mistura barras. Não fechar documentos alheios. Vista isolada renderizada em arquivo próprio; apartamento salvo fechado.

Próximo: padronizar as demais caixas com montagem comum compatível, instalar guia G1 para conferir altura efetiva de G2, fixação/carga; avançar nas portas comuns. Não repetir os21/181 ensaios nem insistir nas sobreposições sem dados novos.
