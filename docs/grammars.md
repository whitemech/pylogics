
In this section, all the grammars used 
by the library are reported here.

## Propositional Logic

The file 
[`pl.lark`](https://github.com/whitemech/pylogics/blob/main/pylogics/parsers/pl.lark)
contains the specification of the Lark grammar, and it is reported below:

```lark
start: propositional_formula

?propositional_formula: prop_equivalence
?prop_equivalence: prop_implication (EQUIVALENCE prop_implication)*
?prop_implication: prop_or (IMPLY prop_or)*
?prop_or: prop_and (OR prop_and)*
?prop_and: prop_not (AND prop_not)*
?prop_not: NOT* prop_wrapped
?prop_wrapped: prop_atom
            | LEFT_PARENTHESIS propositional_formula RIGHT_PARENTHESIS
?prop_atom: atom
         | prop_true
         | prop_false

atom: SYMBOL_NAME
prop_true: TRUE
prop_false: FALSE

LEFT_PARENTHESIS : "("
RIGHT_PARENTHESIS : ")"
EQUIVALENCE : "<->"
IMPLY : ">>"|"->"
OR: "||"|"|"
AND: "&&"|"&"
NOT: "!"|"~"
TRUE.2: /true|TRUE/
FALSE.2: /false|FALSE/

// Symbols cannot start with uppercase letters, because these are reserved. Moreover, any word between quotes is a symbol.
// More in detail:
// 1) either start with [a-z_], followed by at least one [a-zA-Z0-9_-], and by one [a-zA-Z0-9_] (i.e. hyphens only in between)
// 2) or, start with [a-z_] and follows with any sequence of [a-zA-Z0-9_] (no hyphens)
// 3) or, any sequence of ASCII printable characters (i.e. going from ' ' to '~'), except '"'.
SYMBOL_NAME: FIRST_SYMBOL_CHAR _SYMBOL_1_BODY _SYMBOL_1_TAIL
           | FIRST_SYMBOL_CHAR _SYMBOL_2_BODY
           | DOUBLE_QUOTES _SYMBOL_3_BODY DOUBLE_QUOTES

_SYMBOL_QUOTED: DOUBLE_QUOTES _SYMBOL_3_BODY DOUBLE_QUOTES
_SYMBOL_1_BODY: /[a-zA-Z0-9_\-]+/
_SYMBOL_1_TAIL: /[a-zA-Z0-9_]/
_SYMBOL_2_BODY: /[a-zA-Z0-9_]*/
_SYMBOL_3_BODY: /[ -!#-~]+?/

DOUBLE_QUOTES: "\""
FIRST_SYMBOL_CHAR: /[a-z_]/


%ignore /\s+/
```

## Linear Temporal Logic

The Lark grammar for Linear Temporal Logic is defined
in [`ltl.lark`](https://github.com/whitemech/pylogics/blob/main/pylogics/parsers/ltl.lark),
and it is reported below:

```lark
start: ltlf_formula

?ltlf_formula:         ltlf_equivalence
?ltlf_equivalence:     ltlf_implication (EQUIVALENCE ltlf_implication)*
?ltlf_implication:     ltlf_or (IMPLY ltlf_or)*
?ltlf_or:              ltlf_and (OR ltlf_and)*
?ltlf_and:             ltlf_weak_until (AND ltlf_weak_until)*
?ltlf_weak_until:      ltlf_until (WEAK_UNTIL ltlf_until)*
?ltlf_until:           ltlf_release (UNTIL ltlf_release)*
?ltlf_release:         ltlf_strong_release (RELEASE ltlf_strong_release)*
?ltlf_strong_release:  ltlf_unaryop (STRONG_RELEASE ltlf_unaryop)*

?ltlf_unaryop:     ltlf_always
             |     ltlf_eventually
             |     ltlf_next
             |     ltlf_weak_next
             |     ltlf_not
             |     ltlf_wrapped

?ltlf_always:      ALWAYS ltlf_unaryop
?ltlf_eventually:  EVENTUALLY ltlf_unaryop
?ltlf_next:        NEXT ltlf_unaryop
?ltlf_weak_next:   WEAK_NEXT ltlf_unaryop
?ltlf_not:         NOT ltlf_unaryop
?ltlf_wrapped:     ltlf_atom
             |     LEFT_PARENTHESIS ltlf_formula RIGHT_PARENTHESIS
?ltlf_atom:        ltlf_symbol
          |        ltlf_true
          |        ltlf_false
          |        ltlf_tt
          |        ltlf_ff
          |        ltlf_last

ltlf_symbol: SYMBOL_NAME
ltlf_true: prop_true
ltlf_false: prop_false
ltlf_tt: TT
ltlf_ff: FF
ltlf_last: LAST

// Operators must not be part of a word
UNTIL.2: /U(?=[ "\(])/
RELEASE.2: /R(?=[ "\(])/
ALWAYS.2: /G(?=[ "\(])/
EVENTUALLY.2: /F(?=[ "\(])/
NEXT.2: /X\[!\](?=[ "\(])/
WEAK_NEXT.2: /X(?=[ "\(])/
WEAK_UNTIL.2: /W(?=[ "\(])/
STRONG_RELEASE.2: /M(?=[ "\(])/


END.2: /end/
LAST.2: /last/

TT.2: /tt/
FF.2: /ff/

%ignore /\s+/

%import  .pl.SYMBOL_NAME -> SYMBOL_NAME
%import  .pl.prop_true -> prop_true
%import  .pl.prop_false -> prop_false
%import  .pl.NOT -> NOT
%import  .pl.OR -> OR
%import  .pl.AND -> AND
%import  .pl.EQUIVALENCE -> EQUIVALENCE
%import  .pl.IMPLY -> IMPLY
%import  .pl.LEFT_PARENTHESIS -> LEFT_PARENTHESIS
%import  .pl.RIGHT_PARENTHESIS -> RIGHT_PARENTHESIS
```

## Past Linear Temporal Logic

The Lark grammar for Past Linear Temporal Logic is defined
in [`pltl.lark`](https://github.com/whitemech/pylogics/blob/main/pylogics/parsers/pltl.lark),
and it is reported below:

```lark
start: pltlf_formula

?pltlf_formula:     pltlf_equivalence
?pltlf_equivalence: pltlf_implication (EQUIVALENCE pltlf_implication)*
?pltlf_implication: pltlf_or (IMPLY pltlf_or)*
?pltlf_or:          pltlf_and (OR pltlf_and)*
?pltlf_and:         pltlf_since (AND pltlf_since)*
?pltlf_since:       pltlf_unaryop (SINCE pltlf_unaryop)*

?pltlf_unaryop:    pltlf_historically
             |     pltlf_once
             |     pltlf_before
             |     pltlf_not
             |     pltlf_wrapped

?pltlf_historically: HISTORICALLY pltlf_unaryop
?pltlf_once:         ONCE pltlf_unaryop
?pltlf_before:       BEFORE pltlf_unaryop
?pltlf_not:          NOT pltlf_unaryop
?pltlf_wrapped:      pltlf_atom
             |       LEFT_PARENTHESIS pltlf_formula RIGHT_PARENTHESIS
?pltlf_atom:       pltlf_symbol
           |       pltlf_true
           |       pltlf_false
           |       pltlf_tt
           |       pltlf_ff
           |       pltlf_start

pltlf_symbol: SYMBOL_NAME
pltlf_true: prop_true
pltlf_false: prop_false
pltlf_tt: TT
pltlf_ff: FF
pltlf_start: START

// Operators must not be part of a word
SINCE.2: /S(?=[ "\(])/
HISTORICALLY.2: /H(?=[ "\(])/
ONCE.2: /O(?=[ "\(])/
BEFORE.2: /Y(?=[ "\(])/
FIRST.2: /first/
START.2: /start/

%ignore /\s+/

%import  .pl.SYMBOL_NAME -> SYMBOL_NAME
%import  .pl.prop_true -> prop_true
%import  .pl.prop_false -> prop_false
%import  .pl.NOT -> NOT
%import  .pl.OR -> OR
%import  .pl.AND -> AND
%import  .pl.EQUIVALENCE -> EQUIVALENCE
%import  .pl.IMPLY -> IMPLY
%import  .pl.LEFT_PARENTHESIS -> LEFT_PARENTHESIS
%import  .pl.RIGHT_PARENTHESIS -> RIGHT_PARENTHESIS
%import  .ltl.TT -> TT
%import  .ltl.FF -> FF
```

## Linear Dynamic Logic

The Lark grammar for Linear Dynamic Logic is defined
in [`ldl.lark`](https://github.com/whitemech/pylogics/blob/main/pylogics/parsers/ldl.lark),
and it is reported below:

```lark
start: ldlf_formula

?ldlf_formula:     ldlf_equivalence
?ldlf_equivalence: ldlf_implication (EQUIVALENCE ldlf_implication)*
?ldlf_implication: ldlf_or (IMPLY ldlf_or)*
?ldlf_or:          ldlf_and (OR ldlf_and)*
?ldlf_and:         ldlf_unaryop (AND ldlf_unaryop)*

?ldlf_unaryop:     ldlf_box
             |     ldlf_diamond
             |     ldlf_not
             |     ldlf_wrapped
?ldlf_box:         LEFT_SQUARE_BRACKET regular_expression RIGHT_SQUARE_BRACKET ldlf_unaryop
?ldlf_diamond:     LEFT_ANGLE_BRACKET regular_expression RIGHT_ANGLE_BRACKET ldlf_unaryop
?ldlf_not:         NOT ldlf_unaryop
?ldlf_wrapped:    ldlf_atom
             |    LEFT_PARENTHESIS ldlf_formula RIGHT_PARENTHESIS
?ldlf_atom:       ldlf_tt
          |       ldlf_ff
          |       ldlf_last
          |       ldlf_end


ldlf_tt: TT
ldlf_ff: FF
ldlf_last: LAST
ldlf_end: END

regular_expression: re_union

?re_union:      re_sequence (UNION re_sequence)*
?re_sequence:   re_star (SEQ re_star)*
?re_star:       re_test STAR?
?re_test:       ldlf_formula TEST
        |       re_wrapped
?re_wrapped:    re_propositional
           |    LEFT_PARENTHESIS regular_expression RIGHT_PARENTHESIS
re_propositional: propositional_formula


LEFT_SQUARE_BRACKET: "["
RIGHT_SQUARE_BRACKET: "]"
LEFT_ANGLE_BRACKET: "<"
RIGHT_ANGLE_BRACKET: ">"
UNION: "+"
SEQ: ";"
TEST: "?"
STAR: "*"

%ignore /\s+/

%import  .pl.propositional_formula
%import  .pl.TRUE -> TRUE
%import  .pl.FALSE -> FALSE
%import  .pl.SYMBOL_NAME -> SYMBOL_NAME
%import  .pl.EQUIVALENCE -> EQUIVALENCE
%import  .pl.IMPLY -> IMPLY
%import  .pl.OR -> OR
%import  .pl.AND -> AND
%import  .pl.NOT -> NOT
%import  .pl.LEFT_PARENTHESIS -> LEFT_PARENTHESIS
%import  .pl.RIGHT_PARENTHESIS -> RIGHT_PARENTHESIS
%import  .ltl.LAST -> LAST
%import  .ltl.END -> END
%import  .ltl.TT -> TT
%import  .ltl.FF -> FF
```
