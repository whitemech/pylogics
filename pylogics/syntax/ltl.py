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

"""Classes for linear temporal logic."""
from abc import ABC
from functools import partial

from pylogics.helpers.misc import enforce
from pylogics.syntax.base import (
    AbstractAtomic,
    BinaryOp,
    FalseFormula,
    Formula,
    Logic,
    UnaryOp,
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


class _LTLUnaryOp(UnaryOp, _LTL):
    """LTL Unary operation."""

    def __post_init__(self):
        """Check that the argument is of LTL logic."""
        enforce(
            self.argument.logic == Logic.LTL, "operand does not belong to LTL logic"
        )


class _LTLBinaryOp(BinaryOp, _LTL):
    """LTL Unary operation."""

    def __post_init__(self):
        """Check that the agument is of LTL logic."""
        enforce(
            all(op.logic == Logic.LTL for op in self.operands),
            "operands do not belong to LTL logic",
        )


class Atomic(AbstractAtomic, _LTL):
    """An atomic proposition of LTL."""


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
