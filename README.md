# Update-Stellaris-Mod
Update Stellaris Mod from stellaris.smods.ru

This program reads the installed mods for Stellaris and checks their updates on the website http://stellaris.smods.ru/.

The verification is done by comparing the date of the mod file with the Last revision on the site.
You can download multiple files at once. See the Settings menu.

If you want to see information about the selected fashion.
Used multi-upload files, see Settings.
Sorry, only on Russian language.

Эта программа считывает установленные моды для Stellaris и проверяет их обновления на сайте http://stellaris.smods.ru/.

Проверка осуществляется путем сравнения даты файла mod с Last revision на сайте.
Можно загружать сразу несколько файлов. Смотри меню Настройки.

При желании посмотреть информацию о выбранном моде.

Справка:
Если моды не отображаются установите путь. Меню Настройки или файл "umgui.ini" pathMods.
В Windows, обычно, путь к модам - /Users/Имя пользователя/Documents/Paradox Interactive/Stellaris.
 
При ошибках загрузки, отображения модов удалите файл modid.ini. После удаления и перезапуска файл будет создан заново.
Формат файла id мода = http-адрес к stellaris.smods.ru, http-адрес к modsbase.com.
 
Информаци о моде  - двойной щелчок мыши и правая кнопка на таблице модов.
Значок в строке состояния показывает список открытых потоков и окон.
Используется мультизагрузка файлов, смотри Настройки.
Извините, пока только на русском языке.
P.S. Фон в "О Программе" меняются автоматически и по щелчку на картинке.

Python 3.6.5
with the module:
PyQt 5.10.1
BeautifulSoup 4
dateutil 2.7.3
requests 2.18.4

Qt Designer v 5.9.1
Notepad++ v 7.5.6.
