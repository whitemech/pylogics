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
