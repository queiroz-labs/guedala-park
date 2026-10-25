from pathlib import Path
import json,re,html,hashlib,zipfile,shutil
root=(Path(__file__).resolve().parent / '.').resolve();base=(Path(__file__).resolve().parent / '../..').resolve();project=(Path(__file__).resolve().parent / '../../..').resolve();repo=(Path(__file__).resolve().parent / '../../../..').resolve()
labels=json.loads(((Path(__file__).resolve().parent / 'Rotulos_R23.json').resolve()).read_text(encoding='utf-8'));updates={r['object']:r['after'] for r in labels['changes']}
catalog=json.loads(((Path(__file__).resolve().parent / '../Controles_R21_2026-10-14/Controles_R21.json').resolve()).read_text(encoding='utf-8'))
catalog['file']=labels['file'];catalog['revision']='R23';catalog['source_catalog']='Controles_R21_2026-10-14/Controles_R21.json'
for row in catalog['catalog']:row['label']=updates.get(row['control'],row['label'])
((Path(__file__).resolve().parent / 'Controles_R23.json').resolve()).write_text(json.dumps(catalog,ensure_ascii=False,indent=2),encoding='utf-8')
rooms=[('quarto','Quarto'),('escritorio','Escritório'),('cozinha','Cozinha'),('lavanderia','Lavanderia'),('banheiro','Banheiro'),('banco','Sala e banco')]
guide=['# Guia dos controles atuais R23','', 'Usar **01 — CONTROLES ATUAIS**, escolher o ambiente e editar o campo do objeto original. Os nomes internos abaixo são estáveis; os rótulos identificam a implantação espelhada. Vínculos de acesso não são novos atuadores: selecionar seu objeto original e não editar Placement do vínculo.','']
for room,title in rooms:
 guide+=['## '+title,'','| Controle / objeto original | Campo de estudo | Condição de uso |','|---|---|---|']
 rows=[r for r in catalog['catalog'] if r['room']==room]
 if room in ['quarto','escritorio']:
  def key(r):
   m=re.search(r'porta\s*(\d)',r['label'])
   return (0,int(m[1])) if m else (1,rows.index(r))
  rows=sorted(rows,key=key)
 for r in rows:
  fields='; '.join(k+': '+v for k,v in r['fields'].items());note=r['note']
  if r['shortcut']:note='Selecionar o objeto vinculado. '+note
  guide+=['| '+r['label'].replace('|','/')+' — `'+r['control']+'` | '+fields.replace('|','/')+' | '+note.replace('|','/')+' |']
 guide+=['']
guide+=['Os demais percursos de objetos, painéis e folha da mesa seguem as sequências registradas nas respectivas revisões; não ganharam novos atuadores. Valores de estudo não comprovam batentes ou instalação e não autorizam combinações arbitrárias.','', '[Cobertura e pendências](Cobertura_modulos_R23.md) · [Conjunto atual](../Entrega_atual_R23.md).']
((Path(__file__).resolve().parent / 'Guia_controles_R23.md').resolve()).write_text('\n'.join(guide)+'\n',encoding='utf-8')
modules=json.loads(((Path(__file__).resolve().parent / '../Visibilidade_R22_2026-10-14/Inventario_modulos_R22.json').resolve()).read_text(encoding='utf-8'))
modules['file']=labels['file'];modules['source_inventory']='Inventario_modulos_R22.json; body properties unchanged by labels-only R23'
status=[
 ('Quatro gavetas R08 e duas folhas de correr R14','Ferragens-gabarito, folgas/apoios/carga/batentes reais; programa550/650 preservado'),
 ('Canto simples R04, duas portas independentes e faixas fixas','Limitador físico, fixação/carga/tolerâncias; contatos STEP desconhecidos'),
 ('Duas folhas de correr670×237, curso640 proposto','Aplicação baixa/larga, guias/retenção/apoios/carga reais; reservas semSTEP oficial'),
 ('Cabeceira/vizinha alternadas R18; apoios comuns propostos','Segundo painel18/conjunto36 e apoio da vizinha sem cálculo de fixação/carga; batente/tolerâncias'),
 ('Par de portas comuns R10','Hidráulica/recortes, fixação/carga/batente e encontros reais com gavetas'),
 ('G1/G2/G3 R08, G2 oficial R07; bandejas455/nove gabaritos','Peso caixa/frente/conteúdo, fixação/tolerâncias/contatos perfil-fundo; MOVENTO estático'),
 ('Cocção com modelos de equipamentos preservados','Recortes, apoio e ventilação; Venax3/5vs10cm, distância inferiorKE4GC e isolamentoLG'),
 ('R13 sobre rodas, cabos fixos/cabeças retiradas; frente106/base180','Silicone/carga do rodízio, guias/batente/piso, pega e estrutura independente; nãoMOVENTO/NL'),
 ('Aéreo D com par R10 e canal técnico preservado','Caminho de retorno do Suggar, ventilação/fixação/carga/batente'),
 ('Aéreo C com par R10 e programa interno preservado','Produtos/conteúdo reais, fixação/carga/batente/alcance'),
 ('Aéreo B com par R10','Micro100 acima por escolha, divergente do manual300; ventilação/fixação/carga/batente'),
 ('Aéreo A com par R10','Ventilação/instalação geladeira, fixação/carga/batente/tolerâncias'),
 ('Prateleira aberta do micro, sem mecanismo de porta','Fixação/carga/recortes/passagem; espaço escolhido não dispensa o manual'),
 ('Cesto R15, giro55 e saco removível, frente dividida','Ferragem/retenção/carga/hidráulica/Telca; manutenção interceptaLoop20L em300/400'),
 ('Par R10; modelos da lavanderia preservados','Organização interna, fixação/carga/batente; E21/varal/datums/conexões pendentes'),
 ('Duas gavetas comuns R08','Fixação/carga/tolerâncias; limite de curso em relação à cama de referência não é margem real de uso'),
 ('Quatro portas alternadas R18, apoios comuns','Fixação da parede/divisores/conjunto36, material/peso, conteúdo, batente/tolerâncias'),
 ('Duas portas R12, centro livre','Entrada ideal fecha antes do uso; folha/eixo/maçaneta não medidos; hidráulica/fixação/carga/batente'),
 ('Duas folhas madeira18+espelho4, duas prateleiras removíveis','Vidro/adesivo/pinos/retenção/carga/proteção; luminária/fotometria/elétrica reais'),
 ('Banco R16, quatro setores e programa; exterior1800×550/topo470','Estrutura/fixação/carga/retencão; rotina da folha é proposta nova, pega/transporte/instalação pendentes')]
coverage=['# Cobertura dos vinte módulos — R23','', 'Inventário documental da geometria existente; sem novas medidas ou lista de corte. **C×P×A do corpo** abaixo são propriedades nativas do CAD, não medidas físicas ou envelope acabado de todo o conjunto. No banco, corpo1800×450×400 não substitui exterior1800×550/topo470. Na baixa, corpo145 não substitui frente106/base180.','', '| Módulo / objeto | Corpo CAD C×P×A (mm) | Solução incorporada | Pendência real |','|---|---|---|---|']
for row,(done,pending) in zip(modules['modules'],status):
 dims=row['cad_body_dimensions_mm'];text='×'.join(f'{dims[p]:g}' for p in ['Comprimento','Profundidade','Altura'])
 coverage+=['| '+row['label']+' — `'+row['object']+'` | '+text+' | '+done+' | '+pending+' |']
coverage+=['', 'A R23 acrescenta identificação coerente; R22 corrigiu exibição e R21 organizou controles. Não repetiu testes de movimentos. Fixação, carga, tolerâncias e dados físicos/comerciais continuam condicionantes. E21/PE12/micro e demais equipamentos têm fontes e limites na [R17](../Equipamentos_R17_2026-10-14/README.md).','', '[Conjunto atual](../Entrega_atual_R23.md) · [Pendências técnicas detalhadas](../Apartamento_espelhado_R20_2026-10-14/Pendencias_apartamento_R20.md).']
((Path(__file__).resolve().parent / 'Cobertura_modulos_R23.md').resolve()).write_text('\n'.join(coverage)+'\n',encoding='utf-8');((Path(__file__).resolve().parent / 'Inventario_modulos_R23.json').resolve()).write_text(json.dumps(modules,ensure_ascii=False,indent=2),encoding='utf-8')
# Preserve the old gallery in the same directory so all its relative assets still resolve.
gallery=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R28_2026-10-14.html').resolve();old=(Path(__file__).resolve().parent / '../../04_Documentacao/Galeria_R01_2026-10-13.html').resolve()
if not old.exists():shutil.copy2(gallery,old)
views=json.loads(((Path(__file__).resolve().parent / '../Vistas_R21_2026-10-14/Configuracao_vistas_R21.json').resolve()).read_text(encoding='utf-8'))
css='*{box-sizing:border-box}body{margin:0;color:#263b35;background:#f3f0e8;font:17px/1.55 system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:32px 24px}h1{font-size:clamp(30px,5vw,46px);line-height:1.15}h2{font-size:24px}a{color:#22634e}figure{margin:28px 0;padding:18px;background:white;border-radius:10px}img{display:block;width:100%;height:auto}figcaption{padding:12px 6px 0}.tag{font-size:13px;letter-spacing:.07em;text-transform:uppercase}.note{border-left:4px solid #a56b34;padding:12px 18px;background:#fffaf0}@media(max-width:760px){main{padding:24px 16px}}'
parts=['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · FreeCAD R23</title><style>'+css+'</style></head><body><main>', '<p class="tag">Guedala Park · FreeCAD · R23 · 14/10/2026</p><h1>O apartamento espelhado e os acessos dos armários</h1><p>Cozinha à esquerda ao entrar, portas vizinhas com sentidos opostos e canto simples. Corpos dos armários visíveis e45 acessos organizados por ambiente.</p>', '<p><a href="Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd">Arquivo FreeCAD atual</a> · <a href="Entrega_atual_R23.md">Conjunto e pendências</a> · <a href="Rotulos_R23_2026-10-14/Guia_controles_R23.md">Guia dos controles</a></p>', '<figure><img src="Visibilidade_R22_2026-10-14/Apartamento_R22.png" alt="Apartamento espelhado com os corpos atuais dos armários visíveis"><figcaption>Implantação atual. A R23 ajustou somente rótulos; mantém a geometria e a exibição desta vista R22.</figcaption></figure>', '<p class="note">Modelo de estudo. As vistas abaixo mostram poses ilustrativas e contexto selecionado; o arquivo atual mantém seus valores salvos. Ferragens, fixação, carga, tolerâncias e instalações reais seguem com pendências. Sem liberação de corte, furação ou compra.</p>']
for name,scene in views['scenes'].items():
 path='Vistas_R21_2026-10-14/'+name+'_R22.png';parts+=['<h2>'+html.escape(scene['title'])+'</h2><figure><img loading="lazy" src="'+path+'" alt="'+html.escape(scene['title'],quote=True)+'"><figcaption>'+html.escape(scene['note'])+'</figcaption></figure>']
parts+=['<p><a href="Rotulos_R23_2026-10-14/Cobertura_modulos_R23.md">Cobertura dos vinte módulos</a> · <a href="Galeria_R01_2026-10-13.html">Galeria R01 preservada — histórica</a> · <a href="Plano_ate_19h_2026-10-14.md">Plano até19h</a></p></main></body></html>']
gallery.write_text('\n'.join(parts)+'\n',encoding='utf-8')
block='**14/10/2026 — FreeCAD atual R23:** apartamento espelhado, cozinha à esquerda ao entrar e portas vizinhas com aberturas opostas. Canto vigente usa duas portas independentes e faixas fixas; a articulação79T8500 das notas anteriores foi aposentada. Controles por ambiente, corpos atuais visíveis e rótulos coerentes com a orientação física. Programa/modelos preservados; cotas e ferragens propostas, sem corte/furação/compra. A rotina nova da almofada no setor da folha do banco permanece proposta, distinta do aceite anterior para bebidas/balde. '
for p,links in [((Path(__file__).resolve().parent / '../../../../README.md').resolve(),'[Galeria atual](01_Projeto/Modelo_FreeCAD/04_Documentacao/Galeria_R28_2026-10-14.html) · [Arquivo e pendências](01_Projeto/Modelo_FreeCAD/04_Documentacao/Entrega_atual_R23.md).'),((Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),'[Galeria atual](Modelo_FreeCAD/Galeria.html) · [Arquivo e pendências](Modelo_FreeCAD/Entrega_atual_R23.md).'),((Path(__file__).resolve().parent / '../../../../ESTADO_ATUAL.md').resolve(),'[Modelo atual, resultados e pendências](Modelo_FreeCAD/Entrega_atual_R23.md) · [Vistas dos acessos](Modelo_FreeCAD/Galeria.html).')]:
 text=p.read_text(encoding='utf-8')
 if '**14/10/2026 — FreeCAD atual R23:**' not in text:
  first,rest=text.split('\n',1);text=first+'\n\n'+block+links+' As entradas datadas abaixo preservam o histórico; onde houver divergência de implantação/cinemática, consultar a versão atual.\n'+rest
  p.write_text(text,encoding='utf-8')
modelread=(Path(__file__).resolve().parent / '../../04_Documentacao/Historico_FreeCAD.md').resolve();text=modelread.read_text(encoding='utf-8');first,rest=text.split('\n',1)
if '[Rótulos e documentação — R23]' not in text:text=first+'\n\n[Rótulos e documentação — R23](Rotulos_R23_2026-10-14/README.md): **apartamento atual**. [Arquivo e resultados](Entrega_atual_R23.md) · [Galeria atual](Galeria.html) · [Guia dos controles](Rotulos_R23_2026-10-14/Guia_controles_R23.md) · [Cobertura dos vinte módulos](Rotulos_R23_2026-10-14/Cobertura_modulos_R23.md).\n'+rest
text=text.replace('[Peças atuais visíveis — R22](Visibilidade_R22_2026-10-14/README.md): **apartamento atual**.','[Peças atuais visíveis — R22](Visibilidade_R22_2026-10-14/README.md): base preservada e incorporada àR23.');modelread.write_text(text,encoding='utf-8')
plan=(Path(__file__).resolve().parent / '../../04_Documentacao/Plano_ate_19h_2026-10-14.md').resolve()
plan.write_text('''# Continuidade do FreeCAD até19h — 14/10/2026

Elias autorizou continuar, polir e revisar até19h de hoje em São Paulo. O agendamento existente retoma esta conversa a cada30min, com avisos apenas sobre mudanças relevantes, conclusão, falha ou informação indispensável.

## Etapas concluídas

| Etapa | Resultado atual |
|---|---|
| Implantação | Apartamento inteiro espelhado na R20; cozinha à esquerda ao entrar pelo vão do modelo |
| Portas | Sentidos vizinhos opostos na R18, mantidos após reflexão; encontros alterados conferidos em seu escopo |
| Navegação |45 acessos por seis ambientes R21; fontes e pais preservados |
| Exibição |101 resultados atuais expostos R22; oito vistas de acesso inspecionadas |
| Identificação | R23 alinha folhas/frentes/dobradiças/laterais aos controles e à orientação física |
| Documentação | Galeria atual, guia e cobertura por vinte módulos reconciliados; R01 preservada como histórico |

Revisão atual: [R23](Rotulos_R23_2026-10-14/Guedala_Park_R23_Rotulos_Consistentes.FCStd). [Conjunto atual e pendências](Entrega_atual_R23.md).

## Continuação e fechamento até19h

Avançar somente quando houver trabalho independente útil ou nova evidência documental suficiente. Prioridades técnicas continuam fixação/carga/tolerâncias/batentes, ferragens reais de correr/cesto/rodas, vidro/adesivo/hidráulica e divergências de ventilação/instalação dos equipamentos. Não substituir dados físicos ausentes por medidas inventadas, modificar escolhas expressas ou mover instalações desconhecidas.

Com apenas dependências físicas/comerciais/estruturais indisponíveis, manter o modelo e os resultados prontos, registrar a dependência e ficar quieto. Não reconstruir revisões, repetir poses/reaberturas/vistas ou criar revisões artificiais para preencher o prazo. O fechamento entrega arquivo atual, mudanças/resultados com limites e pendências reais; não há liberação de corte, furação, compra ou contato com fornecedores.

Consultar sempre [Estado_noturno.md](Canto_2026-10-13/Cinematica_R03/Estado_noturno.md). O prazo continua19h; trabalho pronto não exige repetição.
''',encoding='utf-8')
# Structural verification of the newly reconciled local index, not repeated CAD tests.
targets=[]
for match in re.finditer(r'(?:href|src)="([^"]+)"',gallery.read_text(encoding='utf-8')):
 ref=match[1]
 if '://' in ref or ref.startswith('#'):continue
 target=((Path(__file__).resolve().parent / '../..').resolve()/ref.split('#')[0]).resolve();assert target.exists(),target;targets.append(str(target))
p=Path(labels['file']);assert hashlib.sha256(Path(labels['source']).read_bytes()).hexdigest()==labels['source_sha256']
with zipfile.ZipFile(p) as z:assert z.testzip() is None
report={'file':str(p),'crc_ok':True,'source_R22_unchanged':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'gallery_local_targets_checked':len(targets),'control_entries':len(catalog['catalog']),'modules':len(modules['modules']),'legacy_gallery_preserved':str(old),'scope':'Documentary reconciliation and labels only. No repeated movement, collision or reopening tests.'}
((Path(__file__).resolve().parent / 'Consolidacao_R23.json').resolve()).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True))
