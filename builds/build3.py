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


from fem_tools import Beam
from fem_tools import FEMComput

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
    spring1 = beam.add_spring(C=2*C, L=L)
    # Дальше наращиваем стержень
    rod1 = beam.add_rod(E=E, F=F, n1=spring1.node2, L=L)
    # Еще один
    rod2 = beam.add_rod(E=E, F=F, n1=rod1.node2, L=L)
    # 3-ий стержень
    rod3 = beam.add_rod(E=E, F=F, n1=rod2.node2, L=L)
    # В конце добавляем пружинку
    spring2 = beam.add_spring(C=C, n1=rod3.node2, L=L)

    # Добавляем закрепление конструкции
    # Получаем нулевой узел конструкции
    # В левом узле пружинки 1
    beam.add_pinning(spring1.node1)
    # К последнему узлу - правому пружинки 2
    spring2.node2.add_pinning()

    # Добавляем точечные усилия к конструкции
    # Прикладываем в 2-ом узле - правом узле стержня rod1 силу F1
    beam.add_point_force(rod1.node2, -F1)
    # или
    # rod1.node2.add_point_force(-F1)

    # Добавляем распределённые усилия
    # К стержню 2 добавляем треугольную распределённую нагрузку
    beam.add_linear_distributed_force(rod2, q1=0, q2=q2)
    # или
    # rod2.add_linear_distributed_force(q1=0, q2=q2)

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(beam)

    # Сохраняем файл нашей модели
    beam.save(file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
