# Belief Revision
## Introduction
Belief Revision for the second assignment in Introduction to Artificial Intelligence course at DTU 02180 May 2022

With this project it is possible to create a belief base, query it for entailment, and to revise it.

There are two possible ways to create a belief base. 
The first one is to populate a belief base with pre-defined clauses.
The other way is to define each clause manually through expansion.

Revision is then done through further expansion, or contraction.

## How to run the program
To run the program simply run `menu.py` by typing `py menu.py` in a terminal. Several AGM postulates have also been made,
these can be run by running `agm_postulates.py` by typing `py agm_postulates` in a terminal.

When running the menu file, then a menu with 6 options will be shown. In order to choose an option, type the number in front of the desired option into the terminal.

Each option is described in more detail under [menu options](#menu-options). For option 2-4, after choosing the option, you have to enter a propositional logic formula.

The syntax for a propositional logic sentence can be seen under [Formula Syntax](#formula-syntax).

## Menu Options
1. 'See belief base': this option will simply print the current belief base into the console
2. 'Query knowledge base for entailment': Enter a formula that will be queried with the existing belief base
3. 'Expand Belief Base': Enter a formula that should be added to the belief base through expansion
4. 'Contract Belief Base': Enter a formula that should be contracted from the belief base
5. 'Reset Belief Base': Delete all clauses in the belief base.
6. 'Exit': terminate the program

## Formula Syntax
Syntax for propositional logic sentences: 
 - Available variables are all letters from A-Z. 
 - Available operators are (the syntax is written in parentheses): not(~), and(&), or(|), implies(>>), if-and-only-if(%)
 Example: A&B>>E|D
 
