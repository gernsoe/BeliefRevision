import re


class PropKB:
    "A KB for Propositional Logic.  Inefficient, with no indexing."

    def __init__(self):
        #, sentence=None):
        self.clauses = []
        #if sentence:
        #    self.tell(sentence)

    def tell(self, sentence):
        "Add the sentence's clauses to the KB"
        if isinstance(sentence, str):
            sentence = expr(sentence)
        # self.clauses.extend(conjuncts(to_cnf(sentence)))
        self.clauses.extend(sentence)

    '''
    def ask_generator(self, query):
        "Yield the empty substitution if KB implies query; else False"
        if not tt_entails(Expr('&', *self.clauses), query):
            return
        yield {}

    def retract(self, sentence):
        "Remove the sentence's clauses from the KB"
        for c in conjuncts(to_cnf(sentence)):
            if c in self.clauses:
                self.clauses.remove(c)
    '''


class Expr:
    def __init__(self, op, *args):
        self.op = str(op)
        self.args = map(expr, args) ## Coerce args to Exprs

    def __call__(self, *args):
        """Self must be a symbol with no args, such as Expr('F').  Create a new
        Expr with 'F' as op and the args as arguments."""
        return Expr(self.op, *args)

    '''
    def __repr__(self):
        "Show something like 'P' or 'P(x, y)', or '~P' or '(P & Q) >> (Q & P)'"
        if len(self.args) == 0: # Constant or proposition with arity 0
            return str(self.op)
        elif is_symbol(self.op): # Functional or Propositional operator
            return '%s(%s)' % (self.op, ', '.join(map(repr, self.args)))
        elif len(self.args) == 1: # Prefix operator
            return self.op + repr(self.args[0])
        else: # Infix operator
            return '(%s)' % (' '+self.op+' ').join(map(repr, self.args))

    def __eq__(self, other):
        """x and y are equal iff their ops and args are equal."""
        return (other is self) or (isinstance(other, Expr)
            and self.op == other.op and self.args == other.args)

    def __hash__(self):
        "Need a hash method so Exprs can live in dicts."
        return hash(self.op) ^ hash(tuple(self.args))
    '''

    # https://docs.python.org/3/library/operator.html
    def __and__(self, other):    return Expr('&',  self, other)
    def __invert__(self):        return Expr('~',  self)
    def __rshift__(self, other): return Expr('>>', self, other)
    def __or__(self, other):     return Expr('|',  self, other)
    def __xor__(self, other):    return Expr('^',  self, other)
    def __mod__(self, other):    return Expr('<=>',  self, other)

def expr(s):
    if isinstance(s, Expr): return s
    ## Replace a symbol or number, such as 'P' with 'Expr("P")'
    s = re.sub(r'([a-zA-Z0-9_.]+)', r'Expr("\1")', s)
    ## Now eval the string.  (A security hole; do not use with an adversary.)
    return eval(s, {'Expr':Expr})