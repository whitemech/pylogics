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

"""Classes for past linear temporal logic."""
from abc import ABC
from functools import partial

from pylogics.syntax.base import (
    AbstractAtomic,
    FalseFormula,
    Formula,
    Logic,
    Not,
    TrueFormula,
    _BinaryOp,
    _UnaryOp,
)


class _PLTL(Formula, ABC):
    """Interface for PLTL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.PLTL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class _PLTLUnaryOp(_UnaryOp, _PLTL):
    """PLTL Unary operation."""

    ALLOWED_LOGICS = {Logic.PLTL}


class _PLTLBinaryOp(_BinaryOp, _PLTL):
    """PLTL Unary operation."""

    ALLOWED_LOGICS = {Logic.PLTL}


class Atomic(AbstractAtomic, _PLTL):
    """An atomic proposition of PLTL."""


class PropositionalTrue(TrueFormula, _PLTL):
    """
    A propositional true.

    This is equivalent to 'a | ~a'. for some atom 'a'.
    It requires reading any symbol, at least once.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.PLTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalFalse()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalTrue({self.logic})"


class PropositionalFalse(FalseFormula, _PLTL):
    """
    A propositional false.

    This is equivalent to 'a & ~a'. for some atom 'a'.
    It requires reading no symbol, at least once.
    The meaning of this formula is a bit blurred with 'ff'
    with respect to 'tt' and 'true'.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.PLTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalTrue()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalFalse({self.logic})"


class Before(_PLTLUnaryOp):
    """The "before" formula in PLTL."""

    SYMBOL = "before"


class Since(_PLTLBinaryOp):
    """The "since" formula in PLTL."""

    SYMBOL = "since"


class Once(_PLTLUnaryOp):
    """The "once" formula in PLTL."""

    SYMBOL = "once"


class Historically(_PLTLUnaryOp):
    """The "historically" formula in PLTL."""

    SYMBOL = "historically"


Start = partial(Not, Before(TrueFormula(logic=Logic.PLTL)))
