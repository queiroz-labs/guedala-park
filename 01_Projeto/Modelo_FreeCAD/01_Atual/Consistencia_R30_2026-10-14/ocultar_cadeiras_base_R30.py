# Macro R30: oculta as cadeiras novas na base de edição; os vínculos espelhados continuam exibindo-as.
import FreeCAD as App, FreeCADGui as Gui, Part, json, traceback
ARQ = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Guedala_Park_R30_Juntas_Rotulos.FCStd"
LOG = r"C:/Users/Elias/Documents/PROJETOS/Guedala park/guedala-park/01_Projeto/Modelo_FreeCAD/01_Atual/Consistencia_R30_2026-10-14/Ocultar_cadeiras_base_R30.json"
log = {"ok": False}
try:
    d = App.openDocument(ARQ); App.setActiveDocument(d.Name)
    nomes = ["CadeiraLinaR30_1", "CadeiraLinaR30_2", "CadeiraLinaR30_3", "CadeiraEscritorioR30_1"]
    links = {"CadeiraLinaR30_1": "EspelhoPecaR074", "CadeiraLinaR30_2": "EspelhoPecaR075", "CadeiraLinaR30_3": "EspelhoPecaR076", "CadeiraEscritorioR30_1": "EspelhoPecaR043"}
    # qualquer outro objeto da base que esteja visível por engano (fora de módulos, que já usam o mesmo padrão)
    base = d.getObject("BaseEdicaoR30")
    visiveis_base = [o.Name for g in base.Group for o in [g] + list(getattr(g, "Group", [])) if getattr(o, "Visibility", False) and not o.Name.startswith("Modulo")]
    for n in nomes:
        d.getObject(n).Visibility = False
    d.recompute()
    conf = {}
    for n in nomes:
        lk = d.getObject(links[n])
        conf[n] = {"origem_visivel": d.getObject(n).Visibility, "vinculo_visivel": lk.Visibility, "vinculo_tem_forma": not Part.getShape(lk).isNull()}
    log.update({"visiveis_na_base_antes": visiveis_base, "conferencia": conf})
    if all((not c["origem_visivel"]) and c["vinculo_visivel"] and c["vinculo_tem_forma"] for c in conf.values()):
        d.save(); log["salvo"] = True
    log["ok"] = True
except Exception:
    log["erro"] = traceback.format_exc()
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
