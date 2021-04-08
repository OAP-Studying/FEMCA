#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль показывает, как собрать модель конструкции и сохранить её  файл
ДЗ Вдовиной Алисы РКТ2-81
"""
import sys
from pathlib import Path
# Абсолютной путь до основной директории
main_dir = Path(__file__).resolve().parent.parent
# Добавляем её в путь поиска модулей
sys.path.append(str(main_dir))


from fem_tools.calc import FEMComput
from fem_tools.structure import Beam

# Имя модели
name_model = 'model3'
# Абсолютный путь до файла модели
file_model = f'{main_dir}/models/{name_model}.txt'
# Файл результатов
file_res = f'{main_dir}/results/{name_model}_res.txt'
# Комментарий к модели и расчётам
comment = "ДЗ Вдовиной Алисы РКТ2-81"


def main():
    # Модуль Юнга
    E = 1
    # Площадь поперечного сечения
    F = 1
    # Длина элемента
    L = 1
    # Жёсткость пружинки
    C = 2*E*F/L
    # Точечное усилие в конструкции
    F1 = 2*E*F
    # Максимальная нагрузка в треугольной рспределённой
    q2 = E*F/L

    # Начинаем построения
    # Заготовка - пустая конструкция
    beam = Beam()
    # Собираем конструкцию, добавляем пружинку
    node1 = beam.add_spring(C=2*C, L=L)
    # Дальше наращиваем стержень
    node2 = beam.add_rod(E=E, F=F, n1=node1, L=L)
    # Еще один
    node3 = beam.add_rod(E=E, F=F, n1=node2, L=L)
    # 3-ий стержень
    node4 = beam.add_rod(E=E, F=F, n1=node3, L=L)
    # В конце добавляем пружинку
    node5 = node1 = beam.add_spring(C=C, n1=node4, L=L)

    # Добавляем закрепление конструкции
    # Получаем нулевой узел конструкции
    node0 = beam.nodes[0]
    # добавляем к нему закрепление
    beam.add_pinning(node0)
    # К последнему узлу: 5-ому
    beam.add_pinning(node5)

    # Добавляем точечные усилия к конструкции
    # Прикладываем в 2-ом узле силу F1
    beam.add_point_force(node2, -F1)

    # Добавляем распределённые усилия
    # Получаем второй элемент конструкции
    el = beam.elements[2]
    # К этому элементу добавляем треугольную распределённую нагрузку
    beam.add_linear_distributed_force(el, q1=0, q2=q2)

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)

    # Сохраняем файл нашей модели
    beam.save(file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
