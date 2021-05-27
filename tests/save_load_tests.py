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
        comp2 = FEMComput(ls2)

        # Сохраняем результаты вычислений обеих моделей
        comp1.save_results(self.f_res1)
        comp2.save_results(self.f_res2)

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
        comp2 = FEMComput(ls2)

        # Сохраняем результаты вычислений обеих моделей
        comp1.save_results(self.f_res1)
        comp2.save_results(self.f_res2)

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

