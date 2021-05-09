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

    def test_mult_row_and_col(self):
        """Умножение строки на столбец"""
        row = Matrix([1, 2], to_row=True)
        col = Matrix([3, 4])
        res = Matrix([11])
        msg = f"\n{row * col} НЕ РАВНО {res}"
        self.assertEqual(row * col, res, msg)

    def test_mult_col_and_row(self):
        """Умножение столбца на строку"""
        col = Matrix([1, 2])
        row = Matrix([3, 4], to_row=True)
        res = Matrix([[3, 4], [6, 8]])
        msg = f"\n{col * row} НЕ РАВНО\n{res}"
        self.assertEqual(col * row, res, msg)

    def test_mult_cols(self):
        """Умножение столбца на столбец"""
        col = Matrix([1, 2])
        with self.assertRaises(Exception):
            # столбец нельзя умножить на столбецц
            # Неподходящие размерности
            col * col

    def test_mult_rows(self):
        """Умножение столбца на столбец"""
        row = Matrix([1, 2], to_row=True)
        with self.assertRaises(Exception):
            # строку нельзя умножить на строку
            # Неподходящие размерности
            row * row

    def test_mult_bad_matrix(self):
        """Умножить не соразмерные матрицы"""
        A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        B = Matrix([[1, 2], [3, 4]])
        with self.assertRaises(Exception):
            # несоразмерные матрицы нельзя умножать
            A * B

    def test_mult_good_matrix(self):
        """Умножение соразмерных матриц"""
        A = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        res = Matrix([[30, 36, 42], [66, 81, 96], [102, 126, 150]])
        msg = f"\n{A * A} НЕ РАВНО\n{res}"
        self.assertEqual(A * A, res, msg)

    def test_mult_col_and_num(self):
        """Умножение столбца на число"""
        col = Matrix([1, 2, 3])
        num = 2
        res = Matrix([2, 4, 6])
        msg = f"\n{col}умножить на {num} НЕ РАВНО\n{res}"
        self.assertEqual(col * num, res, msg)

    def test_mult_row_and_num(self):
        """Умножение строки на число"""
        row = Matrix([1, 2, 3], to_row=True)
        num = 2
        res = Matrix([2, 4, 6], to_row=True)
        msg = f"\n{row}умножить на {num} НЕ РАВНО {res}"
        self.assertEqual(row * num, res, msg)

    def test_mult_matrix_and_num(self):
        """Умножение матрицы на число"""
        m = Matrix([[1, 2], [3, 4]])
        num = 2
        res = Matrix([[2, 4], [6, 8]])
        msg = f"\n{m}умножить на {num} НЕ РАВНО\n{res}"
        self.assertEqual(m * num, res, msg)

    def test_assign_number_to_column_row(self):
        """Присвоить число строке столбца"""
        col = Matrix([1, 2, 3])
        col[0] = 0
        res = Matrix([0, 2, 3])
        msg = f"\n{col}НЕ РАВНО \n{res}"
        self.assertEqual(col, res, msg)

    def test_assign_number_to_row_column(self):
        """Присвоить число столбцу строки"""
        row = Matrix([1, 2, 3], to_row=True)
        row[0] = 0
        res = Matrix([0, 2, 3], to_row=True)
        msg = f"\n{row}НЕ РАВНО \n{res}"
        self.assertEqual(row, res, msg)

    def test_assign_good_one_matrix_to_matrix_row(self):
        """Присвоить валидную матрицу строку строке матрицы"""
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        one_m = Matrix([10, 11, 12], to_row=True)
        m[0] = one_m
        res = Matrix([[10, 11, 12], [4, 5, 6], [7, 8, 9]])
        msg = f"\n{m}НЕ РАВНО \n{res}"
        self.assertEqual(m, res, msg)

    def test_assign_bad_one_matrix_to_matrix_row(self):
        """Присвоить НЕвалидную матрицу строку строке матрицы"""
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        one_m = Matrix([10, 11, 12, 14], to_row=True)
        with self.assertRaises(Exception):
            # размерности не подходят
            m[0] = one_m

    def test_assign_same_row_to_matrix_row(self):
        """Присвоить строке матрицы её же строку"""
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m[0] = m[2]
        res = Matrix([[7, 8, 9], [4, 5, 6], [7, 8, 9]])
        msg = f"\n{m}НЕ РАВНО \n{res}"
        self.assertEqual(m, res, msg)

    def test_mult_row_of_matrix_by_num(self):
        """Умножить строку матрицы на число"""
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        m[0] *= 2
        res = Matrix([[2, 4, 6], [4, 5, 6], [7, 8, 9]])
        msg = f"\n{m}НЕ РАВНО \n{res}"
        self.assertEqual(m, res, msg)

    def test_sub_row_of_matrix_by_num(self):
        """Делить строку матрицы на число"""
        m = Matrix([[2, 4, 6], [4, 5, 6], [7, 8, 9]])
        m[0] /= 2
        res = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        msg = f"\n{m}НЕ РАВНО \n{res}"
        self.assertEqual(m, res, msg)

    def test_compare_matrix_row_and_separate_row(self):
        """Cравнить строку матрицы и отдельную строку"""
        m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        row = Matrix([1, 2, 3], to_row=True)
        msg = f"\n{m[0]} НЕ РАВНО {row}"
        self.assertTrue(m[0] == row, msg)

if __name__ == '__main__':
    unittest.main()
