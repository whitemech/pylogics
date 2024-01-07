# -*- coding: utf-8 -*-
# Copyright 2021-2024 The Pylogics contributors
#
# ------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    assert Logic.PLTL == formula_1.logic == formula_2.logic


@suppress_health_checks_for_lark
@given(from_lark(pltl_parser._parser))
def test_to_string(formula):
    """Test that the output of 'to_string' is parsable."""
    expected_formula = parse_pltl(formula)
    formula_str = to_string(expected_formula)
    actual_formula = parse_pltl(formula_str)
    assert actual_formula == expected_formula
