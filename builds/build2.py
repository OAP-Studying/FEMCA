#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль показывает, как собрать модель конструкции и сохранить её  файл
ДЗ Ерахтина Артёма РКТ2-81
"""
import sys
from pathlib import Path
# Абсолютной путь до основной директории
main_dir = Path(__file__).resolve().parent.parent
# Добавляем её в путь поиска модулей
sys.path.append(str(main_dir))

from fem_tools import Force
from fem_tools import Distance
from fem_tools import FEMComput
from fem_tools import save_model
from fem_tools import LineStructure

# Имя модели
name_model = 'model2'
# Абсолютный путь до файла модели
file_model = f'{main_dir}/models/{name_model}.txt'
# Файл результатов
file_res = f'{main_dir}/results/{name_model}_res.txt'
# Комментарий к модели и расчётам
comment = "ДЗ Ерахтина Артёма РКТ2-81"


def main():
    # Модуль Юнга
    E = 1
    # Площадь поперечного сечения
    A = 1
    # Длина элемента
    L = 1
    # Жёсткость пружинки
    C = 2*E*A/L
    # Первое усилие в конструкции
    F1 = 2*E*A
    # Второе усилие в конструкции
    F2 = 3*E*A

    # Начинаем построения
    # Заготовка - пустая конструкция
    line_struct = LineStructure()
    # Добавляем первый стержень
    rod1 = line_struct.add_rod(E=E, A=A, D=Distance(L))
    # К правому узлу стержня rod1 добавляем еще один элемент стержень
    rod2 = line_struct.add_rod(E=E, A=A, n1=rod1.n2, D=Distance(L))
    # К правому узлу стержня rod1 добавляем последний стержень
    rod3 = line_struct.add_rod(E=E, A=A, n1=rod2.n2, D=Distance(L))
    # К правому узлу стержня rod1 добавляем пружинку, длина в противополоную сторону
    spring1 = line_struct.add_spring(C=C, n1=rod1.n2, D=Distance(-L))

    # Добавляем закрепление конструкции
    # К полседнему узлу - узлу node2 пружинки
    line_struct.add_pinning(spring1.n2)
    # к третьему узлу - правому узлу стержня rod3
    rod3.n2.add_pinning()

    # Добавляем усилия к конструкции
    # В левом узле стержня rod1 точечную силу F1
    line_struct.add_point_force(rod1.n1, Force(F1))
    # В правом узле стержня rod2 точечную силу F2
    rod2.n2.add_point_force(Force(F2))

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(line_struct)

    # Сохраняем файл нашей модели
    save_model(line_struct, file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
