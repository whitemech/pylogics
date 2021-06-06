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

"""Test grammars documentation page."""

from tests.conftest import DOCS_DIRECTORY, LIBRARY_DIRECTORY
from tests.test_docs.base import BaseTestMarkdownDocs


class TestGrammars(BaseTestMarkdownDocs):
    """Test that the docs' and library's grammars are the same."""

    MD_FILE = DOCS_DIRECTORY / "grammars.md"

    @classmethod
    def setup_class(cls):
        """Set up the test."""
        super().setup_class()

        grammar_directory = LIBRARY_DIRECTORY / "parsers"

        for formalism in ["pl", "ltl", "pltl", "ldl"]:
            text = (grammar_directory / f"{formalism}.lark").read_text()
            setattr(cls, formalism + "_grammar", text)

        cls.actual_grammars = cls.extract_code_blocks(filter_="lark")

    def test_pl_grammar(self):
        """Test PL grammar is as expected."""
        assert self.actual_grammars[0] == self.pl_grammar

    def test_ltl_grammar(self):
        """Test LTL grammar is as expected."""
        assert self.actual_grammars[1] == self.ltl_grammar

    def test_pltl_grammar(self):
        """Test PLTL grammar is as expected."""
        assert self.actual_grammars[2] == self.pltl_grammar

    def test_ldl_grammar(self):
        """Test LDL grammar is as expected."""
        assert self.actual_grammars[3] == self.ldl_grammar
