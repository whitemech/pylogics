# History

## 0.2.1 (2023-06-06)

The main change of this release is to relax the supported grammar, in particular regarding the symbols definition.

* Wip/grammar by @francescofuggitti in https://github.com/whitemech/pylogics/pull/81
  * Earlier, symbols could not contain uppercase letters. Now, symbols cannot *start* with uppercase letters.
  * Now, hyphens can only occur in the middle characters of a word, i.e. neither at the start nor at the end of the symbol (unless quoted).
  * Double quoted words can contain all printable characters (except the double quote ".


## 0.1.1 (2021-09-25)

- Fixed bug in LDLf parsing; the regular expression of type "test"
  was not parsed correctly ([#76](https://github.com/whitemech/pylogics/pull/76)). 
- Other minor bug fixing

## 0.1.0 (2021-06-07)

- Improved to the behaviour of `Not`:
  - Make `Not` to simplify when argument is a boolean formula. If `Not` is applied to `TrueFormula`, then the output is `FalseFormula`; 
    likewise, if it is applied to `FalseFormula`, the output is `TrueFormula`.
  - Fix: replace `__neg__` with `__invert__`
- Improved simplification of monotone operators: check also
  the presence of `phi OP ~phi` and reduce according to the 
  binary operator involved.
- Added tests to check consistency between code and documentation.
- Updated grammars so to be compliant with 
  version `0.2.0` of [this standard](https://marcofavorito.me/tl-grammars/v/7d9a17267fbf525d9a6a1beb92a46f05cf652db6/).



## 0.1.0a0 (2021-04-23)

- Added support for Propositional Logic parsing, 
  syntax representation and parsing.
- Added support for Linear Temporal Logic
  parsing and syntax representation.
- Added support for Past Linear Temporal Logic
  parsing and syntax representation.
- Added support for Linear Dynamic Logic 
  parsing and syntax representation.
