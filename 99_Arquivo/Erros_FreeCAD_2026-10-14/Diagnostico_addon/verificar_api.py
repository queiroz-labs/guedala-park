# Read-only API inspection for the responsible agent in an existing FreeCAD GUI.
# Does not start observers, servers, dialogs, or capture interactions.
from PySide import QtCore, QtGui
try:
    from PySide import QtWidgets
except ImportError:
    QtWidgets = QtGui

required = {
    'QtCore.QObject': hasattr(QtCore, 'QObject'),
    'QtCore.QEvent.HoverEnter': hasattr(QtCore.QEvent, 'HoverEnter'),
    'QtCore.QEvent.MouseButtonPress': hasattr(QtCore.QEvent, 'MouseButtonPress'),
    'QtGui.QMouseEvent.x': hasattr(QtGui.QMouseEvent, 'x'),
    'QtGui.QMouseEvent.y': hasattr(QtGui.QMouseEvent, 'y'),
    'QtWidgets.QMessageBox': hasattr(QtWidgets, 'QMessageBox'),
    'QtWidgets.QMessageBox.Information': hasattr(QtWidgets.QMessageBox, 'Information'),
    'QtWidgets.QMessageBox.exec_': hasattr(QtWidgets.QMessageBox, 'exec_'),
    'QtWidgets.QDialog': hasattr(QtWidgets, 'QDialog'),
    'QtWidgets.QDialog.exec_': hasattr(QtWidgets.QDialog, 'exec_'),
    'QtWidgets.QVBoxLayout': hasattr(QtWidgets, 'QVBoxLayout'),
    'QtWidgets.QTabWidget': hasattr(QtWidgets, 'QTabWidget'),
    'QtWidgets.QTextEdit': hasattr(QtWidgets, 'QTextEdit'),
    'QtWidgets.QListWidget': hasattr(QtWidgets, 'QListWidget'),
    'QtWidgets.QDialogButtonBox': hasattr(QtWidgets, 'QDialogButtonBox'),
    'QtWidgets.QDialogButtonBox.Ok': hasattr(QtWidgets.QDialogButtonBox, 'Ok'),
}
result = {
    'QtCore_module': QtCore.__name__,
    'QObject_module': QtCore.QObject.__module__,
    'QDialog_module': QtWidgets.QDialog.__module__,
    'api_present': required,
    'missing': [key for key, present in required.items() if not present],
}
