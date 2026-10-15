# Complementos autônomos —14/10/2026

Precedência atual: o quadro abaixo de cotas superiores pertence à R26/R27. A R28 posterior desceu o aéreo inteiro do escritório20mm: base1900/topo2450 e folga20 sob teto hipotético2470, preservando a altura externa do corpo550 e seus vãos internos. Assim, o contato nominal0 registrado abaixo foi superado por proposta, sem homologar teto/montagem reais. Usar Entrega_atual_R28 e seu relatório; não interpretar este histórico como instrução de recolocar o aéreo em1920. O prazo19h encerrou a automação; a revisão Astra ficou não verificada.

Elias autorizou continuar resolvendo pendências autonomamente com simplicidade. A versão vigente é [R27](../Geometria_R27_2026-10-14/README.md), incorporando R26. Esta pasta registra os novos escopos e dependências; não repete as auditorias antigas.

## Cotas superiores frente aos tetos de estudo

[Cotas_superiores_R26.json](Cotas_superiores_R26.json):925 sólidos atuais em20 módulos, comparados com alturas horizontais já presentes em`Parametros`/gerador:2470 mm como cenário fora da cozinha/lavanderia e2570 mm como hipótese documentada da cozinha/lavanderia. Seleção corrente sem hóspedes/históricos; dois painéis atuais da cabeceira substituem o bloco anterior. Reflexão conservaZ. Estado salvo fechado, não todos os movimentos ou regiões reais de teto.

Nenhuma peça ultrapassa esses cenários. Há **contato nominal sem margem superior no aéreo principal do escritório**: laterais`Peca384/Peca385` e tampo`Peca388` chegam a2470 mm. O plafon`Peca142` termina a2570 mm. Contato de fronteira não foi classificado como penetração nem corrigido com uma medida inventada. Antes de fabricar o aéreo, conferir teto acabado, instalação, fixação e margem necessária; manter o envelope aprovado enquanto essa medida real estiver ausente.

| Conjunto | Reserva nominal até o cenário |
|---|---:|
| Aéreo escritório |0 mm — montagem/teto reais pendentes |
| A/B/C/D cozinha |20 mm |
| Canto/maleiro/cabeceira do quarto |30 mm |
| Aéreo lavanderia |340 mm |

Essas reservas não garantem tolerância de obra, inclinação, gesso, vigas ou sustentação. Continua **sem sólido de teto real modelado**; o novo resultado é uma comparação condicional de cotas, não uma auditoria de colisão com o teto físico. Na R27, os únicos perfis alterados mantêm sua ocupação global longe desses limites; não se repetiu a comparação inteira.

A primeira sondagem interrompeu ao exigir validade de toda cópia transformada. Seus116 resultados completos foram reaproveitados; histórico emCotas_superiores_primeira_sondagem.json. Foram encontradas12 cópias auxiliares com validação negativa: dez possuem fonte nativa válida e não foram modificadas; as duas Shapes nativas inválidas G2 motivaram a restauração comprovada R27. Não confundir `State=Up-to-date` com validade da geometriaBRep.

## Rodas da gaveta baixa

Consulta pública dirigida preservada em `.firecrawl/rodizios-silicone-2026-10-14.json` e `.firecrawl/rodizio-fabricante-material-2026-10-14.json`, no workspace. Resultados de lojas/anúncios não foram usados para adotar material/capacidade. A referênciaQuadrilátero1372 permanece gabarito30/39, sem composição/carga homologadas.

[Catálogo oficial SchioppaV111](https://www.schioppa.com.br/wp-content/uploads/2025/01/01_previews__V111_PT-BR_compressed.pdf), arquivado emSchioppa_catalogo_V111.pdf, SHA256`cdd5d3670a0aaf9806c8a791ea414ce884e1ce5670bdd04c049c9d7254f0989c`. A página28 informa revestimentoPVC transparente na linhaColorgel e núcleo acrílico. O menor exemplo dessa linha é35 mm de roda/48 mm de altura total; o exemplo fixo começa em50/65 mm. **Não são o silicone30/39 exigido**, não foram escolhidos e não substituem o material aprovado. Não atribuir essa composição aoQuadrilátero, cuja ficha não a informa.

Página10 do fabricante, texto e figura conferidos: cálculo`C=(PE+PMC)×S/N`, com coeficiente1,33 para uso frequente em piso liso e1,5 em piso irregular. Esse critério ajuda a especificar a roda, mas não prova contato simultâneo das seis posições propostas ou distribuição uniforme em uma caixa longa. Madeira da baixa já registrada na R13:12,918/15,502 kg nos cenários750/900, antes de rodas/fixações/conteúdo. Não adotar capacidade dividindo a carga por seis como garantia; material do produto, piso, distribuição, fixação e flexão ainda faltam.

Não foi encontrado nesses resultados um rodízio fixo30/39 com composição silicone e carga confirmadas em fonte primária. Não afirmar inexistência no mercado. Não houve contato com fabricante/fornecedor, compra, substituição ou nova geometria.

## Depurador

Desenho local oficialSuggarREV.0025 foi inspecionado novamente para a lacuna de retorno: exige saídaØ130, passagem elétricaØ40 e retorno livre de pelo menos20 mm na largura. O canal atual continua bloqueado pelos painéis base/tampo; ligação do aparelho abaixo da base e pontos reais de fixação ainda precisam ser compatibilizados. Não foram abertos painéis, adotados centros de furação por perspectiva ou criada montagem especial para chamar a instalação pronta. Mantém a pendência R17; sem alteração de modelo/programa.

## Encaminhamento

Erro digital dos dois perfis resolvido na R27. Alturas condicionais comparadas; montagem do escritório sem margem nominal identificada. Material/carga das rodas e instalação do depurador permanecem com evidência insuficiente para adoção automática. Não criar revisões artificiais ou repetir estas buscas/cálculos sem dado novo. Revisão final Astra na mesma conversa às18h30, sem fabricação liberada.
