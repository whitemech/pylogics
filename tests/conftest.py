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

"""The conftest.py module for pytest."""
import pytest

from pylogics.syntax.base import reset_cache


@pytest.fixture(scope="class", autouse=True)
def reset_cache_fixture():
    """Reset hash-consing global cache after each test function/class call."""
    reset_cache()
