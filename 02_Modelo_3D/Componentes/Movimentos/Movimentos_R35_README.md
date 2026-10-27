# R35 — auditoria de movimentos e retirada da placa do varal

FreeCAD R35 · [Mapa dos controles](Mapa_dos_controles.csv) · [Testes](Movimentos_validados_R35.json) · [Geometria e interferências](Geometria_e_novos_movimentos_R35.json) · [Visão geral](Apartamento_R35.png)

A R34 foi preservada. A placa de madeira de ocultação do varal, Peca366, foi removida por pedido de Elias. O varal Peca157 permanece.

## O que a auditoria comprovou

Os 60 comandos ativos da R34 realmente movimentavam peças. A medição desta auditoria verifica alterações acima de uma tolerância numérica, em vez de apenas comparar textos das posições. Os três campos antigos Alpha, Beta e Vizinha da planilha R03 não movimentavam a geometria corrente. Isso não comprova uma falha desde R03: as portas A/B foram substituídas pelo mecanismo independente R04; a vizinha passou ao ControleVizinhaR18. Os comandos antigos pertenciam a peças superadas.

Os cálculos antigos foram arquivados em JSON e retirados da planilha corrente. Permanecem nessa planilha apenas a faixa fixa e seu recuo, efetivamente utilizados. As portas atuais A/B agora têm campos claros em ControleCantoR35, dentro de CONTROLES ATUAIS / Quarto. A planilha de cálculo R04 recebe esses campos; a vizinha conserva seu controle R18.

Na R35, 65 comandos foram conferidos em 195 posições, com movimento efetivo e retorno às poses salvas. São 1.127 peças correntes válidas; todas mantêm a geometria e a posição inicial da R34, exceto a placa explicitamente removida. Não se alteraram as medidas do apartamento ou dos módulos para obter movimento.

## Lacunas corrigidas nesta revisão

| Elemento | Causa | Controle e alcance agora disponível |
|---|---|---|
| Canto A/B | Controles úteis dispersos em planilha, ao lado de cálculos R03 superados | ControleCantoR35: AberturaA e AberturaB, 0–86°; abrir A antes de B |
| Mesa extensível | Duas metades existentes com posições constantes | ControleMesaR35.VaoCentral: 0–300 mm; cada metade percorre até 150 mm; pedestal fica parado |
| Grelhas inferior/superior | Peças removíveis desenhadas sem expressão de retirada | Controles independentes de extração frontal, 0–100 mm apenas como visualização de manutenção |
| Conjunto do forno | Cenário de retirada de 600 mm existia no estudo separado, mas não no modelo geral | ControleFornoR35.Extracao: 0–600 mm; desloca o conjunto, não abre a porta do aparelho |
| Varal | Grelha existente com altura fixa | ControleVaralR35.Descida: cenários do estudo interativo em 0/270/860 mm; alturas 2310/2040/1450 mm, sem roupas |

As 15 poses amostradas dos cinco novos comandos não produziram sobreposição dos envelopes delimitadores com outras peças correntes; não houve candidatos à interseção volumétrica. Essa constatação não cobre o percurso contínuo, roupas, pessoas ou instalações ausentes.

## Movimentos ainda não modelados — causa e caminho de solução

| Elemento | Por que permanece sem movimento funcional completo | Como resolver |
|---|---|---|
| Folha central da mesa | A peça está no banco; abrir o vão da mesa não a transporta para o tampo | Modelar a transferência manual e a inserção, conferindo folgas e apoios; não duplicar a folha nem simular um teletransporte como trajetória |
| Sofá Bonnie, relaxamento/baú | Volumes simplificados de estofamento; sem eixos e articulações reais | Separar partes móveis e usar mecanismo/documentação do produto; os estados do site são ilustrativos e alteram envelopes |
| Sofá-cama Daiane do escritório | Arranjos de uso/hóspede do site não são uma montagem cinemática no CAD | Diferenciar reposicionamento do móvel e desdobramento; definir as partes e a trajetória antes de conferir interferências |
| Portas de geladeira, forno e micro-ondas; abertura da lavadora | Gabaritos de aparelhos sem folhas e articulações devidamente separadas | Inserir geometria de abertura do fabricante ou montar estudo explícito com eixos confirmados; extrair o forno inteiro não substitui abrir sua porta |
| Box, janelas e demais portas arquitetônicas | Representações estáticas; painéis móveis, eixos e cursos não estão completos | Conferir tipo e sentido no projeto de origem, separar folhas e criar controles; a entrada do banheiro já possui controle funcional |
| Varal com roupas e mecanismo | Descida da grelha agora existe; roupas, cabos e mecanismo ainda não | Completar envelopes e trajetória de roupas/mecanismo, compatibilizando com aquecedor e bancada; não tratar as três alturas ilustrativas como curso homologado |
| Cadeiras e outros móveis soltos | Posicionamento manual, sem trilho ou articulação modelada | Criar cenários de uso/guarda para circulação; não classificar uma peça solta como mecanismo quebrado |

Calços fixos de dobradiças e apoios estruturais permanecerem parados é comportamento esperado. Propriedades Abertura/Deslocamento nas folhas podem ser comandadas por expressões: alterar o controle central, sem apagar a expressão da peça.

Prioridade para continuar: transferência da folha da mesa; sofás em uso aberto; aberturas dos aparelhos e arquitetura; varal com roupas. A revisão futura do acesso ao banco continua conforme a preferência registrada de Elias, sem reversão automática nesta auditoria.

## Referências locais usadas

- Mesa: 150/180, metades móveis e folha removível.
- [Forno e grelhas: fixações e cenário de retirada](../../../03_Ambientes/Cozinha/Fischer_Grill/Grelhas_manutencao/README.md).
- [Estudo interativo: estados ilustrativos do varal e sofás](../../../ferramentas/site/src/app.js).

Salvar e reabrir o arquivo valida a integridade do CAD; o ensaio de resposta não certifica ferragens, cargas, instalação ou operação simultânea. As condições de uso já registradas, como fechar a entrada do banheiro para abrir o gabinete, continuam vigentes.
