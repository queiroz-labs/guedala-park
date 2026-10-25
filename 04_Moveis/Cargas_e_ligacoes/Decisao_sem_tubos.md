# Decisão sobre sustentação das chapas de madeira

25/10/2026. **Instrução de Elias:** não quer tubos sustentando chapas de madeira no projeto. Qualquer proposta futura de tubo com essa função exige perguntar antes e receber autorização explícita. Esta decisão vale para todos os móveis, inclusive lavanderia, aéreos e bancada.

As alternativas tubulares P11 e P15 e o quadro tubular da bancada R45 estão cancelados como soluções ativas. Preservar os cálculos anteriores somente como histórico identificado. Não substituir automaticamente tubos por outro quadro metálico para contornar a preferência: desenvolver primeiro apoios e ligações de marcenaria, preservando vãos, armazenamento e aparência.

Prioridades: apoio direto já estudado nas prateleiras P01; fundo e ligações positivas P15/P04; análise de rigidez da caixa e suas juntas; seção/constituição da chapa e borda estrutural de madeira quando necessárias. Aumentos de espessura não podem reduzir silenciosamente os espaços aprovados.

## Inventário e retirada

- R50: estrutura da bancada `R45_Ref_Bancada_Estrutura_R45_R02_ESTUDO`, inteiramente oculta, com60 objetos. Contém cinco longarinas, duas travessas e quatro pés tubulares, além de contraventamentos, tampo usinado e cópias de contexto.
- Esse grupo não sustenta o tampo ativo e não possui dependência externa funcional; seu único pai externo é o grupo organizador `R45_Estudos`. A retirada será feita numa nova revisão e conferida por comparação das peças mantidas. O estudo histórico separado continua preservado.
- A proposta P15 de duas longarinas existia somente no cálculo/diagrama; não foi instalada na R50. Foi retirada da lista de soluções a desenvolver.
- A bancada ativa usa `Peca111`/`Peca112`, dois sólidos esquemáticos30×30×720, com cor escura e sem material/seção oca especificados. Não é possível classificá-los como tubos a partir desse CAD. Seu detalhamento passa para solução de marcenaria; não considerar a sustentação ou estabilidade já resolvidas.
- Varões para roupas e componentes de articulação têm funções próprias; esta decisão trata de tubos que sustentam chapas.

Pendências desta decisão: estudar apoios de madeira e rigidez do tampo da bancada; completar os caminhos P15/P04 e a prova das juntas. Retirar uma alternativa de estudo não libera a capacidade dos apoios atuais.

## Histórico cancelado dos reforços externos (movido do README em 25/10/2026)

**Não faz parte do projeto ativo.** Elias rejeitou tubos sustentando chapas em25/10. Números abaixo preservados para rastrear o estudo anterior; não são indicação de compra ou detalhamento futuro.

Duas longarinas ao longo dos 799 mm, próximas da frente e da traseira, **sob** a base. Sem divisória ou perda de altura interna. Os perfis reduziriam a cota inferior externa em 15 ou 20 mm e precisam de quatro terminais positivos na caixa. Não foram incorporados à R50 nem aos quantitativos ativos.

A comparação atribui **todo o conteúdo e toda a base a uma única longarina**, além do peso próprio dessa longarina. Soma uma triagem de flexão transversal do MDF e a reserva de 0,20 mm. O caso misto é 15 kg distribuídos mais 5 kg localizados sobre faixa longitudinal de 50 mm; a concentração transversal é idealizada como ponto. Não há crédito de espalhamento para uma placa mais larga.

| Perfil ideal, altura na vertical | 20 kg distribuídos | 15 kg distribuídos + 5 kg localizados | Misto com MDF E inicial 1.600 MPa |
|---|---:|---:|---:|
| 35 × 15 × 2 mm | 1,616 mm | 2,590 mm | 2,956 mm |
| 30 × 20 × 2 mm | 1,090 mm | 2,044 mm | 2,431 mm |

Valores da tabela = soma conservadora de deformações mais reserva; referência de 2,663 mm. O perfil de **30 × 20 × 2 é o candidato mais robusto desta comparação**. Para o caso misto com E = 1.600 MPa, exige I efetivo mínimo aproximado de **8.652 mm⁴**, com E do aço de 200.000 MPa. Cantos arredondados e tolerâncias precisam entrar no I real, em vez de usar cegamente a seção retangular ideal.

Cada terminal tem envelope estático de cortante de **243,3 N** se praticamente toda a carga se aproximar de uma extremidade. Para limitar seu assentamento a 0,20 mm, a rigidez requerida do **grupo** é cerca de **1.217 N/mm**. São solicitações sem majoração, não capacidade de parafuso. Ainda faltam geometria, excentricidade, solda/assento, grupo de fixadores, resistência e acesso de montagem.

**20 kg concentrados num apoio pequeno não passam nessa triagem**, mesmo com esses perfis: a flexão transversal local do MDF governa. A meta atual continua sendo conteúdo total distribuído, com os casos de concentração explicitamente identificados. Não registrar “20 kg em qualquer posição”.
