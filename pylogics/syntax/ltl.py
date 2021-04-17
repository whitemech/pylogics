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

"""Classes for propositional logic."""
from abc import ABC

from pylogics.syntax.base import AbstractAtomic, BinaryOp, Formula, Logic, UnaryOp


class LTL(Formula, ABC):
    """Interface for LTL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.LTL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class Atomic(AbstractAtomic, LTL):
    """An atomic proposition of LTL."""


class Next(UnaryOp, LTL):
    """The "next" formula in LTL."""

    SYMBOL = "next"


class WeakNext(UnaryOp, LTL):
    """The "weak next" formula in LTL."""

    SYMBOL = "weak_next"


class Until(BinaryOp, LTL):
    """The "next" formula in LTL."""

    SYMBOL = "until"


class Release(BinaryOp, LTL):
    """The "release" formula in LTL."""

    SYMBOL = "release"


class Eventually(UnaryOp, LTL):
    """The "eventually" formula in LTL."""

    SYMBOL = "eventually"


class Always(UnaryOp, LTL):
    """The "always" formula in LTL."""

    SYMBOL = "always"


class WeakUntil(BinaryOp, LTL):
    """The "weak until" formula in LTL."""

    SYMBOL = "weak_until"


class StrongRelease(BinaryOp, LTL):
    """The "strong release" formula in LTL."""

    SYMBOL = "strong_release"


class Last(LTL, Formula):
    """The "last" formula (i.e. weak_next(false)) in LTL."""

    def __hash__(self):
        """Compute the hash."""
        return hash(Last)

    def __eq__(self, other):
        """Compare with another object."""
        return type(other) == Last

    def __str__(self) -> str:
        """Get the string representation."""
        return "last"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return "Last()"
