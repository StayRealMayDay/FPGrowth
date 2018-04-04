# -*-coding:utf-8-*-
from FPGrowth.FPTree import FPTree

def main():
    a = {1: 12, 2: 20, 3: 1}
    b = FPTree()
    b.createHeaderList(a)
    print(a)

    k = [1, 2, 3, 4]
    s = k[::-1]

    print(type(s))
main()