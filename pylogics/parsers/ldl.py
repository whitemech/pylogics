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
    Logic,
    Not,
    Or,
    TrueFormula,
)
from pylogics.syntax.ldl import Box, Diamond, End, Last, Prop, Seq, Star, Test, Union
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
        return TrueFormula(logic=Logic.LDL)

    @classmethod
    def ldlf_ff(cls, args):
        return FalseFormula(logic=Logic.LDL)

    @classmethod
    def ldlf_last(cls, args):
        return Last()

    @classmethod
    def ldlf_end(cls, args):
        return End()

    @classmethod
    def ldlf_prop_true(cls, args):
        return Diamond(Prop(TrueFormula()), TrueFormula(logic=Logic.LDL))

    @classmethod
    def ldlf_prop_false(cls, args):
        return Diamond(Prop(FalseFormula()), TrueFormula(logic=Logic.LDL))

    @classmethod
    def ldlf_prop_atom(cls, args):
        assert len(args) == 1
        token = args[0]
        symbol = str(token)
        return Diamond(Prop(Atomic(symbol)), TrueFormula(logic=Logic.LDL))

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
            formula, _ = args
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
