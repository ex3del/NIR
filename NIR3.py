import sqlite3 as sq
import pandas as pd
from itertools import chain


'''Программа должна обеспечивать отображение, по выбору пользователя,
каждой из двух таблиц, содержащихся в БД, а также предложение завершить
программу'''


def otobr():
    tab_name = input('''\nВ базе данных присутствуют 2 таблицы\n"vuzkart"-картотека с записями, содержащими сведения о вузах России.
"vuzstat"- таблица содержащая статистические данные по вузам.
Введите имя таблицы, которую хотите отобразить: ''')
    while tab_name not in ['vuzkart', 'vuzstat']:
        print('\nТаблица не существует! Пожалуйста, повторите попытку.\n')
        tab_name = input('''В базе данных присутствуют 2 таблицы\n"vuzkart"-картотека с записями, содержащими сведения о вузах России.
"vuzstat"- таблица содержащая статистические данные по вузам.
Введите имя таблицы, которую хотите отобразить: ''')
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        tablica = cur.execute(f'SELECT rowid, * FROM {tab_name}')
        [print(*i[1:]) for i in tablica]


'''Обеспечить выбор из списка профиля вуза, интересующего пользователя.

Обеспечить выбор порогового значения отношения числа студентов к числу
преподавателей в вузе, интересующего пользователя (при этом должны быть
подсказки по мин и макс значениям этой величины). 

Составить и отобразить на экране перечень полных наименований вузов, соответствующих
выбранному профилю и имеющих значение указанного отношения ниже
порога.'''


def perv_punkt():
    with sq.connect('VUZ.sqlite') as con:
        cur = con.cursor()
        print('\nВ таблице присутствуют вузы со следующими профилями:', end='')
        [print(i[0], end=' ') for i in set(cur.execute('SELECT prof from vuzkart'))]
        spec = input('\nВведите профиль вуза: ')
        while spec not in ['ИТ', 'КЛ', 'МП', 'ГП']:
            print('\nНесуществующий профиль! Пожалуйста, попробуйте  еще раз!\n')
            spec = input('Введите профиль вуза: ')
        vuz_id = list(cur.execute(f'SELECT codvuz FROM vuzkart WHERE prof == "{spec}"'))
        vuz_id = tuple(j for i in vuz_id for j in i if j)
        data = [list(cur.execute(f'SELECT pps, stud from vuzstat WHERE codvuz == "{id}"')) for id in vuz_id]
        data = sorted([j for i in data for j in i], key=lambda x: float(x[1]) / float(x[0]))
        max, min = round(float(data[-1][-1]) / float(data[-1][0]), 2), round(float(data[0][-1]) / float(data[0][0]), 2)
        print(f'''Максимальное соотношение студентов к преподавателям: {max}\nМинимальное соотношение студентов к преподавателям: {min} ''')
        porog = float(input(f'Введите число-соотношение студентов к преподавателям в пределах ({min}, {max}): '))
        while porog <= min or porog >= max:
            print('Пожалуйста, перепроверьте диапазон!')
            porog = float(input(f'Введите число-соотношение студентов к преподавателям в пределах ({min}, {max}): '))
        fin_id = tuple(j for i in list(cur.execute(f'SELECT codvuz FROM vuzstat WHERE stud / pps <= {porog} ')) for j in i)
        vivod = list(cur.execute(f'SELECT z1 FROM vuzkart WHERE codvuz IN {fin_id}'))
        print(f'\nСписок {spec} вузов, где соотношение студентов к преподавателям не больше {porog}:\n')
        [print(*i) for i in vivod]


'''Обеспечить возможность пользователю выбрать из списка субъект РФ или
значение «Все». 
Для выбранного субъекта РФ рассчитать и представить в
виде таблицы распределение работающих в вузах данного субъекта РФ
преподавателей по наличию ученой степени (доктор наук, кандидат наук, без степени). 
Таблица должна иметь столбцы: 
порядковый номер
кол-во преподавателей с ученой степенью 
количество преподавателей в вузах выбранного субъекта РФ с данными учеными степенями
процент от общего количества преподавателей в вузах выбранного субъекта РФ. 
Последняя строка – итоговая, со значениями:
в столбце «наличие ученой степени» - значение «Все», в столбце «количество
преподавателей» - общее количество преподавателей в вузах выбранного
субъекта РФ.'''


def vtor_punkt():
    with sq.connect('VUZ.sqlite') as con:
        def tabl(ids):
            profes = [[j[0] for j in cur.execute(f'SELECT pr FROM vuzstat WHERE codvuz == "{i}"')][0] for i in ids]
            docent = [[j[0] for j in cur.execute(f'SELECT dc FROM vuzstat WHERE codvuz == "{i}"')][0] for i in ids]
            doct = [[j[0] for j in cur.execute(f'SELECT dn FROM vuzstat WHERE codvuz == "{i}"')][0] for i in ids]
            ktn = [[j[0] for j in cur.execute(f'SELECT kn FROM vuzstat WHERE codvuz == "{i}"')][0] for i in ids]
            pps = sum(profes) + sum(doct) + sum(docent) + sum(ktn)
            def toFixed(numObj, digits=0):
                return f"{numObj:.{digits}f}"

            dic_tab["Кол-во преподавателей"].extend([sum(profes), sum(doct), sum(ktn), sum(docent), pps])
            prcnt = [toFixed((int(i) / pps) * 100, 3) for i in dic_tab["Кол-во преподавателей"]]
            dic_tab['Процент от общего кол-ва препод-ей'].extend(prcnt)
            dic_tab['Порядковый номер'].extend(list(range(1, len(dic_tab['Наличие уч. степени']) + 1)))
            print()
            print(pd.DataFrame(dic_tab).to_markdown(index=False))

        cur = con.cursor()
        print('\nВ таблице присутствуют следующие регионы: ')
        [print(i[0].strip(), end='  ') for i in set(cur.execute('SELECT region FROM vuzkart'))]
        reg = input('\n\nВведите интересующий Вас регион, если хотите выбрать все регионы, то введите "Всего": ')
        dic_reg = dict(zip([i[0].strip() for i in set(cur.execute('SELECT region FROM vuzkart'))] + ["Всего"],
                       [i[0] for i in set(cur.execute('SELECT region FROM vuzkart'))] + ["Всего"]))
        dic_tab = {'Порядковый номер': [],
                   'Наличие уч. степени': ['Профессора', 'Доктора наук', 'Кандидаты Наук', 'Без уч. степени', 'Все'],
                   'Кол-во преподавателей': [],
                   'Процент от общего кол-ва препод-ей': []}
        while reg not in dic_reg.keys():
            print('Пожалуйста, укажите корректное значение!')
            reg = input(r'Введите интересующий Вас регион, если хотите выбрать все регионы, то введите "Всего": ')
        if reg == "Всего":
            regs = list(dic_reg.keys())
            id_s = [[i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE region =="{dic_reg[j]}"')] for j in regs][: -1]
            id_s = list(chain.from_iterable(id_s))
            tabl(id_s)
        else:
            id_s = [i[0] for i in cur.execute(f'SELECT codvuz FROM vuzkart WHERE region == "{dic_reg[reg]}"')]
            tabl(id_s)


def vizov(func):
    return {'1': otobr, '2': perv_punkt, '3': vtor_punkt}.get(func)


print('Добро пожаловать в программу!')
while True:
    oper = input('''\nВам доступны следующие операции: 
1) Вывести интересующую таблицу на экран
2) Вузы, выбранного профиля, с заданным порогом студент/преподаватель
3) Информация о преподавательском составе по региону/регионам
4) Завершение программы
Пожалуйста, введите номер операции, которую хотите выполнить: ''')
    while oper not in ['1', '2', '3', '4']:
        print('\nТакой операции не существует! Пожалуйста, повторите попытку.\n')
        oper = input('''\nВам доступны следующие операции: 
1) Вывести интересующую таблицу на экран
2) Вузы, выбранного профиля, с заданным порогом студент/преподаватель
3) Информация о преподавательском составе по региону/регионам
4) Завершение программы
Пожалуйста, введите номер операции, которую хотите выполнить: ''')
    if oper == '4':
        exit(print("Всего доброго!"))
    else:
        vizov(oper)()
