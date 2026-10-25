"""Executar na GUI FreeCAD via execute_python. Somente cria R52; R51 intacta."""
from pathlib import Path
import hashlib, json, shutil, runpy, traceback
import FreeCAD as App
import FreeCADGui as Gui

ROOT=Path('C:/Users/Elias/Documents/PROJETOS/Guedala park')
HERE=ROOT/'guedala-park/01_Projeto/Correcao_integral_R52_2026-10-25'
SOURCE=ROOT/'guedala-park/01_Projeto/Revisao_sem_tubos_R51_2026-10-25/Guedala_Park_R51_Sem_estudo_tubular.FCStd'
TARGET=HERE/'Guedala_Park_R52_Corrigido.FCStd'
EXPECTED='ab5323bb12f8eca40b25bdfe4eadc8a3221c82b0646f354cd1f2832acfb27c16'

def write(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def visual(o):
    v=o.ViewObject
    return {k:str(getattr(v,k)) for k in ['ShapeColor','LineColor','PointColor','Transparency','DisplayMode','DiffuseColor'] if k in v.PropertiesList}

def snapshot(d):
    out={}
    for o in d.Objects:
        r={'type':o.TypeId,'label':o.Label,'visible':o.Visibility,
           'expressions':[(str(k),str(v)) for k,v in o.ExpressionEngine], 'visual':visual(o)}
        if 'Placement' in o.PropertiesList:
            r['local']=list(o.Placement.toMatrix().A)
            r['global']=list((o.getGlobalPlacement() if hasattr(o,'getGlobalPlacement') else o.Placement).toMatrix().A)
        if o.isDerivedFrom('Part::Feature') and not o.Shape.isNull():
            s=o.Shape;b=s.BoundBox
            r['geometry']={'volume':s.Volume,'area':s.Area,'bbox':[b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax],
                           'topology':[len(s.Solids),len(s.Faces),len(s.Edges),len(s.Vertexes)],'valid':s.isValid()}
        out[o.Name]=r
    return out

def numeric_equal(a,b,tol=1e-6):
    return len(a)==len(b) and all(abs(x-y)<=tol for x,y in zip(a,b))

def differences(a,b):
    out=[]
    for n in a:
        x,y=a[n],b[n]
        changed=[]
        for k in ['type','label','visible','expressions','visual']:
            if x.get(k)!=y.get(k):changed.append(k)
        for k in ['local','global']:
            if k in x and not numeric_equal(x[k],y[k]):changed.append(k)
        if 'geometry' in x:
            p,q=x['geometry'],y['geometry']
            if p['topology']!=q['topology'] or not numeric_equal([p['volume'],p['area']]+p['bbox'],[q['volume'],q['area']]+q['bbox']):changed.append('geometry')
            if p['valid']!=q['valid']:changed.append('valid')
        if changed:out.append({'name':n,'changed':changed})
    return out

def prop(o,name,value):
    if name not in o.PropertiesList:o.addProperty('App::PropertyString',name,'Revisao R52')
    setattr(o,name,value)

def run():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    if TARGET.exists():
        assert hashlib.sha256(TARGET.read_bytes()).hexdigest()==EXPECTED,'R52 alterada ja existe; nao sobrescrever.'
    data=json.loads((ROOT/'guedala-park/01_Projeto/Estudo_interativo/fabrication/technical-r14.json').read_text(encoding='utf-8'))['modules']['P20']
    assert 'southco' not in json.dumps(data,ensure_ascii=False).lower(),'Concluir primeiro a normalizacao das fichas P20.'
    if not TARGET.exists():shutil.copy2(SOURCE,TARGET)
    d=next((doc for doc in App.listDocuments().values() if doc.FileName and Path(doc.FileName).resolve()==TARGET.resolve()),None)
    if d is None:d=App.openDocument(str(TARGET))
    assert not any('Touched' in o.State for o in d.Objects),'Candidata aberta possui edicoes; conferir antes de retomar.'
    before=snapshot(d)
    write('Snapshot_antes.json',before)
    d.openTransaction('R52 - corrigir posicoes, exibicao e metadados')
    changes=[]
    tv=d.getObject('Peca131')
    assert abs(tv.LocalY.Value-1280)<1e-6
    tv.LocalY=1180
    prop(tv,'CorrecaoR52','LocalY1280->1180mm: TV Y1180..2150, folga nominal50mm ate folha aberta Y2200. Gabarito preservado; conferir TV/suporte/giro e medidas reais.')
    changes.append({'object':tv.Name,'property':'LocalY','before':1280,'after':1180,'unit':'mm'})
    # Restore intended historical visibility, not removal or cutting of parts.
    hidden=['Peca358','Alternativa500ManterBaseR41','Alternativa500ManterTopoR41','EstudoFrente500R41']
    hidden+=['Peca%03d'%i for i in range(91,99)]
    hidden+=['CadeiraLinaR30_%d'%i for i in range(1,4)]
    hidden+=['AcessoControleR21']+['AcessoControleR%03d'%i for i in range(1,10)]+['AcessoControleR34']
    for n in hidden:
        o=d.getObject(n);assert o is not None,n
        o.Visibility=False
        changes.append({'object':n,'property':'Visibility','before':before[n]['visible'],'after':False})
    # Keep all historical dependencies, but remove obsolete commands from current controls.
    history=d.addObject('App::DocumentObjectGroup','HistoricoControlesR52')
    history.Label='Historico - giro antigo do gabinete do banheiro (substituido na R43)'
    d.getObject('Documentacao').addObject(history)
    controls=d.getObject('ControlesAmbienteR004')
    for n in ['ControlePortaR12','ControlePortaR018']:
        o=d.getObject(n);controls.removeObject(o);history.addObject(o)
        o.Label='HISTORICO - '+before[n]['label']+' (giro substituido por correr R43)'
        prop(o,'StatusR52','Referencia historica de folhas ocultas. Gabinete atual: BC43_Controle.CursoEsquerda/CursoDireita; expressoes antigas preservadas.')
    alias=d.addObject('App::Link','AcessoCorrerBanheiroR52')
    alias.setLink(d.getObject('BC43_Controle'))
    alias.Label='Gabinete banheiro - CORRER - CursoEsquerda / CursoDireita (mm)'
    controls.addObject(alias)
    d.getObject('BC43_Controle').Label='Gabinete banheiro - portas de correr (cursos em mm)'
    drawer=d.getObject('Gaveta009');assert abs(drawer.AlturaParedeSobreFundo.Value-53)<1e-6
    drawer.AlturaParedeSobreFundo=47
    changes.append({'object':drawer.Name,'property':'AlturaParedeSobreFundo','before':53,'after':47,'unit':'mm'})
    proposed=json.loads((ROOT/'guedala-park/01_Projeto/P01_massas_equilibrio_2026-10-25/Correcoes_metadados_propostas.json').read_text(encoding='utf-8'))
    for r in proposed['changes']:
        o=d.getObject(r['object']);assert getattr(o,r['property'])==r['old_value']
        setattr(o,r['property'],r['proposed_value']);changes.append(r)
    for n in ['Gaveta008','Gaveta009']:
        o=d.getObject(n);old=o.Ferragem
        o.Ferragem='Selecao documental R14: Blum MOVENTO 760H4000S BLUMOTION S,400mm e engates T51.7601. Geometria R49 preservada; interface guia/fundo, carga, tolerancias e fixacoes continuam pendentes.'
        changes.append({'object':n,'property':'Ferragem','before':old,'after':o.Ferragem})
    bank=d.getObject('Modulo019');old=list(bank.FerragensR14)
    def qty(r):
        return ('quantidade a definir' if r.get('quantity') is None else str(r['quantity'])+' '+r.get('unit','')).strip()
    bank.FerragensR14=[qty(r)+' - '+r['item']+' - '+str(r.get('reference') or '')+' ['+str(r.get('status',''))+'] '+str(r.get('assembly','')) for r in data['hardwareRows']]
    bank.ResumoR14=data['summary']
    prop(bank,'CorrecaoR52','Ferragens da ficha conciliadas: piano e articuladores com trava; limitacao independente continua a definir. Itens derivados do eixo Southco historico retirados da lista ativa, sem inventar batente ou fixacao.')
    changes.append({'object':bank.Name,'property':'FerragensR14','before':old,'after':list(bank.FerragensR14)})
    # The spreadsheet is a documented summary, not a geometric driver.
    sheet=d.getObject('FichasR14')
    if sheet:sheet.set('D21',"'"+data['summary'])
    info=d.addObject('App::DocumentObjectGroup','ConsolidacaoR52')
    info.Label='R52 - LEIA PRIMEIRO - correcao de inconsistencias'
    prop(info,'Escopo','R51 preservada. TV deslocada100mm para janela; historicos lavanderia/mesa ocultos; controle atual banheiro e metadados conciliados. Dimensoes, armazenamento, materiais e mecanismos ativos preservados.')
    prop(info,'Limites','Sem tubos. FundoP01/formato, micro/F104, interfaceP16, cargas/apoios e ferragens reais continuam condicionados. R52 nao e liberacao integral de fabricacao.')
    prop(info,'Relatorio','README.md e Verificacao_R52.json nesta pasta. Site/fichas locais corrigidos; nenhuma publicacao remota nesta revisao.')
    d.Label='Guedala Park - R52 - posicoes e consistencia corrigidas'
    d.commitTransaction();d.recompute()
    after=snapshot(d);diff=differences(before,after)
    geometry=[r['name'] for r in diff if any(k in r['changed'] for k in ['local','global','geometry','valid'])]
    assert geometry==['Peca131'],geometry
    assert all(before[n]['expressions']==after[n]['expressions'] for n in before),'Expressoes alteradas'
    assert all(before[n]['visual']==after[n]['visual'] for n in before),'Aparencia alterada'
    assert not [n for n,r in after.items() if r.get('geometry',{}).get('valid') is False]
    save=runpy.run_path(str(ROOT/'guedala-park/01_Projeto/Otimizacao_FreeCAD_R50_2026-10-24/serializacao_binaria.py'))['salvar_documento'](d,TARGET)
    write('Alteracoes_R52.json',changes);write('Diferencas_R51_R52.json',diff);write('Snapshot_apos.json',after)
    expected_names=set(after);name=d.Name
    App.closeDocument(name)
    d=App.openDocument(str(TARGET));reopened=snapshot(d)
    assert set(reopened)==expected_names
    rd=differences(after,reopened);assert not rd,rd
    assert all(d.getObject(n).Visibility is False for n in hidden)
    assert d.getObject('AcessoCorrerBanheiroR52').LinkedObject==d.getObject('BC43_Controle')
    assert not any(o.Name in ['ControlePortaR12','ControlePortaR018'] for o in d.getObject('ControlesAmbienteR004').Group)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    report={'source':str(SOURCE),'source_sha256':EXPECTED,'source_unchanged':True,'target':save,
        'objects_before':len(before),'objects_after':len(after),'added':sorted(set(after)-set(before)),
        'expressions_before':sum(len(r['expressions']) for r in before.values()),'expressions_after':sum(len(r['expressions']) for r in after.values()),
        'changed_geometry_or_placement':geometry,'original_visual_properties_preserved':True,
        'native_features':sum('geometry' in r for r in reopened.values()),'invalid_native':[],
        'reopened':True,'reopen_differences':rd,'active_document':d.Name,'hidden_roots':hidden}
    write('Verificacao_R52.json',report)
    Gui.activeDocument().activeView().viewAxonometric();Gui.activeDocument().activeView().fitAll()
    Gui.updateGui()

try:run()
except BaseException:
    write('Erro_criacao_R52.json',traceback.format_exc())
    raise
