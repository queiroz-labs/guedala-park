from PySide6 import QtCore,QtGui,QtSvg
import pathlib
p=pathlib.Path(__file__).parent
app=QtGui.QGuiApplication([])
r=QtSvg.QSvgRenderer(str(p/'Corredor_Berlin_R42.svg'));im=QtGui.QImage(1250,930,QtGui.QImage.Format_ARGB32);im.fill(QtCore.Qt.white);paint=QtGui.QPainter(im);r.render(paint);paint.end();im.save(str(p/'Corredor_Berlin_R42.png'))

