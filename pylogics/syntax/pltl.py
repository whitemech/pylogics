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


Start = partial(Historically, FalseFormula(logic=Logic.PLTL))
First = partial(Not, Before(TrueFormula(logic=Logic.PLTL)))
