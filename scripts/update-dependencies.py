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
from typing import Optional

import requests
import toml
from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version, parse
from pkg_resources import parse_version

URL_PATTERN = "https://pypi.python.org/pypi/{package}/json"


def clean_version_specifier(version_specifier: str) -> str:
    """Clean version specifier by removing '.*' if present."""
    cleaned = version_specifier.replace(".*", "")
    return cleaned


def get_lowest_python_version(specifier_set: SpecifierSet) -> str:
    """Get the lowest Python version that satisfies the specifier set."""
    possible_versions = [
        f"{major}.{minor}.{patch}"
        for major in range(3, 4)
        for minor in range(10)
        for patch in range(10)
    ]
    satisfying_versions = [
        version for version in possible_versions if parse(version) in specifier_set
    ]
    return min(satisfying_versions, default="3")


def get_pyproject_python_version(pyproject_file: str) -> str:
    """Extract the Python version from a pyproject.toml file."""
    pyproject_data = toml.load(pyproject_file)
    python_version_specifier = pyproject_data["tool"]["poetry"]["dependencies"][
        "python"
    ]
    specifier_set = SpecifierSet(python_version_specifier)
    return get_lowest_python_version(specifier_set)


def get_version(package: str, python_version: str) -> Optional[str]:
    """Get the latest version of a package that is compatible with the provided Python version."""
    req = requests.get(URL_PATTERN.format(package=package))
    version = parse_version("0")
    if req.status_code == requests.codes.ok:
        j = req.json()
        releases = j.get("releases", [])
        for release in releases:
            try:
                ver = parse_version(release)
            except InvalidVersion:
                logging.warning(f"Skipping invalid version: {release}")
                continue

            release_info = j["releases"].get(str(ver), [{}])
            if release_info:
                info = release_info[-1]
                if not ver.is_prerelease and info:
                    requires_python = info["requires_python"]
                    requires_python = requires_python if requires_python else ">=3"
                    cleaned_requires_python = clean_version_specifier(requires_python)
                    if Version(python_version) in SpecifierSet(cleaned_requires_python):
                        version = max(version, ver)
    return str(version)


def update_dependencies(pyproject_file: str, poetry_path: str = "poetry") -> None:
    """Update the dev-dependencies in a pyproject.toml file to their latest versions."""
    pyproject_data = toml.load(pyproject_file)
    dev_dependencies = pyproject_data["tool"]["poetry"]["group"]["dev"]["dependencies"]
    python_version = get_pyproject_python_version(pyproject_file)

    for package in dev_dependencies:
        if package == "python":
            continue
        try:
            logging.info(f"Updating {package}")
            latest_version = get_version(package, python_version)
            if latest_version == "0":
                logging.warning(
                    f"Could not find a valid version for {package}, skipping."
                )
                continue
            logging.info(f"Latest version of {package} is {latest_version}")
            subprocess.run(
                [poetry_path, "add", "--group", "dev", f"{package}^{latest_version}"],
                check=True,
            )
        except Exception as e:
            logging.exception(f"Failed to update {package} due to error: {str(e)}")
            continue


def main():
    """Run main function to parse arguments and initiate the update process."""
    parser = argparse.ArgumentParser(
        description="Update the dev-dependencies in a pyproject.toml file to their latest versions."
    )
    parser.add_argument("file_path", help="The path to the pyproject.toml file.")
    parser.add_argument(
        "--poetry_path", default="poetry", help="The path to the Poetry executable."
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    update_dependencies(args.file_path, args.poetry_path)


if __name__ == "__main__":
    main()
