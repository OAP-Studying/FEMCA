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

from fem import Force
from fem import Distance
from fem import FEMComput
from fem import save_model
from fem import LineStructure


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
    A = 1
    # Длина элемента
    L = 1
    # Жёсткость пружинки
    C = 2*E*A/L
    # Точечное усилие в конструкции
    F1 = 2*E*A
    # Максимальная нагрузка в треугольной рспределённой
    q2 = E*A/L

    # Начинаем построения
    # Заготовка - пустая конструкция
    line_struct = LineStructure()
    # Собираем конструкцию, добавляем пружинку
    spring1 = line_struct.add_spring(C=2*C, D=Distance(L))
    # Дальше наращиваем стержень
    rod1 = line_struct.add_rod(E=E, A=A, n1=spring1.n2, D=Distance(L))
    # Еще один
    rod2 = line_struct.add_rod(E=E, A=A, n1=rod1.n2, D=Distance(L))
    # 3-ий стержень
    rod3 = line_struct.add_rod(E=E, A=A, n1=rod2.n2, D=Distance(L))
    # В конце добавляем пружинку
    spring2 = line_struct.add_spring(C=C, n1=rod3.n2, D=Distance(L))

    # Добавляем закрепление конструкции
    # Получаем нулевой узел конструкции
    # В левом узле пружинки 1
    line_struct.add_pinning(spring1.n1)
    # К последнему узлу - правому пружинки 2
    spring2.n2.add_pinning()

    # Добавляем точечные усилия к конструкции
    # Прикладываем в 2-ом узле - правом узле стержня rod1 силу F1
    line_struct.add_point_force(rod1.n2, Force(-F1))
    # или
    # rod1.node2.add_point_force(Force(-F1))

    # Добавляем распределённые усилия
    # К стержню 2 добавляем треугольную распределённую нагрузку
    line_struct.add_linear_distributed_force(rod2, q1=0, q2=q2)
    # или
    # rod2.add_linear_distributed_force(q1=0, q2=q2)

    # Начинаем расчёты
    # Отдельный объект для расчёта конструкции
    comp = FEMComput(line_struct)

    # Сохраняем файл нашей модели
    save_model(line_struct, file_model, comment)
    # Сохраняем результаты расчёта
    comp.save_results(file_res, comment)


if __name__ == "__main__":
    main()
