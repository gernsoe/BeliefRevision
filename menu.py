from belief_base import *
import os


def menu():
    print('1.See belief base')
    print('2.Populate belief base with example')
    print('3.Query belief base for entailment')
    print('4.Expand(Revise) belief Base')
    print('5.Contract belief Base')
    print('6.Reset belief Base')
    print('7.Exit')
    Choice = input()
    os.system('CLS')
    return Choice


Belief_base = BB()
for letter in ascii_uppercase[:22]:
    exec("{} = V('{}')".format(letter, letter))
    #print(letter)
acceptable_characters = []
acceptable_characters.extend(ascii_uppercase[:22])
acceptable_characters.extend(ascii_lowercase[:22])
acceptable_characters.extend(['~','&','|','>>','%',' '])

os.system('CLS')
print('Welcome to the belief state robot!')
print()
server = True


def check_input(u_input):
    u_input = u_input.replace(" ", "")
    if u_input == "":
        return False
    for c in u_input:
        if c not in acceptable_characters:
            return False
    return True

while server:
    Option = menu()
    if Option == str(1):
        print('Belief Base:')
        print(Belief_base)
        print()
        # Check logical entailment.
    #

    if Option == str(2):
        os.system('CLS')
        Belief_base.tell(~P >> Q)
        Belief_base.tell(Q >> P)
        Belief_base.tell(P >> (R & S))
        print('Belief Base populated with example from exercise 9.1')
        print(Belief_base)
        print()
    #

    if Option == str(3):
        print('Provide a formula to check entailment')
        user_input = input()
        if check_input(user_input):
            Proposition = eval(user_input.upper())
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
        else:
            print('Bad input, please refer to the README')

    #

    if Option == str(4):
        print('Which proposition should the belief base be expanded with? (Levi identity)')
        user_input = input()
        if check_input(user_input):
            Proposition = eval(user_input.upper())
            Belief_base.expansion(Proposition)
            print(Belief_base)
            print()
        else:
            print('Bad input, please refer to the README')
    #

    if Option == str(5):
        print('Which proposition should be contracted from the Belief Base?')
        user_input = input()
        if check_input(user_input):
            Proposition = eval(user_input.upper())
            Belief_base.partial_meet_contraction(Proposition)
            print(Belief_base)
            print()
        else:
            print('Bad input, please refer to the README')
    #

    if Option == str(6):
        Belief_base = BB()
    #

    if Option == str(7):
        server = False

