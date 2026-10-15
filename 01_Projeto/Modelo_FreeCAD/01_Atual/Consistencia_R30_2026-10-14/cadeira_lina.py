# Cadeira Lina Estofada (Versatile) — gabarito paramétrico simplificado.
# Envelope de catálogo 440 L x 470 P x 940 A. Demais medidas estimadas pelas fotos (hipótese).
# Sistema local: x = largura (0..L), y = profundidade (0 = frente, P = fundo), z = altura.
import FreeCAD as App, Part, math

P = dict(L=440.0, D=470.0, H=940.0,
         assento=470.0,      # topo do estofado (hipótese)
         estofado=50.0,      # espessura do assento estofado
         saia=60.0,          # altura da moldura sob o assento
         pe=38.0,            # seção do pé no topo
         pe_base=28.0,       # seção do pé no piso (afunilado)
         recuo_encosto=32.0, # inclinação das colunas traseiras no topo
         enc_z0=500.0, enc_z1=830.0, enc_esp=25.0,
         trav_h=30.0, trav_esp=20.0, trav1=860.0, trav2=905.0)

def _loft(r0, r1):
    """r = (x0, y0, x1, y1, z) retângulo horizontal; loft sólido entre dois."""
    def w(r):
        x0, y0, x1, y1, z = r
        pts = [App.Vector(x0, y0, z), App.Vector(x1, y0, z), App.Vector(x1, y1, z), App.Vector(x0, y1, z), App.Vector(x0, y0, z)]
        return Part.makePolygon(pts)
    return Part.makeLoft([w(r0), w(r1)], True)

def pecas(p=P):
    L, D = p["L"], p["D"]
    zf = p["assento"] - p["estofado"]          # topo da moldura
    s, sb = p["pe"], p["pe_base"]
    k = (D - s) / 1.0                          # y frontal do pé traseiro no fundo
    yr = D - s - p["recuo_encosto"]            # y frontal da coluna na altura do assento
    tan = p["recuo_encosto"] / (p["H"] - zf)
    res = []
    # pés dianteiros (afunilados para dentro)
    for x0 in (0.0, L - s):
        xi = x0 + (s - sb if x0 > 0 else 0)
        res.append(("PeFrente", "madeira", _loft((xi, s - sb, xi + sb, s, 0.0), (x0, 0.0, x0 + s, s, zf))))
    # pés traseiros + colunas do encosto
    for x0 in (0.0, L - s):
        xi = x0 + (s - sb if x0 > 0 else 0)
        baixo = _loft((xi, D - sb, xi + sb, D, 0.0), (x0, yr, x0 + s, yr + s, zf))
        alto = _loft((x0, yr, x0 + s, yr + s, zf), (x0, yr + p["recuo_encosto"], x0 + s, D, p["H"]))
        res.append(("PeTrasColuna", "madeira", baixo.fuse(alto).removeSplitter()))
    # moldura (saia) do assento
    z0 = zf - p["saia"]
    res.append(("SaiaFrente", "madeira", Part.makeBox(L - 2 * s, 20, p["saia"], App.Vector(s, 0, z0))))
    res.append(("SaiaTras", "madeira", Part.makeBox(L - 2 * s, 20, p["saia"], App.Vector(s, yr, z0))))
    for x0 in (0.0, L - 20):
        res.append(("SaiaLateral", "madeira", Part.makeBox(20, yr - s, p["saia"], App.Vector(x0 + (0 if x0 == 0 else 0), s, z0))))
    # assento estofado
    ass = Part.makeBox(L, yr + s - 5, p["estofado"], App.Vector(0, 0, zf))
    try:
        ass = ass.makeFillet(10, [e for e in ass.Edges if abs(e.BoundBox.ZMin - p["assento"]) < 1e-6 and abs(e.BoundBox.ZMax - p["assento"]) < 1e-6])
    except Exception:
        pass
    res.append(("Assento", "estofado", ass))
    # encosto estofado e travessas, inclinados com as colunas
    ang = -math.degrees(math.atan(tan))
    def inclinada(larg, esp, alt, z, dy):
        b = Part.makeBox(larg, esp, alt)
        b.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), ang)
        b.translate(App.Vector(s, yr + dy + (z - zf) * tan, z))
        return b
    res.append(("Encosto", "estofado", inclinada(L - 2 * s, p["enc_esp"], p["enc_z1"] - p["enc_z0"], p["enc_z0"], 6)))
    res.append(("TravessaEncosto", "madeira", inclinada(L - 2 * s, p["trav_esp"], p["trav_h"], p["trav1"], 9)))
    res.append(("TravessaEncosto", "madeira", inclinada(L - 2 * s, p["trav_esp"], p["trav_h"], p["trav2"], 9)))
    return res
