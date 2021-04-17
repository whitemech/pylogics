# -*- coding: utf-8 -*-
#
# This file is part of pylogics.
#
# pylogics is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylogics is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylogics.  If not, see <https://www.gnu.org/licenses/>.
#

"""Base classes for pylogics logic formulas."""
from abc import ABC, abstractmethod
from enum import Enum
from typing import FrozenSet, Optional, Sequence

from pylogics.helpers.cache_hash import Hashable
from pylogics.helpers.misc import enforce


class Logic(Enum):
    """This enumeration lists the supported logics."""

    PL = "propositional logic"
    FOL = "first-order logic"
    SOL = "second-order logic"
    LTL = "linear temporal logic"
    LDL = "linear dynamic logic"


class Formula(ABC, metaclass=Hashable):
    """Base class for all the formulas."""

    @property
    @abstractmethod
    def logic(self) -> Logic:
        """Get the formalism of the formula."""

    def __invert__(self) -> "Formula":
        """Negate the formula."""
        return Not(self)

    def __and__(self, other: "Formula") -> "Formula":
        """Put in and with another formula."""
        return And(self, other)

    def __or__(self, other: "Formula") -> "Formula":
        """Put in or with another formula."""
        return Or(self, other)

    def __rshift__(self, other: "Formula") -> "Formula":
        """Define A implies B."""
        return Or(Not(self), other)


class BinaryOp(Formula):
    """Binary operator."""

    SYMBOL: str

    def __init__(self, *operands: Formula):
        """
        Init a binary operator.

        :param operands: the operands.
        """
        super().__init__()
        self._operands = list(operands)

    @property
    def operands(self) -> Sequence[Formula]:
        """Get the operands."""
        return tuple(self._operands)

    @property
    def logic(self) -> Logic:
        """Get the formalism of the formula."""
        # checking the first operand is enough as
        # by the invariant every operand of a
        # binary op belongs to the same formalism.
        return self.operands[0].logic

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.logic, self.operands))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({self.SYMBOL} {' '.join(map(str, self.operands))})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(self._operands)})"

    def __eq__(self, other):
        """Compare with another object."""
        return isinstance(other, type(self)) and self.operands == other.operands


class UnaryOp(Formula, ABC):
    """Unary operator."""

    SYMBOL: str

    def __init__(self, arg: Formula):
        """
        Initialize the unary operator.

        :param arg: the argument.
        """
        super().__init__()
        self._arg = arg

    @property
    def argument(self) -> Formula:
        """Get the argument."""
        return self._arg

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.logic, self.argument))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({self.SYMBOL} {self.argument})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(self.argument)})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return isinstance(other, type(self)) and self.argument == other.argument


class TrueFormula(Formula):
    """A tautology."""

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return Logic.PL

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash(TrueFormula)

    def __str__(self) -> str:
        """Get the string representation."""
        return "true"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return "TrueFormula()"

    def __eq__(self, other):
        """
        Compare with another object.

        We only check whether the other formula is
        an instance of this class, hence making
        the set of instances of this class
        equal between them.
        """
        return isinstance(other, TrueFormula)

    def __neg__(self) -> Formula:
        """Negate."""
        return FALSE


class FalseFormula(Formula):
    """A contradiction."""

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return Logic.PL

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash(FalseFormula)

    def __str__(self) -> str:
        """Get the string representation."""
        return "false"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return "FalseFormula()"

    def __eq__(self, other):
        """
        Compare with another object.

        We only check whether the other formula is
        an instance of this class, hence making
        the set of instances of this class
        equal between them.
        """
        return isinstance(other, FalseFormula)

    def __neg__(self) -> Formula:
        """Negate."""
        return TRUE


TRUE = TrueFormula()
FALSE = FalseFormula()


class _MonotoneBinaryOp(Hashable):
    """
    Metaclass to simplify binary monotone operator instantiations.

    In particular:
    - if the absorbing element of the operation is present in the
      operands, then simplify the formula (e.g. false & p -> false).
    - if there are repeated operands in the list of operands,
      consider them only once (idempotence).
    """

    _absorbing: Optional[Formula] = None

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        cls._check_operands_same_logic()
        operands = cls._simplify_monotone_op_operands(cls, *args)
        if len(operands) == 1:
            return operands[0]

        return super(_MonotoneBinaryOp, cls).__call__(*operands, **kwargs)

    @staticmethod
    def _simplify_monotone_op_operands(cls, *operands):
        operands = list(dict.fromkeys(operands))
        # filter out the identity element
        identity = ~cls._absorbing
        operands = list(filter(lambda x: x != identity, operands))
        if len(operands) == 0:
            return [~cls._absorbing]
        elif len(operands) == 1:
            return [operands[0]]
        elif cls._absorbing in operands:
            return cls._absorbing

        # shift-up subformulas with same operator. DFS on expression tree.
        new_operands = []
        seen_operands = set()
        stack = operands[::-1]  # it is reversed in order to preserve order.
        while len(stack) > 0:
            element = stack.pop()
            if not isinstance(element, cls):
                if element not in seen_operands:
                    new_operands.append(element)
                    seen_operands.add(element)
                continue
            stack.extend(reversed(element.operands))  # see above regarding reversed.

        return new_operands

    @classmethod
    def _check_operands_same_logic(mcs, *operands: Formula):
        """
        Check that the operands belong to the same logic.

        TrueFormula and FalseFormula are not considered.

        :param operands: the sequence of operands.
        :return: None
        :raises: PylogicsError: if the check fails.
        """
        filtered_operands = list(
            filter(lambda x: not isinstance(x, (TrueFormula, FalseFormula)), operands)
        )
        if len(filtered_operands) == 0:
            return
        logic = filtered_operands[0]
        enforce(
            all(sub_formula.logic == logic for sub_formula in filtered_operands),
            message="operands do not belong to the same logic",
        )


class CommutativeBinaryOp(BinaryOp):
    """Commutative binary operator."""

    @property
    def _frozenset_operands(self) -> FrozenSet[Formula]:
        """
        Get the operands in a frozenset.

        It is useful for canonical representation of the same
        (commutative) operator.
        """
        return frozenset(self.operands)

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self._frozenset_operands))

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({repr(set(self._frozenset_operands))})"

    def __eq__(self, other):
        """Compare with another object."""
        return (
            isinstance(other, type(self))
            and self._frozenset_operands == other._frozenset_operands
        )


class And(CommutativeBinaryOp, metaclass=_MonotoneBinaryOp):
    """And operator."""

    _absorbing = FALSE
    SYMBOL = "and"


class Or(CommutativeBinaryOp, metaclass=_MonotoneBinaryOp):
    """Or operator."""

    _absorbing = TRUE
    SYMBOL = "or"


class Not(UnaryOp):
    """Not operator."""

    SYMBOL = "not"

    def __new__(cls, arg, **kwargs):
        """Instantiate the object."""
        if isinstance(arg, Not):
            # ~~phi = phi
            return arg.argument
        return super(Not, cls).__new__(cls)

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return self.argument.logic


class _MetaImpliesOp(Hashable):
    """
    Metaclass for the imply operator.

    It performs some simplifications on the arguments.
    """

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        operands = cls._simplify_operands(*args)
        if len(args) == 0:
            raise ValueError("cannot accept zero arguments")
        if len(operands) == 1:
            return operands[0]

        return super(_MetaImpliesOp, cls).__call__(*operands, **kwargs)

    @staticmethod
    def _simplify_operands(*operands):
        """Simplify operands."""
        operands = list(dict.fromkeys(operands))
        if len(operands) == 0:
            return []
        if len(operands) == 1:
            return [operands[0]]

        new_operands = []
        for operand in operands:
            if operand == FALSE:
                return new_operands
            new_operands.append(operand)
        return operands


class ImpliesOp(BinaryOp, metaclass=_MetaImpliesOp):
    """
    Implication operator.

    The operator over the list of operands is considered right-associative.
    """

    SYMBOL = "implies"


class _MetaEquivalenceOp(Hashable):
    """
    Metaclass for the equivalence operator.

    It performs some simplifications on the arguments.
    """

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        operands = cls._simplify_operands(*args)
        if len(args) == 0:
            raise ValueError("cannot accept zero arguments")
        if len(operands) == 1:
            return operands[0]

        return super(_MetaEquivalenceOp, cls).__call__(*operands, **kwargs)

    @staticmethod
    def _simplify_operands(*operands):
        """Simplify operands."""
        no_duplicate_operands = dict.fromkeys(operands)
        operands = list(no_duplicate_operands)
        if len(operands) == 0:
            return []
        if len(operands) == 1:
            return [operands[0]]
        return operands


class EquivalenceOp(CommutativeBinaryOp, metaclass=_MetaEquivalenceOp):
    """Equivalence operator."""

    SYMBOL = "equivalence"


def ensure_formula(f: Optional[Formula], is_none_true: bool) -> Formula:
    """
    Ensure the argument is a formula.

    :param f: the formula, or None.
    :param is_none_true: if true, None reduces to TrueFormula; FalseFormula otherwise.
    :return: the same set, or an empty set if the arg was None.
    """
    return f if f is not None else TrueFormula() if is_none_true else FalseFormula()