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

"""Classes for natural deduction systems."""

from enum import Enum

from pylogics.syntax.base import Logic, Formula, FalseFormula, And, Or, Not, Implies
from pylogics.exceptions import PylogicsError

from pylogics.syntax.fol import Term, Variable, Constant, Function
from pylogics.syntax.fol import Predicate, ForAll, Exists
from pylogics.deduction.fol.base import AbstractDeductionSystem

class NaturalDeductionRule(Enum):
    """Enumeration of natural deduction rules."""

    and_e1 = "and_e1"   
    and_e2 = "and_e2"   
    and_i = "and_i"     
    assumption = "assumption"
    bot_e = "bot_e"
    copy = "copy"       
    dneg_e = "dneg_e"   
    dneg_i = "dneg_i"   
    exists_e = "exists_e"
    exists_i = "exists_i"
    forall_e = "forall_e"
    forall_i = "forall_i"
    impl_e = "impl_e"   
    impl_i = "impl_i"   
    MT = "MT"
    neg_e = "neg_e"
    neg_i = "neg_i"
    or_e = "or_e"
    or_i1 = "or_i1"
    or_i2 = "or_i2"
    premise = "premise"

class NaturalDeductionProof(list):
    def __init__(self, proof: list):
        super().__init__()
        while proof:
            row, content, *proof = proof
            if isinstance(content, Formula) or isinstance(content, Term):
                justification, *proof = proof
                self.append((row, content, justification))
            elif isinstance(content, list):
                if isinstance(content[0], Term) and isinstance(content[1], Formula):
                    content = [content[0]] + [NaturalDeductionRule.assumption, row] + content[1:]
                self.append((row, NaturalDeductionProof([row] + content), NaturalDeductionRule.assumption))

class NaturalDeduction(AbstractDeductionSystem):
    """Natural Deduction System."""

    ALLOWED_LOGICS = {Logic.PL, Logic.FOL}

    rule = NaturalDeductionRule

    def __init__(self):
        self.check_justification = {
            self.rule.and_e1:self._check_justification_and_e1,
            self.rule.and_e2:self._check_justification_and_e2,
            self.rule.and_i:self._check_justification_and_i,
            self.rule.assumption:self._check_justification_assumption,
            self.rule.bot_e:self._check_justification_bot_e,
            self.rule.copy:self._check_justification_copy,
            self.rule.dneg_e:self._check_justification_dneg_e,
            self.rule.dneg_i:self._check_justification_dneg_i,
            self.rule.exists_e:self._check_justification_exists_e,
            self.rule.exists_i:self._check_justification_exists_i,
            self.rule.forall_e:self._check_justification_forall_e,
            self.rule.forall_i:self._check_justification_forall_i,
            self.rule.impl_e:self._check_justification_impl_e,
            self.rule.impl_i:self._check_justification_impl_i,
            self.rule.MT:self._check_justification_MT,
            self.rule.neg_e:self._check_justification_neg_e,
            self.rule.neg_i:self._check_justification_neg_i,
            self.rule.or_e:self._check_justification_or_e,
            self.rule.or_i1:self._check_justification_or_i1,
            self.rule.or_i2:self._check_justification_or_i2,
            self.rule.premise:self._check_justification_premise,
        }
    
    def proof(self, proof: list):
        """Build a proof in the natural deduction expected format."""
        return NaturalDeductionProof(proof)

    def check_proof(self, proof: NaturalDeductionProof, sound = None) -> bool:
        """Check a given proof according to natural deduction rules."""
        # raise PylogicsError(
        #     f"proof '{proof}' cannot be processed by {self.check.__name__}"  # type: ignore
        # )
     
        sound = sound if sound else {}
        
        for row, content, justiﬁcation in proof:
            if isinstance(content, Formula):
                rule = justiﬁcation[0]
                args = [sound[i] for i in justiﬁcation[1:] if i in sound]
                if rule not in self.check_justification:
                    return False
                if self.check_justification[rule](content, *args) == False:
                    return False
            elif isinstance(content, list):
                if isinstance(content[0][1], Term) and self._find_term(content[0][1], *sound.values()):                    
                    return False # Term occurs outside its assumption
                if self.check_proof(content, {i:sound[i] for i in sound}) == False:
                    return False
            elif isinstance(content, Term):
                continue
            else:
                return False            
            sound[row] = content            
        return True


    def _check_justification_and_e1(self, formula, *args):
        """Check if the deduction is valid according to and-elimination (1) rule."""        
        return str(formula) == str(args[0].operands[0])

    def _check_justification_and_e2(self, formula, *args):
        """Check if the deduction is valid according to and-elimination (2) rule."""        
        return str(formula) == str(args[0].operands[1])

    def _check_justification_and_i(self, formula, *args):
        """Check if the deduction is valid according to and-introduction rule."""        
        return str(formula) == str(args[0] & args[1])

    def _check_justification_assumption(self, formula, *args):
        """Check if the deduction is valid according to assumption rule"""
        return True
    
    def _check_justification_bot_e(self, formula, *args):
        """Check if the deduction is valid according to absurd-elimination rule"""
        return args[0] == FalseFormula()

    def _check_justification_copy(self, formula, *args):
        """Check if the deduction is valid according to copy rule"""
        return str(formula) == str(args[0])

    def _check_justification_dneg_e(self, formula, *args):
        """Check if the deduction is valid according to double negation-elimination rule"""
        return str(~~formula) == str(args[0])

    def _check_justification_dneg_i(self, formula, *args):
        """Check if the deduction is valid according to double negation-introduction rule"""
        return str(formula) == str(~~args[0])

    def _check_justification_impl_e(self, formula, *args):
        """Check if the deduction is valid according to implies-elimination rule"""
        return str(args[0] >> formula) == str(args[1]) 

    def _check_justification_impl_i(self, formula, *args):
        """Check if the deduction is valid according to implies-introduction rule"""
        phi = args[0][ 0][1]
        psi = args[0][-1][1]
        return str(formula) == str(phi >> psi)

    def _check_justification_MT(self, formula, *args):
        """Check if the deduction is valid according to modus tollens rule"""
        return str(formula.argument >> args[1].argument) == str(args[0])

    def _check_justification_neg_e(self, formula, *args):
        """Check if the deduction is valid according to negation-elimination rule"""
        return str(~args[0]) == str(args[1]) and formula == FalseFormula()

    def _check_justification_neg_i(self, formula, *args):
        """Check if the deduction is valid according to negation-introduction rule"""        
        phi = args[0][ 0][1]
        psi = args[0][-1][1]
        return (psi == FalseFormula()) and (str(formula) == str(~phi))

    def _check_justification_or_e(self, formula, *args):
        """Check if the deduction is valid according to or-elimination rule"""
        phi_or_psi = args[0]
        phi, chi_1 = args[1][0][1], args[1][-1][1]        
        psi, chi_2 = args[2][0][1], args[2][-1][1]
        return (str(phi_or_psi) == str(phi | psi)) and (str(formula) == str(chi_1)) and (str(formula) == str(chi_2))

    def _check_justification_or_i1(self, formula, *args):
        """Check if the deduction is valid according to or-introduction 1 rule"""
        return str(formula.operands[0]) == str(args[0])

    def _check_justification_or_i2(self, formula, *args):
        """Check if the deduction is valid according to or-introduction 2 rule"""
        return str(formula.operands[1]) == str(args[0])

    def _check_justification_premise(self, formula, *args):
        """Check if the deduction is valid according to premise rule"""
        return True
    
    
    def _find_term(self, t:Term, *args):
        for x in args:
            if t == x:
                return True
            if 'argument' in dir(x) and self._find_term(t, x.argument):
                return True
            if 'operands' in dir(x) and self._find_term(t, *(x.operands)):
                return True
        return False

    def _find_diff(self, x:Formula, y:Formula):
        diffset = set()
        if type(x) != type(y):
            diffset = diffset | {(x,y)}
        elif 'argument' in dir(x):
            diffset = diffset | self._find_diff(x.argument, y.argument)
        elif 'operands' in dir(x):    
            if len(x.operands) != len(y.operands):
                diffset = diffset | {(x,y)}
            else:
                for a,b in zip(x.operands, y.operands):
                    diffset = diffset | self._find_diff(a,b)
        return diffset

    def _replace(self, formula:Formula, x:Variable, a:Term):
        if formula is x:
            return a
        if isinstance(formula,Not):
            return type(formula)(self._replace(formula.argument, x, a))
        if isinstance(formula,(Or,And,Implies)):
            return type(formula)(*[self._replace(o, x, a) for o in formula.operands])
        if isinstance(formula,(ForAll,Exists)):
            if formula.variable == x:
                return formula
            return type(formula)(formula.variable, [self._replace(o, x, a) for o in formula.operands])
        if isinstance(formula,(Predicate,Function)):
            return type(formula)(formula.name, [self._replace(o, x, a) for o in formula.operands])
        return formula

    def _check_justification_forall_i(self, formula, *args):
        """Check if the deduction is valid according to forall-introduction rule"""
        if not isinstance(formula, ForAll):
            return False
        a, phi_x_a = args[0][0][1], args[0][-1][1] 
        if not isinstance(a, Term):
            return False
        x, phi = formula.variable, formula.formula
        return str(self._replace(phi,x,a)) == str(phi_x_a)

    def _check_justification_forall_e(self, formula, *args):
        """Check if the deduction is valid according to forall-elimination rule"""
        if not isinstance(args[0], ForAll):
            return False
        x, phi = args[0].variable, args[0].formula
        a = [n for m,n in self._find_diff(phi, formula) if m == x]
        if len(a) != 1:
            return False
        a = a[0]
        phi_x_a = self._replace(phi, x, a)
        return str(phi_x_a) == str(formula)

    def _check_justification_exists_i(self, formula, *args):
        """Check if the deduction is valid according to exists-introduction rule"""
        if not isinstance(formula, Exists):
            return False
        x, phi = formula.variable, formula.formula
        a = [n for m,n in self._find_diff(phi, args[0]) if m == x]
        if len(a) > 1:
            return False
        a = a[0] if a else x
        phi_x_a = self._replace(phi, x, a)
        return str(phi_x_a) == str(args[0])

    def _check_justification_exists_e(self, formula, *args):
        """Check if the deduction is valid according to exists-elimination rule"""
        phi = args[0]
        if not isinstance(phi, Exists):
            return False
        a, phi_x_a = args[1][0][1], args[1][1][1]
        if not str(phi_x_a) == str(self._replace(phi.formula, phi.variable, a)):
            return False
        chi = args[1][-1][1]        
        if self._find_term(a, chi):
            return False
        return str(formula) == str(chi)

    @staticmethod
    def Proof(proof: list):
        """Build a proof according to the deduction system."""
        nd = NaturalDeduction()
        return nd.proof(proof)
    
    @staticmethod
    def check(proof: NaturalDeductionProof):
        """Check a given proof according to natural deduction rules."""
        nd = NaturalDeduction()
        return nd.check_proof(proof)    