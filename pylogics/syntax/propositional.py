# -*- coding: utf-8 -*-
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Classes for propositional logic."""
import re
from typing import Union

from pylogics.helpers.misc import RegexConstrainedString
from pylogics.syntax.base import Formula, Logic


class AtomName(RegexConstrainedString):
    """A string that denotes an atomic propositional symbol."""

    REGEX = re.compile(r"[A-Za-z][A-Za-z0-9_]+")


_AtomNameOrStr = Union[str, AtomName]


class Atomic(Formula):
    """An atomic proposition."""

    def __init__(self, name: _AtomNameOrStr):
        """
        Initialize the atomic proposition.

        :param name: the symbol name.
        """
        super().__init__()
        self._name = name

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.PL

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((Atomic, self.name))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"Atomic({self.name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return isinstance(other, Atomic) and self.name == other.name
