<h1 align="center">
  <b>PyLogics</b>
</h1>

<p align="center">
  <a href="https://pypi.org/project/pylogics">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/pylogics">
  </a>
  <a href="https://pypi.org/project/pylogics">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pylogics" />
  </a>
  <a href="">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/pylogics" />
  </a>
  <a href="">
    <img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/pylogics">
  </a>
  <a href="">
    <img alt="PyPI - Wheel" src="https://img.shields.io/pypi/wheel/pylogics">
  </a>
  <a href="https://github.com/whitemech/pylogics/blob/master/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/whitemech/pylogics">
  </a>
</p>
<p align="center">
  <a href="">
    <img alt="test" src="https://github.com/whitemech/pylogics/workflows/test/badge.svg">
  </a>
  <a href="">
    <img alt="lint" src="https://github.com/whitemech/pylogics/workflows/lint/badge.svg">
  </a>
  <a href="">
    <img alt="docs" src="https://github.com/whitemech/pylogics/workflows/docs/badge.svg">
  </a>
  <a href="https://codecov.io/gh/whitemech/pylogics">
    <img alt="codecov" src="https://codecov.io/gh/whitemech/pylogics/branch/master/graph/badge.svg?token=FG3ATGP5P5">
  </a>
</p>
<p align="center">
  <a href="https://img.shields.io/badge/flake8-checked-blueviolet">
    <img alt="" src="https://img.shields.io/badge/flake8-checked-blueviolet">
  </a>
  <a href="https://img.shields.io/badge/mypy-checked-blue">
    <img alt="" src="https://img.shields.io/badge/mypy-checked-blue">
  </a>
  <a href="https://img.shields.io/badge/code%20style-black-black">
    <img alt="black" src="https://img.shields.io/badge/code%20style-black-black" />
  </a>
  <a href="https://www.mkdocs.org/">
    <img alt="" src="https://img.shields.io/badge/docs-mkdocs-9cf">
  </a>
</p>


A Python library for logic formalisms representation and manipulation.

## Install

To install the package from PyPI:
```
pip install pylogics
```

## Tests

To run tests: `tox`

To run only the code tests: `tox -e py3.7`

To run only the linters: 
- `tox -e flake8`
- `tox -e mypy`
- `tox -e black-check`
- `tox -e isort-check`

Please look at the `tox.ini` file for the full list of supported commands. 

## Docs

To build the docs: `mkdocs build`

To view documentation in a browser: `mkdocs serve`
and then go to [http://localhost:8000](http://localhost:8000)

## License

pylogics is released under the MIT License.

Copyright 2021-2024 The Pylogics contributors

## Authors

- [Marco Favorito](https://github.com/marcofavorito)
