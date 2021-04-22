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
    Equivalence,
    FalseFormula,
    Formula,
    Implies,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ldl import (
    Box,
    Diamond,
    LDLFalse,
    LDLTrue,
    Prop,
    Seq,
    Star,
    Test,
    Union,
)
from pylogics.syntax.ltl import (
    Always,
    Eventually,
    Next,
    Release,
    StrongRelease,
    Until,
    WeakNext,
    WeakUntil,
)
from pylogics.syntax.pltl import Before, Historically, Once, Since


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


@to_string.register(Implies)
def to_string_implies(formula: Implies) -> str:
    """Transform an Implies into string."""
    return " -> ".join(_map_operands_to_string(formula.operands))


@to_string.register(Equivalence)
def to_string_equivalence(formula: Equivalence) -> str:
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


@to_string.register(Before)
def to_string_pltl_before(formula: Before) -> str:
    """Transform a 'before' formula into string."""
    return f"Y({to_string(formula.argument)})"


@to_string.register(Since)
def to_string_pltl_since(formula: Since) -> str:
    """Transform a 'since' formula into string."""
    return " S ".join(_map_operands_to_string(formula.operands))


@to_string.register(Once)
def to_string_pltl_once(formula: Once) -> str:
    """Transform a 'once' formula into string."""
    return f"O({to_string(formula.argument)})"


@to_string.register(Historically)
def to_string_pltl_historically(formula: Historically) -> str:
    """Transform a 'historically' formula into string."""
    return f"H({to_string(formula.argument)})"


@to_string.register(LDLTrue)
def to_string_ldl_true(_formula: LDLTrue) -> str:
    """Transform an LDL true into string."""
    return "tt"


@to_string.register(LDLFalse)
def to_string_ldl_false(_formula: LDLFalse) -> str:
    """Transform an LDL false into string."""
    return "ff"


@to_string.register(Diamond)
def to_string_ldl_diamond(formula: Diamond) -> str:
    """Transform an LDL diamond formula into string."""
    return f"<({to_string(formula.regular_expression)})>({to_string(formula.tail_formula)})"


@to_string.register(Box)
def to_string_ldl_box(formula: Box) -> str:
    """Transform an LDL box formula into string."""
    return f"[({to_string(formula.regular_expression)})]({to_string(formula.tail_formula)})"


@to_string.register(Seq)
def to_string_re_seq(formula: Seq) -> str:
    """Transform a sequence regular expression into string."""
    return ";".join(_map_operands_to_string(formula.operands))


@to_string.register(Union)
def to_string_re_union(formula: Union) -> str:
    """Transform a union regular expression into string."""
    return "+".join(_map_operands_to_string(formula.operands))


@to_string.register(Star)
def to_string_re_star(formula: Star) -> str:
    """Transform a star regular expression into string."""
    return f"({to_string(formula.argument)})*"


@to_string.register(Test)
def to_string_re_test(formula: Test) -> str:
    """Transform a test regular expression into string."""
    return f"?({to_string(formula.argument)})"


@to_string.register(Prop)
def to_string_re_prop(formula: Prop) -> str:
    """Transform a propositional regular expression into string."""
    return f"({to_string(formula.argument)})"
