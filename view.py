# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_view_mod(object):
    def setupUi(self, view_mod):
        view_mod.setObjectName("view_mod")
        view_mod.resize(547, 544)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/stellaris.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        view_mod.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(view_mod)
        self.gridLayout.setObjectName("gridLayout")
        self.loadButton = QtWidgets.QPushButton(view_mod)
        self.loadButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadButton.sizePolicy().hasHeightForWidth())
        self.loadButton.setSizePolicy(sizePolicy)
        self.loadButton.setMinimumSize(QtCore.QSize(91, 31))
        self.loadButton.setMaximumSize(QtCore.QSize(91, 31))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/downloads.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.loadButton.setIcon(icon1)
        self.loadButton.setIconSize(QtCore.QSize(20, 20))
        self.loadButton.setObjectName("loadButton")
        self.gridLayout.addWidget(self.loadButton, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(view_mod)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 5)
        self.sizeLabel = QtWidgets.QLabel(view_mod)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sizeLabel.setFont(font)
        self.sizeLabel.setObjectName("sizeLabel")
        self.gridLayout.addWidget(self.sizeLabel, 0, 1, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(view_mod)
        self.progressBar.setMinimumSize(QtCore.QSize(100, 21))
        self.progressBar.setMaximumSize(QtCore.QSize(100, 21))
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 0, 4, 1, 1)

        self.retranslateUi(view_mod)
        QtCore.QMetaObject.connectSlotsByName(view_mod)

    def retranslateUi(self, view_mod):
        _translate = QtCore.QCoreApplication.translate
        view_mod.setWindowTitle(_translate("view_mod", "Описание мода"))
        self.loadButton.setToolTip(_translate("view_mod", "Загрузить мод"))
        self.loadButton.setText(_translate("view_mod", "Загрузить"))
        self.sizeLabel.setText(_translate("view_mod", "Размер мода -"))

