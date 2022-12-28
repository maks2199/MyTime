import datetime  # Импорт библиотеки для работы с датой и временем
import os # Импорт библиотеки для работы с файловой системой
import matplotlib.pyplot as plt

# Основная папка
directory = 'C:/Users\Ae Eau\Desktop\Все папки\Программирование и автоматизация\Анализ данных\Гугл календарь\Подсчет времени календаря\Calendars'

# Список имен календарей
list_calendars = os.listdir(directory)
print(list_calendars)

list_name_of_calendars = []

# Список значений длительностей
list_calendars_duration = []

# Для каждого календаря из папки
for calendar in list_calendars:
    # Открываем входные данные файлов календарей
    path_calendar = directory + '/' + calendar
    name_of_calendar = calendar[:-4]
    list_name_of_calendars.append(name_of_calendar)

    print(list_calendars)
    #print (path_calendar)

    file_calendar = open(path_calendar, 'r', encoding='utf-8')
    file_calendar_content = file_calendar.read()

    #print(file_calendar_content)

    list_files = [] #

    str(file_calendar_content)

    CommonStartData = str(file_calendar_content)

    ############################################################################################
    ################    Фильтрация строк с датой          ######################################
    ############################################################################################

    SeparatedStr = CommonStartData.split('\n') # Разделяю исходную строку на строки по переносу строки
    #print(SeparatedStr)  # Проверяю, что строки разделились верно


    fragment1 = 'DTSTART:2022'  # Задаю фрагмент, по которому буду фильтровать строки
    fragment2 = 'DTEND:2022'  # Задаю фрагмент по которому буду фильтровать строки
    listDate = []  # Задаю пустой список для заполнения строками с датой
    for SimpleStr in SeparatedStr: # Для каждой строки из списка
        if fragment1 in SimpleStr or fragment2 in SimpleStr: # Если она содержит дату начала или конца
            listDate.append(SimpleStr)  # Добавляю ее в список дат
    #print(listDate)  # Проверяю, что даты отфильтрвались верно

    ############################################################################################
    ################    Преобразование формата даты и времени          #########################
    ################    Нахождение разницы дат                         #########################
    ################    Суммирование разниц                            #########################
    ############################################################################################

    index1 = 0  # Задаю стартовый индекс элемента из списка дат
    sumtime = datetime.timedelta (0, 0, 0, 0, 0)  # Задаю стартовое значение для суммарного времени на календарь


    for date_ in listDate:  # Для каждой даты из списка дат
        if index1 % 2 == 0: # Если индекс четный
            strDateStart = listDate[index1]  # То это дата старта события
            #print(strDateStart)  # Проверяем, что вывелась дата старта

            # Вычисляем полное время старта события по индексам симвлов в строке и приводим к целому
            yearStart = int(strDateStart[8] + strDateStart[9] + strDateStart[10] + strDateStart[11])  # Год
            monthStart = int(strDateStart[12] + strDateStart[13]) # Месяц
            dayStart = int(strDateStart[14] + strDateStart[15])  # День
            hourStart = int(strDateStart[17] + strDateStart[18])  # Час
            minStart = int(strDateStart[19] + strDateStart[20])  # Минута

            #print(yearStart, monthStart, dayStart, hourStart, minStart)  # Проверяю, что дата старта вывелась верно
            dt1 = datetime.datetime(yearStart, monthStart, dayStart, hourStart, minStart)  # Приводим дату старта к формату даты
            index1 += 1  # Переходим к следующему индексу
        else:
            strDateEnd = listDate[index1] # Остальные строки - даты конца
            #print(strDateEnd)  # Проверяем, что вывелась дата конца

            # Вычисляем полное время конца события по индексам (отличаются от предыдущего) символов в строке и приводим к целому
            yearEnd = int(strDateEnd[6] + strDateEnd[7] + strDateEnd[8] + strDateEnd[9]) # Год
            monthEnd = int(strDateEnd[10] + strDateEnd[11])  # Месяц
            dayEnd = int(strDateEnd[12] + strDateEnd[13])  # День
            hourEnd = int(strDateEnd[15] + strDateEnd[16])  # Час
            minEnd = int(strDateEnd[17] + strDateEnd[18])  # Минута

            #print(yearEnd, monthEnd, dayEnd, hourEnd, minEnd)   # Проверяю, что дата конца вывелась верно
            dt2 = datetime.datetime(yearEnd, monthEnd, dayEnd, hourEnd, minEnd)  # Приводим дату конца к формату даты

            tdelta = dt2 - dt1  # Считаю продолжительность данного события
            #print(tdelta)  # Проверяю, что вывелась продолжительность события
            # print(tdelta.total_seconds())
            # print(type(tdelta.total_seconds()))
            sumtime += tdelta # увеличиваю суммарное время на значение продолжительности соыбтия
            index1 += 1  # Переходим к следующему индексу
    list_calendars_duration.append(sumtime)
    print("sumtime: ",sumtime)
    print(list_calendars_duration)
    print('Итого потрачено времени: ', calendar, sumtime)  # ВЫВОЖУ ИТОГОВОЕ СУММАРНОЕ ВРЕМЯ

    ############################################################################################
    ################    Визуализация данный                            #########################
    ############################################################################################
list_calendars_duration_seconds = []

for duration in list_calendars_duration:
    duration_seconds = duration.total_seconds()
    list_calendars_duration_seconds.append(duration_seconds)
print(list_calendars_duration_seconds)

labels = list_name_of_calendars
print(len(labels))
sizes = list_calendars_duration_seconds
print(len(sizes))

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()

