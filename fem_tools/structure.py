# -*- coding: utf-8 -*-
"""
structure - отдельний модуль для описания конструкции,
состоящей из КЭ
"""
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass, field
from typing import List


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
class Node(ABC):
    """Класс одного узла в системе"""

    @abstractmethod
    def add_point_force(self):
        """Добавить точечную нагрузку к конструкции"""
        pass


@dataclass
class FEMStructure(FiniteElement):
    """
    Конструкция из конечных элементов
    """
    # Массив конечных элементов, из которых состоит конструкция
    elements: List[FiniteElement] = field(default_factory=list)
    # Массив узлов, которые содержат ссылки на конечные элементы
    nodes: List[Node] = field(default_factory=list)

    @property
    def cnt_elements(self):
        """Общее количество ЭЛЕМЕНТОВ в конструкции"""
        return len(self.elements)

    @cnt_elements.setter
    def cnt_elements(self, value):
        """
        Общее количество элементов вычисляется динамически,
        его нельзя менять
        """
        raise Exception("Попытка задать количество ЭЛЕМЕНТОВ напрямую")

    @property
    def cnt_nodes(self):
        """Общее количество УЗЛОВ"""
        return len(self.nodes)

    @cnt_nodes.setter
    def cnt_nodes(self, value):
        """
        Общее количество узлов, вычисляется динамически
        """
        raise Exception("Попытка задать количество УЗЛОВ напрямую")

    @abstractmethod
    def add_fen_el(self):
        """Добавить конечный элемент к конструкции"""
        pass


@dataclass
class OneNode(Node):
    """Одномерный узел"""
    # Содержит координату своего расположения
    x: float = 0
    # перемещение в данном узле
    u: float = field(init=False, default=None)
    # массив сил приложенных в данном узле
    forces: List[float] = field(default_factory=list)
    # Позиция узла в массиве вершин
    pos: int = field(init=False, default=None)

    def add_point_force(self, value=1):
        """
        Добавить точечную силу - нагрузку
        Принимает:
          value  : значение нагрузки
        """
        self.forces.append(value)

    def add_pinning(self):
        """Добавить закрепление"""
        self.u = 0


@dataclass
class OneFE(FiniteElement):
    """Одномерный конечный элемент"""
    # Глобальный номер начального узла - локального 1-го
    node1: OneNode = field(init=False, default=None)
    # Глобальный номер конечного узла
    node2: OneNode = field(init=False, default=None)
    # Позиция элемента в массиве элементов
    pos: int = field(init=False, default=None)
    # Распределённые нагрузки на элементе
    q: List[List[float]] = field(default_factory=list)

    @property
    def L(self):
        """Длина элемента"""
        # Из конечного узла вычитаем начальный
        return abs(self.node2.x - self.node1.x)

    @L.setter
    def L(self, value):
        """Менять длину элемента нельзя"""
        raise Exception("Попытка изменить длину КЭ")

    def add_linear_distributed_force(self, q1=1, q2=1):
        """
        Добавить распределённую силу - нагрузку
        Принимает:
          q1 : нагрузка в начале элемента
          q2 : нагрузка в конце элемента
        """
        self.q.append([q1, q2])


@dataclass
class Rod(OneFE):
    """Одномерный КЭ - Стержень"""
    # Жесткость (модуль Юнга)
    E: float = None
    # Площадь поперечного сечения
    F: float = None

    @property
    def K(self):
        """Матрица жётскости элемента"""
        C = self.E*self.F/self.L

        return [[C, -C], [-C, C]]


@dataclass
class Spring(OneFE):
    """Одномерный КЭ - Пружинка"""
    # Жесткость пружинки
    C: float = None

    @property
    def K(self):
        """Матрица жётскости элемента"""
        return [[self.C, -self.C], [-self.C, self.C]]


@dataclass
class Beam(FEMStructure):
    """
    Конструкция состоящая из конечных элементов,
    в данном случае стержневая система, которая отслеживает связи между
    конечными элементами - одномерная балка
    """

    def add_fen_el(self, el: OneFE, n1: OneNode = None, n2: OneNode = None, L=None):
        """
        Добавляет конечный элемент к другим элементам конструкции
        el: одномерный конечный элемент
        n1: начальный узел
        n2: конечный узел
        L : длина элемента

        """
        # Добавляем КЭ в массив элементов конструкции
        self.elements.append(el)
        # Сохраняем позицию элемента
        el.pos = self.cnt_elements - 1

        # Если не указали начальный узел
        if not n1:
            # Тогда есть два варианта
            # 1-ый - в конструкции еще нет ни одного узла
            if not self.nodes:
                # Тогда нужно создать начальный узел
                # В позиции 0
                n1 = OneNode(x=0)
                # Добавляем узел в массив узлов конструкции
                self.nodes.append(n1)
                # Сохраняем позицию узла
                n1.pos = self.cnt_nodes - 1
            else:
                # 2-ой в конструкции уже есть элементы
                # Тогда надо вызвать ошибку, что забыли указать узел
                raise Exception("Забыли указать НАЧАЛЬНЫЙ узел элемента 'n1'")

        # Записываем узел n1 как НАЧАЛЬНЫЙ узел элемента
        el.node1 = n1

        # Если не указали КОНЕЧНЫЙ узел элемента
        if not n2:
            # Должны указать длину стержня
            # если не указали длину стрежня
            if not L:
                # Вызываем исключение
                raise("Необходимо указать длину 'L' элемента")
            else:
                # Длину стержня указали
                # Создаём конечный узел, с указанием его координаты
                n2 = OneNode(x=n1.x + L)
                # Добавляем узел в массив узлов конструкции
                self.nodes.append(n2)
                # Сохраняем позицию узла
                n2.pos = self.cnt_nodes - 1

        # Здесь уже точно n2
        # тогда назначаем новый узел КОНЕЧНЫМ узлом элемента
        el.node2 = n2

    def add_rod(self, E, F, n1: OneNode = None, n2: OneNode = None, L=None):
        """
        Добавляет стержень к конструкции
        E : модуль Юнга
        F : Площадь поперечного сечения стержня
        n1: номер узла, из которого начинается
        n2: номер узла, в котором заканчивается
        L : длина стержня
        """
        # Создаём новый конечный элемент - стержень
        rod = Rod(E=E, F=F)
        # Добавляем его к конструкции
        self.add_fen_el(rod, n1, n2, L)

        # Возвращаем последний узел
        return rod

    def add_spring(self, C, n1: OneNode = None, n2: OneNode = None, L=None):
        """
        Добавить пружину к системе
        С : жёсткость пружины
        n1: номер узла, из которого начинается
        n2: номер узла, в котором заканчивается
        L : Длина пружины
        """
        # Создаём новый конечный элемент - пружинка
        spring = Spring(C=C)
        # Добавляем его к конструкции
        self.add_fen_el(spring, n1, n2, L)

        # Возвращаем последний узел
        return spring

    def add_point_force(self, node: OneNode, value=1):
        """
        Добавить точечную силу - нагрузку
        Принимает:
          node   :
          value  : значение нагрузки
        """
        node.add_point_force(value)

    def add_linear_distributed_force(self, el: OneFE, q1=1, q2=1):
        """
        Добавить распределённую силу - нагрузку
        Принимает:
          el  :  КЭ
          q1 : нагрузка в начале элемента
          q2 : нагрузка в конце элемента
        """
        el.add_linear_distributed_force(q1, q2)

    def add_pinning(self, node: OneNode):
        """
        Добавить закрепление
        node : объект вершины
        """
        node.add_pinning()

    @property
    def K(self):
        """Глобальная матрица жётскости"""
        # Создаём заготовку под матрицу
        matrix = []
        for i in range(self.cnt_nodes):
            matrix.append([])
            for j in range(self.cnt_nodes):
                matrix[i].append(0)

        # Обходим все конечные элементы конструкции
        for el in self.elements:
            # Получаем значения его узлов
            N1 = el.node1.pos
            N2 = el.node2.pos
            # Добавляем элементы матрицы жёсткости к глобальной
            matrix[N1][N1] += el.K[0][0]
            matrix[N1][N2] += el.K[0][1]
            matrix[N2][N1] += el.K[1][0]
            matrix[N2][N2] += el.K[1][1]

        # Возвращаем глобальную матрицу
        return matrix

    @property
    def f(self):
        """Вектор известных узловых сил"""
        # Заготовка для вектора
        vector = [0] * self.cnt_nodes

        # Обходим все узлы системы
        for i in range(self.cnt_nodes):
            # В каждом узле обходим суммируем все силы, приложенные в этом узле
            vector[i] += sum(self.nodes[i].forces)

        # Обходим все элементы системы
        for el in self.elements:
            # Нужно теперь добавить распределённые нагрузки
            # Проверяем приложены ли они в текущем элементе
            if el.q:
                # Если они приложены находим индексы узлов элемента
                N1 = el.node1.pos
                N2 = el.node2.pos
                # Проходим все распределённые нагрузки на текущем элементе
                for q1, q2 in el.q:
                    # Распределённые нагрузки заменяем на точечные, приложенные
                    # К узлам элеммента
                    # Вычисляем нагрузки в начале элемента
                    f1 = (el.L/2)*(q1*2/3 + q2*1/3)
                    # Вычисляем нагрузки в конце элемента
                    f2 = (el.L/2)*(q1*1/3 + q2*2/3)

                    # Добавляем получаенные усилия к вектору усилий
                    vector[N1] += f1
                    vector[N2] += f2

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
        # Нули говорят, что в данном узле заделка
        vector = [0] * self.cnt_nodes
        # Обходим все узлы
        for i in range(self.cnt_nodes):
            # В каждом узлесмотрим на перемещение
            # Если перемещение не нулевое, то есть нет заделки
            if self.nodes[i].u != 0:
                # Записываем в вектор строку
                vector[i] = f'u{i}'

        # Возвращаем вектор неизвестных перемещений
        return vector

    @q.setter
    def q(self, value):
        """
        Задавать вектор НЕизвестных перемещений нельзя
        """
        raise Exception("Попытка изменить вектор {q} системы")
