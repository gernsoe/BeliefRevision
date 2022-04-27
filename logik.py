class PropKB:
    "A KB for Propositional Logic.  Inefficient, with no indexing."

    def __init__(self)#, sentence=None):
        self.clauses = []
        #if sentence:
        #    self.tell(sentence)

    def tell(self, sentence):
        "Add the sentence's clauses to the KB"
        self.clauses.extend(conjuncts(to_cnf(sentence)))

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