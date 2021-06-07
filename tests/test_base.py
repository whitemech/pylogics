# -*- coding: utf-8 -*-
#
# Copyright 2021 WhiteMech
#
# ------------------------------
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Tests on the pylogics.syntax.ltl module."""
import pytest

from pylogics.syntax.base import FalseFormula, Logic, Not, TrueFormula


@pytest.mark.parametrize("logic", list(Logic))
def test_not_true(logic):
    """Test that the negation of true gives false."""
    assert FalseFormula(logic=logic) == Not(TrueFormula(logic=logic))


@pytest.mark.parametrize("logic", list(Logic))
def test_not_false(logic):
    """Test that the negation of false gives true."""
    assert TrueFormula(logic=logic) == Not(FalseFormula(logic=logic))
