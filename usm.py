import datetime
import locale
import os
import random
import sys

import requests  # Для запросов GET и POST
from PyQt5 import QtWidgets, QtGui, QtCore
from bs4 import BeautifulSoup  # Для парсинга сайта
from dateutil.parser import *  # Преобразование даты с сайта

# Подключаем окна
import About
import MainWindow
import Options
import view

configUSM = 'configusm.ini'  # Файл параметров
modid_ini = 'modid.ini'      # Файл список ID модов и их http адресов
# Параметры программы
param = {}
param['pathMods'] = '/Documents/Paradox Interactive/Stellaris'               # Путь расположения модов
param['pathLoad'] = 'download'       # Путь для загрузки
param['max_size'] = 2 * 1024 * 1024  # Минимальны размер файла для stream (байт)
param['chunk'] = 2 * 1024            # Размер куска для загрузки stream (байт)
param['max_load'] = 2                # Количество одновременных загрузок
param['max_verify'] = 3              # Кол-во потоков для проверки
param['max_win'] = 4                 # Макс. кол-во окно с инфой
param['max_win_load'] = 2            # Кол-во загрузок из окон с инфой
# Заголовок http-запроса
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
my_headers = {'User-Agent': user_agent, }
mod_id_http = {}       # Словарь {'id': ('http smods', 'http mdosbase')}
list_mod = []          # Список загруженных модов
list_mod_load = []     # Список модов выбранных для загрузки
count_mod_load = 0     # Кол-во загруженных модов
size_mod_load = 0      # Общий размер загруженных модов
prog_state = ('OK', 'CANCEL', 'LOAD', 'ERROR', 'CHECK')
last_tread_col = 0     # Последний запущенный поток из колонки
show_win = {}          # Словарь окрытых окон для просмотра {str ID, указатель на окно}
load_inf = {}          # Словарь потоков загрузки инфы (str ID, указатель на поток} (инфа)
load_ver = {}          # Словарь потоков для проверки {str ID, указатель на поток}
load_mod = {}          # Словарь потоков загрузки мода (главное окно) {str ID, указатель на поток}
load_mod_win = {}      # Словарь потоков загрузки мода (окно просмотра) {str ID, указатель на поток}
thread_is_run = False  # Флаг отмены потока
# Номера столбцов таблице
col_STATE = 0        # Колонка с галочкой
col_NAME = 1
col_ID = 2
col_SIZE = 3
col_DATE = 4
col_CHECK = 5        # Статус мода
col_NEWDATE = 6      # Дата мода на сайте
col_NEWSIZE = 7      # Размер мода на сайте

# Поиск мода на stellaris.smods.ru и modsbase.com по ID return (str http_smods, str http_modbase)
def id_to_http(modID):
    global mod_id_http, prog_state
    http_smods = ''
    http_modbase = ''
        # Пробуем найти адрес в словаре mod_id_http
    if modID in mod_id_http:
        http_smods = mod_id_http[modID][0]
        http_modbase = mod_id_http[modID][1]
    else:
            # Ищем http адрес на smods.ru
        my_page = requests.get('http://stellaris.smods.ru/?s='+modID, headers=my_headers)
        soup = BeautifulSoup(my_page.text, "html.parser")
        try:
            http_smods = soup.find(attrs={"class": "post-title entry-title"}).find('a').get('href')
        except AttributeError:
            prog_state = 'ERROR'
        else:
                # Ищем HTTP адрес на файлохранилище по tr_adr_smods
            send = requests.get(http_smods, headers=my_headers)
            soup = BeautifulSoup(send.text, "html.parser")
            try:
                        # Получаем ссылку на страницу файлохранилища
                http_modbase = soup.find(attrs={"class": "post-excerpt-download"}).get('href')
            except AttributeError:
                prog_state = 'ERROR'
            else:
                    # Пишем найденые адрес в mod_idip и modid.ini
                mod_id_http[modID] = (http_smods, http_modbase)
                with open(modid_ini, "a") as file:
                    file.write(modID + ' = ' + http_smods + ', ' + http_modbase + '\n')
    return http_smods, http_modbase

# Читаем установленные моды, list_ mod(str id_mod, str name_mod, int size_mod, datetime date_mod)
def get_instlled_mod():
    global list_mod, param
    list_mod = []
    if os.path.exists(param['pathMods'] + '/mod'):
        listmods = os.listdir(param['pathMods'] + '/mod')  # Список всех модов
        for mod_list in listmods:
            filename = param['pathMods'] + '/mod/' + mod_list
            # Читаем имя мода из файла .mod
            file = open(filename, 'r')
            name_mod = file.readline()
            name_mod = name_mod[6:-2]
            file.close()
            # Читаем id мода (имя файла без расширения)
            id_mod = str(mod_list[:-4])
            # Читаем размер мода
            filename = param['pathMods'] + '/workshop/content/281990/' + mod_list[:-4]
            size_mod = os.path.getsize(filename + "/" + os.listdir(filename)[0])
            # Читаем дату мода (файла из каталога mod)
            date_mod = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
            inf_mod = [id_mod, name_mod, size_mod, date_mod]
            list_mod += [inf_mod]

# Выводим ссобщение Info, Critical, Warning (тип, инфо, текст, детали, название окна)
def show_info_mes(type_mes, tile_mes, text_mes, inftext_mes, dettext_mes):
    my_msg = QtWidgets.QMessageBox()
    if type_mes == 'warning':
        my_msg.setIcon(QtWidgets.QMessageBox.Warning)
    elif type_mes == 'info':
        my_msg.setIcon(QtWidgets.QMessageBox.Information)
    else:
        my_msg.setIcon(QtWidgets.QMessageBox.Critical)
    my_msg.setText(text_mes)
    my_msg.setInformativeText(inftext_mes)
    my_msg.setDetailedText(dettext_mes)
    my_msg.setWindowTitle(tile_mes)
    my_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    my_msg.exec()

# Поток для загрузки файлов
class threadDownLoad(QtCore.QThread):
    load_thr = QtCore.pyqtSignal(str, str, int, str)
    size_load_thr = QtCore.pyqtSignal(str, int, int)
    mod_id = ''
    mod_name = ''
    info = ''
    thread_size = 0

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

    # Загрузка файла по id мода , имя файла (путь+имя))
    # возвращает размер загруженных данных (строка) и status
    # 'ref' - загрузить главное окно, 'loa' - загрузить мод
    def run(self):
        global my_headers, thread_is_run, param
        # Ищем http-страницу для загрузки файла  tr_adr_modbase, tr_name
        status_show = 'OK'
        my_param = {}   # Параметры для первого POST запроса
        my_param2 = {}  # Параметры для второго POST запроса
        dl_size = 0     # Кол-во загруженных байт для progressBar
        (http_smods, http_modbase) = id_to_http(self.mod_id)
        if thread_is_run:
            if http_modbase != '':
                if self.info == 'ref':
                    # Получаем имя файла
                    (dirname, self.mod_name) = os.path.split(http_modbase)
                    self.mod_name = self.mod_name[:-5]
                    if not os.path.isdir(param['pathLoad']):
                        os.mkdir(param['pathLoad'])
                    self.mod_name = param['pathLoad']+'/' + self.mod_name
                with requests.Session() as my_session:
                    req_load = my_session.get(http_modbase, headers=my_headers)
                    soup = BeautifulSoup(req_load.content, "html.parser")
                    # Получаем параметры для 1-ого POST
                    paramm = soup.find(attrs={"class": "file-panel"}).find_all('input')
                    for pararam in paramm:
                        my_param[pararam.get('name')] = pararam.get('value')
                        # Первый POST запрос
                    if thread_is_run:
                        req_load = my_session.post(req_load.url, headers=my_headers, data=my_param)
                        soup = BeautifulSoup(req_load.content, "html.parser")
                        try:
                            # Получаем параметры для 2-ого POST
                            paramm = soup.find(attrs={"class": "download-link text-center clearfix"}).find_all('input')
                        except AttributeError:
                            # Ошибка при загрузке
                            status_show = 'ERROR'
                        else:
                            for pararam in paramm:
                                my_param2[pararam.get('name')] = pararam.get('value')
                                # Второй POST запрос
                            if thread_is_run:
                                req_load = my_session.post(req_load.url, headers=my_headers, data=my_param2)
                                # Получили ссылку на файл
                                url_load = req_load.url
                                req_load = my_session.get(url_load, headers=my_headers, stream=True)
                                self.thread_size = req_load.headers.get('Content-length')  # Размер файла (строка)
                                self.thread_size = int(self.thread_size)   # Размер файла (int)
                                # Пишем файл
                                if thread_is_run:
                                    file_download = open(self.mod_name, "wb")
                                    if self.thread_size < param['max_size']:  # Если размер мешьше
                                        file_download.write(req_load.content)
                                        file_download.close()
                                    else:
                                        for load_data in req_load.iter_content(chunk_size=param['chunk']):
                                            if thread_is_run:
                                                if load_data:
                                                    dl_size += param['chunk']
                                                    self.size_load_thr.emit(self.mod_id, dl_size, self.thread_size)
                                                    file_download.write(load_data)
                                                    file_download.flush()
                                            else:
                                                file_download.close()
                                                self.thread_size = 0
                                                status_show = 'CANCEL'
                                                break
                                else:
                                    status_show = 'CANCEL'
                            else:
                                status_show = 'CANCEL'
                    else:
                        status_show = 'CANCEL'
            else:
                status_show = 'ERROR'
        else:
            status_show = 'CANCEL'
        self.load_thr.emit(status_show, self.mod_id, self.thread_size, self.mod_name)

# Поток для получени даты, размера и инфо мода
class threadShow(QtCore.QThread):
    fin_thr = QtCore.pyqtSignal(str, str, str, str)
    mod_id = ''
    info = ''

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.thread_size = ''
        self.thread_date = ''
        self.thread_text = ''

    # Получаем ID мода и 'win' или 'ver'
    # win - инфо в новом окне, ver - запустили проверку
    def run(self):
        global my_headers, thread_is_run
        status_show = 'OK'
        # Получаем http адреса
        (http_smods, http_modbase) = id_to_http(self.mod_id)
        if thread_is_run:
            # Получение новой даты (Last revision) мода по http адресу (stellaris.smods.ru) (строка)
            # или информациию об моде (html страница)
            my_page = requests.get(http_smods, headers=my_headers)   # запрос на smods
            if self.info == 'win':    # Получаем текст об моде
                try:
                    self.thread_text = BeautifulSoup(my_page.text, "html.parser").find(attrs={"class": "pad group"})
                    self.thread_text = str(self.thread_text)
                except AttributeError:
                    status_show = 'ERROR'
            else:               # Получаем дату
                soup = BeautifulSoup(my_page.text, "html.parser")
                try:
                    self.thread_date = soup.find(attrs={"class": "datetime"}).string
                except AttributeError:
                    status_show = 'ERROR'
        else:
            status_show = 'CANCEL'
        if thread_is_run:
            # Получение размера мода по http адресу (modsbase.com), возвращает размер (строка)
            my_page = requests.get(http_modbase, headers=my_headers)
            soup = BeautifulSoup(my_page.content, "html.parser")
            try:
                self.thread_size = soup.find(attrs={"class": "size"}).string[1:-1]     # Пишем размер
            except AttributeError:
                status_show = 'ERROR'
        else:
            status_show = 'CANCEL'
        if self.info == 'win':
            self.fin_thr.emit(status_show, self.mod_id, self.thread_text, self.thread_size)
        else:
            self.fin_thr.emit(status_show, self.mod_id, self.thread_date, self.thread_size)

# Окно вывода информации о моде
class view_mod(QtWidgets.QWidget, view.Ui_view_mod):
    def __init__(self, parent=None):
        #super().__init__(parent)
        super(view_mod, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowModality(QtCore.Qt.NonModal)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.setAttribute(QtCore.Qt.WA_NativeWindow, True)
        self.loadButton.clicked.connect(self.on_load_click)
        self.win_mod_id = ''
        self.win_name = ''
        self.act_win = QtWidgets.QAction()
        self.act_win.triggered.connect(self.act_win_click)
        self.inf_load = False   # Идет загрузка инфы
        self.mod_load = False   # Идет загрузка мода

    # Устанавливаем id мода для окна
    def setID(self, mod_id, name_id):
        self.win_mod_id = mod_id
        self.win_name = name_id
        self.setWindowTitle(self.win_name + ' - ' + self.win_mod_id)

    # Дестивие по меню Окна
    def act_win_click(self):
        self.activateWindow()

    # Кнопка Загрузить
    def on_load_click(self):
        global load_mod_win, thread_is_run, param, window
        if not self.mod_load:
            if len(load_mod_win) < param['max_win_load']:
                (http_smods, http_modbase) = id_to_http(self.win_mod_id)
                (dirname, filename) = os.path.split(http_modbase)
                filename = filename[:-5]
                filename = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить", param['pathLoad'] + '/' + filename)
                if filename[0] != '':
                    self.loadButton.setDisabled(True)
                    self.mod_load = True
                    self.progressBar.setValue(0)
                    self.progressBar.setMinimum(0)
                    self.progressBar.setMaximum(0)
                    window.start_load_win(self.win_mod_id, filename[0])
            else:
                show_info_mes('warning', 'Предупреждение', 'Превышено количество загрузок', 'Подождите окончания загрузки', '')

    # При закрытии окна
    def closeEvent(self, evnt):
        global show_win, window
        window.win_menu.removeAction(self.act_win)
        del show_win[self.win_mod_id]
        window.set_status_buttonIcon()
        evnt.accept()

# Окно Настройки
class DialogOptions(QtWidgets.QDialog, Options.Ui_DialogOptions):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.saveButton.clicked.connect(self.save_click)
        self.cancelButton.clicked.connect(self.cancel_click)
        self.toolButton.clicked.connect(self.tool_1_click)
        self.toolButton_2.clicked.connect(self.tool_2_click)

        # Кнопка сохранить
    def save_click(self):
        global param
        old_path = param['pathMods']
        param['pathMods'] = self.textEdit.toPlainText()
        param['pathDownload'] = self.textEdit_2.toPlainText()
        param['max_size'] = int(self.lineEdit.text())
        param['chunk'] = int(self.lineEdit_2.text())
        param['max_load'] = int(self.lineEdit_3.text())
        param['max_verify'] = int(self.lineEdit_4.text())
        param['max_win'] = int(self.lineEdit_5.text())
        param['max_win_load'] = int(self.lineEdit_6.text())
        with open(configUSM, "w") as file:
            file.writelines("pathMods = " + param['pathMods']+"\n")
            file.writelines("pathDownload = " + param['pathDownload']+"\n")
            file.writelines("max_size =  " + self.lineEdit.text()+"\n")
            file.writelines("chunk = " + self.lineEdit_2.text()+"\n")
            file.writelines("max_load = " + self.lineEdit_3.text()+"\n")
            file.writelines("max_verify = " + self.lineEdit_4.text()+"\n")
            file.writelines("max_win = " + self.lineEdit_5.text()+"\n")
            file.writelines("max_win_load = " + self.lineEdit_6.text())
        if old_path != param['pathMods']:
            self.parent().mods_table_create()
        self.close()

        # Кнопка отменить
    def cancel_click(self):
        self.close()

        # Кнопки выбора каталога
    def tool_1_click(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            self.textEdit.setText(directory)

    def tool_2_click(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        if directory:
            self.textEdit_2.setText(directory)

# Окно О программе
class AboutDialog(QtWidgets.QDialog, About.Ui_DialogAbout):
    # Размер картинки 540x338 пикс
    about_pict = 0
    background_list = ()
    background_count = 0

    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.MSWindowsFixedSizeDialogHint)
        self.textEdit_3.clicked.connect(self.next_click)
        self.about_pict = 0
        if os.path.exists('backgroundAbout'):
            self.background_list = os.listdir('backgroundAbout')
            self.background_count = len(self.background_list)

    def set_about_pict(self):
        self.aboutPict.setPixmap(QtGui.QPixmap("backgroundAbout/" + self.background_list[self.about_pict]))

    def next_click(self):
        if self.about_pict != self.background_count-1:
            self.about_pict += 1
        else:
            self.about_pict = 0
        self.set_about_pict()

# Главное окно
class usmApp(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        global show_win, load_inf, load_mod, load_ver, load_mod_win
        super().__init__()
        self.setupUi(self)
        self.aboutWin = None
        self.configWin = None
        self.vv = None
        show_win = {}
        load_inf = {}
        load_ver = {}
        load_mod = {}
        load_mod_win = {}
        # Задаем левую часть statusbar
            # Кол-во модов status_widget
        self.status_widget1 = QtWidgets.QLabel()
        self.status_widget1.setText('Кол-во модов - ')
        self.statusbar.addWidget(self.status_widget1, 0)
            # Общий размер модов status_widget2
        self.status_widget2 = QtWidgets.QLabel()
        self.status_widget2.setText('Размер модов - ')
        self.statusbar.addWidget(self.status_widget2, 0)
            # Задаем даействия на нажатия кнопки
        self.buttonCheckDate.clicked.connect(self.on_verify_click)
        self.buttonLoadAll.clicked.connect(self.on_load_all_click)
        self.buttonCheck.clicked.connect(self.check_uncheck_click)
        self.buttonCancel.clicked.connect(self.cancel_click)
        self.actionOptions.triggered.connect(self.on_options_click)
        self.actionAbout.triggered.connect(self.on_about_click)
        self.menubar.addAction(self.actionOptions)
        self.menubar.addAction(self.actionAbout)
        self.win_menu = QtWidgets.QMenu()
        self.win_menu.setTitle("Окна")
        self.win_menu.addAction(self.main_win)
        self.main_win.triggered.connect(self.main_win_click)
        self.menubar.addMenu(self.win_menu)
        self.win_menu.addSeparator()
        self.separ = QtWidgets.QAction()
        self.separ.setSeparator(True)
        self.win_menu.addAction(self.separ)
        self.win_menu.addAction(self.actionCloseAll)
        self.actionCloseAll.triggered.connect(self.on_close_all)
        self.tableMods.cellClicked.connect(self.on_cell_click)
        self.tableMods.cellDoubleClicked.connect(self.on_dbclick)
            # Контекстное меню для таблицы
        self.tableMods.customContextMenuRequested.connect(self.copy_context_menu)
    # Задаем правую часть statusbar
            # Средняя скорость загрузки
        #self.status_widget3 = QtWidgets.QLabel()
        #self.status_widget3.setText('Ср. скорость - ?')
        #self.statusbar.addPermanentWidget(self.status_widget3, 0)
            # Кол-во модов для обновления
        self.status_widget4 = QtWidgets.QLabel()
        self.status_widget4.setText('Модов для загрузки - ?')
        self.statusbar.addPermanentWidget(self.status_widget4, 0)
            # Размер загрузки для обновления модов
        self.status_widget5 = QtWidgets.QLabel()
        self.status_widget5.setText('Размер загрузки ~ ?')
        self.statusbar.addPermanentWidget(self.status_widget5, 0)
            # Картинка status_buttonIcon
        self.status_buttonIcon = QtWidgets.QPushButton()
        self.status_buttonIcon.setGeometry(QtCore.QRect(0, 0, 15, 15))
        self.status_buttonIcon.setFlat(1)
        self.set_status_buttonIcon()  # Устанавливаем статус icon button
        self.status_buttonIcon.setIconSize(QtCore.QSize(15, 15))
        self.statusbar.addPermanentWidget(self.status_buttonIcon, 0)
        #self.status_buttonIcon.clicked.connect(self.show_run_thread)
        self.mods_table_create()  # Заполняем таблицу
        self.tableMods.setColumnWidth(0, 20)
        self.tableMods.setColumnWidth(5, 55)

    # Заполнение таблицы tableWidget (читаем моды, считаем рамер)
    def mods_table_create(self):
        global prog_state, list_mod
        prog_state = 'OK'
        self.set_status_buttonIcon()
        kolMod = 0  # Кол-во модов
        sizeMod = 0  # Общий размер модов
            # Очистка таблицы tableMods
        while self.tableMods.rowCount() > 0:
            self.tableMods.removeRow(0)
        get_instlled_mod()
        for inf_mod in list_mod:
            self.tableMods.insertRow(kolMod)  # Добавляем строку в таблицу
            self.write_my_table(kolMod, col_NAME, inf_mod[1], 'left')
            self.write_my_table(kolMod, col_ID, inf_mod[0], 'center')
            self.write_my_table(kolMod, col_SIZE, locale.format('%.2f', float(inf_mod[2] / 1024), grouping=True),
                                'right')
            self.write_my_table(kolMod, col_DATE, inf_mod[3].strftime("%d.%m.%y"), 'center')
            # Устанавливаем checkbox в col_STATE
            checkitem = QtWidgets.QTableWidgetItem()
            checkitem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
            checkitem.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            checkitem.setCheckState(QtCore.Qt.Unchecked)
            self.tableMods.setItem(kolMod, col_STATE, checkitem)
            # Пишем остальные столбы пустыми
            self.write_my_table(kolMod, col_CHECK, '', 'center')
            self.write_my_table(kolMod, col_NEWDATE, '', 'center')
            self.write_my_table(kolMod, col_NEWSIZE, '', 'right')
            sizeMod += inf_mod[2]
            kolMod += 1
                # Изменение размеров строк и столбцов
        self.tableMods.resizeColumnsToContents()
        self.tableMods.resizeRowsToContents()
        self.tableMods.setColumnWidth(0, 20)
        table_width = self.get_width_table()
        win_height = self.height()
        self.resize(table_width, win_height)
                # Изменяем statusbar
        self.status_widget1.setText('Кол-во модов - ' + str(kolMod))
        my_status = 'Размер модов - ' + locale.format('%.2f', sizeMod / 1048576, grouping=True) + ' Мб'
        self.status_widget2.setText(my_status)

    # Запись данных в ячеку таблицы (строка, столбец, текст, выравнивание)
    def write_my_table(self, x, y, table_txt, table_align):
        my_item = QtWidgets.QTableWidgetItem()
        my_item.setText(table_txt)
        my_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
        if table_align == 'right':
            my_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        elif table_align == 'center':
            my_item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            my_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        if table_txt == 'OK':
                my_brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
                my_brush.setStyle(QtCore.Qt.SolidPattern)
                my_item.setBackground(my_brush)
        elif table_txt == 'OUT':
                my_brush = QtGui.QBrush(QtGui.QColor(255, 255, 0))
                my_brush.setStyle(QtCore.Qt.SolidPattern)
                my_item.setBackground(my_brush)
        elif table_txt == 'ERROR':
                my_brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
                my_brush.setStyle(QtCore.Qt.SolidPattern)
                my_item.setBackground(my_brush)
        elif table_txt == 'CANCEL':
            my_brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
            my_brush.setStyle(QtCore.Qt.SolidPattern)
            my_item.setBackground(my_brush)
        self.tableMods.setItem(x, y, my_item)
        self.tableMods.repaint()

    # Кнопка выделить все
    def check_uncheck_click(self):
        check_icon = QtGui.QIcon()
        if self.buttonCheck.isChecked():
            for i in range(self.tableMods.rowCount()):
                self.tableMods.item(i, col_STATE).setCheckState(QtCore.Qt.Checked)
            check_icon.addPixmap(QtGui.QPixmap("icon/uncheck.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.buttonCheck.setIcon(check_icon)
            self.buttonCheck.setStatusTip("Снять выделения")
        else:
            for i in range(self.tableMods.rowCount()):
                self.tableMods.item(i, col_STATE).setCheckState(QtCore.Qt.Unchecked)
            check_icon.addPixmap(QtGui.QPixmap("icon/checkall.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.buttonCheck.setIcon(check_icon)
            self.buttonCheck.setStatusTip("Выбрать все")
        self.summa()

    # Подсчитываем кол-во и размер выбранных модов
    def summa(self):
        kolModDownload = 0
        sizeModDownload = 0
        for i in range(self.tableMods.rowCount()):
            if self.tableMods.item(i, col_STATE).checkState() == QtCore.Qt.Checked:
                kolModDownload += 1
                try:
                    newSize = self.tableMods.item(i, col_NEWSIZE).text()
                except AttributeError:
                    newSize = 0
                else:
                    razryd = newSize[-2:]
                    if razryd == 'KB':
                        newSize = float(newSize[:-3])
                    elif razryd == 'MB':
                        newSize = float(newSize[:-3]) * 1024
                    else:
                        newSize = 0
                sizeModDownload += newSize
        self.status_widget4.setText('Модов для загрузки - ' + str(kolModDownload))
        my_summ_size = 'Размер загрузки ~' + locale.format('%.2f', sizeModDownload / 1024, grouping=True) + ' Мб'
        self.status_widget5.setText(my_summ_size)

    # При выборе мода (столбец 0)
    def on_cell_click(self, row, col):
        if col == 0:
            self.summa()

    # Двойной щелчок по строке таблицы
    def on_dbclick(self, row, col):
        if col != 0:
            mod_id = self.tableMods.item(row, col_ID).text()
            mod_name = self.tableMods.item(row, col_NAME).text()
            self.show_mod(mod_id, mod_name)

    # Показываем окно мода с инфой
    def show_mod(self, mod_id, mod_name):
        global show_win, load_inf, param, thread_is_run, list_mod, load_mod_win
        mod_id = mod_id
        thread_is_run = True
        if mod_id in show_win:
            show_win[mod_id].activateWindow()
        else:
            if len(load_inf) < param['max_win']:
                show_win[mod_id] = (view_mod(self))
                show_win[mod_id].setID(mod_id, mod_name)
                show_win[mod_id].inf_load = True
                show_win[mod_id].act_win.setText(mod_name)
                self.win_menu.insertAction(self.separ, show_win[mod_id].act_win)
                if mod_id in load_mod_win:
                    show_win[mod_id].mod_load = True
                    show_win[mod_id].loadButton.setDisabled(True)
                load_inf[mod_id] = (threadShow(self))
                load_inf[mod_id].fin_thr.connect(self.info_mod_signal)
                load_inf[mod_id].mod_id = mod_id
                load_inf[mod_id].info = 'win'
                load_inf[mod_id].start()
                self.set_status_buttonIcon()
                show_win[mod_id].show()
            else:
                show_info_mes('warning', 'Предупреждение', 'Превышено количество окон', 'Закройте окно или увеличьте параметр', '')

    # Сюда будет возвращать сигнал от потока дата, инфо (Окно с инфой)
    def info_mod_signal(self, state, mod_id, mod_text, mod_size):
        global load_inf, show_win
        if mod_id in show_win:
            show_win[mod_id].inf_load = False
            if not show_win[mod_id].mod_load:
                show_win[mod_id].loadButton.setEnabled(True)
                show_win[mod_id].progressBar.setMinimum(100)
                show_win[mod_id].progressBar.setMaximum(100)
                show_win[mod_id].progressBar.setValue(100)
            if state == 'OK':
                # Выводим инфу
                show_win[mod_id].sizeLabel.setText("Размер мода - " + mod_size)
                show_win[mod_id].textEdit.setHtml(str(mod_text))
            else:
                # Выводим ошибку
                show_win[mod_id].sizeLabel.setText("Ошибка")
                mod_text = '<html><span style=" font-size:18pt;">Ошибка при получении данных!</span></p></body></html>'
                show_win[mod_id].textEdit.setHtml(str(mod_text))
                show_win[mod_id].loadButton.setDisabled(True)
        # Освобождаем таблицу потоков для Инфы
        if mod_id in load_inf:
            del load_inf[mod_id]
        self.set_status_buttonIcon()

    # Запуск потока для загрузки из окна
    def start_load_win(self, mod_id, filename):
        global load_mod_win, thread_is_run
        thread_is_run = True
        load_mod_win[mod_id] = (threadDownLoad(self))
        load_mod_win[mod_id].load_thr.connect(self.load_mod_signal)
        load_mod_win[mod_id].size_load_thr.connect(self.refresh_win_progressBar)
        load_mod_win[mod_id].mod_id = mod_id
        load_mod_win[mod_id].mod_name = filename
        load_mod_win[mod_id].info = 'loa'
        load_mod_win[mod_id].start()
        self.set_status_buttonIcon()

    # Окончание загрузки из окна
    def load_mod_signal(self, state, mod_id, load_size, mod_name):
        global load_mod_win, show_win
        if state == 'OK':
            detailedtext = (mod_name+'\nРазмер файла: '+locale.format('%.2f', float(load_size)/1024, grouping=True)+' Кбайт')
            show_info_mes('info', "OK", "Файл " + mod_name, "сохранен", detailedtext)
        elif state == 'ERROR':
            show_info_mes('error',  "Ошибка", "Ошибка загрузки файла", mod_name, "")
        elif state == 'CANCEL':
            show_info_mes('error', "Отмена", "Загрузка файла " + mod_name, "отменена", "")
        del load_mod_win[mod_id]
        self.set_status_buttonIcon()
        if mod_id in show_win:
            show_win[mod_id].mod_load = False
            show_win[mod_id].loadButton.setEnabled(True)
            show_win[mod_id].progressBar.setMinimum(100)
            show_win[mod_id].progressBar.setMaximum(100)
            show_win[mod_id].progressBar.setValue(100)

    # Обновление progressBar в инфо окне
    def refresh_win_progressBar(self, mod_id, l_size, tr_size):
        global show_win
        if mod_id in show_win:
            show_win[mod_id].progressBar.setValue(l_size)
            show_win[mod_id].progressBar.setMaximum(tr_size)

    # Кнопка Загрузить
    def on_load_all_click(self):
        global thread_is_run, prog_state, list_mod_load, last_tread_col, count_mod_load, size_mod_load
        list_mod_load = []
        # Получаем список файлов для загрузки
        for i in range(self.tableMods.rowCount()):
            if self.tableMods.item(i, col_STATE).checkState() == QtCore.Qt.Checked:
                mod_id = self.tableMods.item(i, col_ID).text()
                list_mod_load.append(mod_id)
        if len(list_mod_load) != 0:
            self.summa()
            prog_state = 'LOAD'
            last_tread_col = 0
            count_mod_load = 0
            size_mod_load = 0
            self.set_status_buttonIcon()
            self.buttonCheckDate.setDisabled(True)
            self.buttonLoadAll.setDisabled(True)
            self.actionOptions.setDisabled(True)
            thread_is_run = True
            self.load_all_mod_signal('LOAD', '', '', '')

    # Сюда будем возвращаться от потока загрузки
    def load_all_mod_signal(self, state, mod_id, load_size, mod_name):
        global prog_state, last_tread_col, load_mod, list_mod_load, param
        if state == 'OK' or state == 'ERROR' or state == 'CANCEL':
            # Какой-то поток выполнился, файл загружен
            self.finish_load_thread(state, mod_id, load_size)
            # Освобождаем таблицу потоков для Проверки
            del load_mod[mod_id]
            self.set_status_buttonIcon()
        if prog_state != 'CANCEL':
            len_list = len(list_mod_load)
            len_load_ref = len(load_mod)
            # Если не достигли конца списка и макс. кол-ва загрузок
            while last_tread_col < len_list and len_load_ref < param['max_load']:
                mod_id = list_mod_load[last_tread_col]
                load_mod[mod_id] = (threadDownLoad(self))
                load_mod[mod_id].load_thr.connect(self.load_all_mod_signal)
                load_mod[mod_id].size_load_thr.connect(self.refresh_progressBar)
                load_mod[mod_id].mod_id = mod_id
                load_mod[mod_id].info = 'ref'
                load_mod[mod_id].start()
                len_load_ref = len(load_mod)
                # Действия при запуске потока
                self.start_thread(mod_id)
                self.set_status_buttonIcon()
                last_tread_col += 1
                # Проверка завершена или отменена
        if len(load_mod) == 0:
            self.finish_load()

    # Действия при завершении потока (Загрузка - основное окно)
    def finish_load_thread(self, state, mod_id, load_size):
        global prog_state, count_mod_load, size_mod_load, load_mod
        row_id = self.find_row_id(mod_id)
        self.tableMods.removeCellWidget(row_id, col_CHECK)  # отключаем полосу
        self.tableMods.item(row_id, col_STATE).setCheckState(QtCore.Qt.Unchecked)
        if state == 'OK':
            count_mod_load += 1
            size_mod_load += load_size
        elif state == 'ERROR':
            prog_state = 'ERROR'
        elif state == 'CANCEL':
            prog_state = 'CANCEL'
        self.write_my_table(row_id, col_CHECK, prog_state, 'center')

    # Действия при окончании загрузки (основное окно)
    def finish_load(self):
        global prog_state, count_mod_load, size_mod_load, list_mod_load
        if prog_state == 'LOAD':
            prog_state = 'OK'
            infotext = "Все OK"
        elif prog_state == 'CANCEL':
            infotext = 'Загрузка отменена'
        else:
            infotext = "Были ошибки."
        detailedtext = 'Количество: ' + str(count_mod_load)+'/'+str(len(list_mod_load))
        detailedtext += '\nРазмер: '+locale.format('%.2f', size_mod_load/1024, grouping=True)+' Кб'
        show_info_mes('info', "Сохранено", "Моды загружены", infotext, detailedtext)
        self.status_widget4.setText('Кол-во скаченных модов - '+str(count_mod_load)+'/'+str(len(list_mod_load)))
        my_summ_size = 'Размер записанных модов - '+locale.format('%.2f', size_mod_load/1048576, grouping=True)+' Мб'
        self.status_widget5.setText(my_summ_size)
        self.buttonCheckDate.setEnabled(True)
        self.buttonLoadAll.setEnabled(True)
        self.actionOptions.setEnabled(True)
        self.tableMods.resizeColumnsToContents()
        self.tableMods.resizeRowsToContents()
        self.tableMods.setColumnWidth(0, 20)
        self.set_status_buttonIcon()

    # Обновление progressBar в основном окне (по сигналу от потока)
    def refresh_progressBar(self, mod_id, l_size, tr_size):
        row_id = self.find_row_id(mod_id)
        progress_bar = self.tableMods.cellWidget(row_id, col_CHECK)
        progress_bar.setValue(l_size)
        progress_bar.setMaximum(tr_size)

    # Кнопка Проверить
    def on_verify_click(self):
        global prog_state, last_tread_col, thread_is_run
        last_tread_col = 0
        prog_state = 'CHECK'
        self.set_status_buttonIcon()
        self.buttonCheckDate.setDisabled(True)
        self.buttonLoadAll.setDisabled(True)
        self.actionOptions.setDisabled(True)
        thread_is_run = True
        self.verify_mod_signal('CHECK', '', '', '')

    # Сюда будет возвращаться сигнал от потока дата, размер (Проверка)
    def verify_mod_signal(self, state, mod_id, new_date, new_size):
        global prog_state, last_tread_col, list_mod, load_ver, param
        if state == 'OK' or state == 'ERROR' or state == 'CANCEL':
            # Какой-то поток выполнился, выводим результат
            self.finish_verify_thread(state, mod_id, new_date, new_size)
            # Освобождаем таблицу потоков для Проверки
            del load_ver[mod_id]
            self.set_status_buttonIcon()
            # Запускаем потоки для Проверки, если не отмена
        if prog_state != 'CANCEL':
            len_list = len(list_mod)
            len_load_ver = len(load_ver)
            # Если не достигли конца списка и макс. кол-ва загрузок
            while last_tread_col < len_list and len_load_ver < param['max_verify']:
                mod_id = list_mod[last_tread_col][0]
                load_ver[mod_id] = (threadShow(self))
                load_ver[mod_id].fin_thr.connect(self.verify_mod_signal)
                load_ver[mod_id].mod_id = mod_id
                load_ver[mod_id].info = 'ver'
                load_ver[mod_id].start()
                len_load_ver = len(load_ver)
                # Действия при запуске потока
                self.start_thread(mod_id)
                self.set_status_buttonIcon()
                last_tread_col += 1
            # Проверка завершена или отменена
        if len(load_ver) == 0:
            self.finish_verify()

    # Дествия при завершении потока (Проверка)
    def finish_verify_thread(self, state, mod_id, new_date, new_size):
        global prog_state
        row_id = self.find_row_id(mod_id)
        self.tableMods.removeCellWidget(row_id, col_CHECK)  # отключаем полосу
        if state == 'OK':   # выводим размер, выводим и сравниваем даты
            newdate = parse(new_date)
            newdate = newdate.replace(tzinfo=None)
            self.write_my_table(row_id, col_NEWSIZE, new_size, 'right')
            # Пишем новую дату в таблицу
            self.write_my_table(row_id, col_NEWDATE, newdate.strftime("%d.%m.%y"), 'center')
            olddate = datetime.datetime.strptime(self.tableMods.item(row_id, col_DATE).text(), "%d.%m.%y")
            if newdate > olddate:
                if prog_state != 'ERROR' and prog_state != 'CANCEL':
                    prog_state = 'OUT'
                    state = 'OUT'
                self.tableMods.item(row_id, col_STATE).setCheckState(QtCore.Qt.Checked)
            else:
                self.tableMods.item(row_id, col_STATE).setCheckState(QtCore.Qt.Unchecked)
            self.summa()
        elif state == 'ERROR':
            prog_state = 'ERROR'
        elif state == 'CANCEL':
            prog_state = 'CANCEL'
        # Пишем результат проверки в таблицу
        self.write_my_table(row_id, col_CHECK, state, 'center')

    # Действия при запуске потока (Проверка - Загрузка)
    def start_thread(self, mod_id):
        # Устанавливаем прогресс бар
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(0)
        progress_bar.setValue(0)
        row_id = self.find_row_id(mod_id)
        self.tableMods.setCellWidget(row_id, col_CHECK, progress_bar)

    # Действия при окончании проверки (Проверка)
    def finish_verify(self):
        self.buttonCheckDate.setEnabled(True)
        self.buttonLoadAll.setEnabled(True)
        self.actionOptions.setEnabled(True)
        self.tableMods.resizeColumnsToContents()
        self.tableMods.resizeRowsToContents()
        self.tableMods.setColumnWidth(0, 20)
        self.tableMods.setColumnWidth(5, 55)
        self.set_status_buttonIcon()
        self.summa()

    # Ищем строку в таблице по ID вход - ID, возвращаем - row (номер строки)
    def find_row_id(self, mod_id):
        row_id = self.tableMods.findItems(mod_id, QtCore.Qt.MatchContains)
        row_id = self.tableMods.row(row_id[0])
        return row_id

    # Кнопка Отмена
    @staticmethod
    def cancel_click():
        global thread_is_run
        thread_is_run = False

    # Меню Настройки
    def on_options_click(self):
        global param
        if not self.configWin:
            self.configWin = DialogOptions(self)
        self.configWin.textEdit.setText(param['pathMods'])
        self.configWin.textEdit_2.setText(param['pathLoad'])
        self.configWin.lineEdit.setText(str(param['max_size']))
        self.configWin.lineEdit_2.setText(str(param['chunk']))
        self.configWin.lineEdit_3.setText(str(param['max_load']))
        self.configWin.lineEdit_4.setText(str(param['max_verify']))
        self.configWin.lineEdit_5.setText(str(param['max_win']))
        self.configWin.lineEdit_6.setText(str(param['max_win_load']))
        self.configWin.show()

    # Меню О программе
    def on_about_click(self):
        if not self.aboutWin:
            self.aboutWin = AboutDialog(self)
        self.aboutWin.about_pict = random.randint(0, self.aboutWin.background_count-1)
        self.aboutWin.set_about_pict()
        self.aboutWin.show()

    # Меню Окна - Закрыть все окна
    @staticmethod
    def on_close_all():
        global show_win
        for open_win in list(show_win.values()):
            open_win.close()

    # Меню Окна - Главное окно
    def main_win_click(self):
        self.activateWindow()

    # Устанавливаем значение status_buttonIcon
    def set_status_buttonIcon(self):
        text_tooltip = ''
        global prog_state
        if prog_state == 'ERROR':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/error.png")))
            text_tooltip = "Обнаружены ошибки!"
        elif prog_state == 'OUT':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/out.png")))
            text_tooltip = "Есть обновления"
        elif prog_state == 'OK':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/ok.png")))
            text_tooltip = "Все OK"
        elif prog_state == 'LOAD':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/loading.png")))
        elif prog_state == 'CHECK':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/loading.png")))
        elif prog_state == 'CANCEL':
            self.status_buttonIcon.setIcon(QtGui.QIcon(QtGui.QPixmap("icon/error.png")))
            text_tooltip = "Операция отменена"
        text_run_thread = self.get_run_thread()
        self.status_buttonIcon.setToolTip(text_tooltip + '\n' + text_run_thread)
        self.status_buttonIcon.repaint()

    # Контестное меню для таблицы
    def copy_context_menu(self, pos):
        cmenu = QtWidgets.QMenu(self)
        cmenu.addAction(self.actionID)
        cmenu.addAction(self.actionName)
        cmenu.addAction(self.actionListOut)
        cmenu.addAction(self.actionInfo)
        action_copy = cmenu.exec_(self.tableMods.mapToGlobal(pos))
        if action_copy == self.actionID:
            row_cell = self.tableMods.currentRow()
            copy = str(self.tableMods.item(row_cell, col_ID).text())
            QtWidgets.QApplication.clipboard().setText(copy)
        elif action_copy == self.actionName:
            row_cell = self.tableMods.currentRow(self)
            copy = str(self.tableMods.item(row_cell, col_NAME).text())
            QtWidgets.QApplication.clipboard().setText(copy)
        elif action_copy == self.actionInfo:
            row_cell = self.tableMods.currentRow()
            mod_id = self.tableMods.item(row_cell, col_ID).text()
            mod_name = self.tableMods.item(row_cell, col_NAME).text()
            self.show_mod(mod_id, mod_name)
        elif action_copy == self.actionListOut:
            copy = ''
            for i in range(self.tableMods.rowCount()):
                if self.tableMods.item(i, col_CHECK).text() == 'OUT':
                    copy += str(self.tableMods.item(i, col_ID).text()) + ' ' + str(self.tableMods.item(i, col_NAME).text()) + '\n'
            QtWidgets.QApplication.clipboard().setText(copy)

    # Получение ширины таблицы
    def get_width_table(self):
        width = self.tableMods.horizontalHeader().length()
        width += self.tableMods.verticalHeader().width()
        margins = self.tableMods.contentsMargins()
        width += margins.left() + margins.right() + 45
        return width

    # При закрытии главного окна
    def closeEvent(self, evnt):
        global show_win, load_inf, load_ver, load_mod, load_mod_win
        if show_win or load_inf or load_ver or load_mod or load_mod_win:
            dettext_mes = self.get_run_thread()
            my_msg = QtWidgets.QMessageBox()
            my_msg.setIcon(QtWidgets.QMessageBox.Warning)
            my_msg.setText('Есть неоконченные задания')
            my_msg.setInformativeText('При закрытии все данные будут утеряны. Вы уверены?')
            my_msg.setDetailedText(dettext_mes)
            my_msg.setWindowTitle('Предупреждение')
            my_msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if my_msg.exec() == QtWidgets.QMessageBox.Yes:
                for open_win in list(show_win.values()):
                    open_win.close()
                if show_win:
                    show_info_mes('ERROR', 'Ошибка', 'Невозможно закрыть окна!!', 'Попробуйтие закрыть их из программы', '')
                else:
                    evnt.accept()
            else:
                evnt.ignore()
        else:
            evnt.accept()

    # Получаем список открытых потоков
    @staticmethod
    def get_run_thread():
        global show_win, load_inf, load_ver, load_mod, load_mod_win, count_mod_load, list_mod_load
        dettext_mes = ''
        if show_win:
            dettext_mes += 'Открыты окна:\n'
            for open_win in list(show_win.keys()):
                dettext_mes += open_win + '\n'
        if load_inf:
            dettext_mes += 'Грузиться информация:\n'
            for open_win in list(load_inf.keys()):
                dettext_mes += open_win + '\n'
        if load_ver:
            dettext_mes += 'Идет проверка\n'
        if load_mod:
            dettext_mes += 'Идет загрузка (главное окно) '
            dettext_mes += str(count_mod_load) + '/' + str(len(list_mod_load)) + '\n'
        if load_mod_win:
            dettext_mes += 'Идет загрузка:\n'
            for open_win in list(load_mod_win.keys()):
                dettext_mes += open_win + '\n'
        return dettext_mes

# Запускаем окно программы
def main():
    global window
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')
    window = usmApp()  # Создаём объект класса usmApp
    window.show()      # Показываем окно
    app.exec_()        # и запускаем приложение
    #sys.exit(app.exec_())


locale.setlocale(locale.LC_ALL, '')  # Локальные настройки для разделителя разрядов
# Читаем параметры программы (configUSM)
if not os.path.exists(configUSM):
    with open(configUSM, "w") as file:
        file.writelines("pathMods = /Documents/Paradox Interactive/Stellaris\n")
        file.writelines("pathDownload = Downloads\n")
        file.writelines("max_size = 2097152\n")
        file.writelines("chunk = 2048\n")
        file.writelines('max_load = 2\n')
        file.writelines("max_verify = 3\n")
        file.writelines("max_win = 4\n")
        file.writelines("max_win_load = 5")
else:
    for line in open(configUSM, "r"):
        line = line.split("\n")
        line = line[0]
        line = line.split('=')
        p = line[0].strip()
        v = line[1].strip()
        if p == 'pathMods' or p == 'pathDownload':
            param[p] = v
        else:
            param[p] = int(v)
# Читаем словарь mod_id_http (modid_ini)
if not os.path.exists(modid_ini):
    with open(modid_ini, "w") as file:
        file.write("")
else:
    for line in open(modid_ini, 'r'):
        line = line.split('\n')
        line = line[0]
        line = line.split('=')
        modID = line[0].strip()
        line = line[1].split(',')
        httpSMODS = line[0].strip()
        httpMODSBASE = line[1].strip()
        mod_id_http[modID] = (httpSMODS, httpMODSBASE)
if __name__ == '__main__':
    main()
