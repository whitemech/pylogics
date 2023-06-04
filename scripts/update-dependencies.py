#!/usr/bin/env python3
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
"""
This script updates the dev-dependencies specified in a Poetry managed pyproject.toml file to their latest versions.

The script reads the dev-dependencies from the provided pyproject.toml file and fetches the latest version of each
dependency from PyPI. It then updates the dependency in the pyproject.toml file to this latest version by running
the 'poetry add' command with the '^' compatibility character. If an error occurs while updating a dependency,
that dependency is skipped and the script continues with the next one.

Usage:
    python update_dependencies.py /path/to/pyproject.toml

Requirements:
    - Python 3.x
    - requests library
    - toml library
    - A valid pyproject.toml file managed by Poetry.
"""
import argparse
import logging
import subprocess
from pathlib import Path
from typing import Union

import requests
import toml


def get_latest_version(package: str) -> Union[str, None]:
    """
    Fetch the latest version of a package from PyPI.

    Args:
        package (str): The name of the package.

    Returns:
        Union[str, None]: The latest version of the package, or None if an error occurred.
    """
    try:
        response = requests.get(f"https://pypi.org/pypi/{package}/json")
        response.raise_for_status()
        version = response.json()["info"]["version"]
        logging.info(f"Latest version of {package} is {version}")
        return version
    except requests.HTTPError:
        logging.error(f"Failed to get the latest version for {package}, skipping...")
        return None


def update_dependencies(file_path: Path, poetry_path: Path) -> None:
    """
    Update the dev-dependencies in a pyproject.toml file to their latest versions.

    Args:
        file_path (Path): The path to the pyproject.toml file.
        poetry_path (str): The path to the poetry main entrypoint.
    """
    pyproject = toml.load(str(file_path))
    dev_dependencies = pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"]
    for package in dev_dependencies:
        latest_version = get_latest_version(package)
        if latest_version is not None:
            try:
                command = f"{poetry_path} add --group dev {package}^{latest_version}"
                logging.info(f'Running command "{command}"')
                subprocess.check_call(command, shell=True)
                logging.info(
                    f"Successfully updated {package} to version {latest_version}"
                )
            except subprocess.CalledProcessError:
                logging.error(f"Failed to update {package}, skipping...")
                continue


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO
    )
    parser = argparse.ArgumentParser(
        description="Update the dev-dependencies in a pyproject.toml file."
    )
    parser.add_argument(
        "file_path",
        metavar="path",
        type=Path,
        help="the path to the pyproject.toml file",
    )
    parser.add_argument(
        "--poetry-path",
        metavar="poetry",
        type=Path,
        default="poetry",
        help='the path to the poetry main entrypoint (default: "poetry")',
    )
    args = parser.parse_args()
    update_dependencies(args.file_path, args.poetry_path)
