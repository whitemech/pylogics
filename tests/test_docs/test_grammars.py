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
