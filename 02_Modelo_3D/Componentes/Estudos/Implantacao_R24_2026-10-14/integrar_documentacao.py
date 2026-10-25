from pathlib import Path
import shutil

root=(Path(__file__).resolve().parent / '.').resolve()
cad=(Path(__file__).resolve().parent / '../..').resolve()
project=(Path(__file__).resolve().parent / '../../..').resolve()
repo=(Path(__file__).resolve().parent / '../../../..').resolve()

def write(p,t):p.write_text(t,encoding='utf-8')
delivery=((Path(__file__).resolve().parent / '../../04_Documentacao/Entrega_atual_R23.md').resolve()).read_text(encoding='utf-8')
delivery=delivery.replace('Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd','Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd',1).replace('Guedala_Park_R23_Rotulos_Consistentes.FCStd','Guedala_Park_R24_Implantacao_Corrigida.FCStd',1)
anchor='## Resultados registrados'
new='''## Correções de implantação R24

A auditoria global encontrou o sofá-cama Daiane do escritório atravessando uma parede por erro de sinal de rotação na importação. A R24 restaura as sete peças à posição diária já documentada, preservando dimensões e modelo. Também oculta duas referências exclusivas do modo hóspedes e o volume histórico anterior do tanque. Fontes e R23 preservadas; nenhum armário, controle ou movimento foi alterado.

[Diagnóstico, alteração e limites](Implantacao_R24_2026-10-14/README.md). A versão salva confirmou as alterações e passou em4775 encontros do sofá atual com paredes/pisos/móveis selecionados, sem interpenetração. A conferência estática global anterior dos sólidos inalterados permanece aplicável. Não há sólido de teto para comprovar esse encontro. Restam os recortes reais da bancada/tanque e as demais pendências físicas/comerciais.

'''
assert anchor in delivery
delivery=delivery.replace(anchor,new+anchor,1)
write((Path(__file__).resolve().parent / '../../04_Documentacao/Entrega_atual_R24.md').resolve(),delivery)

state=(Path(__file__).resolve().parent / '../Canto_2026-10-13/Cinematica_R03/Estado_noturno.md').resolve()
t=state.read_text(encoding='utf-8')
t=t.replace('apartamento R23 (espelhamento R20 / controles R21 / exibição R22)', 'apartamento R24 (implantação corrigida / base R23 / espelhamento R20)',1)
anchor='### Nova prioridade autorizada — revisão global de implantação até19h'
new='''### Implantação R24 — correções comprovadas e continuidade

Arquivo atual: Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd. Ler README e Entrega_atual_R24.md. Incorpora R23 preservada. A auditoria global R23 selecionou927 sólidos exibidos (926vigentes e um histórico indevidamente visível),27paredes inteiras e9pisos. Dois positivos foram Peca122/Peca124 do Daiane na paredePeca017. Não há teto sólido modelado. Demais pares estáticos sem penetração, com contatos de fronteira que não comprovam fixação.

Origem comprovada: gerar_modelo.py usou +yaw; app.js usa−yaw em XY do CAD. Sete primitivasDaianePeca122..128 foram giradas rigidamente180° ao redor(2570,2220) no referencial-fonte, restaurando o estudoR07 X2570..3470/Y1520..2920, espelhoX3930..4830. Não foi simples translação/redução do sofá ou mudança de escolha. LinksEspelhoPecaR041/R042 ocultos porque peças têmopacity0 no modo diário; LinkEspelhoPecaR123 oculto porquePeca358 é tanque histórico substituído naR15. Fontes mantidas. Três cadeiras têm orientação de frame oposta mas caixa simétrica/geometria idêntica: registrado, sem mudar volume/implantação por isso.

Correcao_R24:5895 objetos comparados, somente7Placements/3visibilidades e rótulo do documento mudaram; pais/expressões/tipos de parâmetros preservados, nenhumaInvalid, R23SHAinalterado. Conferencia_correcao_R24: arquivo salvo abriu emprocessoisolado,7matrizes/volumes e3visibilidades persistiram; cincopeças atuaissofa contra955alvos=4775BBox separados, semcomuns/erros. Não repetiu arquitetura dos inalterados. Seleção atual924 sólidos após ocultações; varanda/teto/medidasfísicas/cadeira-operador/conversãoemcama não homologados. Planta_corrigida_R24.png inspecionada. Galeria/índices atuaisR24; vistas de acessoR22 preservadas como referências anteriores, sem chamar posição antiga do sofá deatual.

Cruzar_modulos:398480 pares entre raízes distintas com ao menosum módulo, quatro positivos; dois tanquehistórico agora oculto, dois tanque/vazioútil x bancada 'a recortar' (recorte/produto real pendentes). Não inventar recorte ou tirar tanque atual. Auditoria_posicoes confirma237links únicos/20módulos/45controles e28itens deprograma selecionados; semduplo espelho. Todos249nósbase auditados para rotação/opacidade; apenas7yaw/3rot/2opacity0 encontrados. Não aplicar correção emmassa no gerador histórico.

Continuação até19h: revisar lacunas de cobertura de movimentos contra arquitetura com leitura dos resultados existentes (Cobertura_movimentos_2026-10-14), depois atuar somente no escopo comprovadamente ausente ou afetado por uma correção. Não repetir varreduras antigas. Revisão técnica e fabricação permanecem limitadas pelas pendências reais anteriores. Manter simplicidade/programa, semcorte/furação/compra/contato comfornecedores.

'''
assert anchor in t
write(state,t.replace(anchor,new+anchor,1))

plan=(Path(__file__).resolve().parent / '../../04_Documentacao/Plano_ate_19h_2026-10-14.md').resolve()
t=plan.read_text(encoding='utf-8').replace('Revisão atual: [R23](Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd). [Conjunto atual e pendências](Entrega_atual_R23.md).','Revisão atual: [R24](Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd). [Conjunto atual e pendências](Entrega_atual_R24.md).')
write(plan,t)

index=(Path(__file__).resolve().parent / '../../04_Documentacao/Historico_FreeCAD.md').resolve();t=index.read_text(encoding='utf-8')
heading='# Apartamento no FreeCAD — revisões de estudo\n'
assert t.startswith(heading)
new='''
[Implantação corrigida — R24](Implantacao_R24_2026-10-14/README.md): **apartamento atual**. Sofá Daiane restaurado à posição documentada após corrigir sinal de rotação da importação; referências de hóspedes/tanque antigo ocultas. Armários e controles preservados. [Arquivo e resultados](Entrega_atual_R24.md) · [Galeria atual](Galeria.html). Revisão global continua até19h com limites registrados.
'''
t=t.replace(heading,heading+new,1).replace('[Rótulos e documentação — R23](Rotulos_R23_2026-10-14/README.md): **apartamento atual**.','[Rótulos e documentação — R23](Rotulos_R23_2026-10-14/README.md): base preservada, incorporada àR24.',1)
t=t.replace('Auditoria externa dos corpos de ferragens não concluída.','Auditoria externa das quatro folhas alteradas posteriormente concluída no escopo amostrado R23; continuidade/tolerâncias/carga/fixação seguem pendentes.',1)
write(index,t)

gallery=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R28_2026-10-14.html').resolve()
old=gallery.read_text(encoding='utf-8')
archive=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R23_2026-10-14.html').resolve()
assert not archive.exists()
shutil.copy2(gallery,archive)
t=old.replace('FreeCAD R23','FreeCAD R24').replace('FreeCAD · R23','FreeCAD · R24').replace('Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd','Implantacao_R24_2026-10-14/Guedala_Park_R24_Implantacao_Corrigida.FCStd').replace('Entrega_atual_R23.md','Entrega_atual_R24.md')
t=t.replace('Visibilidade_R22_2026-10-14/Apartamento_R22.png','Implantacao_R24_2026-10-14/Planta_corrigida_R24.png').replace('Implantação atual. A R23 ajustou somente rótulos; mantém a geometria e a exibição desta vista R22.','Planta atual R24: sofá do escritório restaurado à implantação documentada, sem atravessar a parede. Referências de hóspedes e tanque antigo ocultas. Não é levantamento físico ou planta executiva.')
t=t.replace('<h2>Escritório — quatro portas alternadas</h2>','<p class="note">As oito vistas de acesso abaixo são referências anteriores R22. Armários e movimentos foram preservados; a posição do sofá e o volume antigo do tanque nessas referências foram corrigidos naR24 e não representam a implantação atual. Consulte a planta acima e o arquivo vigente.</p>\n<h2>Escritório — quatro portas alternadas</h2>',1)
write(gallery,t)

for p in [(Path(__file__).resolve().parent / '../../../../README.md').resolve(),(Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),(Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),(Path(__file__).resolve().parent / '../../../../01_Programa_e_decisoes/Registro_de_decisoes.md').resolve(),(Path(__file__).resolve().parent / '../../../../01_Programa_e_decisoes/Painel_de_decisoes.md').resolve()]:
    t=p.read_text(encoding='utf-8')
    t=t.replace('**14/10/2026 — FreeCAD atual R23:**','**14/10/2026 — FreeCAD atual R24:**',1).replace('Entrega_atual_R23.md','Entrega_atual_R24.md',1)
    marker='Controles por ambiente, corpos atuais visíveis e rótulos coerentes com a orientação física.'
    if marker in t:
        t=t.replace(marker,marker+' A revisão global corrigiu o sinal de rotação do sofá Daiane e ocultou referências antigas, preservando o modelo e a implantação aprovada.',1)
    write(p,t)
print('DOCUMENTATION_R24_INTEGRATED')
