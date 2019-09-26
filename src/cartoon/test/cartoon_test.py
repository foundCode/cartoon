# -*- coding: utf-8 -*-
import numpy as np

import tools.utils as utils


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

    import cv2
    # # 'http://wx2.sinaimg.cn/mw690/ac38503ely1fesz8m0ov6j20qo140dix.jpg'
    # # 'https://img001.yayxcc.com/images/cover/201806/1530069619_IvNKW-FN1aH4yUA.jpg'
    image_url = 'https://img001.yayxcc.com/images/comic/10/19457/1520719203ZPP2vxH5Xj_k5EaN.jpg'
    image = utils.get_image_by_url(image_url)
    print(np.shape(image))
    if image is None:
        print('image is none')
    else:
        cv2.imshow('image', image)
        cv2.waitKey()


if __name__ == '__main__':
    main()
