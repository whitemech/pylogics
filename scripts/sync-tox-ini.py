#!/usr/bin/env python3
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
"""
This Python script updates the dependencies in a tox.ini file based on the deps specified in a pyproject.toml file.

The script reads the dev-dependencies from the pyproject.toml file and then updates the
version specifiers in the tox.ini file. The version specifiers in the pyproject.toml file
use the caret (^) version specifier, which is not compatible with pip. Therefore, this script
converts the caret version specifiers into pip-friendly lower and upper bounds.

Usage:

    python sync-tox-ini.py path/to/pyproject.toml path/to/tox.ini

"""
import argparse
import configparser
import logging
from pathlib import Path
from typing import Dict

import toml
from packaging.requirements import Requirement

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def get_dependencies(pyproject_toml_path: Path) -> Dict[str, str]:
    """
    Get the dev and main dependencies from pyproject.toml.

    Args:
        pyproject_toml_path: Path to pyproject.toml.

    Returns:
        A dictionary mapping dependency names to their versions.
    """
    pyproject_toml = toml.load(str(pyproject_toml_path))
    dependencies = (
        pyproject_toml.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )
    dev_dependencies = (
        pyproject_toml.get("tool", {})
        .get("poetry", {})
        .get("group", {})
        .get("dev", {})
        .get("dependencies", {})
    )

    # Merge the two dictionaries
    all_dependencies = {**dependencies, **dev_dependencies}

    return all_dependencies


def parse_version(version: str) -> str:
    """
    Parse a version specifier and convert it into pip-friendly format.

    Args:
        version: Version specifier. Could be in the form '^x.y', '^x.y.z' or 'x.y.z'.

    Returns:
        A string representing the version specifier in pip-friendly format.
    """
    if version[0] != "^":  # if version doesn't start with caret, return as is
        return version

    parts = list(map(int, version[1:].split(".")))
    if len(parts) == 2:  # ^x.y
        major, minor = parts
        return f">={major}.{minor},<{major + 1}"
    elif len(parts) == 3:  # ^x.y.z
        major, minor, patch = parts
        return f">={major}.{minor}.{patch},<{major}.{minor + 1}.0"
    elif len(parts) == 4:  # ^x.y.z.w
        major, minor, patch, patch_level = parts
        return f">={major}.{minor}.{patch}.{patch_level},<{major}.{minor}.{patch + 1}.0"
    else:
        raise ValueError(f"Invalid version specifier: {version}")


def update_tox_ini(tox_ini_path: Path, dependencies: Dict[str, str]) -> None:
    """
    Update dependencies in tox.ini based on the provided dictionary.

    Args:
        tox_ini_path: Path to tox.ini.
        dependencies: A dictionary mapping dependency names to their versions.
    """
    config = configparser.ConfigParser()
    config.read(tox_ini_path)

    for section in config.sections():
        if section.startswith("testenv"):
            deps = config[section].get("deps", "").split("\n")
            new_deps = []
            for dep in deps:
                try:
                    req = Requirement(dep)
                    dep_name = req.name
                    if dep_name in dependencies:
                        new_version = parse_version(dependencies[dep_name])
                        new_dep = dep_name + new_version
                        new_deps.append(new_dep)
                    else:
                        new_deps.append(dep)
                except Exception:
                    new_deps.append(dep)
            config[section]["deps"] = "\n".join(new_deps)

    with tox_ini_path.open("w") as file:
        config.write(file)


def main() -> None:
    """Parse command line arguments and update dependencies in tox.ini based on pyproject.toml."""
    parser = argparse.ArgumentParser(
        description="Update tox.ini dependencies based on pyproject.toml"
    )
    parser.add_argument("pyproject", type=Path, help="Path to pyproject.toml")
    parser.add_argument("tox", type=Path, help="Path to tox.ini")
    args = parser.parse_args()

    logging.info("Reading dev-dependencies from pyproject.toml")
    dependencies = get_dependencies(args.pyproject)
    logging.info("Updating tox.ini")
    update_tox_ini(args.tox, dependencies)
    logging.info("Done")


if __name__ == "__main__":
    main()
