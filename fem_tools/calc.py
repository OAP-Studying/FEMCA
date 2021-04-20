# -*- coding: utf-8 -*-
"""
calc - отдельный модуль для расчёта конструкций
отличается от matan тем, что завязан именно на конструкции
"""
import sys
from copy import deepcopy

# Модели конструкций
from . import structure as s
# Рукописные математические функции
from . import matan as m


class FEMComput:
    """Класс для вычислений МКЭ - одномерный случай"""

    def __init__(self, beam: s.Beam):
        """
        Вызывается при создании экземпляра
        beam : объект конструкции (балка) состоящих
               из конечных элементов
        """
        # Делаем копию конструкции для изменений
        self.beam = deepcopy(beam)
        # Глобальная матрица жескости конструкции
        self.K = self.beam.K
        # Вектор известных узловых усилий
        self.f = self.beam.f
        # Вектор НЕизвестных узловых перемещенией
        self.q = self.beam.q
        # Вычисялемые перемещения для ускорения вычислений
        self.res_q = []

    @property
    def height(self):
        """Количество строк в системе"""
        return len(self.K)

    @height.setter
    def height(self, value):
        """Нельзя менять количество строк системы"""
        raise Exception("Атрибут 'height' нельзя изменять")

    def show_equation(self, message):
        """Показать уравнение в матричном виде"""
        # Флаг выводилось ли подсказка
        is_first = True
        for i in range(self.height):

            # Выводим элементы матрицы K
            K_str = '|'
            for k in self.K[i]:
                K_str += f'{k:7.2f}'
            K_str += '|'

            # Выводим символ умножения матриц
            if i == int(self.height/2):
                mult_str = ' x '
            else:
                mult_str = '   '

            # Выводим элементы вектора u - НЕизвестных узловых перемещений
            q_str = f'|{self.q[i]:^3}|'

            # Символ равно
            if i == int(self.height/2):
                eql_str = ' = '
            else:
                eql_str = '   '

            # Выводим элементы вектора f - известных узловых перемещений
            f_str = f'|{self.f[i]:6.2f}|'

            # результирующая строка матричного уравнения
            res_row = K_str + mult_str + q_str + eql_str + f_str

            # Если строк ещё не выводили, то нужно ещё
            # Вывесте подсказки, чтобы показать где какая матрица
            if is_first:
                help_K = 'K'.center(len(K_str), ' ')
                help_q = 'q'.center(len(q_str), ' ')
                help_f = 'f'.center(len(f_str), ' ')
                help_str = f'{help_K}   {help_q}   {help_f}\n'
                # Выводим сообщение
                print("\n"+f"{message}".center(len(help_str)-1, '-'))
                print(help_str)
                # Опускаем флаг, подсказку уже выводили
                is_first = False

            # Печатаем эту строку уравнения
            print(res_row)

    def enter_boundary_conditions(self):
        """
        Введём граничные условия методом Пиана-Айронса
        """
        # Обходим вектор узловых перемещений
        for i in range(len(self.q)):
            # Если в каком-то узле перемещенее равно нулю
            if self.q[i] == 0:
                # Значит в этом узле нам нужно закрепить конструкцию
                # Что немало важно, в этом узле находится заделка

                # Согласно методу Пиана-Айронса
                # В i-ой строке и i-ом ставим единицу
                self.K[i][i] = 1

                # Остальные элементы в i-ой строке приравниваем нулю
                # Обходим элементы выбранной строки
                for col in range(len(self.K[i])):
                    # Если номер узла не равен номеру столбца в строке
                    # Там где поставили единичку
                    if i != col:
                        # То зануляем элемент в этой строке
                        self.K[i][col] = 0

                # остальные элементы в i-ом столбце приравниваем нулю
                # Обходим элементы выбранного столбца
                for row in range(len(self.K)):
                    # Если номер узла не равен номеру строки в столбце
                    # Где до этого ставили единичку
                    if i != row:
                        # То зануляем этот элемент в столбце
                        self.K[row][i] = 0

                # То есть меняем матрицу K так (пусть закрепили в 0-ом узле):
                #  1  2  3  4      1  0  0  0
                #  5  6  7  8      0  6  7  8
                #  9 10 11 12  =>  0 10 11 12
                # 13 14 15 16      0 14 15 16

                # Осталось изменить вектор известных узловых усилий
                self.f[i] = 0

                # То есть изменили вектор f(для примера закрепили в 0-ом узле)
                #  1    0
                #  2    2
                #  3 => 3
                #  4    4

    def find_q(self, method='gauss', recalculate=False):
        """
        Найти вектор неизвестных узловым перемещений
            method: метод решения систему уравнений (inv, guass)
            recalculate: пересчитать в любом случае
        """
        # если задан параметр пересчитать - то есть в любом случае
        # произвести расчёт занаво или еще не было посчитано
        if recalculate or not self.res_q:
            # В зависимости от метода находм векторстолбец q
            if method == 'inv':
                self.res_q = m.find_with_inv(self.K, self.f)
            elif method == 'gauss':
                self.res_q = m.find_with_gauss(self.K, self.f)
            else:
                raise Exception(f'Ошибочный параметр method="{method}"')

        # возвращаем посчитанное значение вектора перемещений
        # или то, чо было вычисленно ранее
        return self.res_q

    def show_q(self):
        """Вывести узловые перемещения"""
        # Вектор неизвестных узловых перемещений
        unknown = self.q
        # Найденный вектор узловых перемещений
        known = self.find_q()

        print("\nУзловые перемещения\n")
        for i in range(self.height):
            # Выводим НЕизвестный вектор
            str_unknown = f'|{unknown[i]:^3}|'

            # Выводим символ равно
            if i == int(self.height/2):
                eql_str = ' = '
            else:
                eql_str = '   '

            # Выводим ИЗВЕСТНЫЙ вектор
            str_known = f'|{known[i]:6.2f}|'

            # Собираем строку выражения и печатаем её
            res_str = str_unknown + eql_str + str_known
            print(res_str)

    def apply_q_to_structure(self):
        """Нанести перемещения на конструкцию"""
        # Найдем вектор узловых перемещений
        q = self.find_q()

        # Узлы в конструкции должы быть в том же порядке, что и векторе q
        # Каждому узлу конструкции указываем соответствующее перемещение
        for i in range(len(q)):
            self.beam.nodes[i].u = q[i]

    def aprox_u(self, el: s.OneFE, x: float):
        """Апрокисимация поля перемещения ОДНОГО элемената
        el: конечный элемент
        x : координа относительно элемента, в которой нужно
            вычислить перемещение, задаётся в безразмерном виде
            от 0 до 1 включительно
        """
        # 'x' или локальная координата должна быть >= 0 и <= 1
        # Иначе нужно вызывать исключенеи
        if x < 0 or x > 1:
            raise Exception(f'Координата x={x} не внутри [0, 1]')

        # Находим перемещение в начале элемента
        u1 = el.node1.u
        # Находим перемещение в конце элемента
        u2 = el.node2.u

        # Функции форм конечного элемента
        N1 = 1 - (x*el.L)/el.L
        N2 = (x*el.L)/el.L

        # Перемещение в точке x элемента
        # Это скалярное произведение вектором u и N
        return u1*N1 + u2*N2

    def show_all_aprox_u(self, step=0.25):
        """
        Показать апроксимации ПЕРЕМЕЩЕНИЙ всех элементов
        step - c какой точностью разбиваем элемент от 0 до 1 невключительно
        """
        # step или шаг должен строго быть > 0 и < 1
        # Иначе нужно вызывать исключенеи
        if step <= 0 or step >= 1:
            raise Exception(f'Параметр точности step={step} не внутри (0, 1)')

        # Выведем апроксимацию перемещений на всех элементах конструкции
        # Вспомогательное сообщение
        message = '\n'+'Апроксимация перемещений'.center(50, '-')
        print(message)
        # Обходим все элементы конструкции
        for i in range(self.beam.cnt_elements):
            # Выбираем один элемент из конструкции
            el = self.beam.elements[i]
            # Если элемент пружина, указываем это
            if isinstance(el, s.Spring):
                print(f'\nЭлемент {i} - ПРУЖИНКА, L={el.L}')
            else:
                # Элемент не пружины, выводим простое сообщение
                print(f'\nЭлемент {i}, L={el.L}')

            # Берём точки элемента с шагом step, начиная из точки 0
            x = 0
            while x <= 1:
                # Нам нужно в любом случае вывести значение u в точке 1
                # Для этого нужно отслеживать изменение координаты x
                # ближе к концу стержня
                # Если следующая точка выходит за рамки элемента
                if x + step > 1:
                    # Приравниваем значение точки единице
                    # То есть ставим точку в конец объекта
                    x = 1
                # Выводим перемещение в точке x
                print(f'\tu({x:5.2f}) = {self.aprox_u(el, x):5.2f}')
                # Переходим к следующей точке элемента
                # с шагом step
                x += step

    def aprox_force(self, el: s.OneFE):
        """Апроксимация усилий в элементе"""
        # По формуле N(x) = EF*u'(x) найдем усилия
        # В нашем простом примере производная от перемещения
        # u'(x) не зависит от x, следовательно
        # Усилие в каждой точке конечного элементо
        # - это константа, и можно не передавать x

        # Находим перемещение в начале элемента
        u1 = el.node1.u
        # Находим перемещение в конце элемента
        u2 = el.node2.u

        # Производные от функции форм конечного элемента
        _N1 = -1/el.L
        _N2 = 1/el.L

        # Производная от функции перемещения u'(x)
        # Это скалярное произведение векторов u и N'
        _u = u1*_N1 + u2*_N2

        # Если элемент пружинка
        if isinstance(el, s.Spring):
            EF = el.C * el.L
        else:
            EF = el.E * el.F

        # находим усилие по известной формуле N(x) = EF*u'(x)
        return EF*_u

    def show_all_aprox_force(self):
        """Показать апроксимации Усилий всех элементов"""
        # Выведем апроксимацию перемещений на всех элементах конструкции
        # Вспомогательное сообщение
        message = '\n'+'Апроксимация УСИЛИЙ'.center(50, '-')
        print(message)

        # Обходим все элементы конструкции
        for i in range(self.beam.cnt_elements):
            # Выбираем один элемент из конструкции
            el = self.beam.elements[i]
            # Если элемент пружина, указываем это
            if isinstance(el, s.Spring):
                review = f'Элемент {i} - ПРУЖИНКА, L={el.L}'
            else:
                # Элемент не пружины, выводим простое сообщение
                review = f'Элемент {i}, L={el.L}'

            # находим апроксимацию усилий в этом элементе
            N = self.aprox_force(el)
            # Добавляем к описанию конечного элемента
            review = f'{review}, N(0..L) = {N:5.2f}'
            # Выводим описание элемента
            print(review)

    def display_results(self):
        """Выводим результаты на экран"""
        # Выводим матричное уравнение
        self.show_equation("Уравнение в матричном виде")
        # Введём граничные условия методом Пиана-Айронса
        self.enter_boundary_conditions()
        # Снова выводим матричное уравнение
        self.show_equation("Введём граничные условия методом Пиана-Айронса")
        # Найдём и выведем узловые перемещения
        self.show_q()
        # Нанесём перемещения на конструкцию (копию внутри объекта self)
        self.apply_q_to_structure()
        # Выведем апроксимации перемещений для всех элементов конструкции
        self.show_all_aprox_u()
        # Выведем апроксимации усилий для всех элементов
        self.show_all_aprox_force()

    def save_results(self, file_name, comment=''):
        """Сохраняем результаты вычислений в файл"""
        # Открываем файл на запись
        file = open(file_name, 'w', encoding='utf8')
        # Переопределяем стандартный вывод
        sys.stdout = file
        # Выводи комментарий к результатам, если он существует
        if comment:
            print(comment)

        # Записываем результаты в файл
        self.display_results()

        # Закрываем файл
        file.close()
        # Возвращаем стандартный вывод
        sys.stdout = sys.__stdout__
