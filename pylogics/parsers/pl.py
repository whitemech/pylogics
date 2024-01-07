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

"""Parser for propositional logic."""

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
from pylogics.syntax.pl import Atomic


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
        return cls._starred_binaryop(args, Equivalence, cls.prop_equivalence.__name__)

    @classmethod
    def prop_implication(cls, args):
        return cls._starred_binaryop(args, Implies, cls.prop_implication.__name__)

    @classmethod
    def prop_or(cls, args):
        return cls._starred_binaryop(args, Or, cls.prop_or.__name__)

    @classmethod
    def prop_and(cls, args):
        return cls._starred_binaryop(args, And, cls.prop_and.__name__)

    @classmethod
    def prop_not(cls, args):
        return cls._process_unaryop(args, Not)

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
    lark_path = "pl.lark"


__parser = _PLParser()


def parse_pl(formula: str) -> Formula:
    """
    Parse the propositional formula.

    This is the main entrypoint for PL parsing.

    :param formula: the string representation of the formula.
    :return: the parsed formula.
    """
    return __parser(formula)
