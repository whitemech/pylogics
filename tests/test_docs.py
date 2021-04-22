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

"""Tests for the docs pages."""

from pylogics.parsers import parse_ldl, parse_ltl, parse_pl, parse_pltl


def test_pl_parsing():
    """Test PL parsing."""
    parse_pl("a")
    parse_pl("b")
    parse_pl("a & b")
    parse_pl("a | b")
    parse_pl("a >> b")
    parse_pl("a <-> b")
    parse_pl("a <-> a")
    parse_pl("!(a)")
    parse_pl("true & false")
    parse_pl("true | false")


def test_ltl_parsing():
    """Test LTL parsing."""
    parse_ltl("a")
    parse_ltl("b")
    parse_ltl("X(a)")
    parse_ltl("N(b)")
    parse_ltl("F(a)")
    parse_ltl("G(b)")
    parse_ltl("G(a -> b)")
    parse_ltl("a U b")
    parse_ltl("a R b")
    parse_ltl("a W b")
    parse_ltl("a M b")


def test_pltl_parsing():
    """Test PLTL parsing."""
    parse_pltl("a")
    parse_pltl("b")
    parse_pltl("Y(a)")
    parse_pltl("O(b)")
    parse_pltl("H(a)")
    parse_pltl("a S b")


def test_ldl_parsing():
    """Test LDL parsing."""
    parse_ldl("tt")
    parse_ldl("ff")
    parse_ldl("<a>tt")
    parse_ldl("[a & b]ff")
    parse_ldl("<a + b>tt")
    parse_ldl("<a ; b><c>tt")
    parse_ldl("<(a ; b)*><c>tt")
    parse_ldl("<true><a>tt")
    parse_ldl("<(?<a>tt;true)*>(<b>tt)")
