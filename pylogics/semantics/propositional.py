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

"""Semantics for propositional logic."""
from dataclasses import dataclass
from functools import singledispatch
from typing import Dict, Set, Union, cast

from pylogics.exceptions import PylogicsError
from pylogics.helpers.misc import enforce
from pylogics.semantics.base import base_semantics
from pylogics.syntax.base import (
    AtomName,
    BinaryOp,
    FalseFormula,
    Formula,
    TrueFormula,
    UnaryOp,
)
from pylogics.syntax.propositional import Atomic

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
def evaluate_prop(formula: Formula, _interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula against an interpretation."""
    raise PylogicsError(
        f"formula '{formula}' cannot be processed by {evaluate_prop.__name__}"  # type: ignore
    )


@evaluate_prop.register(BinaryOp)
def evaluate_binary_op(formula: BinaryOp, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over a binary operator."""
    return base_semantics(formula, evaluate_prop, interpretation)


@evaluate_prop.register(UnaryOp)
def evaluate_unary_op(formula: UnaryOp, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over a unary operator."""
    return base_semantics(formula, evaluate_prop, interpretation)


@evaluate_prop.register(Atomic)
def evaluate_atomic(formula: Atomic, interpretation: _PropInterpretation) -> bool:
    """Evaluate a propositional formula over an atomic formula."""
    return formula.name in _PropInterpretationWrapper(interpretation)


@evaluate_prop.register(TrueFormula)
def evaluate_true(_formula: TrueFormula, _interpretation: _PropInterpretation) -> bool:
    """Evaluate a "true" formula."""
    return True


@evaluate_prop.register(FalseFormula)
def evaluate_false(
    _formula: FalseFormula, _interpretation: _PropInterpretation
) -> bool:
    """Evaluate a "false" formula."""
    return False
