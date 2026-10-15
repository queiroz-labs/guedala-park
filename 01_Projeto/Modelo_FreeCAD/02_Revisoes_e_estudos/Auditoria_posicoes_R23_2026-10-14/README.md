# Auditoria estrutural de posições - R23

Leitura independente de `Document.xml`, `GuiDocument.xml`, inventários e fonte gráfica. Nenhuma GUI, runtime CAD, salvamento, teste de movimento, colisão ou comparação de checksum em massa foi usado. O apartamento R23 permaneceu intacto. As correções abaixo são entregues para integração/revisão pelo responsável; esta pasta não contém uma revisão CAD nova.

## Resultado útil

**Duas inconsistências factuais exigem correção localizada:** implantação do sofá Daiane com sinal de rotação importado incorreto e exibição do volume histórico do tanque. Há também duas peças Daiane que a fonte gráfica torna invisíveis na rotina diária e que o CAD exibe. A composição espelhada propriamente dita e a cobertura dos módulos/controles não apresentaram lacuna estrutural nesta leitura.

### Sofá-cama Daiane do escritório

O estudo existente do escritório R07 descreve o envelope diário local x2..92/y152..292cm, com origem global X255cm. Portanto, o envelope de planta de base é **X2570..3470/Y1520..2920mm**. O `Base_interativa.json` incorpora essa mesma implantação: raiz2570/2220mm e yaw−90°. Não é o sofá Bonnie da sala.

`Estudo_interativo/src/app.js`, função `mesh`, transforma X/Z por `[cos,+sin;−sin,cos]`. No referencial CAD X/Y isso equivale a **Rz=−yaw**. O importador `gerar_modelo.py`215–218 usa **Rz=+yaw** e gira a origem em torno da mesma raiz. Isso importou as sete peças Daiane para o lado contrário da raiz. Por exemplo, Peca122 ocupa X1670..2570, em vez de X2570..3470; Peca124 ocupa X2380..2570, em vez de X2570..2760. Y, Z e dimensões são coerentes com as peças simplificadas da fonte.

Restaurar a implantação documentada exige girar rigidamente as sete peças em180° em torno da raiz(2570,2220,0) ou aplicar os placements equivalentes da evidência. Uma translação única não corrige encosto/frente e distribuição das peças. A implantação espelhada restaurada ocuparia X3930..4830/Y1520..2920. Não se alterou modelo, dimensão ou definição de uso do sofá.

| Nó fonte | Peça CAD | Vínculo espelhado | Exibição diária da fonte |
|---|---|---|---|
| daiane/round/1 | Peca122 | EspelhoPecaR036 | Visível |
| daiane/round/2 | Peca123 | EspelhoPecaR037 | Visível |
| daiane/round/3 | Peca124 | EspelhoPecaR038 | Visível |
| daiane/round/4 | Peca125 | EspelhoPecaR039 | Visível |
| daiane/round/5 | Peca126 | EspelhoPecaR040 | Visível |
| daiane/round/6 | Peca127 | EspelhoPecaR041 | **opacity0**, somente referência do modo hóspedes |
| daiane/round/7 | Peca128 | EspelhoPecaR042 | **opacity0**, somente referência do modo hóspedes |

O importador não tratou opacity0. Os dois últimos vínculos estão visíveis na R23 diária. Ocultá-los nessa pose restaura a exibição original sem apagar as referências de hóspedes. Não comprova mecanismo ou trajetória real do sofá.

### Histórico antigo do tanque

`Peca358` tem rótulo explícito de histórico oculto e VisibilityFalse. `montar_cesto.py`73–76 o ocultou ao criar o tanque atual R15, `PecaCestoR022`. Porém, seu vínculo **EspelhoPecaR123** está VisibilityTrue tanto no XML do objeto quanto no GUI, dentro de VistaAmbienteR004 e ApartamentoEspelhadoR20 também visíveis. Assim, a fonte histórica reaparece pela composição.

É uma caixa380×350×200mm, base2630/6500/700; espelho X4390..4770/Y6500..6850/Z700..900. LinkTransformTrue e reflexão correta. A ação indicada é ocultar esse vínculo, preservando a fonte e o tanque atual. Não reduzir ou retirar o tanque vigente para apagar interferências.

## Cobertura e estados salvos

- 237 vínculos espelhados/237 fontes únicas,209 vínculos visíveis na R23. Todos têm a matriz de reflexão Xnovo=7400−Xbase, Y/Z preservados, LinkTransformTrue; sem vínculo para outro vínculo ou pai geométrico acrescentando segunda reflexão. Nenhuma raiz original geométrica foi encontrada diretamente visível além da composição.
- Todos20 módulos do inventário possuem exatamente um vínculo visível e dimensões de corpo XML iguais ao inventário. Os13 componentes de equipamentos selecionados estão presentes e vinculados. Três peças Loop são corpo/tampa/pedal distintos; duas E21 são corpo/duto, não duplicações da mesma fonte.
- Quatro raízes geométricas não compostas são referências antigas de canecos, todas ocultas em ReferenciasFerragens. Não são módulos ou equipamentos vigentes faltantes.
- 45 controles têm campos/rótulos/atalhos coerentes com o catálogo. Os11 atalhos permanecem ocultos e apontam para os objetos originais.51 vínculos diretos simples de campos numéricos têm valores iguais aos controladores. Os campos de operação estão em0, exceto a entrada ideal do banheiro90°, estado de base documentado; B2/B3 do canto são células de planilha em0deg, não propriedades ausentes.
- 28 itens de programa selecionados têm existência e cobertura:15 conteúdos do banco R16,4 cabos/cabeças da baixa R13 e9 gabaritos G2. Eles não substituem o inventário de todos os bens reais nem comprovam manuseio/cabimento físico.

## Extensão ao restante da importação de base

Os249 nós do `Base_interativa.json` têm somente7yaw não zero,3rot não zero e2opacity0; não há outro tiltZ não zero. Os10 nós rotacionados foram associados aos nomes CAD pela ordem exata do importador, com dimensões conferidas.

As três cadeiras Lina (Peca099/100/101) também têm frame/heading com sinal oposto ao transformador gráfico. Contudo, o CAD atual usa caixas simétricas giradas±90° em torno do centro: **os envelopes são idênticos**, e o detalhe do encosto não existe no CAD. Isso não configura novo choque ou posição volumétrica errada. Registrar a diferença sem aplicar mudança indiscriminada a todos os nós; eventual correção de heading precisa ser integrada conscientemente pelo responsável.

## Evidência e limites

[Auditoria_XML.json](Auditoria_XML.json) registra matrizes, vínculos, pais, visibilidade, controles e28 itens. [Sofa_tanque_evidencias.json](Sofa_tanque_evidencias.json) registra as sete matrizes salvas/restauradas e tanque vigente/histórico. [Nos_base_rotacao_opacidade.json](Nos_base_rotacao_opacidade.json) cobre todos os casos de rotação/opacidade de base. Scripts reproduzem somente a leitura desses dados.

Não foram recalculados BREP, expressões não triviais, colisões, movimento contínuo, parede física, carga, fixação ou ferragens. Envelope derivado de Comprimento/Profundidade/Altura é apenas corpo nativo, não conjunto acabado ou lista de corte: banco450/400 não substitui exterior550/topo470; baixa145 não substitui frente106/base180. Partes fora dessas caixas nominais exigem contexto, não são automaticamente erros.

Fontes posicionais locais: `Escritorio/Ajuste_sofa_e_UltraComfort_R07.md`, `Escritorio/README.md`, `Escritorio/Sofa_e_porta_R11.md`, `Estudo_interativo/src/app.js`, `Modelo_FreeCAD/Base_interativa.json`, `Modelo_FreeCAD/gerar_modelo.py`, `Cesto_R15_2026-10-14/montar_cesto.py` e `Montagem_R15.json`. Nenhum novo aparelho, ferragem, contato com fornecedor ou liberação de fabricação foi proposto.
