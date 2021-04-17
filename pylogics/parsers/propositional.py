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

from pylogics.parsers.base import AbstractParser, AbstractTransformer
from pylogics.syntax.base import (
    And,
    EquivalenceOp,
    Formula,
    ImpliesOp,
    Logic,
    Not,
    Or,
    make_boolean,
)
from pylogics.syntax.propositional import Atomic


class _PLTransformer(AbstractTransformer):
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
        return cls._starred_binaryop(args, EquivalenceOp, cls.prop_equivalence.__name__)

    @classmethod
    def prop_implication(cls, args):
        return cls._starred_binaryop(args, ImpliesOp, cls.prop_implication.__name__)

    @classmethod
    def prop_or(cls, args):
        return cls._starred_binaryop(args, Or, cls.prop_or.__name__)

    @classmethod
    def prop_and(cls, args):
        return cls._starred_binaryop(args, And, cls.prop_and.__name__)

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
        return make_boolean(True, logic=Logic.PL)

    @classmethod
    def prop_false(cls, args):
        assert len(args) == 1
        return make_boolean(False, logic=Logic.PL)

    @classmethod
    def atom(cls, args):
        assert len(args) == 1
        return Atomic(str(args[0]))


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
