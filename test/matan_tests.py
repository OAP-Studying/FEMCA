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

    def test_add_cols(self):
        """Сложение двух столбцов"""
        A = Matrix([1, 2])
        B = Matrix([3, 4])
        C = Matrix([4, 6])
        msg = f"\n{A} + \n{B} НЕ РАВНО \n{C}"
        self.assertEqual(A+B, C, msg)

    def test_add_rows(self):
        """Сложение двух столбцов"""
        A = Matrix([1, 2], to_row=True)
        B = Matrix([3, 4], to_row=True)
        C = Matrix([4, 6], to_row=True)
        msg = f"\n{A} + {B} НЕ РАВНО {C}"
        self.assertEqual(A+B, C, msg)

    def test_add_matrix(self):
        """Сложение двух матриц"""
        A = Matrix([[1, 2], [3, 4]])
        B = Matrix([[5, 6], [7, 8]])
        C = Matrix([[6, 8], [10, 12]])
        msg = f"\n{A} + \n{B} НЕ РАВНО \n{C}"
        self.assertEqual(A+B, C, msg)

    def test_add_col_and_row(self):
        """Сложение столбца и строки"""
        col = Matrix([1, 2])
        row = Matrix([3, 4], to_row=True)
        with self.assertRaises(Exception):
            # столбец и строку нельзя складывать
            col + row

    def test_add_row_and_col(self):
        """Сложение строки и столбца"""
        row = Matrix([1, 2], to_row=True)
        col = Matrix([3, 4])
        with self.assertRaises(Exception):
            # строку и столбец нельзя складывать
            row + col


if __name__ == '__main__':
    unittest.main()
