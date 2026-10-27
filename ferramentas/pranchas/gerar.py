"""python ferramentas/pranchas/gerar.py: SVG + HTML A3 + PDF R02 + impacto.

Não abre nem modifica o CAD. As dimensões de construção vêm do CSV/JSON;
constantes neste arquivo são somente paginação, escalas e estilos de desenho.
"""
import hashlib
import argparse
from io import BytesIO
from html import escape
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap

sys.dont_write_bytecode = True
from medidas import Medida, carregar, resolver, numero
from desenho import Folha, pdf

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / '06_Entregas/Caderno_pranchas'
NOMINAL, MEDIDO = '#94621c', '#006b60'


def cad(value, ref):
    return Medida(value, 'nominal', ('R53:'+ref,))


def valor(f, key, medida, movel='', mostrar=True):
    f.cotas[key] = dict(mm=None if medida.mm is None else round(medida.mm, 3), origem=medida.origem,
                        fontes=list(medida.fontes), movel=movel, prancha=f.codigo)
    if medida.mm is None:
        msg = f'{key}: a levantar'
        if msg not in f.avisos:
            f.avisos.append(msg)
        return 'PENDENTE'
    return f'{medida.mm:g} '+('M' if medida.origem == 'medido' else 'N')


def cota(f, key, medida, x, y, xx, yy, movel=''):
    txt = valor(f, key, medida, movel)
    color = MEDIDO if medida.origem == 'medido' else NOMINAL
    f.linha(x,y,xx,yy,color, .18, medida.origem != 'medido')
    for a,b in ((x,y),(xx,yy)):
        f.linha(a-1,b+1,a+1,b-1,color)
    f.texto((x+xx)/2+1,(y+yy)/2-1,txt,2.5,color)


def chamada(f, x, y, text, occupied, color='#263238'):
    """Distribui rótulos de papel sem alterar a coordenada do símbolo."""
    width=max(7,len(text)*1.4)
    offsets=[(dx,dy) for radius in range(1,9) for dx,dy in
             ((radius*4,-3),(radius*4,3),(-radius*4-width,-3),(-radius*4-width,3),(0,-radius*4),(0,radius*4))]
    for dx,dy in offsets:
        xx,yy=x+dx,y+dy;box=(xx,yy-3,xx+width,yy+1)
        if not (15<xx and xx+width<201 and 35<yy<208):continue
        if all(box[2]<b[0] or box[0]>b[2] or box[3]<b[1] or box[1]>b[3] for b in occupied):
            occupied.append(box);f.linha(x,y,xx,yy-1,color,.1)
            f.texto(xx,yy,text,2.4,color);return
    f.avisos.append('Chamada sem espaço: '+text+'; consultar tabela de coordenadas.')


class Projeto:
    def __init__(self, cenario=None):
        self.rows = carregar(ROOT)
        self.recalculo = None
        if cenario:
            sys.path.insert(0, str(ROOT/'ferramentas/medidas'))
            from recalcular import entradas, base, calcular
            self.rows = entradas(ROOT, cenario)
            self.recalculo = calcular(self.rows, base(ROOT))
        self.doc = json.loads((ROOT/'06_Entregas/Planta_cotada/Cotas.json').read_text(encoding='utf-8'))
        self.data = self.doc['pranchas']
        self.geo = json.loads((ROOT/'06_Entregas/Caderno_pranchas/Geometria.json').read_text(encoding='utf-8'))
        path = ROOT/self.geo['cad_path']
        if hashlib.sha256(path.read_bytes()).hexdigest() != self.geo['cad_sha256']:
            raise ValueError('Exportação desatualizada: executar exportar.py e verificação completa do modelo.')
        mirror = self.m(self.data['mirror']).mm
        self.objects = {}
        for item in self.geo['objects']:
            b = item['box']
            self.objects[item['id']] = dict(item, box=[mirror-b[3], b[1], b[2], mirror-b[0], b[4], b[5]])
        self.modules = {}
        for name in sorted({o['module'] for o in self.objects.values() if o['module']}):
            objs = [o for o in self.objects.values() if o['module'] == name]
            boxes = [o['box'] for o in objs]
            self.modules[name] = dict(id=name, room=objs[0]['room'], label=name,
                box=[min(b[i] for b in boxes) if i<3 else max(b[i] for b in boxes) for i in range(6)])
        self.alterados = set()
        if self.recalculo:
            for name, box in self.recalculo['envelopes'].items():
                obj = self.modules.get(name, self.objects.get(name))
                if obj is None:
                    raise ValueError('Alvo recalculado ausente da exportação: '+name)
                if box != obj['box']:
                    self.alterados.add(name)
                if any(box[j+3] <= box[j] for j in range(3)):
                    raise ValueError('Envelope recalculado não positivo: '+name)
                obj['box'] = box

    def m(self, code):
        return resolver(self.rows, code)

    def refs(self, record):
        return [self.m(k) for k in record['refs']]

    def pe(self, room):
        return self.m(self.data['ceiling'][room])

    def plano(self, code, title, kind):
        f=Folha(code,title,50)
        ox,oy=30,42
        labels=[]
        def rect(b, color, fill=None):
            f.caixa(ox+b[0]/50,oy+b[1]/50,b[2]/50,b[3]/50,color,fill)
        for record in self.data['floors']:
            ms=self.refs(record); b=[m.mm for m in ms]
            if None in b:
                f.avisos.append('Piso incompleto: '+record['room']);continue
            rect(b,'#d9dfe0','#f5f6f3')
        for record in self.data['walls']:
            ms=self.refs(record);b=[m.mm for m in ms]
            if None in b:
                raise ValueError('Parede sem dimensão: '+str(record['refs']))
            rect(b,'#526269','#c4ccce')
        for record in self.data['openings']:
            ms=self.refs(record); b=[m.mm for m in ms]
            if None in b[:4]:
                f.avisos.append(record['id']+': posição pendente');continue
            rect(b[:4],'#627d92','#e4eff4')
            if kind=='paredes':
                length=max(b[2],b[3]); i=2 if b[2]>=b[3] else 3
                valor(f,record['id']+'-vao',ms[i],record['room'])
                f.texto(ox+b[0]/50,oy+b[1]/50-2,record['id'],2.1)
        if kind=='layout':
            for obj in self.objects.values():
                b=obj['box']
                if obj['module'] in self.alterados:
                    continue  # Nunca esticar painéis, ferragens ou espessuras.
                if b[5]<=0 or obj['label'].startswith(('glass','door','floor')):
                    continue
                rect([b[0],b[1],b[3]-b[0],b[4]-b[1]],'#96a0a2')
            for name,obj in self.modules.items():
                b=obj['box'];rect([b[0],b[1],b[3]-b[0],b[4]-b[1]],'#263e4b')
                chamada(f,ox+(b[0]+b[3])/100,oy+(b[1]+b[4])/100,name,labels)
            f.texto(210,45,'R53: envelopes de todas as peças visíveis exportadas',3.2)
            for i,(name,obj) in enumerate(self.modules.items()):
                b=obj['box']; y=55+i*6
                f.texto(210,y,name,3)
                f.texto(224,y,' × '.join(valor(f,name+'-'+k,cad(v,name),name) for k,v in
                    [('L',b[3]-b[0]),('P',b[4]-b[1]),('H',b[5]-b[2])]),2.7,NOMINAL)
        elif kind=='paredes':
            seen=set()
            for record in self.data['floors']:
                room=record['room']
                if room in seen:continue
                seen.add(room);ms=self.refs(record);x,y,w,h=[m.mm for m in ms]
                cota(f,room+'-largura',ms[2],ox+x/50,oy+(y+h/2)/50,ox+(x+w)/50,oy+(y+h/2)/50,room)
                cota(f,room+'-profundidade',ms[3],ox+(x+w/2)/50,oy+y/50,ox+(x+w/2)/50,oy+(y+h)/50,room)
            f.texto(210,43,'ABERTURAS - dimensões em mm',3.5)
            for i,r in enumerate(self.data['openings']):
                ms=self.refs(r); y=54+i*13
                f.texto(210,y,r['id']+' / '+r['room'],3)
                for col,(k,j) in enumerate([('L',2),('P',3),('peitoril',4),('H',5)]):
                    label=k+': '+valor(f,r['id']+'-'+k,ms[j],r['room'])
                    f.texto(210+col*47,y+5,label,2.5,MEDIDO if ms[j].origem=='medido' else NOMINAL)
        else:
            # Tabela completa em duas folhas próprias; planta mantém os códigos R01.
            for r in self.data['points']:
                ms=self.refs(r); x,y,_=[m.mm for m in ms]
                if x is None or y is None:
                    f.avisos.append(r['id']+': sem coordenadas R01');continue
                color=MEDIDO if all(m.origem=='medido' for m in ms[:2]) else NOMINAL
                f.caixa(ox+x/50-1,oy+y/50-1,2,2,color,'#ffffff')
                # Chamada deslocada só graficamente; o símbolo permanece na coordenada.
                chamada(f,ox+x/50,oy+y/50,r['id'],labels,color)
                for j,k in enumerate(('X','Y')):valor(f,r['id']+'-'+k,ms[j],r['room'])
            f.texto(210,48,'PONTOS R01 / 53 funções',4)
            notes=['Símbolos na posição nominal herdada; alturas e coordenadas nas folhas PT1/PT2.',
                   'C: cozinha; L: lavanderia; B: banheiro; S: sala; E: escritório; Q: quarto.',
                   'E06 adiada; Q06, S05 e E05 sem implantação.',
                   'Não dimensiona circuitos, tubulação ou proteção.',
                   'Conferir pontos da construtora, acessos e manutenção com RT.',
                   'Coordenadas X/Y em milímetros nos eixos desta planta.']
            yy=60
            for note in notes:
                for line in textwrap.wrap(note,80): f.texto(210,yy,line,3);yy+=5
                yy+=5
        f.texto(30,211,'Planta: X para a direita; Y para baixo. Medidas em mm; imprimir a 100%.',3)
        f.texto(30,218,'Paredes e aberturas reconstituídas; conferir alinhamentos e espessuras no imóvel.',3)
        return f

    def tabela_pontos(self, index, points):
        f=Folha('PT'+str(index),'Pontos R01 - cotas e funções / '+str(index),None)
        f.texto(15,38,'Código / tipo',3);f.texto(48,38,'X / Y / altura (mm)',3);f.texto(145,38,'Função e condição',3)
        for i,r in enumerate(points):
            y=47+i*7
            f.texto(15,y,r['id']+' / '+r['type'],2.7)
            ms=self.refs(r)
            if r['ceiling']:ms[2]=self.pe(r['room'])
            for j,m in enumerate(ms):
                s=valor(f,r['id']+'-'+('X','Y','Z')[j],m,r['room'])
                f.texto(48+j*30,y,s,2.5,MEDIDO if m.origem=='medido' else NOMINAL)
            f.texto(145,y,r['label'][:116],2.5)
        return f

    def elevacao(self, spec):
        code,title,room,axis,names,extras=spec
        f=Folha(code,title,25)
        a=0 if axis=='x' else 1
        selected=[self.modules[n] for n in names]+[self.objects[n] for n in extras]
        if not selected:raise ValueError('Elevação vazia: '+code)
        lo=min(o['box'][a] for o in selected);hi=max(o['box'][a+3] for o in selected)
        pe=self.pe(room); nominal_pe=self.geo['ceilings_at_export'][room]
        if pe.mm is None or pe.mm<=0:raise ValueError('Pé-direito inválido: '+room)
        ox,by=32,180
        def project(b):return [ox+(b[a]-lo)/25,by-b[5]/25,(b[a+3]-b[a])/25,(b[5]-b[2])/25]
        f.linha(25,by,ox+(hi-lo)/25+10,by,'#263238',.5)
        f.linha(25,by-pe.mm/25,ox+(hi-lo)/25+10,by-pe.mm/25,NOMINAL,.4)
        cota(f,'pe-direito',pe,17,by,17,by-pe.mm/25,','.join(names) or room)
        f.texto(25,by-pe.mm/25-5,'TETO ACABADO',2.7)
        f.texto(213,40,'MÓDULO / L / BASE / TOPO R53 / FOLGA TETO',2.7)
        upper={'P02','P03','P04','P09','P10','P11','P12','P15','P17','P19'}
        lanes=[]
        labels=[]
        for i,obj in enumerate(selected):
            name=obj['id'];b=obj['box']
            tag=name if name in names else 'A'+str(extras.index(name)+1)
            f.caixa(*project(b),'#405863',None,.35)
            if name in self.modules and name not in self.alterados:
                for part in self.objects.values():
                    if part['module']==name:
                        f.caixa(*project(part['box']),'#a2aaac',None,.10)
            if (b[5]-b[2])/25>6:
                f.texto(ox+(b[a]-lo)/25+1,by-b[2]/25-3,tag,2.7)
            width=cad(b[a+3]-b[a],name); base=cad(b[2],name);top=cad(b[5],name)
            gap=pe.menos(top)
            line=[tag,valor(f,name+'-L',width,name),valor(f,name+'-base',base,name),
                  valor(f,name+'-topo',top,name),valor(f,name+'-folga',gap,name)]
            yy=48+i*5
            for x,s in zip((213,247,282,321,365),line):f.texto(x,yy,s,2.5,NOMINAL)
            if name in names:
                left,right=ox+(b[a]-lo)/25,ox+(b[a+3]-lo)/25
                lane=next((j for j,spans in enumerate(lanes) if all(right<=u or left>=v for u,v in spans)),len(lanes))
                if lane==len(lanes):lanes.append([])
                lanes[lane].append((left,right))
                cota(f,name+'-largura',width,left,188+lane*7,right,188+lane*7,name)
            if gap.mm<0:
                f.avisos.append(f'{name}: R53 ultrapassa o teto em {-gap.mm:g} mm; revisar peça/implantação.')
            if self.recalculo and name in upper:
                # Cenário: fechamento real ao teto; não inventar redimensionamento da caixa.
                valor(f,name+'-fechamento-recalculado',gap,name)
                if gap.mm >= 0:
                    f.caixa(ox+(b[a]-lo)/25,by-pe.mm/25,(b[a+3]-b[a])/25,gap.mm/25,'#25658c',None,.3)
            if name in upper and not self.recalculo:
                # Preserva a folga nominal de referência; ajusta a altura útil ao PD atual.
                nominal_gap=cad(nominal_pe-b[5],name+':folga nominal')
                target_top=pe.menos(nominal_gap)
                target_height=target_top.menos(base)
                valor(f,name+'-altura-parametrica',target_height,name)
                valor(f,name+'-topo-parametrico',target_top,name)
                if target_height.mm<=0:
                    f.avisos.append(name+': altura paramétrica não positiva; proposta omitida.')
                else:
                    f.linha(ox+(b[a]-lo)/25,by-target_top.mm/25,ox+(b[a+3]-lo)/25,by-target_top.mm/25,'#25658c',.6,True)
                    f.texto(213,126+list(n for n in names if n in upper).index(name)*5,
                            name+' H estudo = '+valor(f,name+'-altura-parametrica',target_height,name)+'; base fixa / topo segue PD',2.5,'#25658c')
        f.texto(25,217,'Azul: fechamento recalculado, não modelado; caixas conforme regras.' if self.recalculo else 'Traço azul: topo paramétrico; caixas cinza: R53 fixa.',3)
        f.texto(25,223,'Ajuste dimensional não define corte, fixação ou montagem.',3)
        for i,name in enumerate(extras):
            f.texto(213,158+i*4.5,'A'+str(i+1)+': '+self.objects[name]['label'][:95],2.4)
        if not names and code=='E02':
            f.texto(213,135,'A face oposta não contém módulo de marcenaria na R53.',2.8)
            f.texto(213,142,'Mostra a interface nominal da lixeira junto ao banheiro.',2.8)
        pts=[r for r in self.data['points'] if r['room']==room]
        f.texto(213,185,'PONTOS DO AMBIENTE: altura / ver PT1-PT2',2.7)
        for i,r in enumerate(pts):
            m=self.pe(room) if r['ceiling'] else self.refs(r)[2]
            s=valor(f,r['id']+'-altura',m,','.join(names) or room)
            f.texto(213+(i%3)*62,193+(i//3)*5,r['id']+' '+s,2.5,MEDIDO if m.origem=='medido' else NOMINAL)
            pos=self.refs(r)[a]
            valor(f,r['id']+'-posicao-'+axis,pos,','.join(names) or room)
            if pos.mm is not None and m.mm is not None and lo<=pos.mm<=hi:
                px,py=ox+(pos.mm-lo)/25,by-m.mm/25
                color=MEDIDO if pos.origem==m.origem=='medido' else NOMINAL
                f.caixa(px-1,py-1,2,2,color,'#ffffff')
                chamada(f,px,py,r['id'],labels,color)
        return f

    def detalhe(self):
        f=Folha('DT1','Detalhe-tipo - fechamento ao teto / P03',25)
        b=self.modules['P03']['box'];pe=self.pe('quarto');top=cad(b[5],'P03');gap=pe.menos(top)
        x,y=55,180;w=(b[4]-b[1])/25
        f.caixa(x,y-b[5]/25,w,(b[5]-b[2])/25,'#405863','#eef2f2')
        f.linha(35,y-pe.mm/25,150,y-pe.mm/25,'#263238',.5)
        cota(f,'PD',pe,30,y,30,y-pe.mm/25,'P03')
        cota(f,'fechamento',gap,x+w+10,y-b[5]/25,x+w+10,y-pe.mm/25,'P03')
        if gap.mm>=0:
            f.caixa(x,y-pe.mm/25,w,gap.mm/25,'#25658c',None,.4)
        else:f.avisos.append('Fechamento negativo: não desenhado; caixa R53 não cabe sob o teto.')
        f.texto(180,65,'Altura do fechamento = PD efetivo - topo da caixa R53',3.5)
        f.texto(180,75,'Resultado: '+valor(f,'fechamento',gap,'P03'),3.5,NOMINAL)
        notes=['Envelope de estudo; espessura, juntas e acesso de montagem com oficina/RT.',
               'Não representa nova peça incorporada ao FCStd.',
               'Não reduzir automaticamente peças existentes para ocultar conflito.',
               ('Cenário: caixa fixa; fechamento recalculado, não modelado.' if self.recalculo else 'P03 e aéreos: altura de estudo = PD - folga nominal - base R53.'),
               'Conferir teto em vários pontos; usar altura livre limitante no CSV.']
        yy=92
        for note in notes:
            for line in textwrap.wrap(note,78):f.texto(180,yy,line,3);yy+=6
            yy+=5
        return f

    def nichos(self):
        f=Folha('NC1','Módulos - alturas livres entre planos horizontais R53',None)
        f.texto(15,40,'Módulo',3);f.texto(45,40,'Vãos verticais entre envelopes / de baixo para cima / mm',3)
        for i,(name,obj) in enumerate(self.modules.items()):
            b=obj['box']; parts=[]
            if name in self.alterados:
                f.texto(15,49+i*8,name+' — envelope alterado; vãos internos dependem de remodelagem.',2.7)
                continue
            for o in self.objects.values():
                if o['module']!=name:continue
                bb=o['box'];dx,dy,dz=(bb[j+3]-bb[j] for j in range(3))
                if dz<min(dx,dy) and dx>=(b[3]-b[0])*.5 and dy>=(b[4]-b[1])*.5:
                    parts.append((bb[2],bb[5]))
            merged=[]
            for z,zz in sorted(parts):
                if merged and z<=merged[-1][1]:merged[-1][1]=max(zz,merged[-1][1])
                else:merged.append([z,zz])
            gaps=[a[0]-before[1] for before,a in zip(merged,merged[1:])]
            texts=[valor(f,name+'-vao-'+str(j),cad(v,name),name) for j,v in enumerate(gaps)]
            f.texto(15,49+i*8,name,3)
            f.texto(45,49+i*8,' / '.join(texts) if texts else 'Sem par de planos horizontais identificável no envelope.',2.7,NOMINAL)
        f.texto(15,218,'Triagem geométrica: planos que cobrem ao menos metade da largura e profundidade do módulo.',2.8)
        f.texto(15,224,'Não confirma vão útil de porta, gaveta, recorte ou ferragem; conferir peça específica antes de executar.',2.8)
        return f


ELEVACOES=[
 ('E01','Cozinha - face da bancada e aéreos','cozinha','x',[f'P{i:02}' for i in range(5,14)],['Peca138','Peca351','Peca134','Peca139','Peca308','FischerFrenteR31']),
 ('E02','Cozinha - face oposta / interface da lixeira','cozinha','x',[],['Peca144','Peca145']),
 ('E03','Lavanderia - tanque, cesto e aéreo','lavanderia','x',['P14','P15'],['Peca152','Peca357','Peca155']),
 ('E04','Banheiro - gabinete, bancada e espelho','banho','x',['P18','P19'],['Peca399','Peca185']),
 ('E05','Roupeiro - P01-P03 e maleiro / face principal','quarto','x',['P01','P02','P03'],[]),
 ('E06','Roupeiro - retorno do canto P02','quarto','y',['P02'],[]),
 ('E07','Quarto - cabeceira e aéreo P04','quarto','y',['P04'],['CabeceiraDoisPaineisR25']),
 ('E08','Escritório - bancada e gaveteiro','escritorio','x',['P16'],['Peca110']),
 ('E09','Escritório - aéreo P17','escritorio','y',['P17'],[]),
 ('E10','Escritório - TV e prateleira','escritorio','y',[],['Peca130','Peca131']),
 ('E11','Sala - painel TV e prateleiras','sala','y',[],['Peca084','Peca085','Peca086','Peca088']),
 ('E12','Sala - banco P20','sala','y',['P20'],[]),
]


def finalizar(f, total, sha):
    f.caixa(8,8,404,281,'#263238',None,.4)
    f.texto(15,20,f.codigo+' | '+f.titulo,4.5)
    f.texto(15,28,'GUEDALA PARK  /  CADERNO R02  /  GEOMETRIA E COTAS',2.6)
    for i,msg in enumerate(f.avisos[:4]):f.texto(15,231+i*4,msg[:175],2.5,'#a32c28')
    if len(f.avisos)>4:f.texto(15,248,f'+{len(f.avisos)-4} avisos: ver Impacto.json',2.6,'#a32c28')
    f.linha(8,256,412,256)
    f.texto(15,263,'N / tracejado: planta ou nominal (inclui CAD e derivadas com parcela nominal)',2.6,NOMINAL)
    f.texto(15,269,'M / contínuo: medido; derivada M somente quando todas as parcelas são medidas',2.6,MEDIDO)
    f.texto(15,279,'ESTUDO — NÃO EXECUTAR',4,'#9d2925')
    nominal=sum(v['mm'] is not None and v['origem']!='medido' for v in f.cotas.values())
    f.texto(215,263,f'R02 | {f.codigo} | {total} folhas | '+('Sem escala' if not f.escala else f'A3 / 1:{f.escala}'),3)
    f.texto(215,270,f'{nominal} cotas nominais | RT: __________________________',3)
    f.texto(215,277,'R53 SHA256: '+sha[:24]+'...',2.4)
    if f.escala:
        f.linha(335,282,385,282,'#263238',.5)
        f.texto(335,287,f'50 mm no papel = {50*f.escala:g} mm reais',2.4)


def gerar(cenario=None):
    p=Projeto(cenario)
    pages=[p.plano('PL1','Planta cotada - paredes e aberturas','paredes'),
           p.plano('PL2','Planta de layout - envelopes R53','layout'),
           p.plano('PL3','Planta de pontos R01','pontos')]
    pages += [p.tabela_pontos(1,p.data['points'][:27]),p.tabela_pontos(2,p.data['points'][27:])]
    pages += [p.elevacao(s) for s in ELEVACOES]
    pages.append(p.nichos())
    pages.append(p.detalhe())
    cover=Folha('00','Índice e critérios de leitura',None)
    cover.texto(20,43,'CADERNO A3  |  R02',7)
    for i,f in enumerate(pages):cover.texto(20,55+i*7,f.codigo+'   '+f.titulo,3.2)
    for i,line in enumerate(['Plantas 1:50; elevações e detalhe 1:25.',
                             'Imprimir sem ajustar à página; conferir barra de 50 mm.',
                             'Caixas R53 são envelopes, não contornos de usinagem.',
                             'Fontes: CSV de medidas + Cotas.json + exportação R53.',
                             'Campo medido vence nominal. Branco = pendência.',
                             'Ajustes ao teto são estudos separados da R53.',
                             'R00 preservado; esta revisão não foi publicada.',
                             'Ver Impacto.json: alterações, fontes e conflitos.']):cover.texto(240,60+i*10,line,3)
    pages.insert(0,cover)
    if p.recalculo:
        for f in pages:
            f.texto(15,34,'CENÁRIO — recalculado, não modelado; conferir Impacto_moveis.json',2.5,'#9d2925')
            if f.codigo in ('PL1','PL2'):
                for code in ('DIM-01','DIM-06','DIM-07'):
                    if p.rows[code]['valor_medido'].strip():
                        f.avisos.append(code+': conferir PR-WALLS e vãos; largura medida não resolve alinhamentos compartilhados.')
            for r in p.recalculo['resultados']:
                if f.codigo in r['pranchas'] and r['status'] != 'OK':
                    f.avisos.append(r['movel']+'/'+r['cota']+': '+r['status'])
    current={f.codigo+':'+k:v for f in pages for k,v in f.cotas.items()}
    previous_path=OUT/'Ultima_geracao.json'
    if cenario and not previous_path.exists():
        previous_path=ROOT/'06_Entregas/Caderno_pranchas/Ultima_geracao.json'
    previous=json.loads(previous_path.read_text(encoding='utf-8'))['cotas'] if previous_path.exists() else {}
    changes=[]
    for key in sorted(set(current)|set(previous)):
        old,new=previous.get(key),current.get(key)
        if old!=new:changes.append(dict(cota=key,antes=old,depois=new))
    report=dict(revisao='R02',cad_sha256=p.geo['cad_sha256'],primeira_geracao=not previous,
                alteracoes=changes,avisos=[dict(prancha=f.codigo,mensagem=s) for f in pages for s in f.avisos])
    for f in pages:finalizar(f,len(pages),p.geo['cad_sha256'])
    # PDF primeiro; nenhuma referência anterior avança se a renderização falhar.
    dest=BytesIO();pdf(pages,dest)
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'Guedala_Park_Pranchas_R02.pdf').write_bytes(dest.getvalue())
    for f in pages:(OUT/(f.codigo+'.svg')).write_text(f.svg(),encoding='utf-8')
    body=''.join(f'<section><img src="{f.codigo}.svg" alt="{escape(f.titulo)}"></section>' for f in pages)
    html='<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Guedala Park R02</title><style>@page{size:A3 landscape;margin:0}body{margin:0;background:#dce1e2;font-family:Arial}nav{padding:16px}section{width:420mm;height:297mm;margin:8mm auto;background:white;break-after:page}section:last-child{break-after:auto}img{width:420mm;height:297mm;display:block}@media print{section{margin:0}body{background:white}nav{display:none}}</style><nav><a href="Guedala_Park_Pranchas_R02.pdf">PDF R02</a> · <a href="Impacto.html">Alterações e avisos</a></nav>'+body+'</html>'
    (OUT/'index.html').write_text(html,encoding='utf-8')
    (OUT/'Impacto.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rows=[]
    def desc(v):
        return 'ausente' if v is None else ('pendente' if v['mm'] is None else f'{v["mm"]:g} mm')+' / '+v['origem']
    for change in changes:
        v=change['depois'] or change['antes']
        rows.append('<tr>'+''.join('<td>'+escape(s)+'</td>' for s in
                    (change['cota'],v['movel'],desc(change['antes'])+' → '+desc(change['depois'])))+'</tr>')
    warnings=''.join('<li>'+escape(a['prancha']+': '+a['mensagem'])+'</li>' for a in report['avisos'])
    (OUT/'Impacto.html').write_text('<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Impacto R02</title><style>body{font:15px Arial;max-width:1100px;margin:30px auto}td,th{padding:8px;border-bottom:1px solid #ccc;text-align:left}li{margin:6px}</style><h1>Impacto da última geração R02</h1><p>'+str(len(changes))+' cotas alteradas. Comparação com a geração imediatamente anterior; primeira execução registra inclusão.</p><h2>Avisos</h2><ul>'+warnings+'</ul><h2>Antes → depois</h2><table><tr><th>Prancha:cota</th><th>Móvel</th><th>Alteração</th></tr>'+''.join(rows)+'</table></html>',encoding='utf-8')
    (OUT/'Ultima_geracao.json').write_text(json.dumps(dict(revisao='R02',cotas=current),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if p.recalculo:
        (OUT/'Impacto_moveis.json').write_text(json.dumps(p.recalculo,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'R02: {len(pages)} folhas; {len(current)} cotas; {len(changes)} alterações; {len(report["avisos"])} avisos.')


if __name__=='__main__':
    try:
        import reportlab
    except ImportError:
        runtime=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
        if not runtime.exists():
            raise SystemExit('Instale reportlab no Python: python -m pip install reportlab')
        raise SystemExit(subprocess.call([str(runtime),'-B',str(Path(__file__).resolve()),*sys.argv[1:]],env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')))
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cenario',type=Path)
    parser.add_argument('--saida',type=Path)
    args=parser.parse_args()
    if args.cenario and not args.saida:
        parser.error('--cenario exige --saida fora do repositório')
    if args.saida:
        output=args.saida.resolve()
        if output==ROOT or ROOT in output.parents:
            parser.error('--saida deve ficar fora do repositório')
        OUT=output
    gerar(args.cenario)
