# -*- coding: utf-8 -*-
"""
Тесты на сохранение и загрузку модели
Идея тестов простая - модель, которую сохранили,
при загрузке из файла должна получиться точно такой же
и результаты вычислений должны получиться такие же
"""
import unittest
import os
import random
from fem import LineStructure, Distance, Force
from fem import FEMComput
from fem import load_model, save_model


class TestSaveLoad(unittest.TestCase):
    """Тестирование на сохранение и загрузку моделей"""

    def setUp(self):
        # Файлы для конструкции собираемой кодом на питоне
        self.f_model1 = 'model1.txt'
        self.f_res1 = 'res1.txt'
        # Файлы для конструкции загружаемой из self.f_model1
        self.f_model2 = 'model2.txt'
        self.f_res2 = 'res1.txt'

    def tearDown(self):
        # Удаляем мусорные файлы после тестов
        trash = [self.f_model1, self.f_res1, self.f_model2, self.f_res2]
        for file in trash:
            if os.path.exists(file):
                os.remove(file)