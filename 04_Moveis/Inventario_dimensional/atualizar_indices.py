from pathlib import Path
p=Path(__file__).parent
root=p.parent.parent
for f,prefix in [(root/'README.md','01_Projeto/'),(p.parent/'Painel_de_decisoes.md','')]:
 text=f.read_text(encoding='utf8')
 banner=f'> **Consolidação R45 — 23/10/2026:** [Relatório dimensional e ferragens]({prefix}Consolidacao_R45_2026-10-23/Relatorio.html) · [FreeCAD R45]({prefix}Consolidacao_R45_2026-10-23/Guedala_Park_R45_Consolidado.FCStd). Revisados 20 módulos e 171 interfaces; 52 dobradiças vigentes; capacidade FGVTN corrigida para 35 kg. R44 preservada, geometria principal mantida e alternativas reunidas em grupos ocultos. Não equivale a aprovação integral de fabricação. Referências de revisão vigente abaixo ficam como histórico; consultar esta consolidação e seus limites primeiro.\n\n'
 if not text.startswith('> **Consolidação R45'):f.write_text(banner+text,encoding='utf8')
