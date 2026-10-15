from pathlib import Path
import ast
root=(Path(__file__).resolve().parent / '.').resolve()
code=((Path(__file__).resolve().parent / '../Apoios_R11_2026-10-14/varrer_frentes.py').resolve()).read_text(encoding='utf-8').replace('R11','R12').replace('my=56.5',"my=row['hinge_y_mm']")
ast.parse(code);((Path(__file__).resolve().parent / 'varrer_frentes.py').resolve()).write_text(code,encoding='utf-8')
