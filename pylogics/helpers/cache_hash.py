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

"""Base classes for pylogics logic formulas."""
from abc import ABCMeta
from functools import wraps
from typing import Any, Callable, cast


def _cache_hash(fn) -> Callable[[Any], int]:
    """
    Compute the (possibly memoized) hash.

    If the hash for this object has already
    been computed, return it. Otherwise,
    compute it and store for later calls.

    :param fn: the hashing function.
    :return: the new hashing function.
    """

    @wraps(fn)
    def __hash__(self):
        if not hasattr(self, "__hash"):
            self.__hash = fn(self)
        return cast(int, self.__hash)

    return __hash__


def _getstate(fn):
    """
    Get the state.

    We need to ignore the hash value because in case the object
    is serialized with e.g. Pickle, if the state is restored
    with another instance of the interpreter, the stored hash might
    be inconsistent with the PYTHONHASHSEED initialization of the
    new interpreter.
    """

    @wraps(fn)
    def __getstate__(self):
        d = fn(self)
        d.pop("__hash")
        return d

    return __getstate__


def default_getstate(self):
    """Implement the default getstate."""
    return self.__dict__


def default_setstate(self, state):
    """Implement the default getstate."""
    self.__dict__ = state


def _setstate(fn):
    """
    Set the state.

    The hash value needs to be set to None
    as the state might be restored in another
    interpreter in which the old hash value
    might not be consistent anymore.
    """

    @wraps(fn)
    def __setstate__(self, state):
        fn(self, state)
        if hasattr(self, "__hash"):
            delattr(self, "__hash")

    return __setstate__


class Hashable(ABCMeta):
    """
    A metaclass that makes class instances to cache their hash.

    It sets:
        __hash__
        __getstate__
        __setstate__

    """

    def __new__(mcs, *args, **kwargs):
        """Create a new instance."""
        class_ = super().__new__(mcs, *args, **kwargs)

        class_.__hash__ = _cache_hash(class_.__hash__)

        getstate_fn = (
            class_.__getstate__ if hasattr(class_, "__getstate__") else default_getstate
        )
        class_.__getstate__ = _getstate(getstate_fn)

        setstate_fn = (
            class_.__setstate__ if hasattr(class_, "__setstate__") else default_setstate
        )
        class_.__setstate__ = _setstate(setstate_fn)
        return class_
