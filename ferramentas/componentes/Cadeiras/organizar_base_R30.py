# Macro R30: recolhe a base de edição (fonte dos vínculos espelhados) numa pasta oculta.
# Não apaga nem move geometria: só reorganiza a árvore e a visibilidade.
import FreeCAD as App, FreeCADGui as Gui, Part, json, traceback
ARQ = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Cadeiras/Guedala_Park_R30_Juntas_Rotulos.FCStd"
LOG = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/02_Modelo_3D/Componentes/Cadeiras/Organizacao_base_R30.json"
log = {"ok": False}
try:
    d = App.openDocument(ARQ)
    App.setActiveDocument(d.Name)
    def bb_links():
        res = {}
        for o in d.getObject("ApartamentoEspelhadoR20").OutListRecursive:
            if o.TypeId == "App::Link":
                sh = Part.getShape(o)
                if sh.isNull():
                    continue
                b = sh.BoundBox
                res[o.Name] = [round(b.XMin, 3), round(b.YMin, 3), round(b.ZMin, 3), round(b.XMax, 3), round(b.YMax, 3), round(b.ZMax, 3)]
        return res
    antes = bb_links()
    base = ["Ambiente_quarto", "Ambiente_escritorio", "Ambiente_sala", "Ambiente_cozinha", "Ambiente_lavanderia",
            "Ambiente_banho", "Ambiente_circulacao", "ParedesInteiras", "ParedesCortadas",
            "ControlesPortasR10", "ControlesPortasR11", "ControlesPortasR12", "ControlesCorrerR14", "ControlesBancoR16", "ControlesPortasR18"]
    d.openTransaction("R30 base de edição oculta")
    g = d.getObject("BaseEdicaoR30") or d.addObject("App::DocumentObjectGroup", "BaseEdicaoR30")
    g.Label = "99 — BASE DE EDIÇÃO (oculta; alimenta o apartamento atual — não apagar)"
    movidos = []
    for n in base:
        o = d.getObject(n)
        if o is not None and o not in g.Group:
            g.addObject(o); movidos.append(n)
    g.Visibility = False
    for n in base:
        d.getObject(n).Visibility = False
    d.getObject("ApartamentoEspelhadoR20").Visibility = True
    d.getObject("ControlesAtuaisR21").Visibility = True
    d.commitTransaction()
    d.recompute()
    g.ViewObject.ShowInTree = False
    depois = bb_links()
    dif = [n for n in antes if antes[n] != depois.get(n)]
    log.update({"movidos": movidos, "vinculos": len(antes), "vinculos_alterados": dif,
                "invalidos": [o.Name for o in d.Objects if "Invalid" in o.State or "Error" in o.State],
                "objetos": len(d.Objects), "topo": [o.Label for o in d.Objects if not o.InList and o.TypeId == "App::DocumentObjectGroup"]})
    if not dif and not log["invalidos"]:
        d.save(); log["salvo"] = True
        Gui.SendMsgToActiveView("ViewFit")
    log["ok"] = True
except Exception:
    log["erro"] = traceback.format_exc()
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
