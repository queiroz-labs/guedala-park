"""Inspecao somente leitura dos solidos G2. Rodar com FreeCADCmd; nunca salva CAD."""
from pathlib import Path
import hashlib,json
import FreeCAD as App
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'04_Moveis/Inventario_dimensional/Gavetas/Conferencia_solidos_G2.json'
def bounds(sh,optimal=True):
    b=sh.optimalBoundingBox() if optimal else sh.BoundBox
    return [b.XMin,b.YMin,b.ZMin,b.XMax,b.YMax,b.ZMax]
def world(o):
    s=o.Shape.copy()
    s.Placement=o.getGlobalPlacement().multiply(o.Placement.inverse()).multiply(s.Placement)
    return s
def main():
    release=json.loads((ROOT/'ferramentas/site/current_release.json').read_text(encoding='utf-8'))
    cad=ROOT/release['cadPath']; before=hashlib.sha256(cad.read_bytes()).hexdigest()
    proposal=json.loads((OUT.parent/'Proposta_FGVTN_500.json').read_text(encoding='utf-8'))
    assert before==proposal['cad_sha256']
    doc=App.openDocument(str(cad))
    try:
        names=['MontagemG2R019','BandejaG2R06','BandejaG2R001','MontagemG2R016','MontagemG2R017','MontagemG2R018','MontagemG2R020','MontagemG2R021','GavetaComumR062']
        shapes={n:world(doc.getObject(n)) for n in names}
        data={n:dict(standard_box_mm=bounds(s,False),optimal_box_mm=bounds(s),volume_mm3=s.Volume,
            valid=s.isValid(),solids=len(s.Solids),faces=len(s.Faces),
            vertex_z_range_mm=[min(v.Point.z for v in s.Vertexes),max(v.Point.z for v in s.Vertexes)]) for n,s in shapes.items()}
        contacts=[]
        for a,b in [('MontagemG2R019','BandejaG2R06'),('MontagemG2R019','BandejaG2R001'),('BandejaG2R06','BandejaG2R001')]:
            hit=shapes[a].common(shapes[b]); distance=shapes[a].distToShape(shapes[b])[0]
            contacts.append(dict(a=a,b=b,distance_mm=distance,common_volume_mm3=hit.Volume,
                positive_solid_volume_mm3=sum(s.Volume for s in hit.Solids if s.Volume>1e-7),
                common_area_mm2=hit.Area,common_faces=len(hit.Faces),common_solids=len(hit.Solids),
                common_valid=hit.isValid()))
        assemblies={}
        for n in ['BandejaG2R06','BandejaG2R001']:
            o=doc.getObject(n)
            assemblies[n]=dict(status=o.Status,children=[dict(object=c.Name,label=c.Label,optimal_box_mm=bounds(world(c))) for c in o.Group if hasattr(c,'Shape') and not c.Shape.isNull()])
        result=dict(cad_sha256=before,cad_opened_read_only=True,cad_saved=False,cad_changed=False,
            scope='Current saved geometry only, no proposed solids or hardware; BRep contact is not strength or physical support certification.',
            shapes=data,contacts=contacts,tray_assemblies=assemblies)
        assert hashlib.sha256(cad.read_bytes()).hexdigest()==before
        OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(result,ensure_ascii=True))
    finally: App.closeDocument(doc.Name)
main()
