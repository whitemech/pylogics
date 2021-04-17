# -*- coding: utf-8 -*-
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Transform formulae to string."""
import functools
from typing import Sequence

from pylogics.exceptions import PylogicsError
from pylogics.syntax.base import (
    And,
    EquivalenceOp,
    FalseFormula,
    Formula,
    ImpliesOp,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.propositional import Atomic


@functools.singledispatch
def to_string(formula: Formula) -> str:
    """Transform a formula to string."""
    raise PylogicsError(f"formula '{formula}' is not supported")


def _map_operands_to_string(operands: Sequence[Formula]):
    """Map a list of operands to a list of strings (with brackets)."""
    return map(lambda sub_formula: f"({to_string(sub_formula)})", operands)


@to_string.register(And)
def to_string_and(formula: And) -> str:
    """Transform an And into string."""
    return " & ".join(_map_operands_to_string(formula.operands))


@to_string.register(Or)
def to_string_or(formula: Or) -> str:
    """Transform an Or into string."""
    return " | ".join(_map_operands_to_string(formula.operands))


@to_string.register(Not)
def to_string_not(formula: Not) -> str:
    """Transform a Not into string."""
    return f"~({to_string(formula.argument)})"


@to_string.register(ImpliesOp)
def to_string_implies(formula: ImpliesOp) -> str:
    """Transform an Implies into string."""
    return " -> ".join(_map_operands_to_string(formula.operands))


@to_string.register(EquivalenceOp)
def to_string_equivalence(formula: EquivalenceOp) -> str:
    """Transform an Equivalence into string."""
    return " <-> ".join(_map_operands_to_string(formula.operands))


@to_string.register(Atomic)
def to_string_atomic(formula: Atomic) -> str:
    """Transform an atomic formula into string."""
    return formula.name


@to_string.register(TrueFormula)
def to_string_true(_formula: TrueFormula) -> str:
    """Transform the "true" formula into string."""
    return "true"


@to_string.register(FalseFormula)
def to_string_false(_formula: FalseFormula) -> str:
    """Transform the "false" formula into string."""
    return "false"
