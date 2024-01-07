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

"""Classes for linear temporal logic."""
from abc import ABC
from functools import partial

from pylogics.syntax.base import (
    AbstractAtomic,
    FalseFormula,
    Formula,
    Logic,
    TrueFormula,
    _BinaryOp,
    _UnaryOp,
)


class _LTL(Formula, ABC):
    """Interface for LTL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.LTL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class _LTLUnaryOp(_UnaryOp, _LTL):
    """LTL Unary operation."""

    ALLOWED_LOGICS = {Logic.LTL}


class _LTLBinaryOp(_BinaryOp, _LTL):
    """LTL Unary operation."""

    ALLOWED_LOGICS = {Logic.LTL}


class Atomic(AbstractAtomic, _LTL):
    """An atomic proposition of LTL."""


class PropositionalTrue(TrueFormula, _LTL):
    """
    A propositional true.

    This is equivalent to 'a | ~a'. for some atom 'a'.
    It requires reading any symbol, at least once.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.LTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalFalse()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalTrue({self.logic})"


class PropositionalFalse(FalseFormula, _LTL):
    """
    A propositional false.

    This is equivalent to 'a & ~a'. for some atom 'a'.
    It requires reading no symbol, at least once.
    The meaning of this formula is a bit blurred with 'ff'
    with respect to 'tt' and 'true'.
    """

    def __init__(self):
        """Initialize."""
        super().__init__(logic=Logic.LTL)

    def __invert__(self) -> "Formula":
        """Negate."""
        return PropositionalTrue()

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"PropositionalFalse({self.logic})"


class Next(_LTLUnaryOp):
    """The "next" formula in LTL."""

    SYMBOL = "next"


class WeakNext(_LTLUnaryOp):
    """The "weak next" formula in LTL."""

    SYMBOL = "weak_next"


class Until(_LTLBinaryOp):
    """The "next" formula in LTL."""

    SYMBOL = "until"


class Release(_LTLBinaryOp):
    """The "release" formula in LTL."""

    SYMBOL = "release"


class Eventually(_LTLUnaryOp):
    """The "eventually" formula in LTL."""

    SYMBOL = "eventually"


class Always(_LTLUnaryOp):
    """The "always" formula in LTL."""

    SYMBOL = "always"


class WeakUntil(_LTLBinaryOp):
    """The "weak until" formula in LTL."""

    SYMBOL = "weak_until"


class StrongRelease(_LTLBinaryOp):
    """The "strong release" formula in LTL."""

    SYMBOL = "strong_release"


Last = partial(Always, FalseFormula(logic=Logic.LTL))
