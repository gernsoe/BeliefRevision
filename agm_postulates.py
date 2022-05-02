from belief_base import *
import os

for letter in ascii_uppercase[:22]:
    exec("{} = V('{}')".format(letter, letter))

def success_test_contraction():
    bb = BB()
    bb.tell(~P >> Q)
    bb.tell(Q >> P)
    bb.tell(P >> (R & S))
    phi = (P&R&S)
    bb.partial_meet_contraction(phi)
    assert(not bb.entails(bb.clauses, phi))
    print("Success postulate test passed for contraction")

def inclusion_test_contraction():
    bb = BB()
    bb.tell(~P >> Q)
    bb.tell(Q >> P)
    bb.tell(P >> (R & S))
    phi = (P&R&S)
    original_bb = bb.__copy__()
    bb.partial_meet_contraction(phi)
    assert(bb.is_subset(original_bb.clauses, bb.clauses))
    print("Inclusion postulate test passed for contraction")

def vacuity_test_contraction():
    bb = BB()
    bb.tell(~P>>Q)
    bb.tell(Q>>P)
    bb.tell(P>>(R&S))
    phi = Not(P&R&S)
    original_bb = bb.__copy__()
    assert(not bb.entails(bb.clauses, phi))
    bb.partial_meet_contraction(phi)
    assert(bb.clauses == original_bb.clauses)
    print("Vacuity postulate test passed for contraction")

def extensioniality_test_contraction():
    bb = BB()
    bb.tell(~P>>Q)
    bb.tell(Q>>P)
    bb.tell(P>>(R&S))
    phi_distributive_left = P|(Q&R)
    phi_distributive_right = (P|Q)&(P|R)
    original_bb = bb.__copy__()
    bb.partial_meet_contraction(phi_distributive_left)
    original_bb.partial_meet_contraction(phi_distributive_right)
    assert(original_bb.clauses == bb.clauses)
    print("Extensioniality postulate test passed for contraction")

def contraction_postulates():
    success_test_contraction()
    inclusion_test_contraction()
    vacuity_test_contraction()
    extensioniality_test_contraction()

def success_test_expansion():
    bb = BB()
    bb.tell(A&B&~C)
    phi = C
    assert(not bb.entails(bb.clauses, phi))
    bb.expansion(phi)
    assert(bb.entails(bb.clauses, phi))
    print("Success postulate test passed for expansion")

def inclusion_test_expansion():
    bb = BB()
    bb.tell(A&B&~C)
    original_bb = bb.__copy__()
    phi = C
    bb.expansion(phi)
    original_bb.tell(phi)
    assert(bb.is_subset(original_bb.clauses, bb.clauses))
    print("Inclusion postulate test passed for expansion")

def vacuity_test_expansion():
    bb = BB()
    bb.tell(A&B)
    original_bb = bb.__copy__()
    phi = C
    assert(not bb.entails(bb.clauses, Not(phi)))
    bb.expansion(phi)
    original_bb.tell(phi)
    assert(bb.clauses == original_bb.clauses)
    print("Vacuity postulate test passed for expansion")


def consistensy_test_expansion():
    bb = BB()
    bb.tell(A&B)
    phi = C

    #assert that phi is not a contradiction:
    assert(not bb.entails([phi]))

    #assert that knowledge base is consistent after expansion with phi
    bb.expansion(phi)

    assert(not bb.entails(bb.clauses))
    print("Consistensy postulate test passed for expansion")

def extensioniality_test_expansion():
    bb = BB()
    bb.tell(~P>>Q)
    bb.tell(Q>>P)
    bb.tell(P>>(R&S))
    original_bb = bb.__copy__()

    phi_distributive_left = P|(Q&R)
    phi_distributive_right = (P|Q)&(P|R)

    bb.expansion(phi_distributive_left)
    original_bb.expansion(phi_distributive_right)

    bb_cnf = []
    original_bb_cnf = []
    for prop in bb.clauses:
        bb_cnf.append(convert_to_cnf(prop))

    for prop in original_bb.clauses:
        original_bb_cnf.append(convert_to_cnf(prop))

    assert(original_bb_cnf == bb_cnf)
    print("Extensioniality postulate test passed for expansion")

def expansion_postulates():
    success_test_expansion()
    inclusion_test_expansion()
    vacuity_test_expansion()
    consistensy_test_expansion()
    extensioniality_test_expansion()

contraction_postulates()
expansion_postulates()
