import math
from string import ascii_uppercase
from string import ascii_lowercase
from itertools import chain, combinations

class BB:
    def __init__(self):
        self.clauses = []

    def __copy__(self):
        copy_bb = BB()
        for prop in self.clauses:
            copy_bb.clauses.append(prop)
        return copy_bb

    def __repr__(self):
        str = ""
        for prop in self.clauses:
            str = str+prop.tostring()+" "
        return str

    def tell(self, prop):
        self.clauses.append(prop)
        self.clauses = self.remove_dubs(self.clauses)

    def entails(self, knowledge, query=None):
        clauses = []
        for prop in knowledge:
            cnf = convert_to_cnf(prop)
            clauses.extend(cnf)
        #clauses.extend(self.clauses)
        if not query == None:
            query = Not(query)
            query = convert_to_cnf(query)
            clauses.extend(query)
        new_knowledge = []
        while True:
            all_combinations = self.combine_elements(clauses)
            for clause1, clause2 in all_combinations:
                changed, resolvents = self.resolve(clause1, clause2)
                if changed:
                    if self.has_empty_clause(resolvents):
                        return True
                    new_knowledge.extend(resolvents)
                    new_knowledge = self.remove_dubs(new_knowledge)
            if self.is_subset(clauses, new_knowledge):
                return False
            if new_knowledge:
                clauses.extend(new_knowledge)
                clauses = self.remove_dubs(clauses)

    def combine_elements(self, clauses):
        result = []
        length = len(clauses)
        for i in range(length):
            for j in range(i + 1, length):
                result.append((clauses[i], clauses[j]))
        return result

    def has_empty_clause(self, resolvent):
        if not resolvent:
            return True
        for clause in resolvent:
            if not clause:
                return True
        return False

    def resolve(self, clause1, clause2):
        clauses = []
        changed = False
        for c1 in clause1:
            for c2 in clause2:
                if str(c1) == "~"+str(c2) or "~"+str(c1) == str(c2):
                    c1_result = list(filter(lambda var: var != c1, clause1))
                    c2_result = list(filter(lambda var: var != c2, clause2))
                    c1_result.extend(c2_result)
                    result = self.remove_dubs(c1_result)
                    clauses.append(result)
                    changed = True
        return changed, clauses

    def is_subset(self, l, sub_l):
        if(all(x in l for x in sub_l)):
            return True
        return False

    def remove_dubs(self, list):
        result = []
        for element in list:
            if element not in result:
                result.append(element)
        return result

    def generate_remainders(self, phi):
        powerset = chain.from_iterable(combinations(self.clauses, r) for r in range(1, len(self.clauses)+1))
        remainders = []
        anti = []

        #find all subsets that does not entail phi
        for tup in powerset:
            if not self.entails(list(tup), phi):
                anti.append(tup)

        # If there are no subsets that don't entail phi, the new knowledge base should be empty.
        if len(anti) == 0:
            return []

        #now find all of those subsets, with the maximal size
        max_size = len(anti[-1])
        for tup in anti:
            if len(tup) == max_size:
                remainders.append(tup)

        return remainders

    def expansion(self, phi):
        self.partial_meet_contraction(Not(phi))
        self.tell(phi)

    def partial_meet_contraction(self, phi):
        remainders = self.generate_remainders(phi)
        new_kb = self.select_and_intersect(remainders)
        self.clauses = new_kb

    def select_and_intersect(self, remainders):
        if len(remainders) == 0:
            return []
        elif len(remainders) == 1:
            return list(remainders[0])
        max_size = 0
        intersected = []
        max_size_kbs = []
        combinations = self.combine_elements(remainders)
        for l1, l2 in combinations:
            intersect = intersection(list(l1), list(l2))
            if len(intersect) > max_size:
                max_size = len(intersect)
            intersected.append(intersect)

        for kb in intersected:
            if len(kb) == max_size:
                max_size_kbs.append(kb)

        age_of_formulas = 0 # the lower the older, i.e. better
        oldest_seen = math.inf
        oldest_kb = max_size_kbs[0]

        for kb in max_size_kbs:
            for prop in kb:
                age_of_formulas += self.clauses.index(prop)
            if age_of_formulas < oldest_seen:
                oldest_seen = age_of_formulas
                oldest_kb = kb
            age_of_formulas = 0

        return list(oldest_kb)


class Proposition:
    def __init__(self, op, *vars):
        self.op = str(op)
        self.vars = vars

    def __eq__(self, other):
        if not isinstance(other, Proposition):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.op == other.op and self.vars == other.vars


    def tostring(self):
        if (len(self.vars) == 0):
            return str(self.op)
        elif (len(self.vars) == 1):
            return self.op + (self.vars[0].tostring())
        else:
            return "(" + (self.vars[0].tostring()) + self.op + (self.vars[1].tostring()) + ")"


    def __and__(self, other):
        return And(self, other)
    def __invert__(self):
        return Not(self)
    def __rshift__(self, other):
        return Implies(self, other)
    def __or__(self, other):
        return Or(self, other)
    def __mod__(self, other):
        return Iff(self, other)


def intersection(l1, l2):
    intersect = [value for value in l1 if value in l2]
    return intersect


def And(left, right):
    return Proposition('^', left, right)
def Or(left, right):
    return Proposition('v', left, right)
def Implies(left, right):
    return Proposition('->', left, right)
def Iff(left, right):
    return Proposition('<->', left, right)
def Not(suffix):
    return Proposition('~', suffix)
def V(var):
    return Proposition(var)

def convert_to_cnf(E):
    cnf = eliminate(E)
    cnf = negation_inwards(cnf)
    cnf = distribute(cnf)
    cnf = cnf_to_clauses(cnf)
    return cnf

def cnf_to_clauses(cnf):
    cnf = cnf.tostring()
    cnf = cnf.replace("(", "")
    cnf = cnf.replace(")", "")
    cnf = cnf.replace("v", "")
    negate_next = False
    result = []
    smallerArray = []
    for char in cnf:
        if char == "~":
            negate_next = True
        elif char != "^":
            if negate_next:
                smallerArray.append("~" + char)
                negate_next = False
            else:
                smallerArray.append(char)
        else:
            result.append(smallerArray)
            smallerArray = []
    result.append(smallerArray)
    return result


def is_variable(E):
    return len(E.tostring()) <= 2 # Variable string is only 1 long


def eliminate(E):
    if is_variable(E):
        return E
    elif E.op == '->':
        return Or(Not(eliminate(E.vars[0])), eliminate(E.vars[1]))
    elif E.op == '<->':
        return And(eliminate(Implies(E.vars[0], E.vars[1])), eliminate(Implies(E.vars[1], E.vars[0])))
    elif E.op == '^':
        return And(eliminate(E.vars[0]), eliminate(E.vars[1]))
    elif E.op == 'v':
        return Or(eliminate(E.vars[0]), eliminate(E.vars[1]))
    elif E.op == '~':
        return Not(eliminate(E.vars[0]))


def negation_inwards(E):
    if is_variable(E):
        return E
    elif E.op == '~':
        if E.vars[0].op == '~':
            return negation_inwards(E.vars[0].vars[0])
        elif E.vars[0].op == 'v':
            return And(negation_inwards(Not(E.vars[0].vars[0])), negation_inwards(Not(E.vars[0].vars[1])))
        elif E.vars[0].op == '^':
            return Or(negation_inwards(Not(E.vars[0].vars[0])), negation_inwards(Not(E.vars[0].vars[1])))
    else:
        if E.op == '->':
            return Implies(negation_inwards(E.vars[0]), negation_inwards(E.vars[1]))
        elif E.op == '<->':
            return Iff(negation_inwards(E.vars[0]), negation_inwards(E.vars[1]))
        elif E.op == '^':
            return And(negation_inwards(E.vars[0]), negation_inwards(E.vars[1]))
        elif E.op == 'v':
            return Or(negation_inwards(E.vars[0]), negation_inwards(E.vars[1]))


def distribute(E):
    if is_variable(E):
        return E
    elif E.op == 'v':
        if E.vars[0].op == '^':
            return And(distribute(Or(E.vars[0].vars[0], E.vars[1])), distribute(Or(E.vars[0].vars[1], E.vars[1])))
        elif E.vars[1].op == '^':
            return And(distribute(Or(E.vars[0], E.vars[1].vars[0])), distribute(Or(E.vars[0], E.vars[1].vars[1])))
        else:
            return Or(distribute(E.vars[0]), distribute(E.vars[1]))
    else:
        return E