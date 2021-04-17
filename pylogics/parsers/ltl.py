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
from pylogics.syntax.ltl import (
    Always,
    Atomic,
    Eventually,
    Last,
    Next,
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
        return cls._starred_binaryop(args, EquivalenceOp, cls.ltlf_equivalence.__name__)

    @classmethod
    def ltlf_implication(cls, args):
        return cls._starred_binaryop(args, ImpliesOp, cls.ltlf_implication.__name__)

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
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = Always(f)
        return f

    @classmethod
    def ltlf_eventually(cls, args):
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = Eventually(f)
        return f

    @classmethod
    def ltlf_next(cls, args):
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = Next(f)
        return f

    @classmethod
    def ltlf_weak_next(cls, args):
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = WeakNext(f)
        return f

    @classmethod
    def ltlf_not(cls, args):
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = Not(f)
        return f

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
        return make_boolean(True, logic=Logic.LTL)

    @classmethod
    def ltlf_false(cls, _args):
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
