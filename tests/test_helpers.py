# -*- coding: utf-8 -*-
#
# Copyright 2021 Marco Favorito
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
