# Macro R30: substitui as três caixas da cadeira Lina por gabaritos desenhados.
import sys, json, traceback
DIR = r"C:/Users/Elias/AppData/Local/Temp/claude/C--Users-Elias-Documents-PROJETOS-Guedala-park/555f571b-8c80-4302-9f3e-cb9762a71dc4/scratchpad"
sys.path.insert(0, DIR)
import FreeCAD as App, FreeCADGui as Gui, Part
import importlib, lina; importlib.reload(lina)
ARQ = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd"
LOG = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Cadeiras_Lina_R30.json"
COR = {"madeira": (0xc4 / 255, 0xa2 / 255, 0x7b / 255), "estofado": (0xd8 / 255, 0xd0 / 255, 0xc2 / 255)}
pares = [("Peca099", "EspelhoPecaR074"), ("Peca100", "EspelhoPecaR075"), ("Peca101", "EspelhoPecaR076")]
log = {"ok": False}
try:
    d = App.openDocument(ARQ); App.setActiveDocument(d.Name)
    sala = d.getObject("Ambiente_sala")
    pcs = lina.pecas()
    d.openTransaction("R30 cadeiras Lina desenhadas")
    novos = []
    for i, (caixa, link) in enumerate(pares, 1):
        cx = d.getObject(caixa); lk = d.getObject(link)
        p = d.addObject("App::Part", f"CadeiraLinaR30_{i}")
        p.Label = f"Cadeira Lina Estofada (Versatile) — gabarito R30 {i}"
        p.Placement = cx.Placement
        for prop, val in [("Fonte", "versatilemoveis.com.br/produto.php?id=783 · fotos do fabricante"),
                          ("Status", "Gabarito simplificado: envelope 44x47x94 de catálogo; assento 47, pés 38->28, saia 6, inclinação do encosto 3,2 graus estimados pelas fotos. Não é desenho do fabricante.")]:
            p.addProperty("App::PropertyString", prop, "Referencia"); setattr(p, prop, val)
        sala.addObject(p)
        for nome, mat, shp in pcs:
            f = d.addObject("Part::Feature", f"Lina{i}_{nome}")
            f.Label = f"Lina {i} · {nome} ({mat})"
            f.Shape = shp
            p.addObject(f)
            f.ViewObject.ShapeColor = COR[mat]
        cx.Visibility = False
        cx.Label = "Histórico oculto — envelope R09 da " + cx.Label
        lk.LinkedObject = p
        lk.Label = f"Cadeira Lina Estofada — gabarito R30 {i} (espelhada)"
        novos.append(p.Name)
    d.commitTransaction(); d.recompute()
    conf = {}
    for i, (caixa, link) in enumerate(pares, 1):
        p = d.getObject(f"CadeiraLinaR30_{i}"); lk = d.getObject(link)
        sb = Part.getShape(p).BoundBox; lb = Part.getShape(lk).BoundBox
        esperado = [round(7400 - sb.XMax, 1), round(sb.YMin, 1), round(sb.ZMin, 1), round(7400 - sb.XMin, 1), round(sb.YMax, 1), round(sb.ZMax, 1)]
        obtido = [round(x, 1) for x in (lb.XMin, lb.YMin, lb.ZMin, lb.XMax, lb.YMax, lb.ZMax)]
        conf[link] = {"origem": [round(x, 1) for x in (sb.XMin, sb.YMin, sb.ZMin, sb.XMax, sb.YMax, sb.ZMax)], "espelho": obtido, "confere": esperado == obtido}
    log.update({"novos": novos, "conferencia_espelho": conf,
                "invalidos": [o.Name for o in d.Objects if "Invalid" in o.State or "Error" in o.State], "objetos": len(d.Objects)})
    if all(c["confere"] for c in conf.values()) and not log["invalidos"]:
        d.save(); log["salvo"] = True
    log["ok"] = True
except Exception:
    log["erro"] = traceback.format_exc()
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
