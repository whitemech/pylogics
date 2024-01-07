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

"""Parser for past linear temporal logic."""

from pylogics.parsers.base import AbstractParser, AbstractTransformer
from pylogics.syntax.base import (
    And,
    Equivalence,
    Formula,
    Implies,
    Logic,
    Not,
    Or,
    make_boolean,
)
from pylogics.syntax.pltl import (
    Atomic,
    Before,
    Historically,
    Once,
    PropositionalFalse,
    PropositionalTrue,
    Since,
    Start,
)


class _PLTLTransformer(AbstractTransformer):
    @classmethod
    def start(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def pltlf_formula(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def pltlf_equivalence(cls, args):
        return cls._starred_binaryop(args, Equivalence, cls.pltlf_equivalence.__name__)

    @classmethod
    def pltlf_implication(cls, args):
        return cls._starred_binaryop(args, Implies, cls.pltlf_implication.__name__)

    @classmethod
    def pltlf_or(cls, args):
        return cls._starred_binaryop(args, Or, cls.pltlf_or.__name__)

    @classmethod
    def pltlf_and(cls, args):
        return cls._starred_binaryop(args, And, cls.pltlf_and.__name__)

    @classmethod
    def pltlf_since(cls, args):
        return cls._starred_binaryop(args, Since, cls.pltlf_since.__name__)

    @classmethod
    def pltlf_historically(cls, args):
        return cls._process_unaryop(args, Historically)

    @classmethod
    def pltlf_once(cls, args):
        return cls._process_unaryop(args, Once)

    @classmethod
    def pltlf_before(cls, args):
        return cls._process_unaryop(args, Before)

    @classmethod
    def pltlf_not(cls, args):
        return cls._process_unaryop(args, Not)

    @classmethod
    def pltlf_wrapped(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 3:
            _, formula, _ = args
            return formula
        cls._raise_parsing_error(cls.pltlf_wrapped.__name__, args)

    @classmethod
    def pltlf_atom(cls, args):
        assert len(args) == 1
        return Atomic(args[0])

    @classmethod
    def pltlf_true(cls, _args):
        return PropositionalTrue()

    @classmethod
    def pltlf_false(cls, _args):
        return PropositionalFalse()

    @classmethod
    def pltlf_tt(cls, _args):
        return make_boolean(True, logic=Logic.PLTL)

    @classmethod
    def pltlf_ff(cls, _args):
        return make_boolean(False, logic=Logic.PLTL)

    @classmethod
    def pltlf_start(cls, _args):
        return Start()

    @classmethod
    def pltlf_symbol(cls, args):
        assert len(args) == 1
        token = args[0]
        symbol = str(token)
        return Atomic(symbol)


class _PLTLParser(AbstractParser):
    """Parser for linear temporal logic."""

    transformer_cls = _PLTLTransformer
    lark_path = "pltl.lark"


__parser = _PLTLParser()


def parse_pltl(formula: str) -> Formula:
    """
    Parse the past linear temporal logic formula.

    This is the main entrypoint for PLTL parsing.

    :param formula: the string representation of the formula.
    :return: the parsed formula.
    """
    return __parser(formula)
