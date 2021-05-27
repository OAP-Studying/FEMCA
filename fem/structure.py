# -*- coding: utf-8 -*-
"""
structure - отдельний модуль для описания конструкции,
состоящей из КЭ
"""

from . import matan

import math
from typing import List
from dataclasses import dataclass, field
from abc import ABC, abstractmethod, abstractproperty


def get_alpha(x, y):
    """
    Получам угол наклон вектора относитель оси x
    x: проекция вектора на ось x
    y: проекция вектора на ось y
    """
    # Если сила ТОЛЬКО вдоль оси y
    if x == 0:
        # В зависимости от напрвления силы вдоль y
        # задаём угол наклона силы
        if y < 0:
            alpha = math.radians(270)
        else:
            alpha = math.radians(90)
    elif y == 0:
        # В зависимости от напрвления силы вдоль x
        # задаём угол наклона силы
        if x < 0:
            alpha = math.radians(180)
        else:
            alpha = 0
    else:
        if x > 0 and y > 0:
            alpha = math.atan(y/x)
        elif x < 0 and y > 0:
            alpha = math.pi - math.atan(abs(y/x))
        elif x < 0 and y < 0:
            alpha = math.radians(270) - math.atan(abs(x/y))
        else:
            # x > 0 and y < 0
            alpha = math.radians(360) - math.atan(abs(y/x))

    # Возвращаем угол альфа - наклон к оси x
    return alpha


class Vector(ABC):
    """
    Класс вектора, его ТОЛЬКО наследовать
    Нужно определить сеттеры для свойств x и y
    """

    def __init__(self, x=0, y=0, *, val=None, alpha=0):
        """
        x - проекция на ось oX
        y - проекция на ось oY
        val - значение силы
        alpha - угол от оси oX до силы [град]
        """
        # Если передали значение силы
        if val:
            # Задаём значение силы
            self.val = val
            # Значение угла
            self.alpha = math.radians(alpha % 360)
        else:
            # Знаит передали прокции на оси x и y
            self.apply_projections(x, y)

    def apply_projections(self, x, y):
        """Применить проекции силы"""
        # Получаем значение силы
        self.val = math.sqrt(x**2 + y**2)
        # Задаём угол наклона к оси x
        self.alpha = get_alpha(x, y)

    @property
    def x(self):
        """Проекция силы на ось x"""
        res = round(self.val*math.cos(self.alpha), 2)
        if res == 0:
            return 0
        else:
            return res

    @x.setter
    @abstractmethod
    def x(self, val):
        """Изменить проекцию силы на ось x"""
        pass

    @property
    def y(self):
        """Проекция силы на ось y"""
        res = round(self.val*math.sin(self.alpha), 2)
        if res == 0:
            return 0
        else:
            return res

    @y.setter
    @abstractmethod
    def y(self, val):
        """Изменить проекцию силы на ось y"""
        pass


class Force(Vector):
    """
    Класс представляет Силу
    Прокции силы можно менять
    """
    @Vector.x.setter
    def x(self, val):
        """Изменить проекцию силы на ось x"""
        self.apply_projections(x=val, y=self.y)

    @Vector.y.setter
    def y(self, val):
        """Изменить проекцию силы на ось y"""
        self.apply_projections(x=self.x, y=val)


class Distance(Vector):
    """
    Класс расстояния
    В данном случае проекции расстояния менять нельз
    """
    @Vector.x.setter
    def x(self, val):
        """Изменить проекцию дистанции на ось x"""
        raise Exception("Нельзя менять проекци X объекта расстояния")

    @Vector.y.setter
    def y(self, val):
        """Изменить проекцию дистанции на ось y"""
        raise Exception("Нельзя менять проекци Y объекта расстояния")


@dataclass
class Node:
    """Класс одного узла в системе"""
    # Содержит координаты своего расположения
    x: float = None
    y: float = None
    # перемещение в данном узле
    # Вдоль оси x
    u: float = field(init=False, default=None)
    # Вдоль оси y
    v: float = field(init=False, default=None)
    # массив сил приложенных в данном узле
    forces: List[Force] = field(init=False, default_factory=list)
    # Позиция узла в массиве вершин
    pos: int = field(init=False, default=None)

    def add_point_force(self, value: Force):
        """
        Добавить точечную силу - нагрузку
        Принимает:
          value  : значение нагрузки
        """
        self.forces.append(value)

    def add_pinning(self):
        """Добавить закрепление"""
        self.u = 0
        self.v = 0


@dataclass
class FiniteElement(ABC):
    """Абстрактный класс одного обособленного конечного элемента"""
    # Самое базовое свойтсво, которым должны обладать КЭ - это матрица жёсткости
    # Умышленно здесь не указали нагрузки в узлах и количество узлов и тп
    # Так как элемент может быть не одномерным в будущем

    @abstractproperty
    @property
    def K(self):
        """Матрица жётскости элемента"""
        # наследники этого класса должны определить этот метод
        pass

    @K.setter
    def K(self, value):
        """
        Задавать матрицу жёсткости нельзя, вызываем исключение
        """
        raise Exception("Попытка изменить матрицу жосткости элемента")


@dataclass
class LineFE(FiniteElement):
    """Линейный конечный элемент"""
    # объекты узлов нв концах стержня
    n1: Node = field(init=False, default=None)
    n2: Node = field(init=False, default=None)
    # Позиция элемента в массиве элементов
    pos: int = field(init=False, default=None)
    # Распределённые нагрузки на элементе
    q: List[List[Force]] = field(init=False, default_factory=list)

    # Так называем КЕШ простой матрицы жёсткости
    # Чтобы каждый раз не вычислять её
    _simple_K: matan.Matrix = field(init=False, default=None)

    @property
    def L(self):
        """Длина элемента"""
        # Из конечного узла вычитаем начальный
        return math.sqrt((self.n1.x-self.n2.x)**2 + (self.n1.y-self.n2.y)**2)

    @L.setter
    def L(self, value):
        """Менять длину элемента нельзя"""
        raise Exception("Попытка изменить длину стержня КЭ")

    @property
    def Lx(self):
        """Проекция элемента на ось x"""
        return self.n2.x-self.n1.x

    @Lx.setter
    def Lx(self, val):
        """Изменить проекцию элемента на ось x"""
        raise Exception("Нельзя менять проекци X элемента")

    @property
    def Ly(self):
        """Проекция силы на ось y"""
        return self.n2.y-self.n1.y

    @Ly.setter
    def Ly(self, val):
        """Изменить проекцию элемента на ось y"""
        raise Exception("Нельзя менять проекци Y элемента")

    @property
    def alpha(self):
        """Угол наклона элемента к оси x"""
        # Возврвщаем угол наклона
        return get_alpha(self.Lx, self.Ly)

    @alpha.setter
    def alpha(self, value):
        """Задавать угол альфа нельзя"""
        raise Exception("Попытка изменить угол наклона стержня КЭ")

    def get_simple_K(self):
        """Получить ПРОСТУЮ матрицу жёсткости без учета материала"""
        # Если матрица еще не вычислялась
        if not self._simple_K:
            # Вычисляем её
            # Перед созданием матрицы зададимся косинусом
            # и синусом угла наклона элемента
            cos_a = math.cos(self.alpha)
            sin_a = math.sin(self.alpha)

            # Упрощённая матрица жёсткости
            self._simple_K = matan.Matrix(
                [[cos_a**2,     cos_a*sin_a,  -cos_a**2,    -cos_a*sin_a],
                 [cos_a*sin_a,  sin_a**2,     -cos_a*sin_a, -sin_a**2],
                 [-cos_a**2,    -cos_a*sin_a, cos_a**2,     cos_a*sin_a],
                 [-cos_a*sin_a, -sin_a**2,    cos_a*sin_a,  sin_a**2]])

            # Теперь округляем все элементы матрицы жеёсткости с точностью
            # До второго знака после запятой
            for i in range(self._simple_K.rows):
                for j in range(self._simple_K.cols):
                    self._simple_K[i, j] = round(self._simple_K[i, j], 2)

        # Возвращаем ПРОСТУЮ матрицу жёсткости
        return self._simple_K

    def add_linear_distributed_force(self, q1: Force, q2: Force):
        """
        Добавить распределённую нагрузку - ВДОЛЬ элемента
        Принимает:
          q1 : нагрузка в начале элемента
          q2 : нагрузка в конце элемента
        """
        # Приведём силы по краям элемента к объектам сил
        self.q.append([q1, q2])


@dataclass
class Rod(LineFE):
    """Стержневой КЭ"""
    # Жесткость (модуль Юнга)
    E: float = None
    # Площадь поперечного сечения
    A: float = None

    @property
    def K(self):
        """Матрица жётскости стержня"""
        # коэффициент перед матрицей
        c = self.E*self.A/self.L

        # Результирующая матрица жёсткости стержня
        return self.get_simple_K()*c


@dataclass
class Spring(LineFE):
    """КЭ Пружинка"""
    # Жесткость пружинки
    C: float = None

    @property
    def K(self):
        """Матрица жётскости пружинки"""
        # Результирующая матрица жёсткости пружинки
        return self.get_simple_K()*self.C


@dataclass
class LineStructure(FiniteElement):
    """
    Конструкция состоящая из линейных КЭ
    """
    # Массив конечных элементов, из которых состоит конструкция
    items: List[LineFE] = field(init=False, default_factory=list)
    # Массив узлов, которые содержат ссылки на конечные элементы
    grid: List[Node] = field(init=False, default_factory=list)

    def add_fen_el(self, el: LineFE, n1: Node = None, n2: Node = None, D: Distance = None):
        """
        Добавляет конечный элемент к другим элементам конструкции
        el: одномерный конечный элемент
        n1: начальный узел
        n2: конечный узел
        D : длина - протяжённость элемента

        """
        # Добавляем КЭ в массив элементов конструкции
        self.items.append(el)
        # Сохраняем позицию элемента
        el.pos = len(self.items) - 1

        # Если не указали начальный узел
        if not n1:
            # Тогда есть два варианта
            # 1-ый - в конструкции еще нет ни одного узла
            if not self.grid:
                # Тогда нужно создать начальный узел
                # В позиции 0
                n1 = Node(x=0, y=0)
                # Добавляем узел в массив узлов конструкции
                self.grid.append(n1)
                # Сохраняем позицию узла
                n1.pos = len(self.grid) - 1
            else:
                # 2-ой в конструкции уже есть элементы
                # Тогда надо вызвать ошибку, что забыли указать узел
                raise Exception("Забыли указать НАЧАЛЬНЫЙ узел элемента 'n1'")

        # Записываем узел n1 как НАЧАЛЬНЫЙ узел элемента
        el.n1 = n1

        # Если не указали КОНЕЧНЫЙ узел элемента
        if not n2:
            # Должны указать длину стержня
            # если не указали длину стрежня
            if not D:
                # Вызываем исключение
                raise Exception("Необходимо указать длину элемента")
            else:
                # Длину стержня указали
                # Создаём конечный узел, с указанием его координаты
                n2 = Node(x=n1.x+D.x, y=n1.y+D.y)
                # Добавляем узел в массив узлов конструкции
                self.grid.append(n2)
                # Сохраняем позицию узла
                n2.pos = len(self.grid) - 1

        # Здесь уже точно n2
        # тогда назначаем новый узел КОНЕЧНЫМ узлом элемента
        el.n2 = n2

    def add_rod(self, E, A, n1: Node = None, n2: Node = None, D: Distance = None):
        """
        Добавляет стержень к конструкции
        E : модуль Юнга
        A : Площадь поперечного сечения стержня
        n1: номер узла, из которого начинается
        n2: номер узла, в котором заканчивается
        D : длина - протяжённость стержня
        """
        # Создаём новый конечный элемент - стержень
        rod = Rod(E, A)
        # Добавляем его к конструкции
        self.add_fen_el(rod, n1, n2, D)

        # Возвращаем последний добавленный элемент
        return rod

    def add_spring(self, C, n1: Node = None, n2: Node = None, D: Distance = None):
        """
        Добавить пружину к системе
        С : жёсткость пружины
        n1: номер узла, из которого начинается
        n2: номер узла, в котором заканчивается
        D : длина - протяжённость пружины
        """
        # Создаём новый конечный элемент - пружинка
        spring = Spring(C=C)
        # Добавляем его к конструкции
        self.add_fen_el(spring, n1, n2, D)

        # Возвращаем последний добавленный элемент
        return spring

    def add_point_force(self, node: Node, value: Force):
        """
        Добавить точечную силу - нагрузку
        Принимает:
          node   :
          value  : значение нагрузки
        """
        node.add_point_force(value)

    def add_linear_distributed_force(self, el: LineFE, q1: Force, q2: Force):
        """
        Добавить распределённую нагрузку - ВДОЛЬ элемента
        Принимает:
          el  :  КЭ
          q1 : нагрузка в начале элемента
          q2 : нагрузка в конце элемента
        """
        el.add_linear_distributed_force(q1, q2)

    def add_pinning(self, node: Node):
        """
        Добавить закрепление
        node : объект вершины
        """
        node.add_pinning()

    @property
    def K(self):
        """Глобальная матрица жётскости"""
        # Создаём заготовку под матрицу
        matrix = matan.Matrix(size=len(self.grid)*2, filler=0)

        # Обходим все конечные элементы конструкции
        for el in self.items:
            # Получаем индексы узлов в матрице жёсткости
            u1 = el.n1.pos*2
            v1 = u1 + 1
            u2 = el.n2.pos*2
            v2 = u2 + 1
            # Добавляем элементы матрицы жёсткости к глобальной
            matrix[u1, u1] += el.K[0, 0]
            matrix[u1, v1] += el.K[0, 1]
            matrix[u1, u2] += el.K[0, 2]
            matrix[u1, v2] += el.K[0, 3]

            matrix[v1, u1] += el.K[1, 0]
            matrix[v1, v1] += el.K[1, 1]
            matrix[v1, u2] += el.K[1, 2]
            matrix[v1, v2] += el.K[1, 3]

            matrix[u2, u1] += el.K[2, 0]
            matrix[u2, v1] += el.K[2, 1]
            matrix[u2, u2] += el.K[2, 2]
            matrix[u2, v2] += el.K[2, 3]

            matrix[v2, u1] += el.K[3, 0]
            matrix[v2, v1] += el.K[3, 1]
            matrix[v2, u2] += el.K[3, 2]
            matrix[v2, v2] += el.K[3, 3]

        # Теперь округляем все элементы матрицы жеёсткости с точностью
        # До второго знака после запятой
        for i in range(matrix.rows):
            for j in range(matrix.cols):
                matrix[i, j] = round(matrix[i, j], 2)

        # Возвращаем глобальную матрицу
        return matrix

    @property
    def f(self):
        """Вектор известных узловых сил"""
        # Заготовка для вектора
        vector = matan.Matrix(rows=len(self.grid*2), filler=0)

        # Обходим все узлы системы
        for i in range(len(self.grid)):
            # В каждом узле обходим и суммируем все силы, приложенные в этом узле
            # Сумма проекций вдоль оси x
            sum_Fx = sum(F.x for F in self.grid[i].forces)
            # Сумма проекций вдоль оси y
            sum_Fy = sum(F.y for F in self.grid[i].forces)
            # Заполняем вектор столбец
            vector[i*2] += sum_Fx
            vector[i*2+1] += sum_Fy

        # Добавляем распределённые нагрузки
        # Обходим все элементы системы
        for el in self.items:
            # Проверяем приложены ли распределёнки в текущем элементе
            if el.q:
                # Если они приложены находим индексы узлов элемента
                N1 = el.n1.pos
                N2 = el.n2.pos
                # Проходим все распределённые нагрузки на текущем элементе
                for q1, q2 in el.q:
                    # Распределённые нагрузки заменяем на точечные, приложенные
                    # К узлам элеммента
                    # Вычисляем нагрузки в начале элемента
                    f1x = (el.Lx/2)*(q1.x*2/3 + q2.x*1/3)
                    f1y = (el.Ly/2)*(q1.y*2/3 + q2.y*1/3)
                    # Вычисляем нагрузки в конце элемента
                    f2x = (el.Lx/2)*(q1.x*1/3 + q2.x*2/3)
                    f2y = (el.Ly/2)*(q1.y*1/3 + q2.y*2/3)

                    # Добавляем получаенные усилия к вектору усилий
                    vector[N1*2] += f1x
                    vector[N1*2+1] += f1y
                    vector[N2*2] += f2x
                    vector[N2*2+1] += f2y

        # Возвращаем вектор известных узловых сил
        return vector

    @f.setter
    def f(self, value):
        """
        Задавать вектор известных усилий нельзя
        """
        raise Exception("Попытка изменить вектор {f} системы")

    @property
    def q(self):
        """Вектор неизвестных узловых перемещений"""
        # Заготовка для вектора
        vector = matan.Matrix(rows=len(self.grid*2), filler=0)
        # Обходим все узлы
        for i in range(len(self.grid)):
            # В каждом узле смотрим на перемещение
            # Если перемещение не нулевое, то есть нет заделки
            if self.grid[i].u != 0:
                # Записываем в вектор строку
                vector[i*2] = f'u{i+1}'
            if self.grid[i].v != 0:
                # Записываем в вектор строку
                vector[i*2+1] = f'v{i+1}'

        # Возвращаем вектор неизвестных перемещений
        return vector

    @q.setter
    def q(self, value):
        """
        Задавать вектор НЕизвестных перемещений нельзя
        """
        raise Exception("Попытка изменить вектор 'q' системы")
