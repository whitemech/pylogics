The library can also be used through 
the syntax APIs.

Each class needed to build the syntax tree
of a formula of a certain logics 
is in `pylogics.syntax.<id>`,
where `<id>` is the logic formalism 
identifier.
See [this page](supported_logics.md)
for information about the supported 
formalisms.

The basic boolean connectives are defined
in `pylogics.syntax.base`. These are:

- `And`
- `Or`
- `Not`
- `Implies`
- `Equivalence`

The binary operators take
in input a sequence of arguments
instances of a subclass of `Formula`.
Note that as a precondition the operands.
must belong to the same logic formalism

E.g. to build $a & b$, one can do: 
```python
from pylogics.syntax.pl import Atomic
a = Atomic("a")
b = Atomic("b")
formula = a & b
```

Now `formula` is an instance of `pylogics.syntax.base.And`.
For the other operators (except equivalence):
```
a | b
!a
a >> b
```

For `true` and `false`, you can use
`TrueFormula` and `FalseFormula`,
respectively:

```python
from pylogics.syntax.base import Logic, TrueFormula, FalseFormula
true = TrueFormula(logic=Logic.PL)
false = TrueFormula(logic=Logic.PL)
```

## Linear Temporal Logic

For LTL, you can use the following classes,
defined in `pylogics.syntax.ltl`:

- `Atom`, an LTL atom
- `Next` (unary operator)
- `WeakNext` (unary operator)
- `Until` (binary operator)
- `Release` (binary operator)
- `WeakUntil` (binary operator)
- `StrongRelease` (binary operator)
- `Eventually` (unary operator)
- `Always` (unary operator)

To combine the above using boolean connectives,
you can use the classes in `pylogics.syntax.base`
described above.

## Past Linear Temporal Logic

For PLTL, you can use the following classes,
defined in `pylogics.syntax.pltl`:

- `Atom`, a PLTL atom
- `Before` (unary operator)
- `Since` (binary operator)
- `Once` (unary operator)
- `Historically` (unary operator)

To combine the above using boolean connectives,
you can use the classes in `pylogics.syntax.base`
described above.


## Linear Dynamic Temporal Logic

For LDL, you can use the following classes,
defined in `pylogics.syntax.ldl`:

- `TrueFormula(logic=Logic.LDL)`, the boolean positive constant `tt`
- `FalseFormula(logic=Logic.LDL)`, the boolean negative constant `ff`
- `Diamond(regex, ldlf_formula)`
- `Box(regex, ldlf_formula)`

To combine the above using boolean connectives,
you can use the classes in `pylogics.syntax.base`
described above.

To build regular expressions:

- `Prop(propositional)`, where `propositional` is a 
  propositional formula (i.e. `propositional.logic` is `Logic.PL`)
- `Union` (binary operator)
- `Seq` (binary operator)
- `Test(ldlf_formula)` (unary operator)
- `Star(regex)` (unary operator)
