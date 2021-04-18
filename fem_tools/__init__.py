# -*- coding: utf-8 -*-
"""
fem_tools - пакет предоставляющий полезные функции и классы
для метода конечных элементов (МКЭ)
"""
from .structure import Beam
from .calc import FEMComput

__all__ = ['Beam', 'FEMComput']
