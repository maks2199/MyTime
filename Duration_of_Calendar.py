import datetime  # Импорт библиотеки для работы с датой и временем

# Получаем входные данные в виде текста экспортированного календаря.
# TODO реализовать загрузку этого текста из имеющегося файла
File_Calendar = open(English2022.ics)
# Имена файлов:
# English2022.ics

CommonStartData = """


"""
############################################################################################
################    Фильтрация строк с датой          ######################################
############################################################################################

SeparatedStr = CommonStartData.split('\n') # Разделяю исходную строку на строки по переносу строки
print(SeparatedStr)  # Проверяю, что строки разделились верно

fragment1 = 'DTSTART:2022'  # Задаю фрагмент, по которому буду фильтровать строки
fragment2 = 'DTEND:2022'  # Задаю фрагмент по которому буду фильтровать строки
listDate = []  # Задаю пустой список для заполнения строками с датой
for SimpleStr in SeparatedStr: # Для каждой строки из списка
    if fragment1 in SimpleStr or fragment2 in SimpleStr: # Если она содержит дату начала или конца
        listDate.append(SimpleStr)  # Добавляю ее в список дат
print(listDate)  # Проверяю, что даты отфильтрвались верно

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
        print(strDateStart)  # Проверяем, что вывелась дата старта

        # Вычисляем полное время старта события по индексам симвлов в строке и приводим к целому
        yearStart = int(strDateStart[8] + strDateStart[9] + strDateStart[10] + strDateStart[11])  # Год
        monthStart = int(strDateStart[12] + strDateStart[13]) # Месяц
        dayStart = int(strDateStart[14] + strDateStart[15])  # День
        hourStart = int(strDateStart[17] + strDateStart[18])  # Час
        minStart = int(strDateStart[19] + strDateStart[20])  # Минута

        print(yearStart, monthStart, dayStart, hourStart, minStart)  # Проверяю, что дата старта вывелась верно
        dt1 = datetime.datetime(yearStart, monthStart, dayStart, hourStart, minStart)  # Приводим дату старта к формату даты
        index1 += 1  # Переходим к следующему индексу
    else:
        strDateEnd = listDate[index1] # Остальные строки - даты конца
        print(strDateEnd)  # Проверяем, что вывелась дата конца

        # Вычисляем полное время конца события по индексам (отличаются от предыдущего) символов в строке и приводим к целому
        yearEnd = int(strDateEnd[6] + strDateEnd[7] + strDateEnd[8] + strDateEnd[9]) # Год
        monthEnd = int(strDateEnd[10] + strDateEnd[11])  # Месяц
        dayEnd = int(strDateEnd[12] + strDateEnd[13])  # День
        hourEnd = int(strDateEnd[15] + strDateEnd[16])  # Час
        minEnd = int(strDateEnd[17] + strDateEnd[18])  # Минута

        print(yearEnd, monthEnd, dayEnd, hourEnd, minEnd)   # Проверяю, что дата конца вывелась верно
        dt2 = datetime.datetime(yearEnd, monthEnd, dayEnd, hourEnd, minEnd)  # Приводим дату конца к формату даты

        tdelta = dt2 - dt1  # Считаю продолжительность данного события
        print(tdelta)  # Проверяю, что вывелась продолжительность события
        sumtime += tdelta # увеличиваю суммарное время на значение продолжительности соыбтия
        index1 += 1  # Переходим к следующему индексу

print('Итого потрачено времени: ', sumtime)  # ВЫВОЖУ ИТОГОВОЕ СУММАРНОЕ ВРЕМЯ
# Конец программыЮ