"""Conferência documental e da cena vigente; não abre nem altera o FreeCAD.

--atualizar gera o CSV vinculado ao README; --saida gera a leitura HTML externa.
Não certifica norma, conforto, passagem útil ou instalação.
"""
from pathlib import Path
import argparse, csv, gzip, hashlib, html, json, subprocess, xml.etree.ElementTree as ET, zipfile

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'02_Modelo_3D/Conferencia_uso.csv'
FIELDS = ['id','frente','ambiente','verificacao','valor','unidade','confiabilidade',
          'situacao','leitura','acao','fonte','cad_sha256']


def conferir():
    release = json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf8'))
    cad = ROOT/release['cadPath']
    digest = hashlib.sha256(cad.read_bytes()).hexdigest()
    base = json.loads(gzip.decompress((ROOT/'02_Modelo_3D/Base_verificacao.json.gz').read_bytes()))
    if digest != release['cadSHA256'] or base['sha256'] != digest:
        raise ValueError('Modelo, release e verificação não correspondem')
    with zipfile.ZipFile(cad) as archive:
        xml = ET.fromstring(archive.read('Document.xml'))
    def prop(name, key):
        node = xml.find(f".//ObjectData/Object[@name='{name}']/Properties/Property[@name='{key}']/Float")
        if node is None:
            raise ValueError(f'Propriedade ausente: {name}.{key}')
        return float(node.get('value'))
    # Mesma cena do site, sem DOM, renderização ou alteração de fontes.
    js = r"""
const fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const src=process.argv[1],read=n=>fs.readFileSync(path.join(src,n),'utf8'),app=read('app.js');
const c=vm.createContext({console,matchMedia:()=>({matches:true})});
vm.runInContext(['data.js','cad-data.js','visual-finishes.js','site-copy.js','cad-sync.js'].map(read).join('\n')+'\n'+app.slice(0,app.indexOf("const canvas=$('scene')")),c);
vm.runInContext('globalThis.conferencia=[];for(const table of ["compact","extended"])for(const dining of ["stored","use"]){Object.assign(state,{table,dining});buildScene();conferencia.push({table,dining,...diningClearance(state)});}',c);
process.stdout.write(vm.runInContext('JSON.stringify({cases:conferencia,heights:PROJECT.ceilingByRoom})',c));
"""
    scene = json.loads(subprocess.check_output(['node','-e',js,str(ROOT/'ferramentas/site/src')],text=True,encoding='utf8'))
    rows = []
    def add(id,front,room,check,value,unit,confidence,status,reading,action,source):
        for ref in source.split('|'):
            if not ref.startswith('https://') and not (ROOT/ref.split('#')[0]).exists():
                raise ValueError('Fonte ausente: '+ref)
        rows.append(dict(zip(FIELDS,[id,front,room,check,str(value),unit,confidence,status,reading,action,source,digest])))
    model_readme = '02_Modelo_3D/README.md'
    height_source = '01_Programa_e_decisoes/Pesquisa_pe_direito.md'
    bathroom = '03_Ambientes/Banheiro/Conferencia_bancada_porta.md'
    kitchen = '03_Ambientes/Cozinha/Medidas_e_folgas.md'
    for code,room,name in [('PE','entrada','Porta_Entrada'),('PB','banho','Porta_Banheiro'),
                           ('PQ','quarto','Porta_Quarto'),('PO','escritorio','Porta_Escritorio')]:
        width,height = prop(name,'Largura_Livre'),prop(name,'Altura_Livre')
        add(code,'portas e circulacao',room,'Vão livre entre batentes no CAD',f'{width:g} x {height:g}','mm',
            'projeto/nominal','campo/documento',
            'Escolha nominal de projeto; perfis e espessura da folha continuam gráficos, sem produto especificado.',
            'Conferir folha, eixo, batente, guarnição, maçaneta, sentido e passagem útil no quadro de esquadrias ou na vistoria.',model_readme)
    old_leaf = base['objetos']['Peca076']['caixa_global']
    leaf = max(old_leaf[3]-old_leaf[0],old_leaf[4]-old_leaf[1])
    add('PE-D','portas e circulacao','entrada','Folha antiga oculta / passagem nominal',f'{leaf:g} / {prop("Porta_Entrada","Largura_Livre"):g}','mm',
        'histórico / projeto nominal','campo/documento','A folha antiga oculta é referência histórica; não dimensiona a porta vigente.',
        'Obter quadro de portas e especificação do produto; conferir os 800 mm livres no local.',model_readme)
    for case in scene['cases']:
        label = ('fechada' if case['table']=='compact' else 'aberta')+'; cadeiras '+('guardadas' if case['dining']=='stored' else 'em uso')
        for suffix,key,check in [('F','tableToFridge','Mesa até frente fechada da geladeira'),('L','lateralGap','Faixa lateral nominal junto às cadeiras')]:
            add(f'S-{case["table"]}-{case["dining"]}-{suffix}','portas e circulacao','sala/cozinha',check,
                round(case[key]*10,2),'mm','projeto/nominal','conferencia de uso',
                label+'. Distância do modelo entre volumes; não demonstra passagem com pessoas, puxadores ou portas abertas.',
                'Usar mesa fechada como referência cotidiana; conferir o estado aberto com ocupação e abertura da geladeira.',
                'ferramentas/site/src/app.js|03_Ambientes/Sala_e_jantar/Mesa_e_cadeiras.md')
    add('C-P','banheiro e cozinha','cozinha','Frente nominal de bancada',1550-630,'mm','projeto/nominal','campo',
        '1550 mm da faixa documental menos bancada de estudo de 630 mm; não desconta pessoas ou aberturas.',
        'Conferir parede acabada, puxadores e abertura simultânea dos aparelhos antes de fechar profundidade dos móveis.',kitchen+'|03_Ambientes/Cozinha/README.md')
    add('L-P','banheiro e cozinha','lavanderia','Reserva remanescente com lavadora aberta',1540-1200,'mm','projeto/nominal','conferencia de uso',
        'Conta unidimensional: faixa de 1540 menos reserva de 1200 mm do manual com porta aberta. Os 340 mm não incluem a pessoa.',
        'Conferir operação e retirada da roupa com varal recolhido, sem tratar essa sobra como corredor livre.',kitchen)
    for id,check,value,reading,action in [
        ('B-V','Frente nominal do vaso VIP',1240-590,'Profundidade documental menos vaso nominal de 590 mm; sem eixo real de esgoto.','Conferir eixo do esgoto, posição acabada e uso antes de instalar.'),
        ('B-B','Frente nominal da bancada de 450 mm',1240-450,'Modelo idealizado do estudo existente; não é trajetória do giro real.','Manter 450 mm como hipótese; conferir eixo e maçaneta da porta antes de aumentar a bancada.'),
        ('B-G','Folga ideal bancada/folha hipotética de 700 mm',1240-450-700,'Somente 1240 - 450 - 700. Não inclui batente, maçaneta nem percurso completo da folha.','Não usar como aprovação de giro; conferir porta real e acesso de manutenção BC43.')]:
        add(id,'banheiro e cozinha','banho',check,value,'mm','projeto/nominal','campo/documento',reading,action,bathroom)
    add('B-A','banheiro e cozinha','banho','Torneira, espelheiro e manutenção','pendente','',
        'documental','RT/oficina','Arion centralizada atrás da cuba; alcance, base e alavanca sem desenho suficiente. Retirada BC43 possui estudo condicionado.',
        'Conferir desenho/peça da Arion, sifão, engates e trajeto de retirada com porta e vaso reais; não alterar a sequência por hipótese.',bathroom)
    add('B-I','banheiro e cozinha','banho','Box até o teto e instalações','pendente','',
        'projeto/nominal','RT/campo','Altura do box acompanha teto acabado ainda não medido; fixação, vedação e interfaces elétricas/hidráulicas não resolvidas.',
        'Compatibilizar altura real, trilho e suporte com RT e vidraceiro; identificar volumes elétricos e acesso aos registros.',
        '03_Ambientes/Banheiro/README.md|03_Ambientes/Banheiro/Comparacao_rotas_agua_quente.md')
    for id,room,check,value,unit,status,reading,action,source in [
        ('K-M','cozinha','ME23P: intenção / exigência superior','100 / 300','mm','divergencia',
         'A intenção de 100 mm não atende os 300 mm indicados no manual; folgas laterais não comprovam compensação.',
         'Proposta: acomodar 300 mm e rever o móvel, ou escolher equipamento adequado ao espaço. Preservar a pendência até uma decisão; não instalar no arranjo incompatível.',kitchen),
        ('K-L','lavanderia','LG VC4: reserva livre','640 x 855 + nivelamento','mm','RT/oficina',
         'Reservas documentais: painéis, apoios e conexões ficam fora do espaço livre.',
         'Conferir peças reais e painel isolante de 850 x 600 mm com alumínio junto ao forno/cooktop; MDF comum não foi demonstrado equivalente.',kitchen+'|03_Ambientes/Cozinha/README.md'),
        ('K-F','cozinha','Fischer: separação cooktop/corpo do forno','200','mm','RT/oficina',
         'Exigência do manual Fischer atual, distinta da referência histórica do Venax.',
         'Conferir separação efetiva, apoio e abertura traseira 45 x 560 mm; preservar ventilação e retirada para manutenção.',
         '03_Ambientes/Cozinha/Fischer_Grill/README.md'),
        ('K-R','cozinha','Geladeira IB6: reserva entre obstáculos','801 x 1966 x 847,5','mm','campo/manual',
         'Largura, altura e profundidade documental mínima reservada; não inclui nivelamento adicional nem giro completo de portas.',
         'Conferir ventilação, dobradiças, retirada de gavetas e circulação nos dois estados da mesa.',kitchen),
        ('K-G','cozinha/lavanderia','Gás, exaustão e alimentação elétrica','pendente','','RT/campo',
         'GN e 127 V são diretrizes; grelhas, duto, circuitos e acessos não têm confirmação física.',
         'Preservar ventilação permanente e registros acessíveis; RT confere projeto, capacidade dos circuitos e exaustão.',
         '03_Ambientes/Gas_natural/README.md|03_Ambientes/Cozinha/README.md')]:
        add(id,'banheiro e cozinha',room,check,value,unit,'documental/manual',status,reading,action,source)
    cad_height = prop('Nivel_Parametros','Altura_Nominal')
    for room in ['quarto','escritorio','sala','cozinha','lavanderia','banho','circulacao']:
        planned = float(scene['heights'][room])*10
        finished = prop('Area_Banheiro','Altura_Acabada') if room=='banho' else cad_height
        add('H-'+room,'pe-direito e conforto',room,'Altura acabada CAD / altura final de projeto',
            f'{finished:g} / {planned:g}','mm','projeto/nominal','campo/documento' if finished==planned else 'divergencia',
            f'Delta CAD/projeto: {finished-planned:+g} mm. Referência nominal; teto do banheiro representado por face sem espessura, sem definir sistema ou plenum.',
            'Conferir laje, piso acabado, teto acabado e rebaixos por trecho. Não deduzir espessura de forro nem ajustar armários até o teto sem essa distinção.',height_source+'|'+model_readme)
    add('H-T','pe-direito e conforto','todos','Armários e box até o teto','pendente','','projeto/nominal','campo/RT/oficina',
        'A diretriz de chegar ao teto não define arremate, tolerância de montagem ou espaço de instalações.',
        'Registrar topo do móvel, teto acabado e folga/arremate de montagem por ambiente antes de liberar corte.',
        '04_Moveis/README.md|'+height_source)
    priorities = list(csv.DictReader((ROOT/'03_Ambientes/Conforto_ambiental/Prioridades.csv').open(encoding='utf-8-sig'),delimiter=';'))
    for p in priorities[:2]:
        add('CF-'+p['ordem'],'pe-direito e conforto','todos','Prioridade de conforto existente',p['solucao'],'',
            'estimativa de estudo','campo/RT',p['condicoes'],
            'Conferir operação das janelas/persianas, ruído, chuva e ventilação permanente antes de adotar rotina; não pressupor desempenho térmico medido.',
            '03_Ambientes/Conforto_ambiental/README.md|03_Ambientes/Conforto_ambiental/Prioridades.csv')
    add('CF-L','pe-direito e conforto','cozinha/escritorio','Luz natural e artificial','pendente','','estimativa de estudo','campo/RT',
        'Cozinha sem janela própria e escritório aparecem como pontos de atenção nos estudos condicionais. Não é ensaio de desempenho.',
        'Conferir obstruções, área livre dos vãos e iluminação de tarefa; preservar comandos próprios e validar a instalação.',
        '03_Ambientes/Conforto_ambiental/README.md')
    add('N-1','fontes e criterio','todos','Portaria 725 FAR/FDS','comparacao','','documental','aplicabilidade pendente',
        'Mínimos do programa subsidiado não são cotas físicas e não se estendem automaticamente a todas as modalidades.',
        'Conferir enquadramento, licenciamento e normas aplicáveis com RT; preservar a planta oficial ao estudar o layout.',
        'https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/habitacao/arquivos-1/20250805_Portaria_MCID_725_Especificacoes_MCMV_FAReFDS_COMPILADA_rev.pdf')
    if len({r['id'] for r in rows}) != len(rows):
        raise ValueError('Identificadores repetidos')
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--atualizar',action='store_true')
    parser.add_argument('--saida',type=Path)
    args=parser.parse_args()
    rows=conferir()
    if args.atualizar:
        with OUT.open('w',encoding='utf-8-sig',newline='') as file:
            writer=csv.DictWriter(file,FIELDS,delimiter=';',lineterminator='\n')
            writer.writeheader();writer.writerows(rows)
    if args.saida:
        dest=args.saida.resolve()
        if dest==ROOT or ROOT in dest.parents:
            raise ValueError('HTML de revisão deve ficar fora do repositório')
        dest.mkdir(parents=True,exist_ok=True)
        e=lambda s:html.escape(str(s))
        body=''
        for front in dict.fromkeys(r['frente'] for r in rows):
            body+=f'<h2>{e(front)}</h2><div class="table"><table><thead><tr><th>Item</th><th>Valor e origem</th><th>Leitura</th><th>Ação</th></tr></thead><tbody>'
            for r in rows:
                if r['frente']==front:
                    body+=f'<tr><td><b>{e(r["id"])} · {e(r["ambiente"])}</b><br>{e(r["verificacao"])}</td><td>{e(r["valor"])} {e(r["unidade"])}<br><small>{e(r["confiabilidade"])} · {e(r["situacao"])}</small></td><td>{e(r["leitura"])}</td><td>{e(r["acao"])}</td></tr>'
            body+='</tbody></table></div>'
        (dest/'Conferencia_uso.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Conferência de uso do apartamento</title><style>body{max-width:1200px;margin:auto;padding:24px;background:#f6f4ef;color:#233c3d;font:16px/1.5 system-ui}h1,h2{font-family:Georgia}table{border-collapse:collapse;width:100%;min-width:720px}th,td{border:1px solid #c9d0c5;padding:12px;text-align:left;vertical-align:top}th{background:#e5ebe2}.table{overflow:auto}small{color:#5a675e}h2{margin-top:36px}</style><h1>Conferência de uso do apartamento</h1><p>Portas e circulação, banheiro e cozinha, pé-direito e conforto. Valores documentais e de estudo; medidas reais, instalação e revisão técnica continuam pendentes. Consulte as fontes por item no CSV.</p><p>Proposta: preservar as cotas oficiais, conferir os estados de uso e resolver divergências antes de alterar geometria, comprar ou fabricar.</p>'+body+'</html>',encoding='utf8')
    print(json.dumps({'itens':len(rows),'frentes':list(dict.fromkeys(r['frente'] for r in rows)),
                      'cad_sha256':rows[0]['cad_sha256'],'modelo_alterado':False},ensure_ascii=False))


if __name__=='__main__':
    main()
