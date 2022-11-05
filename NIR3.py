import sqlite3 as sq

'''Программа должна обеспечивать отображение, по выбору пользователя,
каждой из двух таблиц, содержащихся в БД, а также предложение завершить
программу'''
def otobr():
    tab_name = input('''В базе данных присутствуют 2 таблицы\n"vuzkart"-картотека с записями, содержащими сведения о вузах России.
"vuzstat"- таблица содержащая статистические данные по вузам.
Введите название таблицы, которую хотите отобразить: ''')
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
        print('В таблице присутствуют вузы со следующими профилями:', end='')
        [print(i[0], end=' ') for i in set(cur.execute('SELECT prof from vuzkart'))]
        spec = input('\nВведите профиль вуза: ')
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
преподавателей по наличию ученой степени (доктор наук, кандидат наук, без
степени). 
Таблица должна иметь столбцы: порядковый номер, наличие
ученой степени, количество преподавателей в вузах выбранного субъекта РФ
с данной ученой степенью, процент от общего количества преподавателей в
вузах выбранного субъекта РФ. Последняя строка – итоговая, со значениями:
в столбце «наличие ученой степени» - значение «Все», в столбце «количество
преподавателей» - общее количество преподавателей в вузах выбранного
субъекта РФ.'''
def vtor_punkt():
    with sq.connect('VUZ.sqlite') as con:
        input = ('Введите')
        cur = con.cursor()
        print('В таблице присутствуют следующие регионы: ')
        [print(i[0].strip(), end='  ') for i in set(cur.execute('SELECT region FROM vuzkart'))]
        regs = [i for i in set(cur.execute('SELECT region FROM vuzkart'))]
        '''reg = input('Введите интересующий Вас регион, если хотите выбрать все регионы, то введите: ')
        while reg not in:
            print('Пожалуйста, укажите корректное значение!')
            reg = input('Введите интересующий Вас регион, если хотите выбрать все регионы, то введите "*": ')'''
        print(regs)
vtor_punkt()

