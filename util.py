#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from random import randint

PARAGRAPH_TYPE = 'paragraph'
LIST_TYPE = 'list'
LIST_ITEM_TYPE = 'list_item'

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def powerset(elements):
    length = len(elements)
    powerset = []
    subset = []
    def gen(k):
        if k == length:
            powerset.append(subset.copy())
        else:
            gen(k + 1)
            subset.append(elements[k])
            gen(k + 1)
            subset.pop()
    gen(0)
    return powerset


def get_random_list_elem(lst):
    return lst[randint(0, len(lst) - 1)]


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail
