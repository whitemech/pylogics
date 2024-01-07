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

"""Semantics for propositional logic."""
from dataclasses import dataclass
from functools import singledispatch
from typing import Dict, Set, Union, cast

from pylogics.exceptions import PylogicsError
from pylogics.helpers.misc import enforce
from pylogics.semantics.base import base_semantics
from pylogics.syntax.base import (
    AtomName,
    FalseFormula,
    Formula,
    TrueFormula,
    _BinaryOp,
    _UnaryOp,
)
from pylogics.syntax.pl import Atomic

_PropInterpretation = Union[Dict, Set]


@dataclass
class _PropInterpretationWrapper:
    """Wrapper to a propositional interpretation (either a dict or a set)."""

    _interpretation: Dict[AtomName, bool]

    def __init__(self, interpretation: _PropInterpretation):
        """Initialize the object."""
        enforce(
            isinstance(interpretation, (dict, set)),
            "interpretation must be either a dictionary or a set",
        )
        if isinstance(interpretation, set):
            self._interpretation = dict.fromkeys(interpretation, True)
        else:
            self._interpretation = cast(Dict[AtomName, bool], interpretation)

    def __contains__(self, item: str):
        """Check an atom name is present in the interpretation."""
        item = AtomName(item)
        return self._interpretation.get(item, False)


@singledispatch
def evaluate_pl(formula: Formula, _interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula against an interpretation."""
    raise PylogicsError(
        f"formula '{formula}' cannot be processed by {evaluate_pl.__name__}"  # type: ignore
    )


@evaluate_pl.register(_BinaryOp)
def evaluate_binary_op(formula: _BinaryOp, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over a binary operator."""
    return base_semantics(formula, evaluate_pl, interpretation)


@evaluate_pl.register(_UnaryOp)
def evaluate_unary_op(formula: _UnaryOp, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over a unary operator."""
    return base_semantics(formula, evaluate_pl, interpretation)


@evaluate_pl.register(Atomic)
def evaluate_atomic(formula: Atomic, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over an atomic formula."""
    return formula.name in _PropInterpretationWrapper(interpretation)


@evaluate_pl.register(TrueFormula)
def evaluate_true(_formula: TrueFormula, _interpretation: _PropInterpretation) -> bool:
    """Evaluate a "true" formula."""
    return True


@evaluate_pl.register(FalseFormula)
def evaluate_false(
    _formula: FalseFormula, _interpretation: _PropInterpretation
) -> bool:
    """Evaluate a "false" formula."""
    return False
