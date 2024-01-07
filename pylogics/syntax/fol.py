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

"""Classes for first-order logic."""
from abc import ABC
from functools import partial
from typing import Set

from pylogics.helpers.misc import enforce
from pylogics.syntax.base import (
    FalseFormula,
    Formula,
    Logic,
    TrueFormula,
    _BinaryOp,
    _CommutativeBinaryOp,
    _UnaryOp,
)


class _FOL(Formula, ABC):
    """Interface for FOL formulae."""

    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.FOL

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()


class Term(ABC):
    @property
    def logic(self) -> Logic:
        """Get the logic formalism."""
        return Logic.FOL

    def __str__(self) -> str:
        """Get the string representation."""
        return f"{self.name}({', '.join([str(o) for o in self.operands])})" if 'operands' in dir(self) else f"{self.name}" 

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({str(self)})"


class Variable(Term):
    def __init__(self, name: str):
        self.name = name


class Constant(Term):
    def __init__(self, name: str, value = None):
        self.name = name
        self.value = value


class Function(Term):

    def __init__(self, name: str, operands: list):
        self.name = name
        self.operands = operands

    def __call__(self, *operands) -> Term:
        enforce(len(operands) == len(self.operands), f"expected {len(self.operands)} operands, got {len(operands)}.")
        enforce(all([isinstance(t, Term) for t in operands]), f"all operands must be terms")
        return Function(self.name, operands)


class _Quantifier(_BinaryOp):
    """Interface for quantifiers."""

    ALLOWED_LOGICS = {Logic.FOL}

    def __init__(self, variable: Variable, formula: Formula):
        """
        Initialize the quantifier.

        :param variable:
        :param formula:
        """
        enforce(isinstance(variable, Variable), f"{type(self).__name__}: expected {Variable}, got {type(variable)}")
        enforce(formula.logic == Logic.FOL, "tail formula not valid")
        self._variable = variable
        self._formula = formula
        self._operands = [variable, formula]

    @property
    def variable(self) -> Variable:
        """Get the variable."""
        return self._variable
    
    @property
    def formula(self) -> Formula:
        """Get the quantified formula."""
        return self._formula

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self._variable, self._formula))


class Predicate(_FOL):  
    """Predicate formula."""
    def __init__(self, name: str, operands: list = []):
        self._name = name
        self._operands = operands

    @property
    def name(self) -> str:
        """Get the name of the predicate."""
        return self._name
    
    @property
    def operands(self) -> list:
        """Get the operands of the predicate."""
        return self._operands

    def __call__(self, *operands) -> Term:
        enforce(len(operands) == len(self._operands), f"{self}: expected {len(self._operands)} operands, got {len(operands)}.")
        enforce(all([isinstance(t, Term) for t in operands]), f"all operands must be terms")
        return Predicate(self._name, operands)

    def __str__(self) -> str:
        """Get the string representation."""
        return f"{self._name}({', '.join([str(o) for o in self._operands])})" if self.operands else f"{self._name}" 

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({str(self)})"


class ForAll(_Quantifier, _FOL):
    """Universal formula."""
    SYMBOL = "forall"


class Exists(_Quantifier, _FOL):
    """Existential formula."""
    SYMBOL = "exists"

