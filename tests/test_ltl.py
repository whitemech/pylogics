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

"""Tests on the pylogics.syntax.ltlf module."""
from hypothesis import HealthCheck, given, settings
from hypothesis.extra.lark import from_lark

from pylogics.parsers.ltl import __parser as ltl_parser
from pylogics.parsers.ltl import parse_ltl
from pylogics.syntax.base import Logic


@settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much])
@given(from_lark(ltl_parser._parser))
def test_parser(formula):
    """Test parsing is deterministic."""
    formula_1 = parse_ltl(formula)
    formula_2 = parse_ltl(formula)
    assert formula_1 == formula_2
    assert Logic.LTL == formula_1.logic == formula_2.logic
