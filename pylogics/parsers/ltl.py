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
from pylogics.syntax.ltl import (
    Always,
    Atomic,
    Eventually,
    Last,
    Next,
    PropositionalFalse,
    PropositionalTrue,
    Release,
    StrongRelease,
    Until,
    WeakNext,
    WeakUntil,
)


class _LTLTransformer(AbstractTransformer):
    @classmethod
    def start(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def ltlf_formula(cls, args):
        assert len(args) == 1
        return args[0]

    @classmethod
    def ltlf_equivalence(cls, args):
        return cls._starred_binaryop(args, Equivalence, cls.ltlf_equivalence.__name__)

    @classmethod
    def ltlf_implication(cls, args):
        return cls._starred_binaryop(args, Implies, cls.ltlf_implication.__name__)

    @classmethod
    def ltlf_or(cls, args):
        return cls._starred_binaryop(args, Or, cls.ltlf_or.__name__)

    @classmethod
    def ltlf_and(cls, args):
        return cls._starred_binaryop(args, And, cls.ltlf_and.__name__)

    @classmethod
    def ltlf_until(cls, args):
        return cls._starred_binaryop(args, Until, cls.ltlf_until.__name__)

    @classmethod
    def ltlf_weak_until(cls, args):
        return cls._starred_binaryop(args, WeakUntil, cls.ltlf_weak_until.__name__)

    @classmethod
    def ltlf_release(cls, args):
        return cls._starred_binaryop(args, Release, cls.ltlf_release.__name__)

    @classmethod
    def ltlf_strong_release(cls, args):
        return cls._starred_binaryop(
            args, StrongRelease, cls.ltlf_strong_release.__name__
        )

    @classmethod
    def ltlf_always(cls, args):
        return cls._process_unaryop(args, Always)

    @classmethod
    def ltlf_eventually(cls, args):
        return cls._process_unaryop(args, Eventually)

    @classmethod
    def ltlf_next(cls, args):
        return cls._process_unaryop(args, Next)

    @classmethod
    def ltlf_weak_next(cls, args):
        return cls._process_unaryop(args, WeakNext)

    @classmethod
    def ltlf_not(cls, args):
        return cls._process_unaryop(args, Not)

    @classmethod
    def ltlf_wrapped(cls, args):
        if len(args) == 1:
            return args[0]
        if len(args) == 3:
            _, formula, _ = args
            return formula
        cls._raise_parsing_error(cls.ltlf_wrapped.__name__, args)

    @classmethod
    def ltlf_atom(cls, args):
        assert len(args) == 1
        return Atomic(args[0])

    @classmethod
    def ltlf_true(cls, _args):
        return PropositionalTrue()

    @classmethod
    def ltlf_false(cls, _args):
        return PropositionalFalse()

    @classmethod
    def ltlf_tt(cls, _args):
        return make_boolean(True, logic=Logic.LTL)

    @classmethod
    def ltlf_ff(cls, _args):
        return make_boolean(False, logic=Logic.LTL)

    @classmethod
    def ltlf_last(cls, _args):
        return Last()

    @classmethod
    def ltlf_symbol(cls, args):
        assert len(args) == 1
        token = args[0]
        symbol = str(token)
        return Atomic(symbol)


class _LTLParser(AbstractParser):
    """Parser for linear temporal logic."""

    transformer_cls = _LTLTransformer
    lark_path = "ltl.lark"


__parser = _LTLParser()


def parse_ltl(formula: str) -> Formula:
    """
    Parse the linear temporal logic formula.

    This is the main entrypoint for LTL parsing.

    :param formula: the string representation of the formula.
    :return: the parsed formula.
    """
    return __parser(formula)
