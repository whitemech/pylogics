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

"""Parser for propositional logic."""

from lark import Transformer

from pylogics.exceptions import ParsingError
from pylogics.parsers.base import AbstractParser
from pylogics.syntax.base import (
    FALSE,
    TRUE,
    And,
    EquivalenceOp,
    Formula,
    ImpliesOp,
    Not,
    Or,
)
from pylogics.syntax.propositional import Atomic


class _PLTransformer(Transformer):
    """Lark Transformer for propositional logic."""

    @classmethod
    def start(cls, args):
        """Start."""
        return args[0]

    @classmethod
    def propositional_formula(cls, args):
        """Parse the 'propositional_formula' tag."""
        assert len(args) == 1
        return args[0]

    @classmethod
    def prop_equivalence(cls, args):
        """Parse the 'prop_equivalence' tag."""
        if len(args) == 1:
            return args[0]
        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return EquivalenceOp(*subformulas)
        cls._raise_parsing_error(cls.prop_equivalence.__name__, args)

    @classmethod
    def prop_implication(cls, args):
        if len(args) == 1:
            return args[0]
        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return ImpliesOp(*subformulas)
        cls._raise_parsing_error(cls.prop_implication.__name__, args)

    @classmethod
    def prop_or(cls, args):
        if len(args) == 1:
            return args[0]
        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return Or(*subformulas)
        cls._raise_parsing_error(cls.prop_or.__name__, args)

    @classmethod
    def prop_and(cls, args):
        if len(args) == 1:
            return args[0]
        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return And(*subformulas)
        cls._raise_parsing_error(cls.prop_and.__name__, args)

    @classmethod
    def prop_not(cls, args):
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = Not(f)
        return f

    @classmethod
    def prop_wrapped(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 3:
            _, f, _ = args
            return f
        cls._raise_parsing_error(cls.prop_wrapped.__name__, args)

    @classmethod
    def prop_atom(cls, args):
        assert len(args) == 1
        return Atomic(args[0])

    @classmethod
    def prop_true(cls, args):
        assert len(args) == 1
        return TRUE

    @classmethod
    def prop_false(cls, args):
        assert len(args) == 1
        return FALSE

    @classmethod
    def atom(cls, args):
        assert len(args) == 1
        return Atomic(str(args[0]))

    @classmethod
    def _raise_parsing_error(cls, tag_name, args):
        """Raise a parsing error."""
        raise ParsingError(f"error while parsing a '{tag_name}' with tokens: {args}")


class _PLParser(AbstractParser):
    """Parser for propositional logic."""

    transformer_cls = _PLTransformer
    lark_path = "propositional.lark"


__parser = _PLParser()


def parse_prop(formula: str) -> Formula:
    """
    Parse the propositional formula.

    This is the main entrypoint for PL parsing.

    :param formula: the string representation of the formula.
    :return: the parsed formula.
    """
    return __parser(formula)
