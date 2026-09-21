# Cortina — abertura e interferência com móveis

**Continuidade:** Elias autorizou estudar blackout de enrolar no vão e tecido frontal compacto para priorizar os móveis. Ver [cenário integrado R01](Ajustes_integrados_R01.md). A análise de duas waves abaixo permanece diagnóstico do conflito anterior; não é mais a única direção de estudo.

20/09/2026 · Análise solicitada por Elias antes de escolher o sentido de abertura. Cálculos do modelo atual, sem deslocar móveis nem aprovar nova cortina. O objetivo de cobrir a parede inteira permanece escolhido.

## Decisão após o estudo — 20/09/2026

Elias confirmou: “ok, anota recolhimento para o sofa e seguimos”. **Recolhimento para o lado do sofá escolhido.** Permanecem pendentes volume efetivo, profundidade e encontros com os móveis. A escolha não aprova deslocamento de móveis nem troca por blackout de enrolar. A análise abaixo documenta as condições geométricas; a abertura deixou de ser pendência.

## Resultado

**Recolher para o lado do sofá é a melhor candidata entre as aberturas unilaterais**, pois há mais parede ao lado da janela e o tecido aberto se afasta da TV. Abertura central também pode liberar o vidro, mas deixa pacotes junto aos dois conjuntos de móveis. **Nenhuma abertura resolve, sozinha, a interferência da cortina fechada com o layout atual.** Não registrar a solução completa como compatibilizada nem desenhar tecido atravessando os móveis.

## Geometria usada

Fonte: P01 para largura nominal da sala, e `Estudo_interativo/src/app.js` para as posições gráficas. Coordenadas locais: x parte do lado da TV para o sofá; z parte da parede da janela em direção à cozinha. Isso é diferente de afastar o encosto do sofá da parede lateral.

| Elemento | Intervalo / medida no modelo | Qualificação |
|---|---|---|
| Parede da janela | x = 0 a 245 cm | Largura nominal documental; acabamento real a conferir |
| Janela | x = 38 a 177 cm; largura 139 cm | Reconstrução gráfica, não cota da esquadria |
| Parede livre ao lado da janela | 38 cm no lado TV; 68 cm no lado sofá | Derivada da janela gráfica |
| Sofá fechado | x = 135 a 245; z = 0 a 180 cm | Gabarito Bonnie 110 × 180, encostado à parede da janela no modelo |
| Sofá aberto | x = 109 a 245; mesmo z = 0 a 180 cm | Gabarito de profundidade 136; igualmente sem reserva junto à janela |
| Painel da TV | z = 2,5 a 117,5 cm | 115 cm de extensão; somente 2,5 cm entre ponta e parede da janela |
| Prateleiras | z = 5 a 115 cm | Inferior projeta até x = 37 cm; superior até x = 27 cm |
| Parede de apoio da TV | z = 0 a 120 cm | Limite gráfico antes do acesso íntimo |
| Banco e mesa | z = 190 a 370 cm | Vão longitudinal de apenas 10 cm após o sofá |

## Volume recolhido — comparação

Referência técnica: Silent Gliss, *Wave Curtain Workroom Guide*, p. 5 (página 3 do PDF em pranchas duplas). Tabela em milímetros: wave 60 mm/fator 2,1, profundidade 100 mm, pacote 230 mm por metro de trilho mais acabamento de extremidade; wave 80 mm/fator 2,1, profundidade 140 mm, pacote 180 mm/m mais acabamento. São parâmetros de um sistema de referência, não orçamento ou seleção de marca. Blackout, tecido, costura e terminais podem aumentar o pacote.

Para 2,45 m de trilho e wave 60 mm:

- Uma folha inteira: 2,45 × 23 = **56,35 cm**, mais extremidade/retornos.
- Duas folhas iguais: 56,35 ÷ 2 = **28,175 cm por lado**, mais acabamentos de cada pacote.
- Duas camadas em trilhos paralelos não exigem somar automaticamente as larguras dos pacotes: eles ficam um atrás do outro. A profundidade do conjunto aumenta, e prevalece lateralmente o maior pacote real.

| Abertura | Resultado lateral teórico, sem terminais/retornos | Avaliação |
|---|---|---|
| Tudo no lado do sofá | 68 − 56,35 = **11,65 cm** de margem até o vidro | Melhor candidata unilateral; concentra tecido junto ao sofá, exige reserva atrás do braço voltado à janela |
| Central | 38 − 28,175 = **9,825 cm** no lado TV; 68 − 28,175 = **39,825 cm** no lado sofá | Libera o vidro no gabarito, mas mantém pacotes junto a prateleiras/painel e sofá |
| Tudo no lado da TV | 56,35 − 38 = **18,35 cm** sobre o vidro | Pior candidata: mais tecido próximo à TV e menor vão de janela descoberto |

Se o pacote real da camada mais volumosa ultrapassar os 68 cm disponíveis, a vantagem de manter toda a janela descoberta com abertura unilateral deixa de estar comprovada. Os 11,65 cm restantes são margem de estudo para terminais/retornos/tecido, não folga garantida. Acesso à maçaneta e sentido real de correr das folhas também a conferir.

Wave 80 mm reduziria o pacote teórico a **44,10 cm inteiro / 22,05 cm por metade**, mas aumentaria a profundidade da cortina. Não escolher apenas pelo menor pacote lateral.

## Profundidade — conflito comum às três aberturas

Ensaio conservador com **as duas camadas em wave compacto de 60 mm**, cada uma com 10 cm de profundidade e 2 cm de folga na frente/atrás. A referência dá distância mínima ao eixo de 7 cm; para dois eixos paralelos, considerar centros a 7 e 21 cm da parede (14 cm entre eles). Os tecidos ocupam aproximadamente z = 2..12 e 16..26 cm; incluindo a folga frontal, a reserva é **28 cm**.

Isso é um cenário explícito do sistema estudado, não mínimo universal para qualquer cortina dupla. Outros cabeçalhos, tecidos e trilhos exigem novos envelopes. Maçaneta/peitoril salientes podem aumentar o recuo necessário.

- **Sofá:** reserva existente 0 cm; para o ensaio, precisaria começar 28 cm adiante. O sofá passaria a terminar em z = 208, enquanto o banco começa em 190: **sobreposição de 18 cm** entre gabaritos que também se sobrepõem transversalmente.
- **Painel:** manter 115 cm de extensão e iniciar em z = 28 resulta em término em **143 cm**, ultrapassando o limite gráfico de 120 cm da parede em **23 cm**. Não deslocar para dentro do acesso íntimo.
- **Prateleiras:** começar a 28 cm mantendo 110 cm de extensão leva o término a 138 cm, **18 cm além** da parede disponível. O recuo atual é só 5 cm.
- **Duas waves de 80 mm:** o mesmo cálculo de folgas dá reserva de **36 cm**, agravando os conflitos. Reduzem o pacote lateral, mas não são a prioridade neste espaço.

Abertura central reduz a largura dos pacotes, mas não elimina a profundidade necessária com a cortina fechada. Tampouco basta recolher o tecido no lado oposto ao painel: à noite a camada fechada atravessa toda a parede novamente.

## Por que não deslocar todo o jantar automaticamente

Preservar os 10 cm entre sofá e banco, deslocando ambos 28 cm para a cozinha, faria mesa/banco terminarem em z = 398 cm em vez de 370 cm. No modelo, a frente da geladeira está em z = 430,25 cm e a da bancada em 454 cm:

- Mesa–geladeira: **60,25 → 32,25 cm**, no trecho em que se alinham transversalmente.
- Cadeira da cabeceira recolhida (gabarito atual termina em z = 376): **54,25 → 26,25 cm** até a geladeira após o mesmo deslocamento.
- Banco–bancada: **84 → 56 cm**.

São distâncias geométricas entre gabaritos, não larguras normativas nem validação de circulação/abertura de portas. A Lina real ainda não está compatibilizada. O resultado impede tratar esse deslocamento como solução automática.

## Encaminhamento recomendado

1. Usar **abertura para o lado do sofá como candidata preferida**, condicionada ao volume real recolhido e ao acesso à janela. Abertura central é alternativa caso o pacote único seja excessivo ou o uso da janela favoreça divisão.
2. Antes de fechar compra ou imagem fiel, compatibilizar a seção da cortina com a ponta do painel/prateleiras e com o conjunto sofá–banco. A escolha anterior de parede inteira segue válida como intenção estética, mas não havia sido dimensionada.
3. Para preservar ao máximo os móveis, estudar um acabamento frontal de menor volume e o encontro lateral junto ao painel. Uma opção a comparar seria blackout de enrolar próximo ao vão com tecido frontal de parede inteira; isso altera a solução de dois tecidos independentes no trilho e **não foi aprovado**, nem seu cabimento demonstrado. Uma camada wave ainda exige profundidade, portanto essa alternativa não deve ser declarada pronta.
4. Solicitar ao fornecedor, quando houver tecido/sistema, o pacote efetivo de cada camada, profundidade total e solução de retorno; conferir medidas na vistoria. Elias já informou não ter medidas além das fontes atuais, então não exigir novos números dele para continuar o estudo.

## Fontes

- [Planta P01](../../04_Visita_ao_apartamento/referencias/P01_planta_oficial.png).
- [Modelo atual](../Estudo_interativo/src/app.js), [painel e TV](Painel_e_TV_R00.md), [mesa e cadeiras](Mesa_e_tres_cadeiras_R03.md).
- [Silent Gliss — Wave Curtain Workroom Guide](https://www.silentgliss.co.uk/fileadmin/redaktion/used/Images/Web%20Partner%20Downloads/SGGB/Various%20Documents/Wave%20-%20Curtain%20Workroom%20Guide.pdf), tabela de p. 5 e diagrama de distâncias; conferido em 20/09/2026.
- [Silent Gliss — catálogo manual 06/2026](https://www.silentgliss.co.uk/fileadmin/redaktion/contentserv/Smart-Documents/SGGB/SGGB_HD_EN-GB.pdf), notas gerais: pacote varia com tecido e confecção.

Sentido de abertura aprovado explicitamente após o estudo: recolhimento para o sofá. Sem mudança de móveis no modelo, compra ou publicação.
