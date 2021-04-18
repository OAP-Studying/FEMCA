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


def solve(file_model):
    """Решить модель из файла"""
    # Заготовка - пустая конструкция
    beam = Beam()
    # Загружаем модель конструкции из файла
    beam.load(file_model)
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)
    # Выводим результаты расчёта
    comp.display_results()


if __name__ == "__main__":
    # Если в коммандной строке ввели не только имя программы
    if len(sys.argv) > 1:
        # Получаем имя файла модели
        file_model = sys.argv[1]
    else:
        file_model = input('Введите путь до файла модели: ')

    # Проверяем существует ли такой файл
    if os.path.exists(file_model):
        # Решаем модель из файла
        solve(file_model)
    else:
        # Файла не существует выводим сообщение об ошибке
        print(f'Файла\n{os.path.abspath(file_model)}\nНЕ существует')
