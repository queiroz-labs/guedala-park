from pathlib import Path
import json, csv, html, hashlib
from datetime import datetime, timezone, timedelta

p=(Path(__file__).resolve().parent / '.').resolve()
b=(Path(__file__).resolve().parent / '../..').resolve()
d=json.loads(((Path(__file__).resolve().parent / 'Medidas_atual_R28.json').resolve()).read_text(encoding='utf-8'))
items={r['object']:r for r in d['items']}
box=lambda n:items[n]['world_mirrored_bbox_mm']
measurements={
 'micro_top_z':box('Peca351')[5], 'module_B_base_z':next(r for r in d['modules'] if r['object']=='Modulo010')['closed_adopted_bbox_mirrored_mm'][2],
 'e21_body_bbox':box('Peca155'), 'venax_rear_y':box('Peca133')[4],
 'suggar_channel_bbox':box('Peca321'), 'suggar_base_bbox':box('Peca318'), 'suggar_top_bbox':box('Peca319'),
 'wall_y_reference':7000, 'wall_e21_x_reference':4850, 'laundry_edge_x_reference':4380,
 'datum_warning':'Wall and cabinetry reference planes inherited from R17, not measured on site.'}
measurements['micro_top_clearance']=measurements['module_B_base_z']-measurements['micro_top_z']
measurements['e21_side_gaps']=[4850-box('Peca155')[3],box('Peca155')[0]-4380]
measurements['venax_envelope_rear_clearance']=7000-box('Peca133')[4]
assert measurements['micro_top_clearance']==100
assert measurements['e21_side_gaps']==[70,50]
assert measurements['venax_envelope_rear_clearance']==15
((Path(__file__).resolve().parent / 'Cotas_instalacoes_R28.json').resolve()).write_text(json.dumps(measurements,ensure_ascii=False,indent=2),encoding='utf-8')

findings=[
 ('01','Alta','Aquecedor E21: faixa lateral insuficiente','Conflito documental demonstrado no CAD',
  'Há 70 e 50 mm laterais, diante de 200 mm recomendados em cada lado. A faixa de 470 mm não acomoda corpo de 350 mm mais duas reservas de 200 mm: faltam 280 mm nessa configuração.',
  'Compatibilizar a posição do aquecedor, aéreo, varal e instalações com as referências reais e profissional responsável. Corrigir depois a representação: corpo CAD 530 mm versus 483 mm no manual; duto quadrado 80 versus Ø60. Não reduzir esses gabaritos antes de localizar os datums, conexões e terminação. Montagem sobre madeira não é admitida pelo manual.',
  '../Equipamentos_R17_2026-10-14/README.md'),
 ('02','Alta','Micro-ondas ME23P: folga superior divergente','Escolha expressa preservada; requisito não atendido no modelo',
  'Topo do aparelho Z1840 e base do aéreo B Z1940: 100 mm. A referência do manual é 300 mm; a reserva invade o aéreo em 200 mm.',
  'Resolver a compatibilização da instalação antes de executar o nicho. Os 100 mm foram escolhidos por Elias e não foram alterados nesta revisão; essa escolha não demonstra dispensa do manual. Laterais abertas não foram usadas para compensar a diferença.',
  '../Equipamentos_R17_2026-10-14/README.md'),
 ('03','Alta','Depurador Suggar: retorno de ar incompleto','O modelo ainda não representa um caminho de ar contínuo',
  'Canal 196 × 178 mm entre Z1976 e 2532, limitado pela base inteira Z1958–1976 e tampo inteiro Z2532–2550. O topo do aparelho Z1916 fica 42 mm abaixo da base do módulo.',
  'Detalhar ligação, abertura de entrada e saída, retorno e fixação conforme o aparelho escolhido. Conferir acesso ao filtro e distância à cocção. A largura interna de 614 mm, favorável ao nicho de 603 mm, não resolve ventilação. Não fazer recortes por posição inferida.',
  '../Equipamentos_R17_2026-10-14/README.md'),
 ('04','Alta','Forno Venax / cooktop KE4GC / LG','Dimensões de instalação e instruções ainda incompatibilizadas',
  'O envelope do forno termina 15 mm antes da parede; isso não representa os 50 mm do cenário documental. O manual Venax traz 30 mm laterais / 50 mm atrás e também 100 mm em toda a volta. A distância de 200 mm entre fundo do cooktop e topo do forno depende do ponto inferior instalado ainda desconhecido.',
  'Obter corte cotado do KE4GC, referências do corpo/frente/apoio do forno e resolver a divergência do manual. Detalhar ventilação, gás, apoio e recortes. A LG exige isolamento 850 × 600 mm com alumínio voltado ao forno quando a proximidade for inevitável; a lateral de MDF não comprova essa solução. A altura externa de 131 mm do cooktop não deve ser aplicada como profundidade instalada.',
  '../Revisao_fontes_coccao_R23_2026-10-14/Revisao_documental.md'),
 ('05','Antes da execução','Tanque, bancada e hidráulica','Recorte e produto reais não modelados',
  'O tanque e seu vazio útil atravessam a bancada indicada como “a recortar”. A hidráulica do gabinete e do cesto é representada por reservas.',
  'Definir tanque/cuba reais, gabarito de recorte, apoios, vedação e sifões/conexões antes de detalhar a pedra. Não remover interseções com um corte arbitrário.',
  '../Revisao_integrada_R23_2026-10-14/README.md'),
 ('06','Antes da execução','Dobradiças, batentes e gavetas','Movimentos geométricos não equivalem à montagem comercial',
  '86° é limite de estudo: não comprova o limitador 70T3553. Há contatos internos nas fontes STEP de dobradiças e MOVENTO cuja causa continua desconhecida. Guias MOVENTO são sólidos estáticos.',
  'Confirmar montagem comercial, batente, parafusos, canecos, apoios duplos e tolerâncias. Fechar peso da caixa + frente + conteúdo para a classe candidata de 40 kg. LW−42 é largura interna. Manter as fontes oficiais e não desbastar ou deslocar peças para apagar contatos.',
  '../Dobradicas_R10_2026-10-14/README.md'),
 ('07','Antes da execução','Portas de correr do roupeiro e maleiro','Reservas de ferragens, sem STEP oficial',
  'Roupeiro: duas folhas 995 × 1999 mm, curso 965 mm. Maleiro: duas folhas 670 × 237 mm, curso 640 mm. Aplicação muito baixa e larga do maleiro não está comprovada.',
  'Confirmar trilhos, carros, retenção antidesencaixe, batentes, apoio e carga do sistema comum candidato. Substituir as reservas pelo desenho comercial cotado quando disponível; não comprar com base apenas nas caixas de reserva.',
  '../Correr_R14_2026-10-14/README.md'),
 ('08','Antes da execução','Gaveta baixa sobre rodas','Produto e capacidade ainda não definidos',
  'Interno 1187 × 406 × 88 mm; frente 106 mm, base 180 mm e recuo 80 mm preservados. Seis rodízios são gabaritos. Só a madeira pesa aproximadamente 12,92–15,50 kg nos cenários usados.',
  'Confirmar rodízios de silicone, altura real, capacidade, fixação, piso, guias e retirada. Não distribuir a carga por seis como garantia de apoio simultâneo. Preservar cabos fixos com cabeças retiradas; não trocar por MOVENTO ou cabos retráteis.',
  '../Gaveta_rodas_R13_2026-10-14/README.md'),
 ('09','Antes da execução','Banco e cesto: estrutura e uso','Geometria proposta; ferragens e esforço não homologados',
  'Banco 1800 × 550 mm, topo 470; folha 800 × 350 × 70 preservada. Último setor propõe remover almofada, ocupar os outros três setores fechados e recuar a folha 24 mm. Cesto mantém giro de 55° e saco removível.',
  'Dimensionar apoios, fixações, retenção e cargas; conferir pega/manuseio. Na manutenção do cesto, estacionar a Loop com controle 650 antes de retirar a armação, e devolvê-la após recompor e fechar. A posição temporária tem percurso geométrico conferido, mas não valida a operação por uma pessoa.',
  '../Manutencao_R26_2026-10-14/README.md'),
 ('10','Antes da execução','Banheiro: entrada, espelhos e gabinete','Conflito de uso conhecido e levantamento pendente',
  'A folha ideal de entrada, 700 mm não medidos, interfere no gabinete inferior aberto. A condição de uso estudada exige fechar a entrada antes de abrir esse gabinete. Vidros, adesivos e carga dos espelhos são candidatos.',
  'Conferir a situação física na etapa de levantamento e preservar a porta original. Detalhar vidro/adesivo, prateleiras/pinos, hidráulica e fixação. Não há intertravamento; a condição de uso não elimina fisicamente o conflito. Não foi solicitado novamente a Elias o dado indisponível.',
  '../Banheiro_R12_2026-10-14/README.md'),
 ('11','Antes da execução','Teto e fixação dos aéreos','Folga nominal proposta, sem levantamento acabado',
  'Escritório: base 1900, topo 2450, sob teto de estudo 2470; folga nominal 20 mm. Caixa de 2000 × 350 × 550 e espaço interno foram preservados. Cozinha 20 mm e quarto 30 mm nas referências de estudo.',
  'Conferir teto acabado, irregularidades, montagem, suportes e capacidade da parede. Os 20 mm não são mínimo universal nem margem garantida. Não encurtar a caixa para compensar informação ausente.',
  '../Folga_teto_R28_2026-10-14/README.md'),
 ('12','Representação','Mesa/cadeiras e enchimento/box','Interseções de gabaritos não resolvidas por geometria real',
  'Dez contatos mesa × Lina envolvem caixas cheias que ocupam os vazios das cadeiras reais. Três contatos enchimento × box dependem de altura, vidro e perfis não medidos.',
  'Trocar pelos contornos reais quando houver dados suficientes. Manter posição aprovada das cadeiras e não apagar o enchimento para produzir uma auditoria sem contatos. Esses registros não permitem afirmar colisão física nem ausência dela.',
  '../Auditoria_posicoes_R23_2026-10-14/README.md')]
((Path(__file__).resolve().parent / 'Achados_R28.json').resolve()).write_text(json.dumps([dict(zip(['id','prioridade','item','classificacao','evidencia','acao','fonte'],f)) for f in findings],ensure_ascii=False,indent=2),encoding='utf-8')

with ((Path(__file__).resolve().parent / 'Medidas_925_solidos_R28.csv').resolve()).open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f,delimiter=';');w.writerow(['Objeto','Rotulo','Modulo','Tipo','Dimensoes_nativas_mm','Xmin','Ymin','Zmin','Xmax','Ymax','Zmax','DimX','DimY','DimZ','Expressoes'])
 for r in d['items']:w.writerow([r['object'],r['label'],r['root'],r['type'],json.dumps(r['native_dimensions_mm'],ensure_ascii=False),*r['world_mirrored_bbox_mm'],*r['world_bbox_size_mm'],json.dumps(r['expressions'],ensure_ascii=False)])

esc=html.escape
num=lambda x:f'{x:g}'
module_rows=''
for r in d['modules']:
 q=r['body_dimensions_mm'];bb=r['closed_adopted_bbox_mirrored_mm']
 note={'Modulo007':'Corpo não substitui frente 106 / base 180; envelope inclui apoios independentes.', 'Modulo019':'Exterior aprovado 1800 × 550 / topo 470. Profundidade 450 é corpo; encosto externo não está incluído.', 'Modulo016':'Conjunto inteiro baixado 20; vãos preservados.', 'Modulo001':'Envelope de canto em L; não é caixa retangular utilizável.'}.get(r['object'],'')
 module_rows+=f'<tr><td>{esc(r["label"])}<small>{r["object"]}</small></td><td>{" × ".join(num(q[k]) for k in ["Comprimento","Profundidade","Altura"])}</td><td>{num(bb[2])}–{num(bb[5])}</td><td>{r["adopted_solid_count"]}</td><td>{note}</td></tr>'

cards=''.join(f'<article class="finding"><div class="tag">{esc(pr)} · {esc(cl)}</div><h3>{i}. {esc(t)}</h3><p>{esc(ev)}</p><p><b>O que corrigir ou fechar:</b> {esc(ac)}</p><a href="{src}">Evidência técnica registrada</a></article>' for i,pr,t,cl,ev,ac,src in findings)
captions=[('01_geral_R28.png','Apartamento completo','Vista nativa da R28, na implantação espelhada vigente. Não é levantamento da unidade.'),('02_planta_R28.png','Planta atual','Sofá na posição diária corrigida; fontes históricas não substituem resultados atuais.'),('03_cozinha.png','Cozinha','290 peças atuais isoladas para leitura. Equipamentos são volumes de referência; veja itens 02–04.'),('04_lavanderia.png','Lavanderia','69 peças atuais. Folgas laterais do E21 e caminho do duto permanecem pendentes; tanque ainda exige recorte real.'),('05_quarto.png','Quarto','229 peças atuais. Canto simples, roupeiro/maleiro, cabeceira dividida e espelho lateral preservados.'),('06_escritorio.png','Escritório','95 peças atuais. Aéreo com quatro portas, base 1900 e topo 2450; sem diminuição da caixa.'),('07_banheiro.png','Banheiro','84 peças atuais. Entrada ideal mostrada translúcida somente na cópia visual. Gabinetes fechados; não é um novo teste de abertura.'),('08_banco.png','Banco e mesa','53 peças atuais. Caixas das cadeiras Lina translúcidas somente nesta vista para mostrar o banco; não representam os vazios reais das cadeiras.')]
gallery=''.join(f'<figure><a href="{fn}"><img src="{fn}" alt="{esc(title)}" loading="lazy"></a><figcaption><b>{title}.</b> {cap}</figcaption></figure>' for fn,title,cap in captions)
now=datetime.now(timezone(timedelta(hours=-3))).strftime('%d/%m/%Y %H:%M')
content=f'''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guedala Park · revisão R28</title><style>
body{{font:16px/1.55 system-ui,sans-serif;background:#f5f3ee;color:#26312f;margin:0}}main{{max-width:1150px;margin:auto;padding:42px 28px}}h1{{font-size:38px;line-height:1.15}}h2{{margin-top:42px;border-top:1px solid #ccc;padding-top:22px}}h3{{margin:8px 0;font-size:21px}}a{{color:#126565}}.lead{{font-size:20px;max-width:960px}}.stats{{display:flex;gap:14px;flex-wrap:wrap}}.stats div,.finding{{background:white;border:1px solid #ddd;padding:20px;border-radius:10px}}.stats b{{font-size:26px;display:block}}.finding{{margin:16px 0;border-left:5px solid #a36536}}.tag,small{{font-size:13px;color:#596661}}small{{display:block}}table{{border-collapse:collapse;width:100%;background:white;font-size:14px}}td,th{{padding:11px;border-bottom:1px solid #ddd;text-align:left;vertical-align:top}}th{{background:#dfe9e4}}.scroll{{overflow-x:auto}}figure{{margin:24px 0;background:white;padding:14px;border-radius:10px}}img{{width:100%;height:auto;display:block}}figcaption{{padding:12px 2px}}.note{{background:#e3ebe6;padding:18px;border-radius:8px}}code{{overflow-wrap:anywhere}}@media print{{body{{background:white}}main{{padding:0}}article,figure,tr{{break-inside:avoid}}img{{max-height:460px;object-fit:contain}}h2{{break-before:auto}}}}
</style><main><small>Revisão solicitada por Elias · {now} · São Paulo</small><h1>O que ainda precisa ser corrigido no projeto</h1>
<p class="lead">A R28 está consistente nas cotas de corpo dos 20 módulos comparadas às planilhas. A inspeção visual e documental não confirmou um novo deslocamento incorreto de móvel. As prioridades de correção concentram-se na instalação dos equipamentos, no detalhamento comercial das ferragens e nas condições reais de montagem.</p>
<div class="stats"><div><b>20</b>módulos comparados às planilhas</div><div><b>925</b>sólidos atuais inventariados</div><div><b>8</b>vistas inspecionadas</div><div><b>0</b>divergências nos parâmetros comparados</div></div>
<p class="note"><b>Conclusão:</b> estudo CAD organizado e verificável, com pendências que impedem tratá-lo como projeto executivo liberado. As medidas abaixo são do modelo. Não substituem medidas físicas, tolerâncias, resistência, lista de corte ou aprovação de instalação.</p>
<nav><a href="#achados">Correções prioritárias</a> · <a href="#medidas">Cotas dos 20 módulos</a> · <a href="#vistas">Vistas</a> · <a href="#metodo">Escopo e evidências</a></nav>
<h2 id="achados">Pendências e ação necessária</h2><p>Os itens abaixo consolidam achados conhecidos conferidos contra a versão atual. Não são apresentados como doze erros novos descobertos nesta rodada.</p><p class="note"><b>Avanço autônomo posterior:</b> <a href="../Cargas_gavetas_R28_2026-10-14/Cargas_gavetas_R28.html">orçamento de massa das nove gavetas</a>, incluindo as duas bandejas da G2 e correção da distinção entre carga útil e margem restante. G3: madeira 15,63 kg; G2 com bandejas: 8,75 kg no cenário 900 kg/m³. Pesos reais, acessórios, conteúdo, capacidade comercial e fixação ainda pendentes; CAD preservado.</p>{cards}
<h2 id="medidas">Cotas conferidas no arquivo</h2><p>Unidade: mm. C × P × A corresponde às propriedades de corpo; Z é o intervalo do conjunto de sólidos adotados em posição salva, podendo incluir frente, ferragem ou apoio. Uma propriedade de corpo diferente do envelope completo não é, por si só, erro.</p><div class="scroll"><table><thead><tr><th>Módulo</th><th>Corpo C × P × A</th><th>Z do conjunto</th><th>Sólidos</th><th>Observação</th></tr></thead><tbody>{module_rows}</tbody></table></div>
<p><a href="Medidas_925_solidos_R28.csv">Inventário completo dos 925 sólidos em CSV</a> · <a href="Medidas_atual_R28.json">Dimensões nativas, posições e expressões em JSON</a> · <a href="Cotas_instalacoes_R28.json">Cálculo das folgas de instalação</a></p>
<h2 id="vistas">Conferência visual da revisão vigente</h2><p>As seis vistas por ambiente são recortes de seleção, sem paredes e objetos de outros ambientes. Ausência de um objeto numa vista isolada não significa exclusão do apartamento. Todas mostram a posição salva; não foi executada nova sequência de movimentos. Transparências são apenas de cópias visuais.</p>{gallery}
<h2 id="metodo">Escopo, resultados e limites</h2>
<p>Leitura nova da R28 aberta: 5.899 objetos, seleção de 925 sólidos atuais, comparação das três cotas de corpo dos 20 módulos com seus valores de planilha e inventário anterior. Nenhuma divergência nesses campos; nenhuma envoltória com dimensão não positiva ou coordenada não finita. As dimensões nativas disponíveis e expressões dos 925 sólidos foram exportadas, mas não foram homologadas individualmente como cotas de fabricação ou furos comerciais.</p>
<p>Revisão documental cruzou decisões vigentes, equipamentos R17, fontes de cocção, auditorias de implantação e movimentos, controles R28 e revisões de montagem. Os ensaios anteriores foram aproveitados com seus limites: arquitetura de 27 paredes e nove pisos, sem teto físico sólido; colisões do sofá corrigidas na R24, espelho/cabeceira na R25, dois perfis nativos na R27. Não houve repetição de varredura global, booleanas ou testes antigos para somar contagens.</p>
<p>A folga de 20 mm da R28 é proposta sob teto hipotético; seus testes de descida e portas são evidência limitada ao escopo registrado. Amostras de posições não comprovam continuidade, qualquer combinação simultânea, pessoas, tolerâncias, carga ou execução comercial dos mecanismos.</p>
<p>As vistas gerais foram capturadas no documento atual. Os detalhes usaram cópia visual descartada após a inspeção; transformações dessas cópias não foram usadas como teste de validade geométrica. Uma falha de preparação da câmera (“No SWIG wrapped library loaded”) foi resolvida carregando pivy.coin; não alterou o projeto. O arquivo canônico não foi salvo ou modificado, a câmera original foi restaurada e somente a R28 ficou aberta, isTouched=False.</p>
<p><a href="Fechamento_visual.json">Fechamento da sessão</a> · <a href="Achados_R28.json">Achados estruturados</a> · <a href="../Consistencia_controles_R28_2026-10-14/Guia_controles_vigentes_R28.md">Guia vigente dos 46 acessos</a> · <a href="../Entrega_atual_R28.md">Entrega atual e histórico</a></p>
<p>Arquivo: <a href="../Folga_teto_R28_2026-10-14/Guedala_Park_R28_Folga_Teto_Proposta.FCStd">Guedala_Park_R28_Folga_Teto_Proposta.FCStd</a><br>SHA-256 preservado: <code>{d['sha256']}</code>.</p>
<p><small>Este relatório responde à revisão solicitada agora. A consulta suportada do aplicativo não expôs o modelo efetivo deste turno; o relatório não constitui comprovação da revisão final Astra reservada para 18h30. Não houve acesso a transcrições ou metadados internos para tentar comprovar o modelo.</small></p>
</main></html>'''
((Path(__file__).resolve().parent / 'Relatorio_revisao_R28.html').resolve()).write_text(content,encoding='utf-8')
assert hashlib.sha256(Path(d['file']).read_bytes()).hexdigest()==d['sha256']
print(json.dumps({'modules':len(d['modules']),'solids':len(d['items']),'findings':len(findings),'images':len(captions),'sha_unchanged':True,'report':str((Path(__file__).resolve().parent / 'Relatorio_revisao_R28.html').resolve())},ensure_ascii=False))
