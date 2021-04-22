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

"""Parser for linear temporal logic."""

from pylogics.exceptions import ParsingError
from pylogics.parsers.base import AbstractParser, AbstractTransformer
from pylogics.parsers.pl import _PLTransformer
from pylogics.syntax.base import (
    And,
    Equivalence,
    FalseFormula,
    Formula,
    Implies,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ldl import (
    Box,
    Diamond,
    End,
    Last,
    LDLFalse,
    LDLTrue,
    Prop,
    Seq,
    Star,
    Test,
    Union,
)
from pylogics.syntax.pl import Atomic


class _LDLTransformer(AbstractTransformer):
    """Transformer for LDL."""

    _pl_transformer = _PLTransformer()
    _pl_imported = ("pl_atom", "propositional_formula")
    _prefix = "pl__"

    @classmethod
    def start(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def ldlf_formula(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def ldlf_equivalence(cls, args):
        return cls._starred_binaryop(args, Equivalence, cls.ldlf_equivalence.__name__)

    @classmethod
    def ldlf_implication(cls, args):
        return cls._starred_binaryop(args, Implies, cls.ldlf_implication.__name__)

    @classmethod
    def ldlf_or(cls, args):
        return cls._starred_binaryop(args, Or, cls.ldlf_or.__name__)

    @classmethod
    def ldlf_and(cls, args):
        return cls._starred_binaryop(args, And, cls.ldlf_and.__name__)

    @classmethod
    def ldlf_unaryop(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def ldlf_box(cls, args):
        assert len(args) == 4
        _, regex, _, formula = args
        return Box(regex, formula)

    @classmethod
    def ldlf_diamond(cls, args):
        assert len(args) == 4
        _, regex, _, formula = args
        return Diamond(regex, formula)

    @classmethod
    def ldlf_not(cls, args):
        assert len(args) == 2
        return Not(args[1])

    @classmethod
    def ldlf_wrapped(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 3:
            _, formula, _ = args
            return formula
        cls._raise_parsing_error(cls.ldlf_wrapped.__name__, args)

    @classmethod
    def ldlf_atom(cls, args):
        assert len(args) == 1
        formula = args[0]
        return formula

    @classmethod
    def ldlf_tt(cls, args):
        return LDLTrue()

    @classmethod
    def ldlf_ff(cls, args):
        return LDLFalse()

    @classmethod
    def ldlf_last(cls, args):
        return Last()

    @classmethod
    def ldlf_end(cls, args):
        return End()

    @classmethod
    def ldlf_prop_true(cls, args):
        return Diamond(Prop(TrueFormula()), LDLTrue())

    @classmethod
    def ldlf_prop_false(cls, args):
        return Diamond(Prop(FalseFormula()), LDLTrue())

    @classmethod
    def ldlf_prop_atom(cls, args):
        assert len(args) == 1
        token = args[0]
        symbol = str(token)
        return Diamond(Prop(Atomic(symbol)), LDLTrue())

    @classmethod
    def regular_expression(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def re_union(cls, args):
        return cls._starred_binaryop(args, Union, cls.re_union.__name__)

    @classmethod
    def re_sequence(cls, args):
        return cls._starred_binaryop(args, Seq, cls.re_sequence.__name__)

    @classmethod
    def re_star(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 2:
            l, _ = args
            return Star(l)
        cls._raise_parsing_error(cls.re_star.__name__, args)

    @classmethod
    def re_test(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 2:
            _, formula = args
            return Test(formula)
        cls._raise_parsing_error(cls.re_test.__name__, args)

    @classmethod
    def re_wrapped(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 3:
            _, formula, _ = args
            return formula
        cls._raise_parsing_error(cls.re_wrapped.__name__, args)

    @classmethod
    def re_propositional(cls, args):
        assert len(args) == 1
        return Prop(args[0])

    def __getattr__(self, attr: str):
        """Also parse propositional logic."""
        if attr.startswith(self._prefix):
            suffix = attr[len(self._prefix) :]  # noqa
            return getattr(self._pl_transformer, suffix)
        if attr in self._pl_imported:
            return getattr(self._pl_transformer, attr)
        if attr.isupper():
            raise AttributeError("Terminals should not be parsed")
        raise ParsingError(f"No transformation exists for rule: {attr}")


class _LDLParser(AbstractParser):
    """Parser for linear temporal logic."""

    transformer_cls = _LDLTransformer
    lark_path = "ldl.lark"


__parser = _LDLParser()


def parse_ldl(formula: str) -> Formula:
    """
    Parse the linear dynamic logic formula.

    This is the main entrypoint for LDL parsing.

    :param formula: the string representation of the formula.
    :return: the parsed formula.
    """
    return __parser(formula)
