#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main - главный модуль приложения
в него подключаются рукописные вспомательные модули
и решается пример домашего задания
"""
import sys
import os
from fem_tools import Beam
from fem_tools import FEMComput
from fem_tools import load_model
from time import time


def solve(file_model):
    """Решить модель из файла"""
    # Загружаем модель конструкции из файла
    beam = load_model(file_model)
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)
    # Выводим результаты расчёта
    comp.display_results()


def run_speed_test(file_model='models/model_test.txt'):
    """Запустить тест скрости вычисления"""
    # Загружаем тестовую модуль из файла
    beam = load_model(file_model)

    print(f'Количество узлов     : {beam.cnt_nodes}')
    print(f'Количество элементов : {beam.cnt_elements}')
    print('-'*30)

    comp = FEMComput(beam)
    # Вводим граничные условия методом Пиано-Айронса
    comp.enter_boundary_conditions()

    # Расчёт методом Гаусса
    start = time()
    comp.find_q(method='gauss', recalculate=True)
    gauss_time = time() - start
    print(f'Метод Гаусса       : {gauss_time:.3f}')

    # Ресчет с обратной матрицей
    start = time()
    comp.find_q(method='inv', recalculate=True)
    inv_time = time() - start
    print(f'C обратной матрицей: {inv_time:.3f}')

    print("-"*30)
    if gauss_time == inv_time:
        print('Оба метода работают с одинаковой скоростью')
    elif gauss_time < inv_time:
        print("Метод Гаусса работает быстрее")
    else:
        print('Обратная матрица работает быстрее')


if __name__ == "__main__":
    # Если в коммандной строке ввели не только имя программы
    if len(sys.argv) > 1:
        # Тестируем конструкцию?
        if 'test' in sys.argv:
            # Если ввели имя файла конструкции
            if len(sys.argv) > 2:
                # Удаляем ненужные параметры
                sys.argv.pop(0)
                sys.argv.pop(sys.argv.index('test'))
                # Теперь точно имя файла будет на нулевом месте в массиве
                file_model = sys.argv[0]
                # Если файл существует
                if os.path.exists(file_model):
                    # Запускаем тест
                    run_speed_test(file_model)
                else:
                    # Файла не существует выводим сообщение об ошибке
                    print(
                        f'Файла\n{os.path.abspath(file_model)}\nНЕ существует')
            else:
                # Файл для тестов не ввели, значит запускам стандартный
                print("Стандартный тест")
                run_speed_test()

        else:
            # Если здесь, то нужно делать расчёт, а не тесты
            # Получаем имя файла модели
            file_model = sys.argv[1]
            # Проверяем существует ли такой файл
            if os.path.exists(file_model):
                # Решаем модель из файла
                solve(file_model)
            else:
                # Файла не существует выводим сообщение об ошибке
                print(f'Файла\n{os.path.abspath(file_model)}\nНЕ существует')
