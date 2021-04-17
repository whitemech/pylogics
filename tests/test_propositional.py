# -*- coding: utf-8 -*-
#
# Copyright 2021 Marco Favorito
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

"""Tests on the pylogics.syntax.propositional module."""
from hypothesis import HealthCheck, given, settings
from hypothesis.extra.lark import from_lark
from hypothesis.strategies import booleans, dictionaries, one_of, sampled_from, sets

from pylogics.parsers.propositional import __parser as prop_parser
from pylogics.parsers.propositional import parse_prop
from pylogics.semantics.propositional import evaluate_prop
from pylogics.utils.to_string import to_string

SYMBOLS = ["A", "B", "C"]


@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
@given(from_lark(prop_parser._parser))
def test_parser(formula):
    """Test parsing is deterministic."""
    formula_1 = parse_prop(formula)
    formula_2 = parse_prop(formula)
    assert formula_1 == formula_2


@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
@given(from_lark(prop_parser._parser))
def test_to_string(formula):
    """Test that the output of 'to_string' is parsable."""
    expected_formula = parse_prop(formula)
    formula_str = to_string(expected_formula)
    actual_formula = parse_prop(formula_str)
    assert expected_formula == actual_formula


@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
@given(
    from_lark(prop_parser._parser),
    one_of(
        sets(sampled_from(SYMBOLS)),
        dictionaries(keys=sampled_from(SYMBOLS), values=booleans()),
    ),
)
def test_semantics_negation(formula, interpretation):
    """Test that for all models I, (I |= phi) != (I |= ~phi)."""
    positive_formula = parse_prop(formula)
    negative_formula = ~positive_formula
    assert evaluate_prop(positive_formula, interpretation) != evaluate_prop(
        negative_formula, interpretation
    )