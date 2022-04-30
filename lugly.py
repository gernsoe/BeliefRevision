from string import ascii_uppercase
from string import ascii_lowercase
class BB:
    def __init__(self):
        self.clauses = []

    def tell(self, prop):
        cnf = convert_to_cnf(prop)
        for clause in cnf:
            self.clauses.append(clause)


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

test1 = Implies(Not(And(V("P"), Or(Not(V("R")), V("S")))), Implies(Not(V("P")), V("Q")))
test2 = Not(And(V("P"), And(Not(V("R")), V("S"))))
#print(test1.tostring())
CNF = convert_to_cnf(test2)
print(CNF)
#print(to_clauses(CNF))
#print(CNF.tostring())
#CNF = negation_inwards(CNF)
#print(CNF.tostring())
#CNF = distribute(test1)
#print(CNF.tostring())


for letter in ascii_uppercase[:22]:
    exec("{} = V('{}')".format(letter, letter))

#e = input()
#p = eval(e)
#print(p.tostring())