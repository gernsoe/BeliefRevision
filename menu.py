from lugly import *
import os


def menu():
    print('1.See Belief Base')
    print('2.Expand Belief Base')
    print('3.Contract Belief Base')
    print('4.Reset Belief Base')
    print('5.Exit')
    Choice = input()
    os.system('CLS')
    return Choice


Belief_base = BB()
for letter in ascii_uppercase[:22]:
    exec("{} = V('{}')".format(letter, letter))

print('Welcome to the belief state robot!')
server = True

while server:
    Option = menu()
    if Option == str(1):
        print('Belief Base:')
        print(Belief_base.clauses)
        print()
        # Check logical entailment.
    #

    if Option == str(2):
        print('Which new proposition should be added?')
        Proposition = eval(input())
        # Check if this is a proposition other error message and back to main menu
        # Check if the variables are within the set Vars, otherwise cannot be used.

        Belief_base.tell(Proposition)
        os.system('CLS')

    #

    if Option == str(3):
        print('Which proposition should be contracted from the Belief Base?')
        print(Belief_base)
        print()
    #

    if Option == str(4):
        Belief_base = BB()

    #

    if Option == str(5):
        server = False
