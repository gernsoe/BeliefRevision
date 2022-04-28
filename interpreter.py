from lugly import *

def __and__(self, other):    return to_proposition('and',self, other)
def __invert__(self):        return to_proposition('not', self)
def __rshift__(self, other): return to_proposition('implies', self, other)
def __or__(self, other):     return to_proposition('or', self, other)
def __mod__(self, other):    return to_proposition('iff', self, other)  ## (x % y)

e = input()
prop = eval(e)
print(prop.tostring())