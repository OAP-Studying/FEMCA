#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль показывает, как собрать модель конструкции и сохранить её  файл
Конструкция для теста на скорость вычислений
"""
import sys
from pathlib import Path
# Абсолютной путь до основной директории
main_dir = Path(__file__).resolve().parent.parent
# Добавляем её в путь поиска модулей
sys.path.append(str(main_dir))


from fem_tools import Beam
from fem_tools import FEMComput
from fem_tools import save_model

# Имя модели
name_model = 'model_test'
# Абсолютный путь до файла модели
file_model = f'{main_dir}/models/{name_model}.txt'
# Комментарий к модели и расчётам
comment = "Конструкция для теста на скорость вычисления"


def main():
    # Характерная длина элемента
    L = 1
    # Модуль Юнга
    E = 1
    # Площадь поперченого сечения
    F = 1
    # Жёсткость пружинки
    C = E*F/L
    # Заготовка конструкции
    beam = Beam()

    # Система 20x20 узлов

    rod0 = beam.add_rod(E, F, L=L)
    rod1 = beam.add_rod(E, 2*F, n1=rod0.node2, L=L)
    spring2 = beam.add_spring(C, n1=rod1.node2, L=L)
    rod3 = beam.add_rod(2*E, 2*F, n1=spring2.node2, L=L)
    spring4 = beam.add_spring(2*C, n1=rod3.node2, L=L)
    spring5 = beam.add_spring(C, n1=spring4.node2, L=L)
    rod6 = beam.add_rod(E, F, n1=spring5.node2, L=L)
    spring7 = beam.add_spring(3*C, n1=rod6.node2, L=L)

    spring8 = beam.add_spring(C, n1=rod0.node2, L=L)
    rod9 = beam.add_rod(3*E, F, n1=spring8.node2, L=L)

    rod10 = beam.add_rod(E, F, n1=rod3.node2, L=-L)
    spring11 = beam.add_spring(2*C, n1=rod10.node2, L=-L)

    rod12 = beam.add_rod(E, F, n1=spring5.node2, L=-L)
    rod13 = beam.add_rod(E, 3*F, n1=rod12.node2, L=-L)
    sprig14 = beam.add_spring(2*C, n1=rod13.node2, L=-L)
    rod15 = beam.add_rod(E, 3*F, n1=sprig14.node2, L=-L)
    rod16 = beam.add_rod(E, F, n1=rod15.node2, L=-L)
    rod17 = beam.add_rod(2*E, F, n1=rod16.node2, L=-L)
    spring18 = beam.add_spring(C, n1=rod17.node2, L=-L)

    spring19 = beam.add_spring(3*C, n1=rod17.node1, n2=rod12.node2)

    # Добавляем заделки к конструкции
    rod0.node1.add_pinning()
    spring7.node2.add_pinning()
    rod9.node2.add_pinning()
    spring11.node2.add_pinning()
    spring18.node2.add_pinning()

    # Добавляем нагрузки к конструкции
    # Характерная сила
    P = 1
    rod0.node2.add_point_force(P)
    rod1.node2.add_point_force(-2*P)
    spring2.node2.add_point_force(4*P)
    spring5.node2.add_point_force(6*P)
    spring8.node2.add_point_force(3*P)
    rod10.node1.add_point_force(-P)
    rod13.node2.add_point_force(7*P)
    rod15.node2.add_point_force(-5*P)
    rod17.node2.add_point_force(P)
    spring19.add_linear_distributed_force(q1=2, q2=1)

    # Сохраняем файл нашей модели
    save_model(beam, file_model, comment)


if __name__ == "__main__":
    main()
