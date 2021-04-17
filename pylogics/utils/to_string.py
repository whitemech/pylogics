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

"""Transform formulae to string."""
import functools
from typing import Sequence

from pylogics.exceptions import PylogicsError
from pylogics.syntax.base import (
    AbstractAtomic,
    And,
    EquivalenceOp,
    FalseFormula,
    Formula,
    ImpliesOp,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ltl import (
    Always,
    Eventually,
    Last,
    Next,
    Release,
    StrongRelease,
    Until,
    WeakNext,
    WeakUntil,
)


@functools.singledispatch
def to_string(formula: Formula) -> str:
    """Transform a formula to a parsable string."""
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


@to_string.register(AbstractAtomic)
def to_string_atomic(formula: AbstractAtomic) -> str:
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


@to_string.register(Next)
def to_string_next(formula: Next) -> str:
    """Transform a next formula into string."""
    return f"X({to_string(formula.argument)})"


@to_string.register(WeakNext)
def to_string_weak_next(formula: WeakNext) -> str:
    """Transform a weak next formula into string."""
    return f"N({to_string(formula.argument)})"


@to_string.register(Until)
def to_string_until(formula: Until) -> str:
    """Transform a until formula into string."""
    return " U ".join(_map_operands_to_string(formula.operands))


@to_string.register(WeakUntil)
def to_string_weak_until(formula: WeakUntil) -> str:
    """Transform a weak until formula into string."""
    return " W ".join(_map_operands_to_string(formula.operands))


@to_string.register(Release)
def to_string_release(formula: Release) -> str:
    """Transform a release formula into string."""
    return " R ".join(_map_operands_to_string(formula.operands))


@to_string.register(StrongRelease)
def to_string_strong_release(formula: StrongRelease) -> str:
    """Transform a strong release formula into string."""
    return " M ".join(_map_operands_to_string(formula.operands))


@to_string.register(Eventually)
def to_string_eventually(formula: Eventually) -> str:
    """Transform a eventually formula into string."""
    return f"F({to_string(formula.argument)})"


@to_string.register(Always)
def to_string_always(formula: Always) -> str:
    """Transform a always formula into string."""
    return f"G({to_string(formula.argument)})"


@to_string.register(Last)
def to_string_last(formula: Last) -> str:
    """Transform a last formula into string."""
    return "last"
