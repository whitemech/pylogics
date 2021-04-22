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

"""Tests on the pylogics.syntax.pltl module."""
from hypothesis import given
from hypothesis.extra.lark import from_lark

from pylogics.parsers.pltl import __parser as pltl_parser
from pylogics.parsers.pltl import parse_pltl
from pylogics.syntax.base import Logic
from pylogics.utils.to_string import to_string
from tests.conftest import suppress_health_checks_for_lark


@suppress_health_checks_for_lark
@given(from_lark(pltl_parser._parser))
def test_parser(formula):
    """Test parsing is deterministic."""
    formula_1 = parse_pltl(formula)
    formula_2 = parse_pltl(formula)
    assert formula_1 == formula_2
    assert Logic.LTL == formula_1.logic == formula_2.logic


@suppress_health_checks_for_lark
@given(from_lark(pltl_parser._parser))
def test_to_string(formula):
    """Test that the output of 'to_string' is parsable."""
    expected_formula = parse_pltl(formula)
    formula_str = to_string(expected_formula)
    actual_formula = parse_pltl(formula_str)
    assert actual_formula == expected_formula
