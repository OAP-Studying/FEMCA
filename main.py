#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main - главный модуль приложения
в него подключаются рукописные вспомательные модули
и решается пример домашего задания
"""
import sys
import os
from fem import FEMComput
from fem import load_model
from fem import save_model_nastran


def solve(file_model):
    """Решить модель из файла"""
    # Загружаем модель конструкции из файла
    beam = load_model(file_model)
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)
    # Выводим результаты расчёта
    comp.display_results()


if __name__ == "__main__":
    # Если в коммандной строке ввели не только имя программы
    if len(sys.argv) > 1:
        # Запускаем графический интерфейс?
        if '-n' in sys.argv:
            sys.argv.remove('-n')
            sys.argv.pop(0)
            file_model = sys.argv[0]
            if os.path.exists(file_model):
                # сохраяняем в формат настрана
                ls = load_model(file_model)
                nas_model = os.path.splitext(
                    os.path.basename(file_model))[0] + '.dat'
                save_model_nastran(ls, nas_model)
        else:
            # Если здесь, то нужно делать расчёт
            # Получаем имя файла модели
            file_model = sys.argv[1]
            # Проверяем существует ли такой файл
            if os.path.exists(file_model):
                # Решаем модель из файла
                solve(file_model)
            else:
                # Файла не существует выводим сообщение об ошибке
                print(f'Файла\n{os.path.abspath(file_model)}\nНЕ существует')
