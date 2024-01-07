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
