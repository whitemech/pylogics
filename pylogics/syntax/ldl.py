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

"""Classes for linear dynamic logic."""
from abc import ABC
from functools import partial

from pylogics.helpers.misc import enforce
from pylogics.syntax.base import (
    BinaryOp,
    CommutativeBinaryOp,
    FalseFormula,
    Formula,
    Logic,
    TrueFormula,
    UnaryOp,
)


class _LDL(Formula, ABC):
    """Interface for LDL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.LDL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class _RegularExpression(Formula):
    """Regular expression."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.RE


class LDLTrue(TrueFormula):
    """True formula of LDL."""

    def __init__(self):
        """Initialize."""
        super().__init__(Logic.LDL)

    def __str__(self) -> str:
        """Get the string representation."""
        return "tt"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"LDLTrue({self.logic})"

    def __neg__(self) -> Formula:
        """Negate."""
        return LDLFalse()


class LDLFalse(FalseFormula):
    """False formula of LDL."""

    def __init__(self):
        """Initialize."""
        super().__init__(Logic.LDL)

    def __str__(self) -> str:
        """Get the string representation."""
        return "ff"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"LDLFalse({self.logic})"

    def __neg__(self) -> Formula:
        """Negate."""
        return LDLTrue()


class Seq(BinaryOp, _RegularExpression):
    """Sequence of regular expressions."""

    SYMBOL = "seq"

    def __post_init__(self):
        """Check consistency after initialization."""
        enforce(
            all(op.logic == Logic.RE for op in self.operands),
            "not all the operands are regular expressions.",
        )


class Union(CommutativeBinaryOp, _RegularExpression):
    """Union of regular expressions."""

    SYMBOL = "union"

    def __post_init__(self):
        """Check consistency after initialization."""
        enforce(
            all(op.logic == Logic.RE for op in self.operands),
            "not all the operands are regular expressions.",
        )


class Test(UnaryOp, _RegularExpression):
    """Test of an LDL formula."""

    SYMBOL = "test"


class Star(UnaryOp, _RegularExpression):
    """Kleene star of regular expressions."""

    SYMBOL = "star"


class Prop(UnaryOp, _RegularExpression):
    """The propositional regular expression."""

    SYMBOL = "prop"


class _TemporalFormula(_LDL, ABC):
    """LDL Temporal formula."""

    def __init__(self, regular_expression: Formula, tail_formula: Formula):
        """
        Initialize the formula.

        :param regular_expression:
        :param tail_formula:
        """
        enforce(regular_expression.logic == Logic.RE, "regular expression not valid")
        enforce(tail_formula.logic == Logic.LDL, "tail formula not valid")
        self._regular_expression = regular_expression
        self._tail_formula = tail_formula

    @property
    def regular_expression(self) -> Formula:
        """Get the regular expression."""
        return self._regular_expression

    @property
    def tail_formula(self) -> Formula:
        """Get the tail expression."""
        return self._tail_formula

    def __eq__(self, other):
        """Test equality."""
        return (
            type(self) == type(other)
            and self.regular_expression == other.regular_expression
            and self.tail_formula == other.tail_formula
        )

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.regular_expression, self.tail_formula))


class Diamond(_TemporalFormula):
    """Diamond formula."""


class Box(_TemporalFormula):
    """Box formula."""


End = partial(Box, Prop(TrueFormula()), LDLFalse())
Last = partial(Diamond, Prop(TrueFormula()), End())
