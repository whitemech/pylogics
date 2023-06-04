One of the core features of the library is 
the support of parsing strings 
compliant to a certain grammar 
to handily build formulae.

The parsing functions, one for each logic formalism, 
can be imported from `pylogics.parsers`, and their
name is `parse_<id>`, where `<id>` is the 
identifier of the logic formalism.
For example, the parsing for propositional logic (`pl`)
is `parse_pl`, whereas the parsing function
for Linear Temporal Logic (`ltl`) is `parse_ltl`.
For a list of the supported logics and their identifier 
please look at [this page](supported_logics.md).

The library uses [Lark](https://lark-parser.readthedocs.io/en/latest/)
to generate the parser automatically.
The grammar files are reported at [this page](grammars.md).

The syntax for `LTL`, `PLTL` and `LDL`
aims to be compliant with 
[this specification](https://marcofavorito.me/tl-grammars/v/7d9a17267fbf525d9a6a1beb92a46f05cf652db6/).


## Symbols

A symbol is determined by the following regular expression:

```
SYMBOL: [a-z][a-z0-9_-]*|"\w+"
```

That is:

- if between quotes `""`, a symbol can be any 
  non-empty sequence of word characters: `[a-zA-Z0-9_-]+`
- if not, a symbol must:
  
    - have only have lower case characters
    - have at least one character and start with a non-digit character.


## Propositional Logic

Informally, the supported grammar for propositional logic is: 
```
pl_formula: pl_formula <-> pl_formula  // equivalence
          | pl_formula ->  pl_formula  // implication 
          | pl_formula ||  pl_formula  // disjunction 
          | pl_formula &&  pl_formula  // conjunction 
          | !pl_formula                // negation
          | ( pl_formula )             // brackets 
          | true                       // boolean propositional constant
          | false                      // boolean propositional constant
          | SYMBOL                     // prop. atom
```

Some examples:
```python
from pylogics.parsers import parse_pl
parse_pl("a")
parse_pl("b")
parse_pl("a & b")
parse_pl("a | b")
parse_pl("a >> b")
parse_pl("a <-> b")
parse_pl("a <-> a")       # returns a
parse_pl("!(a)")
parse_pl("true | false")  # returns true
parse_pl("true & false")  # returns false
```

## Linear Temporal Logic

Informally, the supported grammar for linear temporal logic is: 
```
ltl_formula: ltl_formula <-> ltl_formula  // equivalence
           | ltl_formula ->  ltl_formula  // implication 
           | ltl_formula ||  ltl_formula  // disjunction 
           | ltl_formula &&  ltl_formula  // conjunction 
           | !ltl_formula                 // negation
           | ( ltl_formula )              // brackets
           | ltl_formula U ltl_formula    // until 
           | ltl_formula R ltl_formula    // release 
           | ltl_formula W ltl_formula    // weak until 
           | ltl_formula M ltl_formula    // strong release 
           | F ltl_formula                // eventually 
           | G ltl_formula                // always 
           | X[!] ltl_formula             // next 
           | X ltl_formula                // weak next 
           | true                         // boolean propositional constant
           | false                        // boolean propositional constant
           | tt                           // boolean logical constant
           | ff                           // boolean logical constant
           | SYMBOL                       // propositional atom
```

Some examples:
```python
from pylogics.parsers import parse_ltl
parse_ltl("tt")
parse_ltl("ff")
parse_ltl("true")
parse_ltl("false")
parse_ltl("a")
parse_ltl("b")
parse_ltl("X(a)")
parse_ltl("X[!](b)")
parse_ltl("F(a)")
parse_ltl("G(b)")
parse_ltl("G(a -> b)")
parse_ltl("a U b")
parse_ltl("a R b")
parse_ltl("a W b")
parse_ltl("a M b")
```

## Past Linear Temporal Logic

Informally, the supported grammar for past linear temporal logic is: 
```
pltl_formula: pltl_formula <-> pltl_formula  // equivalence
            | pltl_formula ->  pltl_formula  // implication 
            | pltl_formula ||  pltl_formula  // disjunction 
            | pltl_formula &&  pltl_formula  // conjunction 
            | !pltl_formula                  // negation
            | ( pltl_formula )               // brackets
            | pltl_formula S pltl_formula    // since 
            | H pltl_formula                 // historically
            | O pltl_formula                 // once 
            | Y pltl_formula                 // before 
            | true                           // boolean propositional constant
            | false                          // boolean propositional constant
            | tt                             // boolean logical constant
            | ff                             // boolean logical constant
            | SYMBOL                         // propositional atom
```

Some examples:
```python
from pylogics.parsers import parse_pltl
parse_pltl("tt")
parse_pltl("ff")
parse_pltl("true")
parse_pltl("false")
parse_pltl("a")
parse_pltl("b")
parse_pltl("Y(a)")
parse_pltl("O(b)")
parse_pltl("H(a)")
parse_pltl("a S b")
```

## Linear Dynamic Logic

Informally, the supported grammar for linear dynamic logic is
(note; it is doubly-inductive): 
```
ldl_formula: ldl_formula <-> ldl_formula   // equivalence
           | ldl_formula ->  ldl_formula   // implication 
           | ldl_formula ||  ldl_formula   // disjunction 
           | ldl_formula &&  ldl_formula   // conjunction 
           | !ldl_formula                  // negation
           | ( ldl_formula )               // brackets
           | <regex>ldl_formula            // diamond formula
           | [regex]ldl_formula            // box formula
           | tt                            // boolean constant
           | ff                            // boolean constant

regex      : regex + regex                 // union 
           | regex ; regex                 // sequence 
           | ?regex                        // test 
           | regex*                        // star 
           | pl_formula                    // prop. formula (see above) 
```

Note: the question mark in the test regular expression 
is on the left, not on the right. This is done
to avoid parse conflicts in the parser generation.

Some examples:
```python
from pylogics.parsers import parse_ldl
parse_ldl("tt")
parse_ldl("ff")
parse_ldl("<a>tt")
parse_ldl("[a & b]ff")
parse_ldl("<a + b>tt")
parse_ldl("<a ; b><c>tt")
parse_ldl("<(a ; b)*><c>tt")
parse_ldl("<true><a>tt")  # Next a
parse_ldl("<(<a>tt?;true)*>(<b>tt)")  # (a Until b) in LDLf
```
