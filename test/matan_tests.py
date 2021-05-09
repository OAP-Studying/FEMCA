# -*- coding: utf-8 -*-
"""Тесты модуля matan"""
import unittest
from fem_tools.matan import Matrix


class TestMatrixOperations(unittest.TestCase):
    """Тестирование операций с матрицами"""

    def test_create_col(self):
        """Тест на создание вектора столбца"""
        col1 = Matrix([[1], [2], [3], [4]])
        col2 = Matrix([1, 2, 3, 4])
        msg = f"Столбцы\n{col1} и \n{col2}должны быть одинаковыми"
        self.assertEqual(col1, col2, msg)

    def test_create_row(self):
        """Тест на создание вектора строки"""
        row1 = Matrix([[1], [2], [3], [4]], to_row=True)
        row2 = Matrix([1, 2, 3, 4], to_row=True)
        msg = f"Строки\n{row1}и\n{row2}должны быть одинаковыми"
        self.assertEqual(row1, row2, msg)


if __name__ == '__main__':
    unittest.main()
