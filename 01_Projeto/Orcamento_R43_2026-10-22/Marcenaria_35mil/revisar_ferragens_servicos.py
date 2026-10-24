from pathlib import Path
import json

root = Path(__file__).parent
# Faixas são premissas de planejamento, não cotações de fornecimento instalado.
hardware = [
('7 pares FGVTN500 com engates',550,700,'Referência anterior R$525,77; conferir kit e montagem'),
('2 pares MOVENTO400 + 4 engates',800,1100,'Guia pública R$356,94 Pix; composição do anúncio não confirma engates'),
('42 dobradiças comuns com bases',504,756,'R$12–18/conjunto; anúncio de referência R$10,50 não homologa todos os recobrimentos'),
('4 dobradiças específicas do canto',100,220,'Provisão R$25–55/conjunto; código a fechar'),
('6 dobradiças do espelheiro com bases',150,300,'Provisão R$25–50/conjunto; carga e recobrimento a fechar'),
('3 sistemas de correr, 6 folhas, incluindo trilhos',650,1200,'Roupeiro, maleiro e gabinete banheiro; sistemas distintos, provisão global'),
('Gaveta de limpeza: 6 rodas/guias',120,240,'Provisão; não somar como décimo par de corrediças'),
('4 cabideiros e suportes',180,350,'8 terminais e eventual apoio central; comprimentos finais pendentes'),
('Conectores, pinos, ancoragens, batentes e fixadores',650,1200,'Inclui 20 Minifix candidatos, 8 pinos do espelho, grelhas, prateleiras e fixação na parede; quantitativo parcial'),
('Aço bruto e fixadores dos reforços',350,700,'Bancada e banco; corte/furação/acabamento em serviços, sem cobrança duplicada'),
('Mecanismo e armação do cesto',600,1500,'Provisão de risco; nenhum mecanismo comercial integralmente validado'),
('4 dobradiças especiais do banco',2400,4400,'R$600–1100/unidade: hipótese entregue/importada, NÃO cotação brasileira; códigos e sentido pendentes'),
('Fretes de ferragens',200,400,'Somente peças; transporte dos móveis em serviços; não duplicar importação já provisionada no banco'),
]
labor = [
('Conferência, executivo fabril e plano de corte',24*45,32*60,'24–32 horas-pessoa × R$45–60'),
('Fabricação em oficina',100*40,140*55,'100–140 horas-pessoa × R$40–55, corte, borda, furação, colagem, pré-montagem'),
('Instalação e regulagem no apartamento',64*40,80*55,'64–80 horas-pessoa × R$40–55: dupla por 4–5 dias de 8h'),
('Estofamento e fabricação metálica',1400,2400,'Somente trabalho especializado: R$700–1200 para cada especialidade'),
('Transporte de móveis e movimentação',600,1000,'Provisão do conjunto; confirmar acesso, elevador e viagens'),
('Indiretos, tributos e remuneração comercial',2400,4000,'Provisão separada, sem percentual supostamente universal; exigir preço final com nota e garantia'),
]
hl,hh=[sum(r[i] for r in hardware) for i in (1,2)]
ll,lh=[sum(r[i] for r in labor) for i in (1,2)]
data={'data':'2026-10-23','status':'estimativa por premissas, não cotação; sem alteração CAD ou orçamento central','ferragens':[dict(item=a,minimo=b,maximo=c,premissa=d) for a,b,c,d in hardware],'servicos':[dict(item=a,minimo=b,maximo=c,premissa=d) for a,b,c,d in labor],'totais':{'ferragens':[hl,hh],'servicos':[ll,lh],'materiais':[13464.33,20646.01],'sensibilidade_total':[13464.33+hl+ll,20646.01+hh+lh]},'cenario_referencia':{'materiais':20800,'ferragens':9200,'servicos':16500,'total':46500},'meta_condicional':{'materiais':16000,'ferragens':6500,'servicos':12500,'total':35000}}
(root/'Revisao_ferragens_servicos_2026-10-23.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def money(x): return f'R${x:,.0f}'.replace(',','.')
def table(rows): return '\n'.join(f'| {a} | {money(b)}–{money(c)} | {d} |' for a,b,c,d in rows)
report=f'''# Revisão de ferragens e serviços — 23/10/2026

O rateio anterior de R$3.700 em ferragens e R$15.450 em serviços não era levantamento. A documentação mais recente traz mecanismos especiais e uma correção importante nas duas gavetas do escritório. **Para trabalhar hoje, proponho cenário de R$46.500 instalado: R$20.800 de materiais + R$9.200 de ferragens + R$16.500 de serviços.** É estimativa de planejamento; não é proposta recebida, teto garantido nem aprovação de compras. Não confundir este cenário com a estimativa histórica de R$46.550: a proximidade é coincidência de composição.

## Ferragens

| Item | Faixa provisória | Base e limite |
|---|---:|---|
{table(hardware)}
| **Total** | **{money(hl)}–{money(hh)}** | Não representa faixa estatística nem preço máximo |

Somente parte dos preços tem referência comercial direta. Os demais são verbas explícitas para impedir omissões; quantidades de pinos, perfis, ancoragens e fixadores ainda não formam lista de compra. Não contar os conjuntos e novamente seus componentes. Puxadores/perfis devem respeitar a solução aprovada: nenhum conjunto novo foi escolhido nesta revisão; cotação precisa explicitar sua inclusão quando aplicável.

**Escritório:** o estudo R45 pede 2 pares 760H4000S e 2 engates esquerdos + 2 direitos T51.7601. FGVTN400 exige 420 mm, frente aos 412 mm existentes; encurtar guias reduz armazenamento e não atende ao pedido. Não adicionar TIP-ON por causa de título comercial. A montagem MOVENTO ainda tem ajustes técnicos pendentes.

**Banco:** estudo R47 usa quatro dobradiças Southco (duas para cada tampa), além de chapas e fixadores. A loja oficial europeia anuncia a E6-10-6110F0-50 por €65,78, sem estoque na consulta; isso não é preço entregue no Brasil. A faixa em reais acima é uma provisão ampla, não conversão cambial, cálculo tributário nem proposta de importação. A seleção do sentido F0/R0 e a validação final continuam pendentes. Não chamar pistão genérico de substituto equivalente.

**Cesto:** há envelope e esforço estudados, mas não mecanismo integralmente aprovado. A provisão não transforma candidato em peça liberada. Mesmo volume nominal de um cesto comercial não prova encaixe hidráulico ou preservação do armazenamento.

## Mão de obra e serviços

| Etapa | Faixa provisória | Memória |
|---|---:|---|
{table(labor)}
| **Total** | **{money(ll)}–{money(lh)}** | Sem cotação local do pacote |

Horas e tarifas são premissas propostas para orçamento, não produtividade medida nem tabela salarial/contratual pesquisada. São 188–252 horas-pessoa de projeto/fábrica/instalação, mais os trabalhos especializados. A tarifa horária considerada é custo de prestação direta; a última linha cobre componentes comerciais ainda não incluídos. Se o fornecedor já os embutir na tarifa ou no pacote, não somar novamente. R$16.500 é referência intermediária arredondada, não conclusão de que R$15.450 anteriores fossem necessariamente insuficientes. A falha anterior era a falta de composição.

Fitas, colas, tecido, espuma, espelho e aço bruto estão em materiais/ferragens. Aqui entra sua aplicação, montagem ou fabricação. A oficina inclui processamento em máquinas próprias; **não somar serviço terceirizado de corte/borda por cima**. Para comparar terceirização, substituir a parcela correspondente da oficina e retirar dos materiais qualquer fita/cola já incluída no serviço. A Gasômetro anuncia aplicação de borda a R$2,50, mas é necessário confirmar unidade, composição e acabamento; isso não precifica toda a fabricação. Transporte da marcenaria fica aqui, sem duplicação na logística geral do apartamento.

## Conjunto e caminho para R$35 mil

Somando extremos das premissas, a sensibilidade é **{money(data['totais']['sensibilidade_total'][0])}–{money(data['totais']['sensibilidade_total'][1])}**. O extremo inferior exige que várias condições favoráveis ocorram juntas e não é preço disponível. O cenário de trabalho R$46.500 está **R$11.500 acima da meta**, sem usar os R$10 mil de reserva.

| Parcela | Cenário de referência | Limite de negociação proposto | Redução necessária |
|---|---:|---:|---:|
| Materiais | R$20.800 | R$16.000 | R$4.800 |
| Ferragens | R$9.200 | R$6.500 | R$2.700 |
| Serviços completos | R$16.500 | R$12.500 | R$4.000 |
| **Total** | **R$46.500** | **R$35.000** | **R$11.500** |

Esta coluna de negociação é uma condição a demonstrar, não economia obtida. R$6.500 em ferragens está abaixo da faixa atual: exige cotação melhor ou revisão técnica dos mecanismos especiais. Não presumir que desconto em dobradiças comuns pagará a diferença.

1. **Materiais:** fechar lista de peças e plano de corte conjunto por cor/espessura; cotar lote com branco apenas oculto e acabamentos industriais aprovados. R$16 mil está na faixa de materiais estudada, mas precisa ser demonstrado pelo aproveitamento real e preços entregues. Sem afinar tampos ou eliminar fundos/prateleiras para forçar resultado.
2. **Banco e cesto primeiro:** cotar a solução especial atual e estudar ferragens mais simples que preservem dois acessos, volume útil, cores e segurança de operação. A economia não está validada. Não retirar retenção da tampa nem converter cesto para outro movimento sem examinar acesso e hidráulica. Cotação nacional das Southco pode reduzir a incerteza mesmo sem redesenho.
3. **Gavetas e portas:** manter MOVENTO apenas onde a geometria a exige; manter sete pares FGVTN como hipótese técnica nas demais, com engates confirmados. Padronizar famílias de dobradiça quando recobrimento/carga permitirem, mantendo as específicas do canto e espelho. Não repetir a economia histórica Blum→FGVTN já contabilizada.
4. **Serviços:** comparar pacote integral com oficina equipada versus corte/borda terceirizados + montagem, sempre com um responsável e escopo idêntico. Produção em lote, medição única bem preparada e instalação contínua podem reduzir horas/retornos. R$12.500 é uma oferta a buscar, não preço de mercado confirmado. Não omitir estofador, serralheria, tributos, fretes ou acabamento final para caber.

**Conclusão:** é possível buscar os R$35 mil sem cortar armazenamento ou mudar cores, mas ainda não há evidência para prometer esse preço. Mantendo todos os mecanismos especiais exatamente como estão em estudo, a meta fica apertada. O maior potencial técnico de redução está no banco/cesto e na organização de fabricação, não na retirada de armários. Se as propostas completas não fecharem, registrar a diferença na execução do apartamento; a reserva de R$10 mil não financia o ajuste.

## Evidências e rastreabilidade

- [FGVTN500, referência comercial do par](https://www.ferragensfloresta.com.br/corredica-invisivel-50cm-com-amortecedor-extracao-total-35kg-fgv-tn/p): valor arquivado anterior R$75,11 Pix, preço regional a reconfirmar.
- [FGVTN Click curva com calço e capas](https://secure.ferragensfloresta.com.br/dobradica-fgv-35mm-com-amortecedor-click-curva--capa-fgv-tn/p): R$10,50. Referência de uma variante, não aprovação para 42 posições.
- [MOVENTO400, Ipê](https://www.ipeferragens.com.br/corredica-blum-movento-400mm-com-tip-on-e-blumotion-40kg): página mostra modelo sem TIP-ON a R$356,94 Pix; confirmar 760H4000S, par e engates antes de compra.
- [Rometal RO40, Ipê](https://www.ipeferragens.com.br/kit-rometal-ro-40-ate-50kg): R$28,25 Pix pelo kit anunciado; trilhos e compatibilidade não comprovados. Não usado como preço dos três sistemas completos.
- [Southco oficial E6-10-6110F0-50](https://shop.southco.com/en_eu/e6-10-6110f0-50): €65,78; sem estoque, sem preço brasileiro entregue.
- [NBK E6-10-695F0-50](https://www.nbk1560.com/products/machine_element/hinge/E6-TW/E6-10-695F0-50/): referência japonesa do segundo código; não usada como cotação brasileira.
- [Gasômetro, aplicação de borda](https://www.madeirasgasometro.com.br/servico-de-colagem-fita-de-borda/p): R$2,50 anunciado; não convertido em total sem metragem executiva.

Fontes locais: Plano_marcenaria_35mil.md; Revisao_materiais_2026-10-23.md; Consolidação R45/Inventario/Ferragens_fixas.md; R45/Gavetas/Alternativas_escritorio/Resultado.html; R45/Portas_e_articulacoes/Cesto_selecao_e_esforcos.md; Southco_banco_R47_2026-10-23/Relatorio.html. R45/R47 são evidências de estudos posteriores ao título histórico da pasta R43; esta revisão não os declara integrados à geometria principal.

Registro apenas orçamentário. Nenhuma cor, dimensão, quantidade de tampas ou gavetas alterada. Nenhuma compra, contato com fornecedor ou alteração do orçamento central. O rateio histórico por cômodo não foi reapresentado como apuração: falta distribuir ferragens/horas efetivamente por módulo. Memória reproduzível em revisar_ferragens_servicos.py e Revisao_ferragens_servicos_2026-10-23.json.
'''
(root/'Revisao_ferragens_servicos_2026-10-23.md').write_text(report,encoding='utf-8')
print(json.dumps(data['totais'],ensure_ascii=False))
