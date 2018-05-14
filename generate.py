#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from tree import *
from html_parsing import *
from xml_parsing import *
from util import *

from functools import reduce
from random import random

STR = 'aabbcc'

def generate_html_from_tree(tree):
    if not(tree):
        return ''
    tag = HTML_TAGS_FROM_TYPE_NAMES[tree.vertex.vType]
    return '<' + tag + '>' + \
           STR + '\n' + generate_html_from_tree(tree.innerEdge) + \
           '</' + tag + '>' + '\n' + \
           generate_html_from_tree(tree.outerEdge)


def generate_xml_from_tree(tree):
    if not(tree):
        return ''
    tag = XML_TAGS_FROM_TYPE_NAMES[tree.vertex.vType]
    return '<text:' + tag + '>' + \
           STR + generate_xml_from_tree(tree.innerEdge) + \
           '</text:' + tag + '>' + \
           generate_xml_from_tree(tree.outerEdge)

def get_random_tree(predicates, difference):
    def check_tree():
        subset_ok = True
        for predicate in predicates:
            subset_ok = subset_ok and predicate(tree)

        diff_done = False
        for predicate in difference:
            diff_done = diff_done or predicate(tree)
        # subset_ok = reduce(lambda x, y: x(tree) and y, predicates, True)
        # diff_done = reduce(lambda x, y: x(tree) or y, difference, False)
        if diff_done:
            return 0
        elif subset_ok:
            return 1
        else:
            return 2

    def gen_adjacent_vertice(cur_tree, inList=False):
        if cur_tree.vertex.vType in [LIST_TYPE, LIST_ITEM_TYPE]:
            if random() < 0.8:
                # print('here1')
                inner_types = [PARAGRAPH_TYPE, LIST_TYPE]
                if cur_tree.vertex.vType == LIST_TYPE:
                    inner_types.append(LIST_ITEM_TYPE)
                cur_tree.innerEdge = Tree(Vertex(get_random_list_elem(inner_types)))
                # print('curt_tree.1', cur_tree.inner.vertex.vType)
                check = check_tree()
                if check == 0:
                    gen_adjacent_vertice(cur_tree, inList)
                    return
                elif check == 1:
                    return

        # outer
        outer_types = [PARAGRAPH_TYPE, LIST_TYPE]
        if inList:
            outer_types.append(LIST_ITEM_TYPE)
        if random() < 0.6:
            # print('here2')
            cur_tree.outerEdge = Tree(Vertex(get_random_list_elem(outer_types)))
            # print('curt_tree.2', cur_tree.inner.vertex.vType)
            check = check_tree()
            if check == 0:
                gen_adjacent_vertice(cur_tree, inList)
            elif check == 1:
                return

        if cur_tree.innerEdge:
            gen_adjacent_vertice(cur_tree.innerEdge, cur_tree.vertex.vType == LIST_TYPE)
        if cur_tree.outerEdge:
            gen_adjacent_vertice(cur_tree.outerEdge, inList)

        check = check_tree()
        if check != 1:
            gen_adjacent_vertice(cur_tree, inList)

    tree = Tree(Vertex())
    tree.vertex.vType = get_random_list_elem([PARAGRAPH_TYPE, LIST_TYPE])
    check = check_tree()
    if check == 0:
        return get_random_tree(predicates, difference)
    elif check == 1:
        return tree

    gen_adjacent_vertice(tree)
    return tree
