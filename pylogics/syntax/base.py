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

"""Base classes for pylogics logic formulas."""
import re
from abc import ABC, abstractmethod
from enum import Enum
from typing import Container, Dict, FrozenSet, Optional, Sequence, Union, cast

from pylogics.exceptions import PylogicsError
from pylogics.helpers.cache_hash import Hashable
from pylogics.helpers.misc import RegexConstrainedString, enforce


class Logic(Enum):
    """Enumeration of logic formalisms."""

    PL = "pl"
    LTL = "ltl"
    LDL = "ldl"
    PLTL = "pltl"
    PLDL = "pldl"
    FOL = "fol"
    MSO = "mso"
    RE = "re"


class _HashConsing(Hashable):
    """
    This metaclass implements hash consing for logic formulae.

    It makes sure the same formula is not repeated across the intepreter.
    """

    _context: Dict[Logic, Dict["Formula", None]] = {}

    def __new__(mcs, *args, **kwargs):
        """Instantiate a new class."""
        instance = super().__new__(mcs, *args, **kwargs)
        instance.__context = mcs._context
        return instance

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        enforce(
            issubclass(cls, Formula),
            "this class cannot be the metaclass of a class that is not a subclass of 'Formula'",
            PylogicsError,
        )
        instance = cast(Formula, super().__call__(*args, **kwargs))
        cached_instance = cls._context.setdefault(instance.logic, {}).get(
            instance, None
        )
        if cached_instance is None:
            # cache the instance.
            cls._context[instance.logic][instance] = None
            cached_instance = instance
        return cached_instance


def reset_cache():
    """Reset hash consing cache."""
    _HashConsing._context = {}


def get_cache_context():
    """Get cache context."""
    return _HashConsing._context


class Formula(ABC, metaclass=_HashConsing):
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


class _MetaOp(_HashConsing):
    """Metaclass for (binary and unary) operators."""

    def __call__(cls, *operands, **kwargs):
        """Init the subclass object."""
        cls._check_not_forbidden_formalism(*operands)
        return super(_MetaOp, cls).__call__(*operands, **kwargs)

    def _check_not_forbidden_formalism(cls, *operands):
        """Check operands belong to same formalism."""
        enforce(len(operands) >= 1, "expected at least one operand.")
        logic = operands[0].logic
        allowed = getattr(cls, "ALLOWED_LOGICS", None)
        forbidden = getattr(cls, "FORBIDDEN_LOGICS", None)
        if allowed is not None:
            forbidden = []

        is_logic_allowed = allowed is not None and logic in allowed
        is_logic_forbidden = forbidden is not None and logic in forbidden
        if is_logic_allowed and not is_logic_forbidden:
            raise ValueError(
                f"error during instantiation of class {cls.__name__}: "
                f"found operand belonging to logic {logic}, which is forbidden"
            )


class _BinaryOp(Formula):
    """
    Binary operator.

    SYMBOL: the symbol to represent this operator in the native string representation.
    ALLOWED_LOGICS: the collection of allowed formalisms whose formulae can be
      the arguments of the operator. This has to be set in concrete classes.
      If None, then the FORBIDDEN_LOGICS field is processed.
    FORBIDDEN_LOGICS: the collection of formalisms whose formula cannot be
      the arguments of the operator. This has to be set in concrete classes.
      If ALLOWED_LOGICS is specified, this field is ignored.
      If this field is None, then no check is applied.
    """

    SYMBOL: str
    ALLOWED_LOGICS: Optional[Container[Logic]] = None
    FORBIDDEN_LOGICS: Optional[Container[Logic]] = None

    def __init__(self, *operands: Formula):
        """
        Init a binary operator.

        :param operands: the operands.
        """
        super().__init__()
        enforce(
            len(operands) >= 2,
            f"expected at least 2 operands, found {len(operands)} operands",
        )
        enforce(
            all(map(lambda x: isinstance(x, Formula), operands)),
            "some argument is not an instance of 'Formula'",
            exception_cls=ValueError,
        )
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
        return (
            isinstance(other, type(self))
            and self.logic == other.logic
            and self.operands == other.operands
        )


class _UnaryOp(Formula, ABC):
    """
    Unary operator.

    SYMBOL: the symbol to represent this operator in the native string representation.
    ALLOWED_LOGICS: the collection of allowed formalisms whose formulae can be
      the argument of the operator. This has to be set in concrete classes.
      If None, then the FORBIDDEN_LOGICS field is processed.
    FORBIDDEN_LOGICS: the collection of formalisms whose formula cannot be
      the argument of the operator. This has to be set in concrete classes.
      If ALLOWED_LOGICS is specified, this field is ignored.
      If this field is None, then no check is applied.
    """

    SYMBOL: str
    ALLOWED_LOGICS: Optional[Container[Logic]] = None
    FORBIDDEN_LOGICS: Optional[Container[Logic]] = None

    def __init__(self, arg: Formula):
        """
        Initialize the unary operator.

        :param arg: the argument.
        """
        enforce(
            isinstance(arg, Formula),
            "argument is not an instance of 'Formula'",
            exception_cls=ValueError,
        )
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
        return (
            isinstance(other, type(self))
            and self.logic == other.logic
            and self.argument == other.argument
        )


class TrueFormula(Formula):
    """A tautology."""

    def __init__(self, logic: Logic = Logic.PL):
        """Initialize."""
        super().__init__()
        self._logic = logic

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return self._logic

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.logic))

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"TrueFormula({self.logic})"

    def __eq__(self, other):
        """
        Compare with another object.

        We only check whether the other formula is
        an instance of this class, hence making
        the set of instances of this class
        equal between them.
        """
        return type(other) == type(self) and self.logic == other.logic

    def __invert__(self) -> "Formula":
        """Negate."""
        return make_boolean(False, logic=self.logic)


class FalseFormula(Formula):
    """A contradiction."""

    def __init__(self, logic: Logic = Logic.PL):
        """Initialize."""
        super().__init__()
        self._logic = logic

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return self._logic

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.logic))

    def __str__(self) -> str:
        """Get the string representation."""
        return "false"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"FalseFormula({self.logic})"

    def __eq__(self, other):
        """
        Compare with another object.

        We only check whether the other formula is
        an instance of this class, hence making
        the set of instances of this class
        equal between them.
        """
        return type(other) == type(self) and self.logic == other.logic

    def __invert__(self) -> "Formula":
        """Negate."""
        return make_boolean(True, logic=self.logic)


def make_boolean(value: bool, logic: Logic) -> Formula:
    """
    Make a boolean formula.

    :param value: the boolean value.
    :param logic: the logic formalism it belongs to.
    :return: the formula.
    """
    formula_cls = TrueFormula if value else FalseFormula
    return formula_cls(logic=logic)


class _MonotoneBinaryOp(_MetaOp):
    """
    Metaclass to simplify binary monotone operator instantiations.

    In particular:
    - if the absorbing element of the operation is present in the
      operands, then simplify the formula (e.g. false & p -> false).
    - if there are repeated operands in the list of operands,
      consider them only once (idempotence).
    """

    _absorbing: bool

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        if len(args) == 0:
            raise ValueError("cannot accept zero arguments")
        cls._check_operands_same_logic()
        operands = cls._simplify_monotone_op_operands(cls, *args)
        if len(operands) == 1:
            return operands[0]

        return super(_MonotoneBinaryOp, cls).__call__(*operands, **kwargs)

    @staticmethod
    def _simplify_monotone_op_operands(cls, *operands):
        operands = list(dict.fromkeys(operands))
        # filter out the identity element
        logic = operands[0].logic
        absorbing = make_boolean(cls._absorbing, logic=logic)
        identity = ~absorbing
        operands = list(filter(lambda x: x != identity, operands))
        if len(operands) == 0:
            return [~absorbing]
        elif len(operands) == 1:
            return [operands[0]]
        elif absorbing in operands:
            return [absorbing]

        # shift-up subformulas with same operator. DFS on expression tree.
        new_operands = []
        seen_operands = set()
        stack = operands[::-1]  # it is reversed in order to preserve order.
        while len(stack) > 0:
            element = stack.pop()
            if not isinstance(element, cls):
                if ~element in seen_operands:
                    # i.e. if you get "phi OP (INV phi)"
                    # then we just return the absorbing element
                    return [absorbing]
                if element not in seen_operands:
                    # thanks to idempotency, we can remove duplicates
                    new_operands.append(element)
                    seen_operands.add(element)
                continue
            # if here, we met a sub-operand of type OP
            # we pop-up the operands of the subformula
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


class _CommutativeBinaryOp(_BinaryOp):
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


class And(_CommutativeBinaryOp, metaclass=_MonotoneBinaryOp):
    """And operator."""

    _absorbing = False
    SYMBOL = "and"
    FORBIDDEN_LOGICS = {Logic.RE}


class Or(_CommutativeBinaryOp, metaclass=_MonotoneBinaryOp):
    """Or operator."""

    _absorbing = True
    SYMBOL = "or"
    FORBIDDEN_LOGICS = {Logic.RE}


class Not(_UnaryOp):
    """Not operator."""

    SYMBOL = "not"
    FORBIDDEN_LOGICS = {Logic.RE}

    def __new__(cls, arg, **kwargs):
        """Instantiate the object."""
        if isinstance(arg, (Not, TrueFormula, FalseFormula)):
            return ~arg
        return super(Not, cls).__new__(cls)

    def __invert__(self):
        """Invert the negation."""
        return self.argument

    @property
    def logic(self) -> Logic:
        """Get the logical formalism."""
        return self.argument.logic


class _MetaImpliesOp(_MetaOp):
    """
    Metaclass for the imply operator.

    It performs some simplifications on the arguments.
    """

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        operands = cls._simplify_operands(*args)
        if len(operands) == 0:
            raise ValueError("cannot accept zero arguments")
        if len(operands) == 1:
            return operands[0]

        return super(_MetaImpliesOp, cls).__call__(*operands, **kwargs)

    @staticmethod
    def _simplify_operands(*operands):
        """Simplify operands."""
        if len(operands) == 0:
            return []
        if len(operands) == 1:
            return [operands[0]]

        logic = operands[0].logic
        false = make_boolean(False, logic=logic)
        new_operands = []
        for operand in operands:
            if operand == false:
                # ex falso sequitur quodlibet
                new_operands.append(~false)
                return new_operands
            new_operands.append(operand)
        return operands


class Implies(_BinaryOp, metaclass=_MetaImpliesOp):
    """
    Implication operator.

    The operator over the list of operands is considered right-associative.
    """

    SYMBOL = "implies"
    FORBIDDEN_LOGICS = {Logic.RE}


class _MetaEquivalenceOp(_MetaOp):
    """
    Metaclass for the equivalence operator.

    It performs some simplifications on the arguments.
    """

    def __call__(cls, *args, **kwargs):
        """Init the subclass object."""
        operands = cls._simplify_operands(*args)
        enforce(len(args) > 0, "cannot accept zero arguments", ValueError)
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


class Equivalence(_CommutativeBinaryOp, metaclass=_MetaEquivalenceOp):
    """Equivalence operator."""

    SYMBOL = "equivalence"
    FORBIDDEN_LOGICS = {Logic.RE}


def ensure_formula(f: Optional[Formula], is_none_true: bool) -> Formula:
    """
    Ensure the argument is a formula.

    :param f: the formula, or None.
    :param is_none_true: if true, None reduces to TrueFormula; FalseFormula otherwise.
    :return: the same set, or an empty set if the arg was None.
    """
    return f if f is not None else TrueFormula() if is_none_true else FalseFormula()


class AtomName(RegexConstrainedString):
    """
    A string that denotes an atomic propositional symbol.

    Symbols cannot start with uppercase letters, because these are reserved. Moreover, any word between quotes is a
     symbol.

    More in detail:

    1) either start with [a-z_], followed by at least one [a-zA-Z0-9_-], and by one [a-zA-Z0-9_] (i.e. hyphens only in
       between);
    2) or, start with [a-z_] and follows with any sequence of [a-zA-Z0-9_] (no hyphens);
    3) or, any sequence of ASCII printable characters (i.e. going from ' ' to '~'), except '"'.
    """

    REGEX = re.compile(
        r"[a-z_]([a-zA-Z0-9_-]+[a-zA-Z0-9_])|[a-z_][a-zA-Z0-9_]*|\"[ -!#-~]+?\""
    )


_AtomNameOrStr = Union[str, AtomName]


class AbstractAtomic(Formula, ABC):
    """An abstract atomic proposition."""

    def __init__(self, name: _AtomNameOrStr):
        """
        Initialize the atomic proposition.

        :param name: the symbol name.
        """
        super().__init__()
        self._name = str(AtomName(name))

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    def __hash__(self) -> int:
        """Compute the hash."""
        return hash((type(self), self.logic, self.name))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"{self.name}"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"Atomic({self.logic}, {self.name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, type(self))
            and self.logic == other.logic
            and self.name == other.name
        )
