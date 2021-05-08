# -*- coding: utf-8 -*-
"""
fio - Отдельный модуль для работы с файлами конструкций
"""
import sys
from .structure import Force, LineStructure
from .structure import Spring
from .structure import Node


def save_model(line_struct: LineStructure, file_name, comment=''):
    """Сохранить модель конструкции"""
    # Открываем файл на запись
    file = open(file_name, 'w', encoding='utf8')
    # Переопределяем стандартный вывод
    sys.stdout = file

    # Выводи комментарий к модели, если он существует
    if comment:
        print(f'# {comment}')

    # Выводим описание файла
    print("# Файл представляет собой модель конструкции из КЭ\n")

    # Первым блоком будет блок описания узлов
    # Заголовок блока
    print("Nodes:")
    # Обходим все узлы в конструкции
    for i, node in enumerate(line_struct.grid):
        # Выводим индекс узла и его расположение в глобальной СК
        print(f'\t{i+1} {node.x:.2f} {node.y:.2f}')

    # Дальше идёт описание конечных элементов
    # Заголовок блока
    print("\nElements:")
    # Проходим все конечные элементы
    for i, el in enumerate(line_struct.items):
        # Получаем индексы улов текущего элемента
        N1 = el.n1.pos
        N2 = el.n2.pos
        # В зависимости от вида КЭ у него могут быть разные параметры
        # Только C в случае пружинки и EF в случае стержня
        # Строка параметров элемента
        param = ''
        # Если это пружинка
        if isinstance(el, Spring):
            # Выводим только её жесткость
            param = f'{el.C:.2f}'
        else:
            # Это стержень
            param = f'{el.E:.2f} {el.A:.2f}'

        # Для одного элемента выводим
        # i - индекс элемента в массиве
        # N1 - номер первого узла
        # N2 - номер второго узла
        # param - параметры элемента
        print(f'\t{i+1} {N1+1} {N2+1} {param}')

    # Дальше записываем где находятся заделки
    print("\nPinning:")
    # Обходим все узлы
    for i, node in enumerate(line_struct.grid):
        # Если в текущем узле заделка
        if node.u == 0 and node.v == 0:
            # Выводим номер этого узла
            print(f'\t{i+1}')

    # Дальше нужно указать точечные усилия в узлах
    # Переменная флаг, мы вообще имеем усилия в узла?
    is_have = False
    # Обходим все узлы
    for i, node in enumerate(line_struct.grid):
        # Обходим все усилия, приложенные к узлу
        for F in node.forces:
            # Если мы тут, то в конструкции точно есть усилия
            # Если до этого не попадались
            if not is_have:
                # Выводим заголовок
                print('\nPoint_Forces:')
                # Поднимаем флаг - говорим что усилия есть
                is_have = True
            # Выводим индекс узла и значения силы
            print(f"\t{i} {F.x:.2f} {F.y:.2f}")

    # Дальше указываем распределенные нагрузки в элементе
    # Переменная флаг, мы вообще имеем распределённую нагрузку в конструкции?
    is_have = False
    # Обходим все элементы конструкции
    for i, el in enumerate(line_struct.items):
        # Обходим все распределённые усилия в элементе
        for q1, q2 in el.q:
            # Если мы тут, то в конструкции точно есть распределёнка
            # Если до этого не попадались
            if not is_have:
                # Выводим заголовок
                print('\nDistributed_Forces:')
                # Поднимаем флаг - говорим что распределённая нагрузка есть
                is_have = True
            # Выводим индекс элемента и нагрузки в его начале и в конце
            print(f'\t{i+1} {q1.x:.2f} {q1.y:.2f} {q2.x:.2f} {q2.y:.2f}')

    # Закрываем файл
    file.close()
    # Возвращаем стандартный вывод
    sys.stdout = sys.__stdout__


def get_block(block, file_name):
    """Загрузить блок данных из файла"""
    # Открываем файл на чтение
    file = open(file_name, 'r', encoding='utf8')
    # Проходим все строки файла
    for line in file:
        # Если строка начинается с загоовка блока
        if line.strip().startswith(block):
            # перестаём перебирать строки
            break

    # Результирующий массив данных из блока
    res_data = []
    # Проходим все строки файла
    for line in file:
        # Если строка НЕ начинается с симола табуляции,
        # то значит блок завершён
        if not line.startswith('\t'):
            # Завершаем перебирать строки
            break
        else:
            # Строка начинается с символа слеша
            # Проверяем не является ли строка комментарием
            if line.strip().startswith("#"):
                # Это комментарий - переходим к следующей строке
                continue

            # Получаем данные из этой строки
            # Все данные разделены пробелами
            # метод сплит вернёт массив подсрок
            data = line.strip().split()
            # Добавляем данные из строки к данным блока
            res_data.append(data)

    # Закрываем файл
    file.close()

    # Возвращаем данные из блока
    return res_data


def load_model(file_name):
    """Загрузка модели из файла"""
    # Заготовка модели
    line_struct = LineStructure()
    # Сначала получаем блок - узлы
    nodes = get_block("Nodes", file_name)
    # Проходим полученные данные, для преобразования к нужным типам
    for index in range(len(nodes)):
        # Первый элемент - это индекс 'i' - целое число
        nodes[index][0] = int(nodes[index][0])
        # Второй элемент - это координата 'x'- вещественное число
        nodes[index][1] = float(nodes[index][1])
        # Третий элемент - это координата 'y'- вещественное число
        nodes[index][2] = float(nodes[index][2])
    # Пройдём отсортированный массив
    for i, x, y in sorted(nodes):
        # Создаём новый узел
        n = Node(x=x, y=y)
        # Сохраняем позицию узла
        n.pos = i-1
        # Вставляем узел в массив узлов
        # В позицию i
        line_struct.grid.insert(i-1, n)

    # Дальше проходим элементы
    elements = get_block("Elements", file_name)
    # Проходим полученные данные, для преобразования к нужным типам
    for el in elements:
        # С первого по 3ий параметры - это целые числа
        for i in range(3):
            el[i] = int(el[i])
        # Остальные элементы - это вещественные числа
        for i in range(3, len(el)):
            el[i] = float(el[i])
    # Проходим элементы и добавляем их к конструкции
    for el in sorted(elements):
        # Разбиваем строку элемента на параметры
        i, N1, N2, *param = el
        # Получаем объекты узлов
        node1 = line_struct.grid[N1-1]
        node2 = line_struct.grid[N2-1]

        if len(param) == 1:
            # Если в параметрах только один элемент
            # То это пружинка, используем соответствующий метод
            C = param[0]
            line_struct.add_spring(C=C, n1=node1, n2=node2)
        else:
            # Иначе это стержень, который имеет
            # Модуль Юнга
            E = param[0]
            # Площадь поперечного сечения
            A = param[1]
            # Добавляем стержень к конструкции
            line_struct.add_rod(E=E, A=A, n1=node1, n2=node2)

    # Дальше обрабатываем заделки
    pinning = get_block("Pinning", file_name)
    # Обходим узлы, в которых находятся заделки
    for n in pinning:
        # Преобразуем индекс узла к целому числу
        i = int(n[0])-1
        # Получаем индекс с нужным индексом
        node = line_struct.grid[i]
        # Добавляем заделку в этот узел
        line_struct.add_pinning(node)

    # Получаем точечные усилия в узлах
    point_forces = get_block("Point_Forces", file_name)
    # Проходим точечные усилия и добавляем их к конструкции
    for i, Fx, Fy in point_forces:
        # преобразуем параметры в нужные типы
        # индекс - целое число
        i = int(i)
        # Усилие - вещественное число
        Fx = float(Fx)
        Fy = float(Fy)
        # Объект силы
        F = Force(Fx, Fy)
        # Получаем узел с нужным индексом
        node = line_struct.grid[i]
        # Добавляем усилие к узлу
        line_struct.add_point_force(node=node, value=F)

    # Получаем распределённые нагрузки
    distributed_forces = get_block("Distributed_Forces", file_name)
    # Проходим данные об распределённых усилиях и добавляем их к конструкции
    for i, f1x, f1y, f2x, f2y in distributed_forces:
        # Преобразуем данные к нужным типам
        # индекс элемента - целое число
        i = int(i)-1
        # Усилия в начале и в конце элемента - вещественные числа
        f1x, f1y, f2x, f2y = map(float, [f1x, f1y, f2x, f2y])
        # Превращаем числа в обхекты сил
        q1 = Force(f1x, f1y)
        q2 = Force(f2x, f2y)
        # Получаем элемент с нужным индексом
        el = line_struct.items[i]
        # Добавляем распределёнку к системе
        line_struct.add_linear_distributed_force(el=el, q1=q1.val, q2=q2.val)

    # В конце возвращаем собранный объект конструкции
    return line_struct
