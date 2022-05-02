from belief_base import *
import os


def menu():
    print('1.See Belief Base')
    print('2.Query knowledge base for entailment')
    print('3.Force-add Proposition to belief base')
    print('4.Expand Belief Base')
    print('5.Contract Belief Base')
    print('6.Reset Belief Base')
    print('7.Exit')
    Choice = input()
    os.system('CLS')
    return Choice


Belief_base = BB()
for letter in ascii_uppercase[:22]:
    exec("{} = V('{}')".format(letter, letter))

Belief_base.tell(~P>>Q)
Belief_base.tell(Q>>P)
Belief_base.tell(P>>(R&S))

print('Welcome to the belief state robot!')
server = True

while server:
    Option = menu()
    if Option == str(1):
        print('Belief Base:')
        print(Belief_base)
        print()
        # Check logical entailment.
    #

    if Option == str(2):
        print('Provide a formula to check entailment')
        Proposition = eval(input())
        # Check if this is a proposition other error message and back to main menu
        # Check if the variables are within the set Vars, otherwise cannot be used.
        entailment = Belief_base.entails(Belief_base.clauses, Proposition)
        os.system('CLS')
        if entailment:
            print(Proposition.tostring()+" follows from KB: ",end="")
            print(Belief_base)
        else:
            print(Proposition.tostring()+" does not follow from KB: ",end="")
            print(Belief_base)
        print()

    #

    if Option == str(3):
        print('Which new proposition should be added directly to the belief base (not expansion)?')
        Proposition = eval(input())
        # Check if this is a proposition other error message and back to main menu
        # Check if the variables are within the set Vars, otherwise cannot be used.
        Belief_base.tell(Proposition)
        os.system('CLS')

    #

    if Option == str(4):
        print('Which proposition should the belief base be expanded with? (Levi identity)')
        Proposition = eval(input())
        Belief_base.expansion(Proposition)
        print(Belief_base)
        print()
    #

    if Option == str(5):
        print('Which proposition should be contracted from the Belief Base?')
        Proposition = eval(input())
        Belief_base.partial_meet_contraction(Proposition)
        print(Belief_base)
        print()
    #

    if Option == str(6):
        Belief_base = BB()

    #

    if Option == str(7):
        server = False
