import datetime  # Библиотека для работы с датой и временем
import os # Библиотека для работы с файловой системой
import matplotlib.pyplot as plt # Библиотека для визуализации

############################################################################################
################    Открытие файлов календаря           ####################################
#############################################################################################

# Основная папка для хранения календарей
directory = 'C:/Users\Ae Eau\Desktop\Все папки\Программирование и автоматизация\Анализ данных\Гугл календарь\Подсчет времени календаря\Calendars'

# Список имен файлов календарей
list_calendars = os.listdir(directory)
# Список имен календарей
list_name_of_calendars = []
# Список значений длительностей
list_calendars_duration = []

# Для каждого календаря из папки
for calendar in list_calendars:
    path_calendar = directory + '/' + calendar  # Путь к данному календарю
    name_of_calendar = calendar[:-4]  # Имя календаря без расширения файла
    list_name_of_calendars.append(name_of_calendar)  # Список имен календарей
    # Открываем календари по их пути в режиме чтения
    file_calendar = open(path_calendar, 'r', encoding='utf-8')
    file_calendar_content = file_calendar.read()  # Заносим содержимое календаря в память
    str_file_calendar_content = str(file_calendar_content)  # Приводим содержимое календаря к строке

    ############################################################################################
    ################    Фильтрация строк с датой          ######################################
    ############################################################################################

    list_simple_str = str_file_calendar_content.split('\n') # Разделяю исходную строку по символу переноса строки

    fragment1 = 'DTSTART:2022'  # Задаю фрагмент, по которому буду фильтровать строки
    fragment2 = 'DTEND:2022'  # Задаю фрагмент по которому буду фильтровать строки
    list_date = []  # Задаю пустой список для заполнения строками с датой
    for simple_str in list_simple_str: # Для каждой строки из списка строк
        if fragment1 in simple_str or fragment2 in simple_str: # Если она содержит дату начала или конца
            list_date.append(simple_str)  # Добавляю ее в список дат

    ############################################################################################
    ################    Преобразование формата даты и времени          #########################
    ################    Нахождение разницы дат                         #########################
    ################    Суммирование времени                            ########################
    ############################################################################################

    index1 = 0  # Задаю стартовый индекс элемента из списка дат
    sumtime = datetime.timedelta (0, 0, 0, 0, 0)  # Задаю стартовое значение для суммарного времени на календарь


    for date_ in list_date:  # Для каждой даты из списка дат
        if index1 % 2 == 0: # Если индекс четный
            str_date_start = list_date[index1]  # То это дата старта события

            # Вычисляем полное время старта события по индексам символов в строке и приводим к целому типу данных
            year_start = int(str_date_start[8] + str_date_start[9] + str_date_start[10] + str_date_start[11])  # Год
            month_start = int(str_date_start[12] + str_date_start[13]) # Месяц
            day_start = int(str_date_start[14] + str_date_start[15])  # День
            hour_start = int(str_date_start[17] + str_date_start[18])  # Час
            minute_start = int(str_date_start[19] + str_date_start[20])  # Минута

            #print(yearStart, monthStart, dayStart, hourStart, minStart)  # Проверяю, что дата старта вывелась верно
            date1 = datetime.datetime(year_start, month_start, day_start, hour_start, minute_start)  # Приводим дату старта к формату даты
            index1 += 1  # Переходим к следующему индексу
        else:
            str_date_end = list_date[index1] # Остальные строки - даты конца

            # Вычисляем полное время конца события по индексам (отличаются от предыдущего) символов в строке и приводим к целому
            year_end = int(str_date_end[6] + str_date_end[7] + str_date_end[8] + str_date_end[9]) # Год
            month_end = int(str_date_end[10] + str_date_end[11])  # Месяц
            day_end = int(str_date_end[12] + str_date_end[13])  # День
            hour_end = int(str_date_end[15] + str_date_end[16])  # Час
            minute_end = int(str_date_end[17] + str_date_end[18])  # Минута

            #print(yearEnd, monthEnd, dayEnd, hourEnd, minEnd)   # Проверяю, что дата конца вывелась верно
            date2 = datetime.datetime(year_end, month_end, day_end, hour_end, minute_end)  # Приводим дату конца к формату даты

            date_delta = date2 - date1  # Считаю продолжительность данного события
            #print(tdelta)  # Проверяю, что вывелась продолжительность события
            sumtime += date_delta # увеличиваю суммарное время на значение продолжительности события
            index1 += 1  # Переходим к следующему индексу

    list_calendars_duration.append(sumtime)  # Добавляем длительность календаря в список длительностей календарей
    print('Итого потрачено времени за 2022 год на', name_of_calendar, ':', sumtime)  # ВЫВОЖУ ИТОГОВОЕ СУММАРНОЕ ВРЕМЯ

############################################################################################
################    Визуализация данных                            #########################
############################################################################################

# Перевод длительностей в секунды

list_calendars_duration_seconds = []  # Задаем список длительностей в секундах

for duration in list_calendars_duration:  # Для каждой длительности из календаря
    duration_seconds = duration.total_seconds()  # Переводим длительность в секундах
    list_calendars_duration_seconds.append(duration_seconds)  # Добавляем длительности (сек) в список длительностей (сек)

# Визуализация

labels = list_name_of_calendars  # Названия участков диаграммы соответствуют названиям календарей
sizes = list_calendars_duration_seconds  # Размеры участков диаграммы соответствуют длительности календаря (сек)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

