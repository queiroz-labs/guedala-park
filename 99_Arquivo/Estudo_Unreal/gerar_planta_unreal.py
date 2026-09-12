"""
gerar_planta_unreal.py
-----------------------
Le o arquivo apartamento_dados.json e monta automaticamente, dentro do
Unreal Engine, o piso e as paredes do apartamento (com vaos de porta),
alem de rotulos de texto para se localizar (SALA, COZINHA, etc.) e um
PlayerStart na entrada, prontos para caminhar com Play.

COMO USAR
1. Coloque este arquivo e o "apartamento_dados.json" na mesma pasta.
2. Edite a linha CAMINHO_JSON logo abaixo com o caminho completo do .json
   nessa pasta (ex: caminho igual ao deste .py, so trocando o nome do arquivo).
3. No Unreal Editor: menu Tools > Execute Python Script... e selecione
   este arquivo (precisa ter ativado o plugin "Python Editor Script Plugin"
   em Edit > Plugins - veja o guia em PDF/Word que acompanha este script).
4. Confira no World Outliner os atores criados. De Play para caminhar.

Pode rodar quantas vezes quiser: cada execucao cria um novo conjunto de
atores (vai duplicar se rodar de novo sem apagar os anteriores). Para
recomecar do zero, selecione os atores antigos no World Outliner
(procure por "Quarto", "Escritorio", "Banho", "Sala, Cozinha" e "Rotulo")
e apague antes de rodar de novo.
"""

import unreal
import json

# ---------------------------------------------------------------------
# EDITE AQUI: caminho completo do apartamento_dados.json no seu computador
# ---------------------------------------------------------------------
CAMINHO_JSON = r"C:\Users\Elias\Desktop\Guedala Park\99_Arquivo/Estudo_Unreal/apartamento_dados.json"


def carregar_dados(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def spawn_cube(subsystem, cube_mesh, cx_m, cy_m, cz_m, sx_m, sy_m, sz_m, nome):
    """Cria um StaticMeshActor cubo, em metros (convertido para cm internamente)."""
    location = unreal.Vector(cx_m * 100.0, cy_m * 100.0, cz_m * 100.0)
    rotation = unreal.Rotator(0.0, 0.0, 0.0)
    actor = subsystem.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    actor.set_actor_label(nome)
    mesh_comp = actor.static_mesh_component
    mesh_comp.set_static_mesh(cube_mesh)
    actor.set_actor_scale3d(unreal.Vector(sx_m, sy_m, sz_m))
    return actor


def build_floor(subsystem, cube_mesh, x, y, w, d, nome):
    espessura_piso = 0.10
    cx = x + w / 2.0
    cy = y + d / 2.0
    spawn_cube(subsystem, cube_mesh, cx, cy, -espessura_piso / 2.0, w, d, espessura_piso, nome + " - piso")


def wall_with_door(subsystem, cube_mesh, room, parede, altura, espessura, altura_porta, nome):
    """
    Gera uma parede (norte/sul/leste/oeste) de um retangulo room = {x,y,largura,profundidade}.
    x,y = canto noroeste (esquerda/cima) do retangulo, no sistema onde
    x cresce para "leste" (direita) e y cresce para "sul" (para baixo).
    Se room['porta'] existir e 'parede' bater com room['porta']['parede'],
    a parede sai dividida em dois trechos + uma verga acima do vao.
    """
    x, y, w, d = room["x"], room["y"], room["largura"], room["profundidade"]
    porta = room.get("porta")
    tem_porta = porta is not None and porta.get("parede") == parede

    if parede == "norte":
        x1, y1 = x, y
        horizontal = True
        comprimento = w
    elif parede == "sul":
        x1, y1 = x, y + d
        horizontal = True
        comprimento = w
    elif parede == "oeste":
        x1, y1 = x, y
        horizontal = False
        comprimento = d
    elif parede == "leste":
        x1, y1 = x + w, y
        horizontal = False
        comprimento = d
    else:
        raise ValueError("parede invalida: " + str(parede))

    if not tem_porta:
        if horizontal:
            cx = x1 + comprimento / 2.0
            spawn_cube(subsystem, cube_mesh, cx, y1, altura / 2.0, comprimento, espessura, altura, nome)
        else:
            cy = y1 + comprimento / 2.0
            spawn_cube(subsystem, cube_mesh, x1, cy, altura / 2.0, espessura, comprimento, altura, nome)
        return

    d0 = porta["distancia_do_canto"]
    dl = porta["largura"]
    d1 = d0 + dl
    verga_altura = altura - altura_porta

    if horizontal:
        if d0 > 0.01:
            spawn_cube(subsystem, cube_mesh, x1 + d0 / 2.0, y1, altura / 2.0, d0, espessura, altura, nome + " (trecho A)")
        if comprimento - d1 > 0.01:
            spawn_cube(subsystem, cube_mesh, x1 + d1 + (comprimento - d1) / 2.0, y1, altura / 2.0,
                       comprimento - d1, espessura, altura, nome + " (trecho B)")
        if verga_altura > 0.01:
            spawn_cube(subsystem, cube_mesh, x1 + d0 + dl / 2.0, y1, altura_porta + verga_altura / 2.0,
                       dl, espessura, verga_altura, nome + " (verga)")
    else:
        if d0 > 0.01:
            spawn_cube(subsystem, cube_mesh, x1, y1 + d0 / 2.0, altura / 2.0, espessura, d0, altura, nome + " (trecho A)")
        if comprimento - d1 > 0.01:
            spawn_cube(subsystem, cube_mesh, x1, y1 + d1 + (comprimento - d1) / 2.0, altura / 2.0,
                       espessura, comprimento - d1, altura, nome + " (trecho B)")
        if verga_altura > 0.01:
            spawn_cube(subsystem, cube_mesh, x1, y1 + d0 + dl / 2.0, altura_porta + verga_altura / 2.0,
                       espessura, dl, verga_altura, nome + " (verga)")


def main():
    dados = carregar_dados(CAMINHO_JSON)

    subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    cube_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    if cube_mesh is None:
        unreal.log_error("Nao encontrei /Engine/BasicShapes/Cube. Confira se o Starter Content / Engine Content esta disponivel.")
        return

    altura = dados["pe_direito_m"]
    espessura = dados["espessura_parede_m"]
    altura_porta = dados["altura_porta_m"]

    # 1) Comodos fechados (Quarto, Escritorio, Banho)
    for room in dados["ambientes_fechados"]:
        nome = room["nome"]
        build_floor(subsystem, cube_mesh, room["x"], room["y"], room["largura"], room["profundidade"], nome)
        for parede in ("norte", "sul", "leste", "oeste"):
            wall_with_door(subsystem, cube_mesh, room, parede, altura, espessura, altura_porta,
                           nome + " - parede " + parede)

    # 2) Area integrada (Sala + Cozinha + Circulacao + Area de Servico, sem paredes internas)
    ai = dados["area_integrada"]
    porta_entrada = ai.get("porta_entrada")
    build_floor(subsystem, cube_mesh, ai["x"], ai["y"], ai["largura"], ai["profundidade"], ai["nome"])
    for parede in ("norte", "sul", "leste", "oeste"):
        room_ai = {"x": ai["x"], "y": ai["y"], "largura": ai["largura"], "profundidade": ai["profundidade"]}
        if porta_entrada and porta_entrada.get("parede") == parede:
            room_ai["porta"] = porta_entrada
        wall_with_door(subsystem, cube_mesh, room_ai, parede, altura, espessura, altura_porta,
                       ai["nome"] + " - parede " + parede)

    # 3) Rotulos de texto flutuante para se localizar
    for rot in dados.get("rotulos_internos", []):
        loc = unreal.Vector(rot["x"] * 100.0, rot["y"] * 100.0, altura * 100.0 * 0.85)
        actor = subsystem.spawn_actor_from_class(unreal.TextRenderActor, loc, unreal.Rotator(0.0, 90.0, 0.0))
        actor.set_actor_label("Rotulo - " + rot["nome"])
        try:
            texto = actor.text_render
            texto.set_text(rot["nome"])
            texto.set_world_size(30.0)
            texto.set_text_render_color(unreal.Color(25, 25, 25, 255))
            texto.set_horizontal_alignment(unreal.HorizTextAligment.EHTA_CENTER)
        except Exception as e:
            unreal.log_warning("Nao consegui configurar o texto do rotulo {}: {}".format(rot["nome"], e))

    # 4) PlayerStart na porta de entrada, para poder dar Play e caminhar
    if porta_entrada:
        px = ai["x"] + porta_entrada["distancia_do_canto"] + porta_entrada["largura"] / 2.0
        py = ai["y"] + ai["profundidade"] - 0.5
        loc = unreal.Vector(px * 100.0, py * 100.0, 100.0)
        player_start = subsystem.spawn_actor_from_class(unreal.PlayerStart, loc, unreal.Rotator(0.0, 180.0, 0.0))
        player_start.set_actor_label("PlayerStart - Entrada")

    unreal.log("Planta gerada! Veja o World Outliner. Se algo ficou girado ou de costas, ajuste manualmente no editor.")


main()
