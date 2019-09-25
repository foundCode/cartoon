# -*- coding: utf-8 -*-
import numpy as np


class O:
    def __init__(self):
        self.value = 0


class A:
    a = O()

    def __init__(self):
        pass


class B(A):
    a = O()
    b = 2

    def __init__(self):
        super().__init__()
        self.a.value = self.b


class C(A):
    a = O()
    c = 3

    def __init__(self):
        super().__init__()
        self.a.value = self.c


def func():
    print('func')


def main():
    b = B()
    print(b.a.value)
    c = C()
    print(b.a.value, c.a.value)

    x = []
    y = [1, 2]
    z = [3, 4]
    x.append(y)
    x.append(z)
    print(x)

    p = np.zeros([2], np.uint8)
    q = np.zeros([1], np.uint8)
    print(p, q)
    print(p == q)


if __name__ == '__main__':
    main()