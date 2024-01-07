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

"""Tests on the pylogics.helpers module."""
import pickle

from pylogics.helpers.cache_hash import Hashable


class MyHashable(metaclass=Hashable):
    """A test class to test 'Hashable' metaclass."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.a = "a"
        self.b = "b"

    def __hash__(self):
        """Compute the hash."""
        return hash((self.a, self.b))


def test_hashable():
    """Test the hashable class."""
    obj = MyHashable()

    assert not hasattr(obj, "__hash")

    h1 = hash(obj)
    h2 = hash(obj)
    assert h1 == h2

    assert hasattr(obj, "__hash")
    assert obj.__hash == h1 == h2

    dumped_obj = pickle.dumps(obj)
    actual_obj = pickle.loads(dumped_obj)
    assert not hasattr(actual_obj, "__hash")
