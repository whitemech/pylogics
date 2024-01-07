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

"""Base module for logic parsers."""
import inspect
import os
from abc import ABC
from pathlib import Path
from typing import Type

from lark import Lark, Transformer

from pylogics.exceptions import ParsingError
from pylogics.syntax.base import Formula

CURRENT_DIR = Path(os.path.dirname(inspect.getfile(inspect.currentframe()))).absolute()  # type: ignore


class AbstractParser(ABC):
    """
    Abstract parser.

    Subclasses of this class need to specify:
    - transformer_cls: the class of the Lark transformer to use
    - lark_path: path to the Lark file that specifies the grammar.
    """

    transformer_cls: Type[Transformer]
    lark_path: str

    def __init__(self):
        """Initialize the parser."""
        self._transformer = self.transformer_cls()
        self._full_lark_path = CURRENT_DIR / self.lark_path
        self._parser = self._load_parser()

    def _load_parser(self) -> Lark:
        """Load the parser."""
        return Lark(
            self._full_lark_path.read_text(),
            parser="lalr",
            import_paths=[str(CURRENT_DIR)],
        )

    def __call__(self, text: str) -> Formula:
        """
        Call the parser.

        :param text: the string to parse.
        :return: the parsed formula.
        """
        tree = self._parser.parse(text)
        formula = self._transformer.transform(tree)
        return formula


class AbstractTransformer(Transformer, ABC):
    """Abstract Lark transformer."""

    @classmethod
    def _raise_parsing_error(cls, tag_name, args):
        """Raise a parsing error."""
        raise ParsingError(f"error while parsing a '{tag_name}' with tokens: {args}")

    @classmethod
    def _starred_binaryop(cls, args, formula_type, func_name):
        """
        Process a binary operator with repetitions.

        This parses rules of the form:   rule -> a (OP b)*

        :param args: The parsing Tree.
        :param formula_type: Constructor of the OP class. It must accept
            a list of arguments.
        :return: a Formula.
        """
        if len(args) == 1:
            return args[0]
        if (len(args) - 1) % 2 == 0:
            subformulas = args[::2]
            return formula_type(*subformulas)
        cls._raise_parsing_error(func_name, args)

    @classmethod
    def _process_unaryop(cls, args, formula_type):
        """
        Process a unary operator.

        This parses rules of the form:   rule -> a (OP b)*

        :param args: The parsing Tree.
        :param formula_type: Constructor of the OP class. It must accept
            a list of arguments.
        :return: a Formula.
        """
        if len(args) == 1:
            return args[0]
        f = args[-1]
        for _ in args[:-1]:
            f = formula_type(f)
        return f
