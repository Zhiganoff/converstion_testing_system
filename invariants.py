#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from util import *

PARAGRAPH_TYPE = 'paragraph'
LIST_TYPE = 'list'
LIST_ITEM_TYPE = 'list_item'

def paragraph_interrupts_list(tree):
    # pass
    # if tree:
    #     if tree.vertex.type == 'list':
    #         return ParagraphInterruptsList(tree.innerEdge) or ParagraphInterruptsList(tree.outerEdge)
    #     elif tree.type == 'listElem':
    #         ParagraphInterruptsList.prevIsListElem = True
    #         return ParagraphInterruptsList(tree)
    #     elif tree.type ==
    #
    #
    # if (tree.type = 'list')
    if not(tree):
        return False
    elif tree.vertex.vType == 'list_item' and tree.outerEdge and \
       tree.outerEdge.vertex.vType == 'paragraph' and tree.outerEdge.outerEdge and \
       tree.outerEdge.outerEdge.vertex.vType == 'list':
       return True
    else:
       return paragraph_interrupts_list(tree.innerEdge) or paragraph_interrupts_list(tree.outerEdge)

def nested_list_depth_2(tree, depth=0):
    if depth == 2:
        return True
    elif not(tree):
        return False
    elif tree.vertex.vType == 'list':
        return nested_list_depth_2(tree.innerEdge, depth + 1) or nested_list_depth_2(tree.outerEdge, depth + 1)
    else:
        return nested_list_depth_2(tree.innerEdge, depth) or nested_list_depth_2(tree.outerEdge, depth)
