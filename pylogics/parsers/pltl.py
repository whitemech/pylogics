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
from pylogics.syntax.pltl import Atomic, Before, Historically, Once, Since, Start


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
        return make_boolean(True, logic=Logic.PLTL)

    @classmethod
    def pltlf_false(cls, _args):
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
