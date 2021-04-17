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

"""Tests on the pylogics.syntax.propositional package."""
from pylogics.parsers.propositional import parse_prop
from pylogics.semantics.propositional import evaluate_prop


def test_propositional():
    """Simple test of propositional logic."""
    f = parse_prop("a & b & (a & b)")
    assert str(f) == "(and a b)"

    assert not evaluate_prop(f, {"a"})
    assert evaluate_prop(f, {"a", "b"})
