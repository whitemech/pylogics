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

"""Test introduction documentation page."""
from pylogics.semantics.pl import evaluate_pl
from tests.conftest import DOCS_DIRECTORY
from tests.test_docs.base import BasePythonMarkdownDocs


class TestIntroduction(BasePythonMarkdownDocs):
    """Test that the code snippet in the introduction are correct."""

    MD_FILE = DOCS_DIRECTORY / "introduction.md"

    def _assert(self, locals_, *mocks):
        """Do assertions after Python code execution."""
        assert self.locals["evaluate_pl"] == evaluate_pl
