"""Cena vetorial em milímetros de papel, compartilhada por SVG e PDF."""
from html import escape
import os
from pathlib import Path


class Folha:
    def __init__(self, codigo, titulo, escala):
        self.codigo, self.titulo, self.escala = codigo, titulo, escala
        self.itens, self.cotas, self.avisos = [], {}, []

    def linha(self, x, y, xx, yy, cor='#34434a', largura=.2, tracejado=False):
        self.itens.append(('line', [x, y, xx, yy], cor, largura, tracejado))

    def caixa(self, x, y, w, h, cor='#34434a', fundo=None, largura=.2):
        if w < 0 or h < 0:
            raise ValueError('Retângulo negativo: não desenhar dimensão incoerente')
        self.itens.append(('rect', [x, y, w, h], cor, fundo, largura))

    def texto(self, x, y, texto, tamanho=2.6, cor='#263238'):
        self.itens.append(('text', [x, y], str(texto), tamanho, cor))

    def svg(self):
        result = ['<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297">',
                  '<rect width="420" height="297" fill="white"/>']
        for typ, v, a, b, c in self.itens:
            if typ == 'line':
                dash = ' stroke-dasharray="1.5 1"' if c else ''
                result.append(f'<line x1="{v[0]}" y1="{v[1]}" x2="{v[2]}" y2="{v[3]}" stroke="{a}" stroke-width="{b}"{dash}/>')
            elif typ == 'rect':
                result.append(f'<rect x="{v[0]}" y="{v[1]}" width="{v[2]}" height="{v[3]}" stroke="{a}" fill="{b or "none"}" stroke-width="{c}"/>')
            else:
                result.append(f'<text x="{v[0]}" y="{v[1]}" font-family="Arial, sans-serif" font-size="{b}" fill="{c}">{escape(a)}</text>')
        return '\n'.join(result + ['</svg>'])


def pdf(folhas, destino):
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.colors import HexColor
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    font='Helvetica'
    fontpath=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts/arial.ttf'
    if fontpath.exists():
        pdfmetrics.registerFont(TTFont('Guedala',str(fontpath)))
        font='Guedala'
    canvas = Canvas(destino if hasattr(destino, 'write') else str(destino), pagesize=(420*mm, 297*mm), invariant=True)
    canvas.setTitle('Guedala Park - Caderno de pranchas R02 - ESTUDO')
    for folha in folhas:
        for typ, v, a, b, c in folha.itens:
            if typ == 'text':
                canvas.setFont(font, b*mm)
                canvas.setFillColor(HexColor(c))
                canvas.drawString(v[0]*mm, (297-v[1])*mm, a)
            elif typ == 'line':
                canvas.setStrokeColor(HexColor(a)); canvas.setLineWidth(b*mm)
                canvas.setDash([1.5*mm, mm] if c else [])
                canvas.line(v[0]*mm, (297-v[1])*mm, v[2]*mm, (297-v[3])*mm)
            else:
                canvas.setDash([]); canvas.setStrokeColor(HexColor(a)); canvas.setLineWidth(c*mm)
                if b:
                    canvas.setFillColor(HexColor(b))
                canvas.rect(v[0]*mm, (297-v[1]-v[3])*mm, v[2]*mm, v[3]*mm, stroke=1, fill=int(bool(b)))
        canvas.showPage()
    canvas.save()
