# Acústica: piso e equipamentos

Estudo NOMINAL de 29/10/2026. **Não é projeto acústico, laudo nem comprovação de desempenho.** Nenhuma compra, escolha, orçamento, site ou geometria foi alterada.

| Assunto | Resultado útil | Decisão que pode mudar |
|---|---|---|
| Olmo colado 3 mm, 30,8101 m² nominais | ΔLw de catálogo: 4 dB; Ln,w do conjunto e L'nT,w no vizinho não determinados | Exigir sistema completo compatível antes de comprar manta |
| Sensibilidade de base homogênea | 70,16–80,69 dB equivalentes; com redução hipotética total de 4 dB: 66,16–76,69 dB | Mostra por que a laje e o ensaio do conjunto são indispensáveis; não classifica a unidade |
| Verba acústica histórica | R$ 1.500 = R$ 48,69/m² líquidos, antes de perdas, adesivos, regularização e serviço | Comparar cotação completa com a verba; preço e ganho por real ainda indisponíveis |
| LG 9 / 12 / 18 mil BTU/h, opções | Lp interno H/L/SL: 38/28/22; 42/28/22; 45/38/32 dB(A) | Solicitar ensaio/modo de uso; opção 18 mil tem referência noturna maior, mas carga térmica continua pendente |
| Suggar DE61IX, modo depurador | Dado acústico não encontrado; não há exaustor separado na lista vigente | Solicitar ruído por velocidade e condições de ensaio antes de comparar substitutos |
| Quarto e sala | 216 sensibilidades de propagação; nível absoluto real não determinado | Posição, reverberação, portas e fundo precisam entrar no projeto antes de escolher posição do split |

## Base local e restrições

- [Pisos e rodapés](../../../01_Programa_e_decisoes/Pisos_e_rodapes.md): Tarkett Ambienta Design Olmo 24192727, vinílico colado 3 mm, camada de uso 0,5 mm. Remover laminado dos dormitórios; não instalar sobre laminado ou manta solta genérica. Rodapé branco fosco de 7 cm, material ainda indefinido.
- [Acabamentos](../../Acabamentos/README.md): **30,8101 m² líquidos de vinílico**, cotas de projeto, não área medida. Não confundir com dez caixas/35,80 m² compráveis do orçamento.
- [Convenção e ata](../../../01_Programa_e_decisoes/Convencao_e_ata_impactos.md), p.20, art.6w: piso não frio requer material acústico; exemplo de carpete de nylon de 6 mm não equivale a homologação do Olmo ou de qualquer manta dessa espessura.
- [Memorial](../../../01_Programa_e_decisoes/Memorial_Cury_impactos.md), §5.9, versus convenção art.58: restrições de climatização e possibilidade condicionada precisam ser conciliadas. Não há posição viável de condensadora demonstrada.
- [Plano de reforma](../../../01_Programa_e_decisoes/Plano_de_reforma_NBR16280.md): compatibilização e responsabilidade técnica continuam necessárias.
- [Análise de pisos](../../../05_Orcamento_e_cronograma/Orcamento/Pisos_e_revestimentos/Analise_pisos.md): R$ 1.500 é provisão de adaptação acústica, não preço de kit ensaiado. Não atualizar orçamento por este estudo.
- [Equipamentos](../../Equipamentos/README.md): EQ04 é depurador Suggar DE61IX; EQ08 Rinnai E21 tem exaustão forçada própria e não é exaustor da cozinha. Climatização é opção condicionada, sem capacidade ou posição escolhida.

## Impacto: cálculo limitado e comparação normativa

**Ln,w** é índice normalizado de laboratório; **L'nT,w** caracteriza o desempenho padronizado em campo, com transmissões e ambiente receptor. **ΔLw** é melhoria do revestimento em montagem de ensaio. São grandezas distintas. Não se pode subtrair a melhoria de uma manta de qualquer laje e declarar resultado real.

A equação `Ln,w,eq = 164 − 35 log10(m')` é a aproximação para **base homogênea**, reproduzida em [Bettarello et al., 2012, p.21, eq.1](https://acoustics.org.nz/wp-content/uploads/Bettarello_F_NZA2012.pdf). O artigo também demonstra limitações para pisos leves/nervurados. Não se deduziu espessura ou densidade da laje do Guedala. A faixa de massa abaixo é teste de sensibilidade, não levantamento da construção.

| H01: massa superficial hipotética kg/m² | Base equivalente dB | Menos H02=4 dB | Menos H02=10 dB | Menos H02=18 dB |
|---|---:|---:|---:|---:|
| 240 | 80,69 | 76,69 | 70,69 | 62,69 |
| 360 | 74,53 | 70,53 | 64,53 | 56,53 |
| 480 | 70,16 | 66,16 | 60,16 | 52,16 |

H02 é **redução total hipotética do sistema**. A coluna 4 permite visualizar a ordem de grandeza do catálogo Olmo, mas não transfere seu ensaio para a laje desconhecida. 10 e 18 dB não são promessa de manta, nem se somam aos 4 dB. Nenhuma coluna é L'nT,w ou previsão do vizinho. Contrapiso, revestimento, pontes rígidas, flancos, espectro e receptor continuam sem caracterização suficiente.

Edições identificadas na pesquisa: **ABNT NBR 15575-3:2021**, [ISO 10140-3:2021](https://www.iso.org/standard/79483.html) (ensaio laboratorial de impacto) e [ISO 717-2:2020](https://www.iso.org/standard/69867.html) (avaliação por índice). O [catálogo ABNT](https://www.abntcatalogo.com.br/) identifica a edição; não foi possível acessar integralmente a tabela licenciada. A edição aplicável ao empreendimento também depende dos documentos do projeto original.

Para orientar a conferência, referências secundárias de 2025 reproduzem **66–80 dB mínimo, 56–65 intermediário, ≤55 superior**, para L'nT,w de piso sobre dormitório. Não generalizar 80 dB para todo receptor: a revisão distingue piso sobre sala. [Referência bibliográfica para conferir a tabela](https://lume.ufrgs.br/bitstream/handle/10183/313828/001311795.pdf?sequence=1). A abertura integral dessa fonte falhou nesta pesquisa. **Comparação formal pendente**, tanto pela tabela primária quanto pela falta de L'nT,w do conjunto. Mesmo o cenário aritmético de 52,16 dB não demonstra desempenho superior.

## Mantas: opções pesquisadas, nenhuma adotada

**Busca brasileira complementar:** [nove fontes e pendências](../Fontes_brasileiras.csv). Aubicon Piso Acabado oferece 3 e 5 mm para vinílico, mas falta homologação do conjunto Olmo/cola, laudo e preço. Tarkett dispensa manta em orientação geral; isso não comprova desempenho do imóvel nem dispensa a convenção. ProAcústica confirma referências/edições, sem acesso integral às tabelas. Sem compra ou contato.

[Catálogo Tarkett abril/2025, p.4 e 8](https://consolidado.tarkett.com.br/images/arquivos/51381%20(21995)%20-%20TARKETT%20INSTITUCIONAL%20-%20LINHA%20AMBIENTA%20-%20CATA%CC%81LOGO%202025%20DIGITAL%20-%20ABRIL25%20-%20V12_17442216514196.pdf) confirma Olmo 24192727 e ΔLw 4 dB da linha padrão 3 mm. Porém, informa capa 0,55 mm versus 0,50 mm do documento local: **confirmar lote**, sem trocar especificação. O relatório completo do Olmo não foi obtido.

| Opção dentro de 1,5–5 mm | Evidência e compatibilidade | Preço observado / quantidade nominal |
|---|---|---|
| REGUPOL sonus multi 3, 3 mm | LVT de 4,5 mm colado, manta colada, laje 150 mm, sem teto, adesivo 43-103: ΔLw 18 dB; Ln,w 59 dB. **Não é Olmo 3 mm** | AUD 601/20 m² = AUD 30,05/m²; 2 rolos/40 m² = AUD 1.202 |
| dB Advanced LVT, 3 mm | Indica LVT colado e dupla colagem; anuncia 18 dB sem norma/base de ensaio suficiente. **Não tratar como ΔLw certificado** | £105/15 m² = £7/m²; 3 rolos/45 m² = £315 |
| DAMTEC Standard, 2 mm | PVC exige camada separadora contra migração; resultados publicados são de outros revestimentos. **Não qualificado para ganho do Olmo** | AUD 11,50/m²; 31 peças = AUD 356,50; com hipótese 10%, 34 = AUD 391 |

São ofertas estrangeiras consultadas em 29/10/2026, sem conversão cambial, frete/importação, instalação, adesivos ou garantia de entrega no Brasil. Quantidades por área, sem paginação nem autorização de compra. Não comparar moedas como custo equivalente. Nenhum preço completo brasileiro compatível foi localizado; **ganho acústico por real e diferença para R$ 1.500 ficam pendentes**, não iguais a zero.

REGUPOL: [fabricante](https://acoustics.regupol.com.au/products/range/regupol-sonus-multi/regupol-sonus-multi-3/), [ensaio RG084, página única](https://acoustics.regupol.com.au/fileadmin/user_upload/acoustics/products/documents/test_reports/au/regupol_sonus_multi/3_under_llvt_vinyl_planks/RG084_REGUPOL_sonus_multi_3_Vinyl_Plank_4.5mm_Acoustic_Test_Normalized_Lnw_59.pdf), [oferta HD Reno](https://hdreno.com.au/products/ecoflooring-regupol-underlay-20000-1000-3mm), correspondência do SKU comercial ainda a conferir. RG084 registra base nua 79 e conjunto 59 dB, mas ΔLw 18 dB: **não é a simples diferença entre quaisquer índices globais**.

dB: [ficha](https://cdn.shopify.com/s/files/1/1377/0999/files/dB_Advanced_LVT_Underlay_3mm_Data_Sheet_v4.pdf?v=1785414179) e [oferta/montagem](https://www.soundinsulationstore.co.uk/products/db-advanced-lvt-underlay). DAMTEC: [ficha abril/2025, p.1–3](https://egillarnason.is/product/kraiburg-damtec-bodenb-4mm/?attachment_id=25022&download_file=25022) e [oferta sem impostos](https://www.m1trade.com.au/shop/material-other-33/damstandard02-2mm-damtec-standard-acoustic-insulation-2-0mm-l1-0m-x-w1-0m-12273). Não transplantar resultados de variantes Itapur/Color para Standard. Não adicionar automaticamente os 4 dB do Olmo aos resultados das mantas.

## Ruído aéreo: catálogo e sensibilidade separados

Fontes primárias (29/10/2026):

| Modelo | Lp interno frio H/L/SL, dB(A) | Fonte e limite |
|---|---|---|
| LG S3-Q09AA31C | 38 / 28 / 22 | [LG](https://www.lg.com/br/ar-condicionado-residencial/s3-q09aa31c/); Lw N/A |
| LG S3-Q12JA33K | 42 / 28 / 22 | [LG](https://www.lg.com/br/ar-condicionado-residencial/dual-inverter-split/s3-q12ja33k/); Lw N/A; página mistura códigos 33K/31K, conferir unidade |
| LG S3-W18KL31C | 45 / 38 / 32 | [LG](https://www.lg.com/br/ar-condicionado-residencial/s3-w18kl31c/); condições/distância ausentes |
| Suggar DE61IX | Dado não encontrado | [Manual REV0025, p.1–2](https://files.suggar.com.br/manuais/DE61IX-DE62IX.pdf); marketing “silencioso” não quantifica ruído |
| Rinnai E21 | Dado não encontrado | [Fabricante](https://www.rinnai.com.br/aquecedores-a-gas/linha-digital/e21-1) e [manual](https://www.rinnai.com.br/uploads/manual/175.pdf) |

Não renomear os campos genéricos LG de 33/36/43 dB(A) como velocidade média. Os dados acima não descrevem condensadora e não informam distância de medição. **Não são níveis confirmados a 1 m. Lw (potência sonora) não é Lp (pressão sonora)**.

O [manual técnico OSHA, III.5, campos sonoros e apêndice B](https://www.osha.gov/otm/section-3-health-hazards/chapter-5) fundamenta a lei de distância e a soma energética. Para fonte pontual em campo livre: `Lp(r)=Lp(r0)−20log10(r/r0)−D`. Dobrar a distância reduz 6,02 dB; reflexões de um apartamento podem reduzir esse benefício. D não representa a isolação medida de uma parede.

| Sensibilidade H03, r0=1 m fictício, D=0 | 1 m | 2 m | 4 m |
|---|---:|---:|---:|
| LG 9, velocidade alta | 38 | 31,98 | 25,96 |
| LG 12, alta | 42 | 35,98 | 29,96 |
| LG 18, alta | 45 | 38,98 | 32,96 |
| Depurador, varredura arbitrária H=50 / 60 / 70 | 50 / 60 / 70 | 43,98 / 53,98 / 63,98 | 37,96 / 47,96 / 57,96 |

Valores em dB(A), **exercício condicional**, não níveis previstos no quarto/sala. H=50/60/70 é varredura arbitrária explicitamente hipotética, não faixa típica pesquisada do Suggar. Sem especificação sonora não se oferece falsa estimativa de equipamento. O CSV repete receptores quarto_H e sala_H com distâncias H de 1/2/4 m e D=0/10/20 dB; não infere parede ou posição pela planta. Cozinha/sala abertas não recebem isolamento automático. Para fontes simultâneas no mesmo receptor: `10log10(Σ10^(Li/10))`; dois sons de 40 dB resultam em 43,01 dB, não 80. Fundo e reverberação ausentes impedem soma real.

**NBR 10152:2017, versão corrigida 2020:** edição identificada em [catálogo ABNT](https://www.abntcatalogo.com.br/3c6f8gw.aspx). Valores residenciais usualmente reproduzidos (dormitório RLAeq 35 / RLASmax 40 / RLNC 30; estar 40/45/35) permanecem **a conferir na tabela 3 licenciada**, não tratados como comprovação primária. Um nível de catálogo instantâneo não é automaticamente LAeq, LASmax ou NC. Como triagem numérica apenas, LG 18 em H03 a 2 m/alta resulta 38,98, acima da referência de 35 para dormitório e abaixo de 40 para estar; isso não demonstra descumprimento nem atendimento no imóvel. Não usar as antigas faixas da edição de 1987.

## Sensibilidade, decisões NOMINAIS e perguntas

| Entrada | Faixa do estudo | Natureza / dado que falta |
|---|---|---|
| H01 massa de base | 240 / 360 / 480 kg/m² | Hipótese; tipo, massa e contrapiso reais desconhecidos |
| H02 melhoria total | 0 / 4 / 10 / 18 dB | Hipótese algébrica; ensaio completo com Olmo ausente |
| H03 distância | 1 / 2 / 4 m, r0=1 m | Hipótese; nem catálogo nem implantação confirmam r0 |
| H04 perda adicional | 0 / 10 / 20 dB | Hipótese; não Rw ou DnT,w da parede |
| Depurador | 50 / 60 / 70 dB(A) em r0 fictício | Varredura arbitrária, não típica; dado real ausente |
| Área / custo | 30,8101 m² / R$ 1.500 | Quantidade nominal e verba histórica; não cotação |

Recomendações NOMINAIS: manter a escolha estética do Olmo, mas **não comprar manta genérica**; pedir solução completa colada compatível e ensaiada. Manter rodapé como acabamento até existir detalhe perimetral do sistema: material/cor não demonstram isolamento, e pontes rígidas podem prejudicar uma camada resiliente. Comparar ruído LG no modo realmente necessário após carga térmica, sem escolher potência menor só pelo silêncio. Não posicionar split ou substituir depurador com base nestas contas.

Perguntas exatas (não houve contatos):

1. **Construtora/condomínio:** qual composição e massa superficial da laje/contrapiso da unidade, e qual relatório L'nT,w do sistema entregue, com identificação do ambiente receptor e norma/edição? Serve para evitar transferência indevida de ΔLw.
2. **Condomínio/RT:** qual critério e documento comprovam aceitação de piso vinílico colado em substituição ao laminado, considerando art.6w? Qual tratamento perimetral/rodapé deve integrar esse sistema?
3. **Tarkett e fornecedor da manta:** qual combinação exata de Olmo 3 mm, manta, adesivo e regularização tem compatibilidade, estabilidade à indentação/cargas e ensaio acústico documentados? Qual preço completo para 30,8101 m², incluindo perdas e instalação?
4. **LG:** quais Lw/Lp por velocidade, distâncias e condições de ensaio das unidades interna e externa dos códigos candidatos? Qual modo atende à carga térmica ainda pendente?
5. **Suggar/Rinnai:** quais níveis sonoros e método de ensaio por velocidade/potência, e quais condições de montagem? Serve para comparar aparelhos sem presumir “silencioso”.
6. **RT acústico/projeto:** quais posições e caminhos viáveis, receptor do pavimento inferior, ruído residual e reverberação considerar? Confirmar tabelas normativas na edição aplicável antes de avaliar desempenho.

## Reprodução e verificação

[Script](../../../ferramentas/estudos/acustica_cenarios.py), [testes](../../../ferramentas/estudos/test_acustica_cenarios.py), [228 cenários](../Cenarios.csv): 12 de impacto condicional +216 aéreos, sem somar cenários como uso simultâneo.

`python -B ferramentas/estudos/acustica_cenarios.py`

`python -B -m unittest discover -s ferramentas/estudos -p test_acustica_cenarios.py`

Seis testes: massa, distância, referência/perda, soma, domínio e rótulo arbitrário do depurador no CSV. Não validam o apartamento. SHA256 de Cenarios.csv: `a25d1aed6de4d364e45ead1d3daf5e2c32aaca273580465593b5089ef74a3cd6`.

Fontes BR01–BR09 preservadas; registro ampliado pelo estudo de envoltória, hash no índice.

Limitações de pesquisa: Firecrawl exigiu identificador de conexão indisponível; pesquisa prosseguiu pela ferramenta web. PDFs atuais Tarkett/Mapei e artigo ANTAC retornaram 403; link profundo ABNT expirado; UFRGS inacessível pela ferramenta. Nenhuma rota negada foi contornada. Texto normativo integral e preço de kit compatível não obtidos; por isso não há avaliação normativa ou custo/ganho inventados. Conteúdo de fabricante acessível e evidências locais foram separados das hipóteses.
