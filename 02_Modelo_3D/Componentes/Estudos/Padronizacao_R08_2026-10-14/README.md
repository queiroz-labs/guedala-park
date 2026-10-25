# Nove gavetas com montagem comum — R08

Nota vigente de 14/10, R28: o campo histórico `payload_formula_kg` em Carga_R08 subtrai também o conteúdo e, portanto, expressa **margem restante**, não carga útil disponível. Histórico preservado. O [quadro de carga atualizado](../Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html) separa as duas fórmulas e inclui explicitamente a madeira das bandejas G2; materiais, massas reais e capacidade comercial continuam pendentes.

Apartamento R08 preservado · [Dimensões](Padronizacao_R08.json) · [Auditoria](Auditoria_R08.json) · [Alturas e profundidades](Alturas_e_profundidades_R08.json) · [Carga](Carga_R08.json)

R08 conserva G2 da R07 e padroniza outras oito caixas como propostas parametrizadas a partir de sua montagem oficial: quatro roupeiro, G1/G3 e duas escritório. Rasgo lateral5, fundo15/recuo12, dianteira16 e duas travas T51.7600; frentes, implantações e cursos anteriores preservados. Não são oito configurações individuais homologadas pela Blum. Sem corte, furação ou compra liberados.

Larguras internas313/541/322 e externas343/571/352 mm, para LW355/583/364 e laterais15. Laterais490/390 para NL500/400. Espaço interno superior em profundidade459/359 mm. Furos e ferragens não foram escalados. As cinco peças de caixa e a frente têm geometria comum parametrizada pelos gabaritos da R07. Furos traseiros Ø6/10 e referências de ligação da dianteira derivam da montagem oficial de G2; fixação individual ainda a conferir. Gaveta baixa de limpeza permanece com mecanismo próprio pendente.

Os32 perfis400/500 das oito caixas,16 travas e48 peças de madeira são sólidos válidos. A transformação rígida dos perfis foi conservada no Placement, sem expressões de movimento próprias: converter suas superfícies para B-spline causou invalidade e foi corrigido. Nenhum perfil principal foi convertido em telescópio animável. Guias ficam no módulo; caixas/travas movem por translação rígida.

As oito caixas alteradas passaram160 posições0–500/400 mm contra estrutura, demais caixas fechadas, perfis de outras gavetas, paredes e referências consideradas. Ensaios anteriores intactos não foram repetidos. Madeira sem interpenetrações; perfis não interceptam a estrutura dos armários.18 pequenas sobreposições perfil/fundo permanecem nas nove caixas, semelhantes às52/54 mm³ da própria montagem oficial R07; causa desconhecida, sem usinagem adicional inventada.

## Folgas nominais

G2: fundo em z628 e menor cota da guia fechada G1 em z744,4: **116,4 mm**. Programa com reserva111: **5,4 mm restantes**, sem garantia de regulagem, tolerância ou flexão. `optimalBoundingBox` usado no fundo: a BoundBox comum de sua B-spline expandiu1,196 mm após translação; vértices/caixa ótima mantêm o topo628. Não confundir esse artefato com mudança da madeira.

Até primeiro obstáculo nominal: roupeiro inferior106,4/superior85; G3340,4/G1112; escritório inferior60,4/superior54 mm. G1 foi confrontada com a bancada CAD em z900, módulo em z180, referência inferior relativa720; bancada ainda reserva sem recortes executivos.

Margens nominais atrás do perfil: roupeiro49,505; cozinha71,505; escritório11,505 mm. A caixa passou a apoiar diretamente atrás da frente18, eliminando o afastamento hipotético7 mm; o corpo não foi alongado nem a implantação ampliada. O escritório ainda chega à referência da cama preparada em y1100 quando abre400, sem margem de uso comprovada nessa configuração.

NL500 do roupeiro continua candidato; `CursoNominal`400 preservado.40 kg também é candidato e inclui caixa/frente/conteúdo. Volumes de madeira e fórmula de massa em `Carga_R08.json`; densidade, pesos reais, organizadores, conteúdo e componentes móveis não medidos. Não interpretar40 kg como carga útil disponível para objetos. Não foram replicadas automaticamente quantidades/furações de parafusos dos apoios.

## Continuação

A R09 incorpora esta revisão e corrige controles das portas comuns, que abriam para dentro. `Inventario_portas_R08.json` e `Diagnostico_porta_pia_R08.json` registram a descoberta. Demais dobradiças físicas, apoios das folhas intermediárias, fixação e carga continuam a desenvolver. Manter montagem comum e não repetir testes prontos sem mudanças.

Reprodução das caixas: `padronizar_gavetas.py`; auditoria: `auditar_gavetas.py`. Gerador cria novo arquivo se R08 já existir e preserva caixas anteriores ocultas. Demais levantamentos registram estado nominal salvo fechado.
