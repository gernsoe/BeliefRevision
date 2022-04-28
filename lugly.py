class Expr:
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


def And(left, right):
    return Expr('^', left, right)


def Or(left, right):
    return Expr('v', left, right)


def Implies(left, right):
    return Expr('->', left, right)


def Iff(left, right):
    return Expr('<->', left, right)


def Not(suffix):
    return Expr('~', suffix)


def V(var):
    return Expr(var)


# (P ^ Q) -> (Q v P)
test1 = Implies(V("P"), V("Q"))
test2 = Implies(Implies(Not((V("P"))), V("Q")), Or(V("Q"), V("P")))
test3 = Implies(Implies(Implies(Or(Not(V("A")), V("B")), V("C")), V("D")), V("E"))

Trial = test2
print(Trial.tostring())


def DoubleNot(E):
    if E.vars[0].op == '~':
        return (E.vars[0].vars[0])


def eliminate(E):
    if (len(E.tostring()) <= 2):
        # <= 2 is to include the Not(Var())
        return E

    if (E.op == '->'):
        return Or(Not(eliminate(E.vars[0])), eliminate(E.vars[1]))

    elif (E.op == '<->'):
        return (And(eliminate(Implies(E.vars[0], E.vars[1])), eliminate(Implies(E.vars[1], E.vars[0]))))

    elif (E.op == '^'):
        return (And(eliminate(E.vars[0]), eliminate(E.vars[1])))

    elif (E.op == 'v'):
        return (Or(eliminate(E.vars[0]), eliminate(E.vars[1])))


CNF = eliminate(Trial)
print(CNF.tostring())