# -*- coding: utf-8 -*-
"""
Тесты на сохранение и загрузку модели
Идея тестов простая - модель, которую сохранили,
при загрузке из файла должна получиться точно такой же
и результаты вычислений должны получиться такие же
"""
import unittest
import os
import random
from fem import LineStructure, Distance, Force
from fem import FEMComput
from fem import load_model, save_model


class TestSaveLoad(unittest.TestCase):
    """Тестирование на сохранение и загрузку моделей"""

    def setUp(self):
        # Файлы для конструкции собираемой кодом на питоне
        self.f_model1 = 'model1.txt'
        self.f_res1 = 'res1.txt'
        # Файлы для конструкции загружаемой из self.f_model1
        self.f_model2 = 'model2.txt'
        self.f_res2 = 'res1.txt'

    def tearDown(self):
        # Удаляем мусорные файлы после тестов
        trash = [self.f_model1, self.f_res1, self.f_model2, self.f_res2]
        for file in trash:
            if os.path.exists(file):
                os.remove(file)

    def test_oleg_model(self):
        """Проверки конструкции Олегатора"""
        # Модуль Юнга
        E = 1
        # Площадь поперечного сечения
        A = 1
        # Длина элемента
        L = 1
        # Жёсткость пружинки
        C = 2 * E * A / L
        # Первое усилие в конструкции
        F1 = 2 * E * A
        # Второе усилие в конструкции
        F2 = 3 * E * A

        # Начинаем построения
        # Заготовка - пустая конструкция
        ls1 = LineStructure()
        # Добавляем первый стержень к конструкции
        rod1 = ls1.add_rod(E=E, A=A, D=Distance(L))
        # К правому узлу стержня rod1 добавляем еще один элемент стержень
        rod2 = ls1.add_rod(E=E, A=A, n1=rod1.n2, D=Distance(L))
        # К правому узлу стержня rod2 добавляем еще один элемент стержень
        rod3 = ls1.add_rod(E=E, A=A, n1=rod2.n2, D=Distance(L))
        # К правому узлу стержня rod2 добавляем пружинку
        spring1 = ls1.add_spring(C=C, n1=rod2.n2, D=Distance(L))

        # Добавляем закрепление конструкции
        # К левому узлу стержня rod1
        ls1.add_pinning(rod1.n1)
        # К правому узлу пружинки
        spring1.n2.add_pinning()

        # Добавляем усилия к конструкции
        # Прикладываем в правом узле стержня rod1 силу F1
        ls1.add_point_force(rod1.n2, Force(-F1))
        # в правом узле стержня rod3 добавляем точечну силу F2
        rod3.n2.add_point_force(Force(F2))

        # Сохраняем файл нашей модели
        save_model(ls1, self.f_model1)

        # Загружаем конструкцию из файла
        ls2 = load_model(self.f_model1)
        # Сохраняем загруженую модель
        save_model(ls2, self.f_model2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_model1, 'r', encoding='utf8')
        cont2 = open(self.f_model2, 'r', encoding='utf8')

        # Первая проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы моделей должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

        # Начинаем расчёты
        # Отдельные объекты для расчёта конструкции
        comp1 = FEMComput(ls1)
        comp2 = FEMComput(ls2)

        # Сохраняем результаты вычислений обеих моделей
        comp1.save_results(self.f_res1)
        comp2.save_results(self.f_res2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_res1, 'r', encoding='utf8')
        cont2 = open(self.f_res2, 'r', encoding='utf8')

        # ВТОРАЯ проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы результатов должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

    def test_artem_model(self):
        """Проверки конструкции Артёма"""
        # Модуль Юнга
        E = 1
        # Площадь поперечного сечения
        A = 1
        # Длина элемента
        L = 1
        # Жёсткость пружинки
        C = 2 * E * A / L
        # Первое усилие в конструкции
        F1 = 2 * E * A
        # Второе усилие в конструкции
        F2 = 3 * E * A

        # Начинаем построения
        # Заготовка - пустая конструкция
        ls1 = LineStructure()
        # Добавляем первый стержень
        rod1 = ls1.add_rod(E=E, A=A, D=Distance(L))
        # К правому узлу стержня rod1 добавляем еще один элемент стержень
        rod2 = ls1.add_rod(E=E, A=A, n1=rod1.n2, D=Distance(L))
        # К правому узлу стержня rod1 добавляем последний стержень
        rod3 = ls1.add_rod(E=E, A=A, n1=rod2.n2, D=Distance(L))
        # К правому узлу стержня rod1 добавляем пружинку, длина в противополоную сторону
        spring1 = ls1.add_spring(C=C, n1=rod1.n2, D=Distance(-L))

        # Добавляем закрепление конструкции
        # К полседнему узлу - узлу node2 пружинки
        ls1.add_pinning(spring1.n2)
        # к третьему узлу - правому узлу стержня rod3
        rod3.n2.add_pinning()

        # Добавляем усилия к конструкции
        # В левом узле стержня rod1 точечную силу F1
        ls1.add_point_force(rod1.n1, Force(F1))
        # В правом узле стержня rod2 точечную силу F2
        rod2.n2.add_point_force(Force(F2))

        # Сохраняем файл нашей модели
        save_model(ls1, self.f_model1)

        # Загружаем конструкцию из файла
        ls2 = load_model(self.f_model1)
        # Сохраняем загруженую модель
        save_model(ls2, self.f_model2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_model1, 'r', encoding='utf8')
        cont2 = open(self.f_model2, 'r', encoding='utf8')

        # Первая проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы моделей должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

        # Начинаем расчёты
        # Отдельные объекты для расчёта конструкции
        comp1 = FEMComput(ls1)
        comp2 = FEMComput(ls2)

        # Сохраняем результаты вычислений обеих моделей
        comp1.save_results(self.f_res1)
        comp2.save_results(self.f_res2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_res1, 'r', encoding='utf8')
        cont2 = open(self.f_res2, 'r', encoding='utf8')

        # ВТОРАЯ проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы результатов должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

    def test_alice_model(self):
        """Проверки конструкции Алисы"""
        # Модуль Юнга
        E = 1
        # Площадь поперечного сечения
        A = 1
        # Длина элемента
        L = 1
        # Жёсткость пружинки
        C = 2 * E * A / L
        # Точечное усилие в конструкции
        F1 = 2 * E * A
        # Максимальная нагрузка в треугольной рспределённой
        q2 = E * A / L

        # Начинаем построения
        # Заготовка - пустая конструкция
        ls1 = LineStructure()
        # Собираем конструкцию, добавляем пружинку
        spring1 = ls1.add_spring(C=2 * C, D=Distance(L))
        # Дальше наращиваем стержень
        rod1 = ls1.add_rod(E=E, A=A, n1=spring1.n2, D=Distance(L))
        # Еще один
        rod2 = ls1.add_rod(E=E, A=A, n1=rod1.n2, D=Distance(L))
        # 3-ий стержень
        rod3 = ls1.add_rod(E=E, A=A, n1=rod2.n2, D=Distance(L))
        # В конце добавляем пружинку
        spring2 = ls1.add_spring(C=C, n1=rod3.n2, D=Distance(L))

        # Добавляем закрепление конструкции
        # Получаем нулевой узел конструкции
        # В левом узле пружинки 1
        ls1.add_pinning(spring1.n1)
        # К последнему узлу - правому пружинки 2
        spring2.n2.add_pinning()

        # Добавляем точечные усилия к конструкции
        # Прикладываем в 2-ом узле - правом узле стержня rod1 силу F1
        ls1.add_point_force(rod1.n2, Force(-F1))
        # или
        # rod1.node2.add_point_force(Force(-F1))

        # Добавляем распределённые усилия
        # К стержню 2 добавляем треугольную распределённую нагрузку
        ls1.add_linear_distributed_force(rod2, q1=0, q2=q2)
        # или
        # rod2.add_linear_distributed_force(q1=Force(0), q2=Force(q2))

        # Сохраняем файл нашей модели
        save_model(ls1, self.f_model1)

        # Загружаем конструкцию из файла
        ls2 = load_model(self.f_model1)
        # Сохраняем загруженую модель
        save_model(ls2, self.f_model2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_model1, 'r', encoding='utf8')
        cont2 = open(self.f_model2, 'r', encoding='utf8')

        # Первая проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы моделей должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

        # Начинаем расчёты
        # Отдельные объекты для расчёта конструкции
        comp1 = FEMComput(ls1)
        comp2 = FEMComput(ls2)

        # Сохраняем результаты вычислений обеих моделей
        comp1.save_results(self.f_res1)
        comp2.save_results(self.f_res2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_res1, 'r', encoding='utf8')
        cont2 = open(self.f_res2, 'r', encoding='utf8')

        # ВТОРАЯ проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы результатов должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

    def test_random_model(self):
        """Тестирование рандомной конструкции"""
        # Модуль Юнга
        E = 1
        # Площадь поперечного сечения
        A = 1
        # Длина элемента
        L = 1
        # Жёсткость пружинки
        C = 1
        # Точечное усилие в конструкции
        F = 1
        # нагрузки в распределёнке
        q1 = 1
        q2 = 1

        # Заготовка конструкции
        ls1 = LineStructure()

        # рандомно выбираем с чего начинаем конструкцию стержень или пружинка
        answer = random.choice(['rod', 'spring'])
        if answer == 'rod':
            # Коэффициенты констант
            Ek = random.randint(1, 4)
            Ak = random.randint(1, 4)
            Lk = random.randint(1, 2)
            ls1.add_rod(E * Ek, A * Ak, D=Distance(L * Lk))
        else:
            # Коэффициенты констант
            Ck = random.randint(1, 5)
            Lk = random.randint(1, 2)
            ls1.add_spring(C * Ck, D=Distance(L * Lk))

        # Дальше добавляем от 2 до 4 элементов рандомно
        for _ in range(random.randint(2, 4)):
            # Получаем последний элемент из массива элементов
            el = ls1.items[-1]
            # рандомно выбираем что добавляем стержень или пружину
            answer = random.choice(['rod', 'spring'])
            if answer == 'rod':
                # Коэффициенты констант
                Ek = random.randint(1, 4)
                Ak = random.randint(1, 4)
                Lk = random.randint(1, 2)
                # Начальный узел элемента - это последний узел в конструкции
                n1 = el.n2
                ls1.add_rod(E * Ek, A * Ak, n1=n1, D=Distance(L * Lk))
            else:
                # Коэффициенты констант
                Ck = random.randint(1, 5)
                Lk = random.randint(1, 2)
                # Начальный узел элемента - это последний узел в конструкции
                n1 = el.n2
                ls1.add_spring(C * Ck, n1=n1, D=Distance(L * Lk))

        # Добавялем заделки в начало и в конец конструкции
        ls1.items[0].n1.add_pinning()
        ls1.items[-1].n2.add_pinning()

        # Добавялем нагрузки к узлам элементов
        # Получаем все узлы где нет заделок
        grid = []
        for node in ls1.grid:
            # Если в узле нет заделки добавляем его
            if not (node.u == 0 and node.v == 0):
                grid.append(node)

        # Теперь выбираем рандомные два элемента из списка узлов
        # сначала перемешиваем этот массив узлов
        random.shuffle(grid)
        # Получаем два узла
        n1 = grid.pop(0)
        n2 = grid.pop(0)

        # В них добавляем рандомные силы
        ls1.add_point_force(n1, Force(F * random.randint(-2, 4)))
        ls1.add_point_force(n2, Force(F * random.randint(-2, 4)))

        # Выбираем сколько раз будем накладывать на конструкцию распределёнку
        # от одного до двух раз
        for _ in range(random.randint(1, 2)):
            # Выбираем рандомный элемент из конструкции
            el = random.choice(ls1.items)
            # Коэффициенты при нагрузках
            q1k = random.randint(-1, 2)
            q2k = random.randint(-1, 2)
            el.add_linear_distributed_force(Force(q1 * q1k), Force(q2 * q2k))

        # Сохраняем файл нашей модели
        save_model(ls1, self.f_model1)

        # Загружаем конструкцию из файла
        ls2 = load_model(self.f_model1)
        # Сохраняем загруженую модель
        save_model(ls2, self.f_model2)

        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_model1)
        cont2 = open(self.f_model2)

        # Первая проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы моделей должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()

        # Начинаем расчёты
        # Отдельные объекты для расчёта конструкции
        comp1 = FEMComput(ls1)
        comТо
        есть
        все
        строки
        должны
        быть
        одинаковыми
        cont1 = open(self.f_res1)
        cont2 = open(self.f_res2)

        # ВТОРАЯ проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы результатов должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()
        # Полученные два файла должны быть одинаковыми
        # То есть все строки должны быть одинаковыми
        cont1 = open(self.f_res1)
        cont2 = open(self.f_res2)

        # ВТОРАЯ проверка, построчно проверяем файлы
        # Считываем за раз строку из первого файла
        i = 0
        for line1 in cont1:
            # Считываем также строку и из второго файла
            line2 = cont2.readline()
            i += 1
            msg = f'[строка {i}] Файлы результатов должны быть одинаковыми'
            self.assertEqual(line1, line2, msg)

        # Закрываем открытые файлы
        cont1.close()
        cont2.close()


if __name__ == '__main__':
    unittest.main()
