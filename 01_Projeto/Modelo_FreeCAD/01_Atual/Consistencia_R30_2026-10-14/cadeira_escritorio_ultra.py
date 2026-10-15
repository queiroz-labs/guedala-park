# Cadeira de escritório GenioDesk ErgoChair Ultra Comfort — gabarito simplificado.
# Envelope do desenho técnico do fabricante: 745 L (braços) x 730 P x 1145-1330 A; assento 455-530.
# Posição modelada: assento a 470, apoio de cabeça com topo a 1200 (dentro das faixas).
# Sistema local: x = largura (0..745), y = profundidade (0 = frente, 730 = fundo), z = altura.
import FreeCAD as App, Part, math

P = dict(L=745.0, D=730.0,
         assento=470.0, assento_esp=60.0, assento_larg=510.0, assento_prof=500.0,
         base_r=320.0, base_cy=375.0, rodizio=60.0,
         encosto_larg=540.0, encosto_z0=520.0, encosto_z1=1060.0, encosto_esp=40.0, encosto_incl=14.0,
         cabeca_larg=320.0, cabeca_z0=1040.0, cabeca_z1=1200.0,
         braco_z=690.0)

def _gira(shape, ang, centro):
    shape.rotate(centro, App.Vector(0, 0, 1), ang)
    return shape

def pecas(p=P):
    L, D = p["L"], p["D"]
    cx, cy = L / 2, p["base_cy"]
    c = App.Vector(cx, cy, 0)
    res = []
    r = p["rodizio"] / 2
    # base estrela de 5 hastes (uma voltada para a frente) e rodízios de 60 mm
    for k in range(5):
        ang = -90 + 72 * k
        haste = Part.makeBox(p["base_r"] - 10, 50, 30, App.Vector(cx, cy - 25, r * 2 + 5))
        res.append(("BaseHaste", "estrutura", _gira(haste, ang, c)))
        roda = Part.makeCylinder(r, 24, App.Vector(cx + p["base_r"] - 5, cy - 12, r), App.Vector(0, 1, 0))
        res.append(("Rodizio", "estrutura", _gira(roda, ang, c)))
    res.append(("CentroBase", "estrutura", Part.makeCylinder(40, 40, App.Vector(cx, cy, r * 2))))
    # pistão e mecanismo
    zs = p["assento"] - p["assento_esp"]
    res.append(("Pistao", "estrutura", Part.makeCylinder(25, zs - 60 - r * 2, App.Vector(cx, cy, r * 2 + 40))))
    res.append(("Mecanismo", "estrutura", Part.makeBox(260, 260, 60, App.Vector(cx - 130, cy - 130, zs - 60))))
    # assento em tela
    al, ap = p["assento_larg"], p["assento_prof"]
    ass = Part.makeBox(al, ap, p["assento_esp"], App.Vector(cx - al / 2, 0, zs))
    try:
        ass = ass.makeFillet(25, [e for e in ass.Edges if abs(e.BoundBox.ZLength - p["assento_esp"]) < 1e-6])
    except Exception:
        pass
    res.append(("Assento", "tela", ass))
    # encosto inclinado e apoio de cabeça
    incl = math.radians(p["encosto_incl"])
    def inclinada(larg, esp, z0, z1, y0):
        b = Part.makeBox(larg, esp, (z1 - z0) / math.cos(incl))
        b.rotate(App.Vector(0, 0, 0), App.Vector(1, 0, 0), -p["encosto_incl"])
        b.translate(App.Vector(cx - larg / 2, y0, z0))
        return b
    y_enc = ap + 20
    res.append(("Encosto", "tela", inclinada(p["encosto_larg"], p["encosto_esp"], p["encosto_z0"], p["encosto_z1"], y_enc)))
    topo_enc_y = y_enc + (p["encosto_z1"] - p["encosto_z0"]) * math.tan(incl)
    yc = D - 50  # costas do apoio de cabeça no limite de 730 do desenho técnico
    res.append(("ApoioCabeca", "tela", Part.makeBox(p["cabeca_larg"], 50, p["cabeca_z1"] - p["cabeca_z0"], App.Vector(cx - p["cabeca_larg"] / 2, yc, p["cabeca_z0"]))))
    res.append(("HasteEncosto", "estrutura", Part.makeBox(60, 30, p["encosto_z0"] - zs + 40, App.Vector(cx - 30, ap - 10, zs - 40))))
    # braços: coluna + apoio
    for x0 in (0.0, L - 100):
        res.append(("BracoApoio", "estrutura", Part.makeBox(100, 260, 30, App.Vector(x0, 120, p["braco_z"] - 30))))
        xc = x0 + 30 if x0 == 0 else x0 + 30
        res.append(("BracoColuna", "estrutura", Part.makeBox(40, 60, p["braco_z"] - 30 - (zs - 20), App.Vector(xc, 300, zs - 20))))
        lado = cx - al / 2 if x0 == 0 else cx + al / 2 - 10
        xs = min(xc, lado), max(xc + 40, lado + 10)
        res.append(("BracoSuporte", "estrutura", Part.makeBox(xs[1] - xs[0], 60, 20, App.Vector(xs[0], 300, zs - 20))))
    return res
