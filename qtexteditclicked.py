from PyQt5 import QtWidgets, QtCore

class QTextEditClicked (QtWidgets.QTextEdit):
    clicked = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        QtWidgets.QTextEdit.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()