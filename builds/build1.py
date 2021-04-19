#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль показывает, как собрать модель конструкции и сохранить её  файл
ДЗ Серебрянникова Олега РКТ2-81
"""
import sys
from pathlib import Path
# Абсолютной путь до основной директории
main_dir = Path(__file__).resolve().parent.parent
# Добавляем её в путь поиска модулей
sys.path.append(str(main_dir))


from fem_tools import Beam
from fem_tools import FEMComput

# Имя модели
name_model = 'model1'
# Абсолютный путь до файла модели
file_model = f'{main_dir}/models/{name_model}.txt'
# Файл результатов
file_res = f'{main_dir}/results/{name_model}_res.txt'
# Комментарий к модели и расчётам
comment = "ДЗ Серебрянникова Олега РКТ2-81"


def main():
    # Модуль Юнга
    E = 1
    # Площадь поперечного сечения
    F = 1
    # Длина элемента
    L = 1
    # Жёсткость пружинки
    C = 2*E*F/L
    # Первое усилие в конструкции
    F1 = 2*E*F
    # Второе усилие в конструкции
    F2 = 3*E*F

    # Начинаем построения
    # Заготовка - пустая конструкция
    beam = Beam()
    # Добавляем первый стержень к конструкции
    rod1 = beam.add_rod(E=E, F=F, L=L)
    # К правому узлу стержня rod1 добавляем еще один элемент стержень
    rod2 = beam.add_rod(E=E, F=F, n1=rod1.node2, L=L)
    # К правому узлу стержня rod2 добавляем еще один элемент стержень
    rod3 = beam.add_rod(E=E, F=F, n1=rod2.node2, L=L)
    # К правому узлу стержня rod2 добавляем пружинку
    spring1 = beam.add_spring(C=C, n1=rod2.node2, L=L)

    # Добавляем закрепление конструкции
    # К левому узлу стержня rod1
    beam.add_pinning(rod1.node1)
    # К правому узлу пружинки
    spring1.node2.add_pinning()

    # Добавляем усилия к конструкции
    # Прикладываем в правом узле стержня rod1 силу F1
    beam.add_point_force(rod1.node2, -F1)
    # в правом узле стержня rod3 добавляем точечну силу F2
    rod3.node2.add_point_force(F2)

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)

    # Сохраняем файл нашей модели
    beam.save(file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
