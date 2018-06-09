# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qtexteditclicked import QTextEditClicked

class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName("DialogAbout")
        DialogAbout.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogAbout.resize(561, 599)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogAbout.sizePolicy().hasHeightForWidth())
        DialogAbout.setSizePolicy(sizePolicy)
        DialogAbout.setMinimumSize(QtCore.QSize(561, 592))
        DialogAbout.setMaximumSize(QtCore.QSize(561, 599))
        DialogAbout.setWindowTitle("О программе")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/stellaris.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogAbout.setWindowIcon(icon)
        DialogAbout.setStyleSheet("background-color: rgb(239, 235, 231);")
        self.aboutPict = QtWidgets.QLabel(DialogAbout)
        self.aboutPict.setGeometry(QtCore.QRect(10, 10, 543, 311))
        self.aboutPict.setMinimumSize(QtCore.QSize(543, 311))
        self.aboutPict.setMaximumSize(QtCore.QSize(543, 311))
        self.aboutPict.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.aboutPict.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.aboutPict.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.aboutPict.setText("")
        self.aboutPict.setPixmap(QtGui.QPixmap("backgroundAbout/about1.jpg"))
        self.aboutPict.setScaledContents(False)
        self.aboutPict.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.aboutPict.setObjectName("aboutPict")
        self.tabWidget = QtWidgets.QTabWidget(DialogAbout)
        self.tabWidget.setGeometry(QtCore.QRect(10, 330, 541, 261))
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit_2.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout_2.addWidget(self.textEdit_2, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit_4 = QtWidgets.QTextEdit(self.tab_3)
        self.textEdit_4.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.textEdit_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textEdit_4.setReadOnly(True)
        self.textEdit_4.setObjectName("textEdit_4")
        self.verticalLayout.addWidget(self.textEdit_4)
        self.tabWidget.addTab(self.tab_3, "")
        self.textEdit_3 = QTextEditClicked(DialogAbout)
        self.textEdit_3.setGeometry(QtCore.QRect(10, 10, 543, 311))
        self.textEdit_3.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.textEdit_3.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255, 0);")
        self.textEdit_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit_3.setUndoRedoEnabled(False)
        self.textEdit_3.setReadOnly(True)
        self.textEdit_3.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.textEdit_3.setObjectName("textEdit_3")
        self.tabWidget.raise_()
        self.aboutPict.raise_()
        self.textEdit_3.raise_()

        self.retranslateUi(DialogAbout)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        _translate = QtCore.QCoreApplication.translate
        self.textEdit.setHtml(_translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Эта программа считывает установленные моды для Stellaris и проверяет их обновления на сайте </span><a href=\"http://stellaris.smods.ru/\"><span style=\" font-size:11pt; font-weight:600; text-decoration: underline; color:#0000ff;\">http://stellaris.smods.ru</span></a><a href=\"http://stellaris.smods.ru/\"><span style=\" font-size:11pt; text-decoration: underline; color:#0000ff;\">/</span></a><a href=\"http://stellaris.smods.ru/\"><span style=\" font-size:8pt; text-decoration: underline; color:#0000ff;\">.</span></a></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Проверка осуществляется путем сравнения даты файла </span><span style=\" font-size:10pt; font-weight:600;\">mod</span><span style=\" font-size:10pt;\"> с </span><span style=\" font-size:10pt; font-weight:600;\">Last revision </span><span style=\" font-size:10pt;\">на сайте.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Можно загружать сразу несколько файлов. Смотри меню Настройки.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">При желании посмотреть информацию о выбранном моде.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; color:#ff0000;\">08.06.2018</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("DialogAbout", "О программе"))
        self.textEdit_2.setHtml(_translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Python 3.6.5</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">с модулями:</p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">PyQt 5.10.1</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">BeautifulSoup 4</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">dateutil 2.7.3</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">requests 2.18.4</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Qt Designer v 5.9.1</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Notepad++ v 7.5.6.</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("DialogAbout", "Среда разработки"))
        self.textEdit_4.setHtml(_translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Если моды не отображаются установите путь. Меню Настройки или файл &quot;umgui.ini&quot; pathMods.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">В Windows, обычно, путь к модам - /Users/Имя пользователя/Documents/Paradox Interactive/Stellaris.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:6pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">При ошибках загрузки, отображения модов удалите файл modid.ini. После удаления и перезапуска файл будет создан заново.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Формат файла id мода = http-адрес к stellaris.smods.ru, http-адрес к modsbase.com.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:6pt;\"> </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Информаци о моде  - двойной щелчок мыши и правая кнопка на таблице модов.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt;\">Значок в строке состояния показывает список открытых потоков и окон.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:6pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">P.S. Фон в &quot;О Программе&quot; меняются автоматически и по щелчку на картинке</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("DialogAbout", "Справка"))
        self.textEdit_3.setHtml(_translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; color:#ffffff;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MV Boli\'; font-size:18pt; color:#ffffff;\">Stellaris Update mods</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Segoe Script\'; font-size:18pt; color:#ffffff;\">from stellaris.smods.ru</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#ffffff;\">version 1.1 alpha</span></p></body></html>"))

