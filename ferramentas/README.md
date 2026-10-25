# Ferramentas

Scripts do projeto. Rode a partir da raiz do repositório (`guedala-park/`).

| Comando | O que faz | Tempo |
|---|---|---|
| `python ferramentas/verificar_tudo.py` | Roda todas as verificações rápidas abaixo de uma vez | segundos |
| `python ferramentas/verificar_modelo/verificar_modelo.py` | Modelo FreeCAD: arquivo vigente, cores (GuiDocument.xml), SHA do release, backups esquecidos | segundos |
| `python ferramentas/verificar_modelo/verificar_modelo.py --completo` | Abre o modelo no FreeCADCmd **sem salvar** e compara com a base: objetos removidos, formas inválidas, expressões perdidas, **colisões novas** | minutos |
| `python ferramentas/verificar_consistencia.py` | Documentos batem entre si (datas, versões, caderno × site) | segundos |
| `python ferramentas/verificar_links.py` | Links locais quebrados nos `.md` | segundos |
| `python -B ferramentas/site/construir.py` | Regenera o site a partir de `ferramentas/site/src/` | segundos |
| `ferramentas/cinematica/consultar.py` | Posições de portas e gavetas sem abrir o FreeCAD | segundos |

O hook de git (`ferramentas/hooks/pre-commit`) roda `verificar_tudo.py` antes de cada commit e bloqueia o commit se houver erro. Para ativar num clone novo: `git config core.hooksPath ferramentas/hooks`.

Detalhes do gerador do site: [site/README.md](site/README.md).
