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

"""Semantics for propositional logic."""
import functools
from typing import Callable

from pylogics.exceptions import PylogicsError
from pylogics.syntax.base import And, Equivalence, Formula, Implies, Not, Or


@functools.singledispatch
def base_semantics(formula: Formula, fn: Callable[..., bool], *args, **kwargs) -> bool:
    """Compute semantics of common boolean operators."""
    raise PylogicsError(f"formula '{formula}' is not recognized.")


@base_semantics.register(And)
def and_semantics(formula: And, fn: Callable[..., bool], *args, **kwargs) -> bool:
    """Evaluate a conjunction formula."""
    return all(fn(sub_formula, *args, **kwargs) for sub_formula in formula.operands)


@base_semantics.register(Or)
def or_semantics(formula: Or, fn: Callable[..., bool], *args, **kwargs) -> bool:
    """Evaluate a disjunction formula."""
    return any(fn(sub_formula, *args, **kwargs) for sub_formula in formula.operands)


@base_semantics.register(Not)
def not_semantics(formula: Not, fn: Callable[..., bool], *args, **kwargs) -> bool:
    """Evaluate a negation."""
    return not fn(formula.argument, *args, **kwargs)


@base_semantics.register(Implies)
def implies_semantics(
    formula: Implies, fn: Callable[..., bool], *args, **kwargs
) -> bool:
    """
    Evaluate an implication formula.

    We use the fact that:

        a -> b -> c === a -> (b -> c)

    is equivalent to

        ~a | ~b | c

    """

    def _visitor():
        for index, sub_formula in enumerate(formula.operands):
            if index < len(formula.operands) - 1:
                yield not fn(sub_formula, *args, **kwargs)
            yield fn(sub_formula, *args, **kwargs)

    return any(_visitor())


@base_semantics.register(Equivalence)
def equivalence_semantics(
    formula: Equivalence, fn: Callable[..., bool], *args, **kwargs
) -> bool:
    """Evaluate an equivalence formula."""
    result = fn(formula.operands[0], *args, **kwargs)
    for sub_formula in formula.operands[1:]:
        result = fn(sub_formula, *args, **kwargs) == result
    return result
