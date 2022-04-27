class Expr:
    def __init__(self, op, *vars):
        self.op = str(op)
        self.vars = vars #map(expr, args) ## Coerce args to Exprs

    def tostring(self):
        if(len(self.vars) == 0):
            return str(self.op)
        elif(len(self.vars) == 1):
            return self.op + (self.vars[0].tostring())
        else:
            return "("+(self.vars[0].tostring()) + self.op + (self.vars[1].tostring())+")"


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

#~((P ^ Q) >> (Q v P))
test2 = Not(Implies(And(V("P"), V("Q")), Or(V("Q"), V("P"))))
test3 = Not(Implies(And(Implies(V("P"),V("Q")), V("R") ), Or(V("Q"), V("P"))))
testV = And(V("P"), V("Q"))
print(test3.tostring())



