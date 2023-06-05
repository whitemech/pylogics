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
from hypothesis import HealthCheck, given, settings
from hypothesis.extra.lark import from_lark

from pylogics.parsers.ltl import __parser as ltl_parser
from pylogics.parsers.ltl import parse_ltl
from pylogics.syntax.base import Logic
from pylogics.utils.to_string import to_string


@given(from_lark(ltl_parser._parser))
@settings(
    max_examples=1000,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
def test_parser(formula):
    """Test parsing is deterministic."""
    formula_1 = parse_ltl(formula)
    formula_2 = parse_ltl(formula)
    assert formula_1 == formula_2
    assert Logic.LTL == formula_1.logic == formula_2.logic


@given(from_lark(ltl_parser._parser))
@settings(
    max_examples=1000,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
def test_to_string(formula):
    """Test that the output of 'to_string' is parsable."""
    expected_formula = parse_ltl(formula)
    formula_str = to_string(expected_formula)
    actual_formula = parse_ltl(formula_str)
    assert actual_formula == expected_formula
