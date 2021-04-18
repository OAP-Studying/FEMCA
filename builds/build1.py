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
    # Добавляем первый стержень
    node1 = beam.add_rod(E=E, F=F, L=L)
    # К первому ущлу добавляем следующую часть
    node2 = beam.add_rod(E=E, F=F, n1=node1, L=L)
    # Ко второму узлу добавяем последний стержень
    node3 = beam.add_rod(E=E, F=F, n1=node2, L=L)
    # Ко второму узлу добавляем пружинку
    node4 = beam.add_spring(C=C, n1=node2, L=L)

    # Добавляем закрепление конструкции
    # Получаем нулевой узел конструкции
    node0 = beam.nodes[0]
    # добавляем к нему закрепление
    beam.add_pinning(node0)
    # К последнему узлу: 4-ому
    beam.add_pinning(node4)

    # Добавляем усилия к конструкции
    # Прикладываем в 1-ом узле силу F1
    beam.add_point_force(node1, -F1)
    # В третьем узле добавляем точечну силу F2
    beam.add_point_force(node3, F2)

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)

    # Сохраняем файл нашей модели
    beam.save(file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
