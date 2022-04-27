from lugly import *


def main():
    P,Q,R = pvars('P', 'Q','R')
    formula1 = ((P | Q) & ~P) >> Q
    while(True):
        s = input()
        eval(s)


if __name__ == '__main__':
    main()
