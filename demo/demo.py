#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : handsomeFu (fuhandsome0219@gmail.com)
# @Time    : 2018/10/23 20:30
# @File    : demo.py
from functools import wraps


def xxx(func):
    print(3)

    @wraps(func)
    def wrapper(b):
        print(2)
        return func(b)

    return wrapper


@xxx    # ===>  a =  xxx(a)
def a(b):
    print(b)


a(123)
