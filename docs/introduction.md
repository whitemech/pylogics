# Introduction

`pylogics` is a Python package 
to parse and manipulate several
logic formalisms, with a focus 
on [temporal logics](https://plato.stanford.edu/entries/logic-temporal/).

> :warning: This library is in early development, and the 
> API might be broken frequently or may contain bugs :bug:.

> :warning: Docs are not thorough and might be inaccurate.
> Apologies.

## Quickstart

For example, consider [Propositional Logic](https://iep.utm.edu/prop-log/).
The following code allows you to parse a propositional logic formula
$\phi = (a \wedge b) \vee (c \wedge d)$:
```python
from pylogics.parsers import parse_pl
formula = parse_pl("(a & b) | (c & d)")
```
The object referenced by `formula` is an instance
of `Formula`. Each instance of `Formula` is associated with 
a certain logic formalism. You can read it
by accessing the `logic` attribute:
```
formlua.logic
```
which returns an instance of the Enum class 
`pylogics.syntax.base.Logic`.

We can evaluate the formula on a propositional interpretation.
First, import the function `evaluate_pl`:
```python
from pylogics.semantics.pl import evaluate_pl
```

`evaluate_pl` takes in input an instance of
`Formula`, with `formula.logic` equal to `Logic.PL`,
and a propositional interpretation $I$ in the form
of a set of strings or a dictionary from strings to booleans.

- when a set is given, each symbol in the set
  is considered true; if not, it is considered
  false.
- when a dictionary is given, the value
  of the symbol in the model is determined by
  the boolean value in the dictionary associated
  to that key. If the key is not present, it is
  assumed to be false.

For example, say we want to evaluate 
the formula over the model $\mathcal{I}_1 = \{a\}$.
We have $\mathcal{I}_1 \not\models \phi$: 
```python
evaluate_pl(formula, {'a'})  # returns False
```

Now consider $\mathcal{I}_2 = \{a, b\}$.
We have $\mathcal{I}_2 \models \phi$: 
```python
evaluate_pl(formula, {'a', 'b'})  # returns True
```

Alternatively, we could have written:
```python
evaluate_pl(formula, {'a': True, 'b': True, 'c': False})  # returns True
```
The value for `d` is assumed to be false, since it is not in the 
dictionary.

## Other logics

Currently, the package provides support for:

- Linear Temporal Logic (on finite traces) 
  ([De Giacomo and Vardi, 2013](https://www.cs.rice.edu/~vardi/papers/ijcai13.pdf),
  [Brafman et al., 2018](http://www.diag.uniroma1.it//~patrizi/docs/papers/BDP@AAAI18.pdf))
- Past Linear Temporal Logic (on finite traces) 
  [(De Giacomo et al., 2020)](http://www.dis.uniroma1.it/~degiacom/papers/2020draft/ijcai2020ddfr.pdf)
- Linear Dynamic Logic (on finite traces)
  ([De Giacomo and Vardi, 2013](https://www.cs.rice.edu/~vardi/papers/ijcai13.pdf),
  [Brafman et al., 2018](http://www.diag.uniroma1.it//~patrizi/docs/papers/BDP@AAAI18.pdf))

We consider the variants of these formalisms that also works for empty
traces; hence (Brafman et al., 2018) is a better reference for the 
supported logics. More details will be provided in the next sections.
