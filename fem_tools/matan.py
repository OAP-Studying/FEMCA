# -*- coding: utf-8 -*-
"""
matan - модуль предоставляющий математическеи функции
для работы с матричными выражениями
можно сказать аналог numpy
"""
from copy import deepcopy
from collections.abc import Iterable


class RowAccess:
    """Доступ к строкам матрицы"""

    def __init__(self, m, i_row):
        # Ссылка на матрицу
        self.m = m
        # Индекс строки
        self.i_row = i_row

    @property
    def cols(self):
        return self.m.cols

    @cols.setter
    def cols(self, value):
        Exception('Нельзя менять количество СТОЛБЦОВ напрямую')

    def valid_index(self, index):
        """Валидация индекса"""
        # Если индекс - это два числа
        if isinstance(index, tuple):
            # индекс строки должен быть обязательно нулевым
            if index[0] != 0 or index[0] != -1:
                raise Exception(f'У строки нет столько строк {index[0]}')
            else:
                # Индекс просто делаем одномерным
                index = index[1]

        # Если индекс отрицателен, то приводим его к правильному виду
        if index < 0:
            index = self.cols + index
        # Теперь проверяем возможен ли такой индекс
        if not(0 <= index < self.cols):
            raise IndexError(f"Bad index={index} not in [0, {self.cols}]")

        # Превращаем индекс в строке в индкс в матрице
        index = self.i_row*self.cols + index
        # Возвращаем индекс элемента строки
        return index

    def __getitem__(self, index):
        """Операция взятия индекса row[index]"""
        # проводим валидацию индекса и преобразуюем в индекс матрицы
        index_matrix = self.valid_index(index)
        # возвращаем элемент матрицы из строки
        return self.m._arr[index_matrix]

    def __setitem__(self, index, value):
        """Быстро задать строку матрицы"""
        # проводим валидацию индекса и преобразуюем в индекс матрицы
        index_matrix = self.valid_index(index)
        # присваиваем элементу матрицы значение
        self.m._arr[index_matrix] = value

    def __str__(self):
        """Строковое представление матрицы строки"""
        str_res = ''
        for j in range(self.cols):
            # Если элемент строки - это СТРОКА
            if isinstance(self[j], str):
                str_res += f"{self[j]:^6}"
            else:
                # Не строка, а число
                str_res += f'{self[j]:6.2f}'
        # Добавляем скобочки к строке
        str_res = f'|{str_res}|'
        # Возвращаем строковое представление матрицы-строки
        return str_res

    def __len__(self):
        """Количество элементов в строке"""
        return self.m.cols

    def __neg__(self):
        """Переопределение операции унарного минуса"""
        return self * (-1)

    def __mul__(self, other):
        """Операция умножение множение"""
        # Если второй объект это матрица
        if isinstance(other, Matrix):
            # Делаем проверку - количество столбцов первой должно
            # быть равно количеству столбцов второй
            if self.cols != other.rows:
                # Не равны => вызываем исключение
                # Размерность первой матрицы
                dim1 = f'1x{self.cols}'
                dim2 = f'{other.rows}x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")

            # Создаём новую матрицу закготовку
            m = Matrix(rows=1, cols=other.cols, filler=0)

            # Умножаем строку на матрицу
            for j in range(m.cols):
                for k in range(other.rows):
                    m[0, j] += self[j] * other[k, j]

            # Возвращаем матрицу умножения
            return m
        elif isinstance(other, RowAccess):
            # Второй объект это строка чей-то матрицы
            # Строку на строку умножать нельзя вызываем исключение
            raise Exception(f'Умножение строки {self} на строку {other}')

        else:
            # other - это число
            # Создаём диагональную матрицу, где на главной диагонале
            # Будет стоять это число other
            # Каждый элемент строки умножаем на это число
            D = Matrix.diag(size=1, filler=other)
            # Возвращаем матрицу умножения
            return D*self

    def __add__(self, other):
        """Сложение двух строк"""
        # oter должна быть матрицей
        if isinstance(other, Matrix):
            # Если размерности двух матриц не совпадают
            if 1 != other.rows and self.cols != other.cols:
                # Вызываем исключение
                dim1 = f'1x{self.cols}'
                dim2 = f'{other.rows}x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")
            else:
                # Создаём заготовку для результирующей матрицы
                res = Matrix(rows=1, cols=self.cols, filler=0)
                # Здесь можно быть спокойными размерости матриц совпали
                for j in range(res.cols):
                    res[0, j] = self[j] + other[0, j]

                # возвращаем результирующую матрицу
                return res
        elif isinstance(other, RowAccess):
            # Второй объект это строка чей-то матрицы
            # Если длины двух строк не совпадают
            if self.cols != other.cols:
                # Вызываем исключение
                raise Exception(f"Длины строк не совпадают {self} и {other}")
            else:
                # Создаём заготовку для результирующей матрицы
                res = Matrix(rows=1, cols=self.cols, filler=0)
                # Здесь можно быть спокойными размерости матриц совпали
                for j in range(res.cols):
                    res[0, j] = self[j] + other[j]

                # возвращаем результирующую матрицу
                return res
        else:
            # other - не матрица-строка => вызываем исключение
            raise Exception(f"{other} - НЕ матрица")

    def __sub__(self, other):
        """Операция вычитания"""
        return self + other*(-1)

    def __truediv__(self, other):
        """Операция деления"""
        return self * (1/other)

    def __eq__(self, other):
        """Переопределение операции сравнения =="""
        # если other - матрица
        if isinstance(other, Matrix):
            # У матриц должны быть равны элементы и размерности
            # Равны ли размерности
            is_dim = self.cols == other.cols and 1 == other.rows
            # Если не равны размерности, то и сравнивать элементы не нужно
            if not is_dim:
                return False
            else:
                # получаем элементы в данной строке матрицы
                elements = [self.m[self.i_row, j] for j in range(self.cols)]
                # Сравниваем элементы
                return elements == other._arr
        elif isinstance(other, RowAccess):
            # Второй объект это строка чей-то матрицы
            # Если не равны размерности, то и сравнивать элементы не нужно
            if not (self.cols == other.cols):
                return False
            else:
                # получаем элементы из двух строк
                row1 = [self.m[self.i_row, j] for j in range(self.cols)]
                row2 = [other.m[other.i_row, j] for j in range(other.cols)]
                # Сравниваем элементы
                return row1 == row2

        else:
            # other - не матрица-строка - вызываем исключение
            raise Exception(f"{other} - НЕ матрица")

    def transpose(self):
        """Транспонировать строку"""
        # Получаем элементы в строке
        row = [self.m[self.i_row, j] for j in range(self.cols)]
        # Создаём вектр столбец
        m = Matrix(row)

        # Возвращаем транспонированную матрицу
        return m

    def to_list(self):
        """Привести строку к виду списка"""
       # Получаем элементы в строке
        row = [self.m[self.i_row, j] for j in range(self.cols)]
        # Возвращаем список
        return row


class Matrix:
    """Представление математической матрицы"""

    def __init__(self, arr=None, *, to_row=False, size=None, rows=None, cols=None, filler=0):
        """При создании получает либо двухмерный либо одномерный массив"""
        # Если передали парамтр size - значит матрица КВАДРАТНАЯ
        if size:
            # Задаём количество строк
            self._rows = size
            # И столбцов матрицы
            self._cols = size
        # Иначе если заданы СТРОКИ и НЕ заданы столбцы
        elif rows and not cols:
            # то это матрица СТОЛБЕЦ
            self._rows = rows
            # то есть столбец 1ин
            self._cols = 1
        # Иначе если заданы СТОЛБЦЫ и НЕ заданы строки
        elif cols and not rows:
            # Это матрица строка
            self._rows = 1
            self._cols = cols
        # Иначе если заданы и СТРОКИ и Столбцы
        elif cols and rows:
            # Задаём количество строк
            self._rows = rows
            # И столбцов матрицы
            self._cols = cols
        # Если передали
        elif arr:
            # Смаотрим какой он двухмерный или одномерный
            # Если двухмерный
            if isinstance(arr[0], Iterable):
                # Если был передан параметр превратить его в вектор строку
                # И длина одного элемента двухмерного массива 1
                if to_row and len(arr[0]) == 1:
                    # Делаем вектор строку
                    self._rows = 1
                    self._cols = len(arr)
                else:
                    # Иначе берём размерность исходного массива
                    self._rows = len(arr)
                    self._cols = len(arr[0])
            else:
                # Если одномерный
                # Если был передан параметр превратить его в вектор строку
                if to_row:
                    self._rows = 1
                    self._cols = len(arr)
                else:
                    # Явно не указали делать матрицу вектор-строкой
                    # то делаем вектор СТОЛБЕЦ
                    self._rows = len(arr)
                    self._cols = 1
        else:
            # Не было указано ничего говорим об ошибке
            raise Exception("Не было пердано ни кол-во СТРОК, ни СТОЛБЦОВ")

        # Заполняем матрицу
        self._arr = []
        # Если передали массив или матрицу
        if arr:
            for line in arr:
                # Если строка тоже массив
                if isinstance(line, Iterable):
                    for x in line:
                        self._arr.append(x)
                else:
                    # Строка это НЕ массив
                    self._arr.append(line)
        else:
            # Если массив не был передан
            # То заполняем матрицу заполнителем filler
            self._arr = [filler for _ in range(self.rows*self.cols)]

    @property
    def rows(self):
        """Количество строк матрицы"""
        return self._rows

    @rows.setter
    def rows(self, value):
        Exception('Нельзя менять количество СТОЛБЦОВ напрямую')

    @property
    def cols(self):
        """Количество столбцов матрицы"""
        return self._cols

    @cols.setter
    def cols(self, value):
        Exception('Нельзя менять количество СТОЛБЦОВ напрямую')

    @property
    def size(self):
        """Размерность матрицы"""
        # Данное свойство есть только когда матрица квадратная
        if self.cols == self.rows:
            return self.cols
        else:
            # Столбцы и строки не равны, вызываем исключения
            raise AttributeError("rows != cols")

    @staticmethod
    def diag(size, filler=1):
        """Диагональная матрица размером size x size"""
        # Создаём матрицу заполненную нулями
        m = Matrix(size=size, filler=0)
        # Заполняем главную диагональ единичками
        for i in range(m.size):
            m[i, i] = filler

        # Возвращаем единичную матрицу
        return m

    @staticmethod
    def E(size):
        """Единичная матрица size x size"""
        return Matrix.diag(size, filler=1)

    def __len__(self):
        """Количество элементов в матрице"""
        return len(self._arr)

    def __index_from_two(self, i_row, i_col):
        """Получаенеи индекса из двух"""
        # Если индексы отрицательные, то приводим их к правильному виду:
        if i_row < 0:
            i_row = self.rows + i_row
        if i_col < 0:
            i_col = self.cols + i_col

        # Теперь нужно проверить верные индексы ли нам передали
        # Они не должны выходить за пределы
        if not(0 <= i_row < self.rows):
            raise IndexError(f"Bad row={i_row} not in [0, {self.rows-1}]")
        if not(0 <= i_col < self.cols):
            raise IndexError(f"Bad col={i_col} not in [0, {self.cols-1}]")

        # После получения строки и столбца
        # Получим индекс элемента во внутреннем одномерном представлении матрицы
        index = i_row*self.cols + i_col
        # Возвращаем индекс элемента
        return index

    def __index_from_one(self, index):
        # Проверяем если у нас матрица одномерная
        if self.rows == 1 or self.cols == 1:
            # Если индекс отрицателен, то приводим его к правильному виду
            if index < 0:
                index = len(self) + index

            # Теперь проверяем возможен ли такой индекс
            if not(0 <= index < len(self)):
                raise IndexError(f"Bad index={index} not in [0, {len(self)-1}]")
        else:
            # Если двухмерная то index - это индекс строки
            # Если индекс отрицателен, то приводим его к правильному виду
            if index < 0:
                index = self.rows + index

            # Теперь проверяем возможен ли такой индекс
            if not(0 <= index < self.rows):
                raise IndexError(f"Bad index={index} not in [0, {self.rows}]")

        # Возвращаем индекс элемента
        return index

    def __getitem__(self, coords):
        """Получение элемента матрицы"""
        # Если передали две координаты
        if isinstance(coords, tuple):
            # Переводим два индекса в одномерное представление
            index = self.__index_from_two(coords[0], coords[1])
            # Возвращаем элемент матрицы
            return self._arr[index]
        else:
            # Передали только одно число
            # На всякий случай проводим валидацию индекса
            index = self.__index_from_one(coords)
            # если матрицу можно представить как одномерный массив - столбец строка
            if self.cols == 1 or self.rows == 1:
                # Возвращаем элемент матрицы
                return self._arr[index]
            else:
                # возвращаем строку с нужным индексом
                return RowAccess(m=self, i_row=index)

    def __setitem__(self, coords, value):
        """Задать элемент матрицы"""
        # Если передали две координаты
        if isinstance(coords, tuple):
            # Переводим два индекса в одномерное представление
            index = self.__index_from_two(coords[0], coords[1])
            # Задаём элемент матрицы
            self._arr[index] = value
        else:
            # Передали только один индекс
            index = self.__index_from_one(coords)
            if isinstance(value, Matrix):
                # если value -  это матрица строка имеет нужное количество столбцов
                if value.rows == 1 and value.cols == self.cols:
                    # каждый элемент строки value, присваиваем каждому элементу
                    # строки с индексом index
                    for j in range(self.cols):
                        self[index, j] = value[0, j]
                else:
                    # Рразмерности "строк" не совпадают
                    # Вызываем исключение
                    dim1 = f'1x{self.cols}'
                    dim2 = f'{value.rows}x{value.cols}'
                    raise Exception(f'Передано {dim2}, а нужно {dim1}')
            elif isinstance(value, RowAccess):
                # Передпли строку какой-то матрицы
                # если строка value имеет нужное количество столбцов
                if value.cols == self.cols:
                    # каждый элемент строки value, присваиваем каждому элементу
                    # строки с индексом index
                    for j in range(self.cols):
                        self[index, j] = value[j]
                else:
                    # Рразмерности "строк" не совпадают
                    # Вызываем исключение
                    dim1 = f'1x{self.cols}'
                    dim2 = f'1x{value.cols}'
                    raise Exception(f'Передано {dim2}, а нужно {dim1}')

            else:
                # передали не матрицу и не строку
                # Проверяем можно ли представить матрицу одномерным массивом
                if self.cols == 1 or self.rows == 1:
                    # писваиваем элементу матрицы значение value
                    self._arr[index] = value
                else:
                    # Строке матрицы присвоили не матрицу строку
                    raise Exception(
                        f'Строке матрицы {index} присвоили не строку {value}')

    def __neg__(self):
        """Переопределение операции унарного минуса"""
        return self * (-1)

    def __mul__(self, other):
        """Операция умножение множение"""
        # Если второй объект это матрица
        if isinstance(other, Matrix):
            # Делаем проверку - количество столбцов первой должно
            # быть равно количеству столбцов второй
            if self.cols != other.rows:
                # Не равны => вызываем исключение
                # Размерность первой матрицы
                dim1 = f'{self.rows}x{self.cols}'
                dim2 = f'{other.rows}x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")

            # Создаём новую матрицу закготовку
            m = Matrix(rows=self.rows, cols=other.cols, filler=0)

            # Умножаем две матрицы
            for i in range(self.rows):
                for j in range(other.cols):
                    for k in range(self.cols):
                        m[i, j] += self[i, k] * other[k, j]

            # Возвращаем матрицу умножения
            return m
        elif isinstance(other, RowAccess):
            # Делаем проверку - количество столбцов первой должно
            # быть равно количеству строк второй
            if self.cols != 1:
                # Не равны => вызываем исключение
                # Размерность первой матрицы
                dim1 = f'{self.rows}x{self.cols}'
                dim2 = f'1x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")

            # Создаём новую матрицу закготовку
            m = Matrix(rows=self.rows, cols=other.cols, filler=0)

            # Умножаем две матрицы
            for i in range(m.rows):
                for j in range(m.cols):
                    m[i, j] += self[i, 0] * other[j]

            # Возвращаем матрицу умножения
            return m
        else:
            # other - это число
            # Создаём диагональную матрицу, где на главной диагонале
            # Будет стоять это число other
            D = Matrix.diag(size=self.rows, filler=other)
            # Возвращаем матрицу умножения
            return D*self

    def __add__(self, other):
        """Сложение двух матриц"""
        # oter должны быть матрицей
        if isinstance(other, Matrix):
            # Если размерности двух матриц не совпадают
            if self.rows != other.rows and self.cols != other.cols:
                # Вызываем исключение
                dim1 = f'{self.rows}x{self.cols}'
                dim2 = f'{other.rows}x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")
            else:
                # Создаём заготовку для результирующей матрицы
                res = Matrix(rows=self.rows, cols=self.cols, filler=0)
                # Здесь можно быть спокойными размерости матриц совпали
                for i in range(res.rows):
                    for j in range(res.cols):
                        res[i, j] = self[i, j] + other[i, j]

                # возвращаем результирующую матрицу
                return res
        elif isinstance(other, RowAccess):
            # Если размерности двух матриц не совпадают
            if self.rows != 1 and self.cols != other.cols:
                # Вызываем исключение
                dim1 = f'{self.rows}x{self.cols}'
                dim2 = f'1x{other.cols}'
                raise Exception(f"неверные размерности матриц {dim1} и {dim2}")
            else:
                # Создаём заготовку для результирующей матрицы
                res = Matrix(rows=1, cols=self.cols, filler=0)
                # Здесь можно быть спокойными размерости матриц совпали
                for j in range(res.cols):
                    res[0, j] = self[0, j] + other[j]

                # возвращаем результирующую матрицу
                return res
        else:
            # other - не матрица - вызываем исключение
            raise Exception(f"{other} - НЕ матрица")

    def __sub__(self, other):
        """Операция вычитания"""
        return self + other*(-1)

    def __truediv__(self, other):
        """Операция деления"""
        return self * (1/other)

    def __eq__(self, other):
        """Переопределение операции сравнения =="""
        # если other - матрица
        if isinstance(other, Matrix):
            # У матриц должны быть равны элементы и размерности
            # Равны ли размерности
            is_dim = self.cols == other.cols and self.rows == other.rows
            # Если не равны размерности, то и сравнивать элементы не нужно
            if not is_dim:
                return False
            else:
                # Сравниваем элементы
                return self._arr == other._arr
        elif isinstance(other, RowAccess):
            # У матриц должны быть равны элементы и размерности
            # Равны ли размерности
            is_dim = self.cols == other.cols and self.rows == 1
            # Если не равны размерности, то и сравнивать элементы не нужно
            if not is_dim:
                return False
            else:
                # Получаем значение элементов в строке other
                row = [other.m[other.i_row, j] for j in range(other.cols)]
                # Сравниваем элементы
                return self._arr == row
        else:
            # other - не матрица - вызываем исключение
            raise Exception(f"{other} - НЕ матрица")

    def __str__(self):
        """Строковое представление матрицы"""
        str_res = ''
        for i in range(self.rows):
            str_row = ''
            for j in range(self.cols):
                # Если элемент матрицы - это СТРОКА
                if isinstance(self[i, j], str):
                    str_row += f"{self[i, j]:^6}"
                else:
                    # Не строка а число
                    str_row += f'{self[i, j]:6.2f}'
            # Добавляем скобочки к строке
            str_row = f'|{str_row}|'
            # и переход на следующую строку
            str_res += str_row + '\n'

        # Возвращаем строковое представление матрицы
        return str_res

    def transpose(self):
        """Транспонировать матрицу"""
        # Создаём матрицу заготовку
        m = Matrix(rows=self.cols, cols=self.rows)
        # Обходим столбцы исходной матрицы
        for j in range(self.cols):
            # Обходим строки исходной матрицы
            for i in range(self.rows):
                # Заполняем матрицу
                m[j, i] = self[i, j]

        # Возвращаем транспонированную матрицу
        return m

    def to_list(self):
        """Привести матрицу к виду списка"""
        # Заготовка под список
        l = []
        # Если строк больне одной
        if self.rows > 1:
            for i in range(self.rows):
                # Если столбццов больше одного
                if self.cols > 1:
                    # заготовка под строку
                    row = []
                    for j in range(self.cols):
                        row.append(self[i, j])
                    l.append(row)
                else:
                    # Всего один элемент в строке
                    l.append(self[i, 0])
        else:
            # Строка всего одна
            for j in range(self.cols):
                l.append(self[0, j])

        # Возвращаем матрицу в виде массива
        return l


def to_valid_diag(A: Matrix, Y: Matrix):
    """Привести систему уравнений A*X=Y к валидному виду"""
    # Чтобы бе проблем в методе Гаусса приводить матрицу к треугольному виду
    # нужно чтобы все диаголнальные элементы матрицы A - были не нулевыми

    # Чтобы случайно перезаписать передаваемые матрицу и вектор
    # Сделаем их локальные копии
    A = deepcopy(A)
    Y = deepcopy(Y)

    # размер матрицы A и столбца Y
    size = len(Y)

    # Обходим диагональные элементы матрицы A
    for i in range(size):
        # Если диагональный элемент матрицы нулевой
        if A[i, i] == 0:
            # обходим весь i-ый столбец
            for i_non_zero in range(size):
                # Чтобы найти номер строки в которой
                # попадётся неннулевой элемент
                if A[i_non_zero, i] != 0:
                    break
            # складываем текущую i-ую строку со строкой, где ненулевой элемент
            # Для матрицы A
            A[i] += A[i_non_zero]
            # для столбца Y
            Y[i] += Y[i_non_zero]

    # Возвращаем матрицу A и Y, приведённые к валидному виду
    return A, Y


def triangulate(A: Matrix, Y: Matrix):
    """Привести систему уравнений A*X=Y к треугольному виду"""
    # Приводим систему к валидному виду
    A, Y = to_valid_diag(A, Y)

    # размер матрицы A и столбца Y
    size = len(Y)

    # Перебираем все строки матрицы
    for j in range(size):
        k = A[j, j]
        # В j-ой строке A[j, j] - точно НЕ равно 0
        # Делим всю строку на этот коэффициент
        A[j] /= k
        Y[j] /= k
        # Для всех последующих строк
        for i in range(j+1, size):
            k = A[i, j]
            # Если k = 0 то в нужной позиции уже стоит 0 и ничего делать не надо
            if k != 0:
                # в i-ой строке делим всю строку на коэффициент стоящий при
                # елементе A[i, j], чтобы в этой позиции получить 1-у
                A[i] /= k
                Y[i] /= k

                # Теперь из i-ой строки вычитаем j-ую строку
                # Чтобы получить 0 в позиции A[i][j]
                A[i] -= A[j]
                Y[i] -= Y[j]

    # Воазвращаем систему приведённую к треугольному виду
    return A, Y


def find_with_gauss(A: Matrix, Y: Matrix):
    """
    Найти решение системы уравнений при помощи метода Гаусса
    A*X=Y -> возвращает вектор столбец X
    """
    # Приводим систему к треугольному виду
    A, Y = triangulate(A, Y)
    # размер матрицы A и столбца Y
    size = len(Y)
    # Возвращаемый вектор столбец X, предварительно заполняем его нулями
    X = Matrix(cols=1, rows=size, filler=0)
    # Начиная с последней строки, двигаясь вверх собираем вектор X
    for i in range(size-1, -1, -1):
        # Временная переменная для хранения значения i-го элемента столбца X
        # Сразу записываем туда элемент Y[i], т.к. в матрице A элемент A[i][i] = 1
        temp = Y[i]
        # Проходим все оставшиеся столбцы в строке
        for j in range(i+1, size):
            # Раскрываем линейную последовательность
            temp -= A[i, j]*X[j]

        # Записываем i-ый элемент массива X
        X[i] = temp

    # Возвращаем искомый вектор столбец X
    return X
