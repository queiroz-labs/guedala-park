# Macro R30: substitui a caixa da cadeira do escritório por gabarito desenhado (Ultra Comfort).
import sys, json, traceback
DIR = r"C:/Users/Elias/AppData/Local/Temp/claude/C--Users-Elias-Documents-PROJETOS-Guedala-park/555f571b-8c80-4302-9f3e-cb9762a71dc4/scratchpad"
sys.path.insert(0, DIR)
import FreeCAD as App, FreeCADGui as Gui, Part
import importlib, ultra as lina; importlib.reload(lina)
ARQ = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd"
LOG = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Cadeira_escritorio_R30.json"
COR = {"estrutura": (0x26 / 255, 0x26 / 255, 0x26 / 255), "tela": (0x3a / 255, 0x3a / 255, 0x3a / 255)}
pares = [("Peca129", "EspelhoPecaR043")]
log = {"ok": False}
try:
    d = App.openDocument(ARQ); App.setActiveDocument(d.Name)
    sala = d.getObject("Ambiente_escritorio")
    pcs = lina.pecas()
    d.openTransaction("R30 cadeira do escritório desenhada")
    novos = []
    for i, (caixa, link) in enumerate(pares, 1):
        cx = d.getObject(caixa); lk = d.getObject(link)
        p = d.addObject("App::Part", f"CadeiraEscritorioR30_{i}")
        p.Label = "Cadeira de escritório ErgoChair Ultra Comfort (GenioDesk, cenário) — gabarito R30"
        p.Placement = cx.Placement
        for prop, val in [("Fonte", "geniodesk.com.br/products/cadeira-ergonomica-ergochair-ultra-comfort · desenho técnico do fabricante"),
                          ("Status", "Gabarito simplificado no envelope 745x730 do desenho técnico; posição assento 470 / topo 1200 dentro das faixas 455-530 / 1145-1330. Encosto 14 graus, braços a 690 e base r320 estimados. Modelo ainda é cenário, sem escolha definitiva.")]:
            p.addProperty("App::PropertyString", prop, "Referencia"); setattr(p, prop, val)
        sala.addObject(p)
        for nome, mat, shp in pcs:
            f = d.addObject("Part::Feature", f"Escritorio{i}_{nome}")
            f.Label = f"Cadeira escritório · {nome} ({mat})"
            f.Shape = shp
            p.addObject(f)
            f.ViewObject.ShapeColor = COR[mat]
        cx.Visibility = False
        cx.Label = "Histórico oculto — envelope R09 da " + cx.Label
        lk.LinkedObject = p
        lk.Label = "Cadeira de escritório Ultra Comfort — gabarito R30 (espelhada)"
        novos.append(p.Name)
    d.commitTransaction(); d.recompute()
    conf = {}
    for i, (caixa, link) in enumerate(pares, 1):
        p = d.getObject(f"CadeiraEscritorioR30_{i}"); lk = d.getObject(link)
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
