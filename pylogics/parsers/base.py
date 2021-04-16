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

"""Base module for logic parsers."""
import inspect
import os
from abc import ABC
from pathlib import Path
from typing import Type

from lark import Lark, Transformer

from pylogics.syntax.base import Formula

CURRENT_DIR = Path(os.path.dirname(inspect.getfile(inspect.currentframe())))  # type: ignore


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
        self._parser = Lark(self._full_lark_path.read_text(), parser="lalr")

    def __call__(self, text: str) -> Formula:
        """
        Call the parser.

        :param text: the string to parse.
        :return: the parsed formula.
        """
        tree = self._parser.parse(text)
        formula = self._transformer.transform(tree)
        return formula
