# Portas comuns — controles corrigidos R09

[Apartamento atual](Guedala_Park_R09_Portas_Comuns.FCStd) · [Altura G1/G2](G1_G2_altura_R09.png) · [Detalhe isolado](Detalhe_G1_G2_R09.FCStd) · [Auditoria das portas](Auditoria_controles_R09.json)

A R09 incorpora a padronização das nove gavetas R08 e corrige17 controles ideais de portas. Não muda dimensões das frentes, posição fechada ou implantação: diferença máxima da geometria fechada0 mm. Revisões anteriores preservadas. Canto simples/cabeceira física R04 e portas de correr preservados.

O modelo-base girava portas comuns para dentro dos armários. A porta da pia, por exemplo, interceptava lateral, base e prateleira em30/45/86 graus; diagnóstico em R08. Seis pares da pia, aéreos A/B/C/D e lavanderia agora abrem para fora com eixos ideais nas laterais externas: esquerda em sentido negativo e direita positivo, ambas por entrada `Abertura` positiva. Corrigido também o sinal das cinco folhas ilustrativas do escritório, mantendo suas posições fechadas.

Foram conferidas85 posições individuais nos17 controles e cinco cenários com todos abertos no mesmo ângulo. Sem interferências com a própria estrutura nos casos examinados. A30/60/86/90 as frentes não se interpenetram. A110, quatro pares de vizinhas dos aéreos cozinha/lavanderia colidem, até306.465 mm³. Isso motivou estudo86 para os12 controles de cozinha/lavanderia, com70T3553 padrão candidato. Entrada110 limita a rotação ideal a86 pela expressão; retorno0 conferido. **Essa expressão não verifica o batente mecânico.** `Limite_estudo_R09.json` registra a conferência do controle.

Estas portas ainda usam eixo ideal, sem a translação real dos braços de dobradiça. As auditorias não certificam ferragem, tolerância, batente, carga, regulagens ou abertura simultânea com gavetas. A ausência de colisão ideal é apenas uma triagem para o próximo detalhamento.

O escritório mantém cinco folhas ilustrativas, sem apoios verticais compatíveis para as intermediárias. Antes de montagem física, estudar distribuição simples com menos folhas/divisores, preservando envelope2000×350×550 e programa; quantidade/divisões não foram aprovadas como execução. Primeiras três portas antigas da cabeceira ainda precisam de detalhamento comum, sem perturbar a vizinha e o canto R04. Apoios, carga e fixação na parede também pendentes.

As gavetas R08 estão incorporadas sem mudança. Com a guia fechada G1 proposta instalada, G2 possui116,4 mm nominais acima do fundo e5,4 mm além da reserva111 do programa. Imagem é montagem estática de caixas e gabaritos, não animação telescópica ou objetos reais. Frentes externas e nove gabaritos preservados.

Próximo: montar dobradiças comuns reais nos seis pares com dados oficiais de caneco/calço/recobrimento e quantidade/carga. Fontes71B3550/173H7100 e articulação de quatro barras da R04 já existem; reutilizar evidência, sem voltar79T8500. A montagem comercial70T3553 está documentada, porém sobreposição própria CAD ainda sem causa; não inventar cortes/deslocamentos para apagá-la. Depois escritório/cabeceira com apoios simples e demais frentes ilustrativas. Não repetir85/160/181 casos sem mudança relevante.

Reprodução `corrigir_controles.py`. `auditar_portas.py` gerou evidência antes do limite86: não reexecutar sobre o arquivo limitado e interpretar pedido110 como rotação efetiva110. Gerador geral atualizado com sinais e pivô externo dos pares, sem reconstruir a R01 histórica. Novas cotas/ferragens continuam propostas, sem corte ou compra.
