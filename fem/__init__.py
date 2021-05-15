# -*- coding: utf-8 -*-
"""
fem - пакет предоставляющий полезные функции и классы
для метода конечных элементов (МКЭ)
"""
from .structure import LineStructure, Force, Distance
from .calc import FEMComput
from .fio import save_model
from .fio import load_model

__all__ = ['LineStructure', 'Force', 'Distance',
           'FEMComput', 'save_model', 'load_model']
