# Gaveta baixa sobre rodas — R13

Apartamento atual · [Fechada](Gaveta_rodas_Fechada_R13.png) · [Aberta400](Gaveta_rodas_Aberta400_R13.png) · [Montagem](Montagem_R13.json) · [Auditoria](Auditoria_R13.json)

A R13 incorpora a R12 e corrige a caixa hipotética da gaveta baixa conforme a solução funcional já aprovada: **rodas de silicone, recuo de80 mm, base de180 mm, cabos fixos e cabeças da vassoura/rodo retiradas**. Ler decisões R02 vigentes. Não instalar MOVENTO nessa gaveta nem interpretar400/442 como NL de corrediça. Não mudar bancada, frentes16/16/40, pia, cocção ou aparelho.

## Caixa e espaço propostos

| Elemento | Representação R13 |
|---|---|
| Frente aplicada preservada | 1223×106×18; mesma implantação, recuada80 das portas principais |
| Caixa externa sem frente aplicada | 1223×442×106; fundo/laterais/paredes18 |
| Conjunto móvel, incluindo frente e rodas | 1223×460×145 nominais; antiga geometria alcançava467 de profundidade apesar do campo442 |
| Interior | 1187×406×88; fundo globalz39–57, bordo145, gabinetes começam180 |
| Trecho estrutural total | 1269 = apoios36 + guias/folgas10 + caixa1223; origem/limite do trecho pia+gaveteiro preservados |
| Rodas | Seis gabaritos fixos em duas fileiras/três colunas; diâmetro30/altura total39/roda13,5 |
| Guiamento | Faixa3 + corrida2 por lado, sem apoio vertical; material, fixação e batente removível pendentes |
| Apoios dos gabinetes | Duas reservas laterais18×530×180; frente no mesmo plano recuado da gaveta, **estrutura não calculada** |

O comprimento1223 do módulo é o conjunto móvel, não os1269 de todo o trecho entre apoios. O campo profundidade foi corrigido para460, incluindo a frente aplicada; a caixa continua442. Geometria nova é7 mm mais curta que a antiga, sem ocupar espaço extra atrás. Reserva posterior até a parede de referência70 mm. Campo Altura145 inclui rodas39 e caixa106.

A caixa anterior tinha laterais15 e largura interna1160, além de fundo/topo acima das referências do corte. A nova representação recupera1187 internos com chapas18 e88 de altura, em vez de padronizar uma corrediça que não faz parte da decisão. Histórico anterior oculto, revisões precedentes preservadas. Cotas e construção são propostas, sem corte/furação/compra.

## Programa e roda de referência

Quatro volumes do arranjo aceito: dois cabos fixos1125×21×21; cabeça da vassoura315×190×65; cabeça do rodo325×95×35. Envelopes das referências Noviça da R02, não produtos existentes/selecionados. Cabos centrados deixam31 mm por extremidade; cabeça mais alta deixa23 até o bordo. Sem empilhar, sem encurtar cabos e sem mecanismo retrátil. Mop/pá e outros objetos não dimensionados continuam fora desta confirmação.

[Quadrilátero1372 — página primária](https://www.quadrilatero.ind.br/produtos/rodizio-fixo-30-cristal-250) e [desenho primário](https://www.quadrilatero.ind.br/img/ecommerce/250-1.jpg), conferidos nesta retomada. Captura em `Fontes/Quadrilatero_1372_desenho.png`, página em JSON homônimo. Desenho indica30/39/40×21/13,5 e furos de montagemØ6,5/4, com posições15/23/33 na chapa40. A página identifica o código, mas não confirmou em texto a composição silicone ou capacidade de carga. **Não selecionar “cristal” como silicone automaticamente.**

As rodas no FCStd são **gabaritos simplificados**, não STEP oficial nem réplica executiva do fabricante. Forma/espessura do garfo, eixo e posição longitudinal do eixo são hipóteses conservadoras: roda no início da chapa, envoltória longitudinal55, sem chamar o eixo inferido pela imagem de cota fornecida. Não utilizar esse modelo para fabricar rodízio ou definir parafuso. A quantidade seis é proposta de distribuição; não certifica capacidade nem garante contato simultâneo das seis rodas em piso irregular.

O volume da madeira é17.224.344 mm³. Cenários750/900 kg/m³ dão12,92/15,50 kg **somente de madeira**, antes de rodas, fixações e utensílios. Não dividir a carga por seis e tratá-la como reação garantida de cada roda. Capacidade, material silicone, fixação, piso e deformação precisam ser confirmados. As rodas sustentam gaveta/conteúdo; estrutura dos gabinetes/pedra precisa ser independente e ainda não foi dimensionada. A faixa35 acima não é viga calculada.

## Percursos e conferências

- Seis peças de madeira, quatro gabaritos de conteúdo,30 peças de rodízios e quatro reservas/guias individuais válidos. Sem interpenetração relevante madeira/conteúdo ou rodízios/madeira. Contato geométrico com piso z0 ideal, sem rolagem física ou irregularidade.
-23 posições da caixa nova:0–400 em passos25, depois425/450/460/500/520/530. Sem interpenetrações relevantes dos40 elementos móveis contra63 paredes/volumes/peças fixas considerados. Não foram repetidas as nove gavetasR08 ou portas anteriores.
-400 herdado permanece posição nominal de estudo, sem batente certificado. Para liberar completamente o conjunto de debaixo da frente dos gabinetes, foi proposto530: extremidade traseira10 mm à frente do início da madeira superior.460 já libera as guias, mas ainda deixa parte sob o gabinete. Em530, levantamento ilustrativo40 também não interceptou os obstáculos. Isso não prova força/pega, pessoa, estacionamento ou retirada real.
- As reservas laterais foram reduzidas60 mm na frente para respeitar o recuo80. São subconjuntos dos volumes maiores testados, portanto não introduzem novas interpenetrações; esse argumento está registrado na auditoria. Não confirma resistência ou fixação.
- Arquivo salvo/reaberto, extensão400→0 e40 formas móveis válidas/atualizadas. Estado fechado, basez39. `Reabertura_R13.json`. Vistas estáticas em FCStd/PNG inspecionadas; bases superiores transparentes somente na vista para revelar conteúdo. Não é organização executiva liberada.

## Edição e próxima etapa

Selecionar `Gaveta007`/Gaveta baixa e editar **Extensao** em mm. `CursoNominal400` é referência herdada; `ExtracaoCompletaEstudo530` informa o percurso ilustrativo, sem impor batente físico. Não animar guias fixas ou interpretar translação rígida como ensaio de rodagem. Cotas novas numéricas; alterar envelope exige revisar caixa, guias, apoios e programa.

Pendências reais: produto com silicone/carga confirmados, fixações, fundo/flexão, guias/desgaste/tolerâncias, batente removível, piso, manuseio e **estrutura independente de gabinetes/pedra**, incluindo cocção ainda condicional. Não propor viga especial ou cortar apoios para apagar interferências sem cálculo/dados.

Próximo trabalho independente: mecanismos comuns de correr do roupeiro/maleiro, depois basculante do cesto mantendo giro55/saco removível e tampas removíveis do banco. R12 banheiro e cantoR04 preservados, com suas condições de uso/batente/vidro ainda pendentes. Não repetir23 posições ou reabertura R13 sem mudanças relevantes.

`montar_gaveta_rodas.py` cria uma revisão a partir da R12 e impede duplicação; não reexecutar sobre trabalho pronto. `auditar_rodas.py` guarda o método e o escopo. Gabaritos não são lista de corte/compra.
