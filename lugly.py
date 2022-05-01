from string import ascii_uppercase
from string import ascii_lowercase
class BB:
    def __init__(self):
        self.clauses = []

    def tell(self, prop):
        cnf = convert_to_cnf(prop)
        for clause in cnf:
            self.clauses.append(clause)

    def entails(self, query):
        clauses = []
        clauses.extend(self.clauses)
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
            if self.is_superset_of(new_knowledge):
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

    def is_superset_of(self, new_knowledge):
        if(all(x in self.clauses for x in new_knowledge)):
            return True
        return False

    def remove_dubs(self, list):
        result = []
        for element in list:
            if element not in result:
                result.append(element)
        return result

class Proposition:
    def __init__(self, op, *vars):
        self.op = str(op)
        self.vars = vars  # map(expr, args) ## Coerce args to Exprs

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


# (P ^ Q) -> (Q v P)
#test1 = Or(And(V("A"), V("B")), V("C"))
#test2 = Implies(Implies(Not((V("P"))), V("Q")), Or(V("Q"), V("P")))
#test3 = Implies(Implies(Implies(Or(Not(V("A")), V("B")), V("C")), V("D")), V("E"))
#test4 = Not(Implies(V("Q"),V("P")))

#Trial = test2


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
        if char is "~":
            negate_next = True
        elif char is not "^":
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



'''

kb = []
kbcnf = []
p1 = Implies(Not(V("P")), V("Q"))
p2 = Implies(V("Q"), V("P"))
p3 = Implies(V("P"), And(V("R"),V("S")))
p4 = Not(And(V("P"), And(V("R"), V("S"))))


kb.extend([p1, p2, p3, p4])
for e in kb:
    kbcnf.append(convert_to_cnf(e))

for c in kbcnf:
    print(c.tostring())
'''


#sentence = eval(input("Input sentence ").upper())
#bb = BB()
#bb.tell(sentence)
#query = eval(input("Input query ").upper())
#print(bb.entails(query))


'''
test1 = Implies(Not(And(V("P"), Or(Not(V("R")), V("S")))), Implies(Not(V("P")), V("Q")))
test2 = Not(And(V("P"), And(Not(V("R")), V("S"))))
test3 = And(V("P"), V("Q"))
test4 = V("Q")
sentence1 = Implies(Not(V("P")), V("Q"))
sentence2 = Implies(V("Q"), V("P"))
sentence3 = Implies(V("P"), And(V("R"), V("S")))
#query = And(V("P"), And(V("R"), V("S")))
#print(test1.tostring())
CNF = convert_to_cnf(test2)
print(CNF)
bb = BB()
bb.tell(sentence1)
bb.tell(sentence2)
bb.tell(test3)
print("Bb:")
print(bb.clauses)
#print(bb.entails(V("P")))
print(bb.entails(query))
'''


#print(to_clauses(CNF))
#print(CNF.tostring())
#CNF = negation_inwards(CNF)
#print(CNF.tostring())
#CNF = distribute(test1)
#print(CNF.tostring())

#e = input()
#p = eval(e)
#print(p.tostring())