#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from vertex import *
from tree import *
from util import *

from bs4 import BeautifulSoup

PARAGRAPH_TAG = 'p'
LIST_TAG = 'ol'
LIST_ITEM_TAG = 'li'

HTML_TYPE_NAMES = {
    PARAGRAPH_TAG : PARAGRAPH_TYPE,
    LIST_TAG      : LIST_TYPE,
    LIST_ITEM_TAG : LIST_ITEM_TYPE
}

HTML_TAGS_FROM_TYPE_NAMES = {
    PARAGRAPH_TYPE : PARAGRAPH_TAG,
    LIST_TYPE : LIST_TAG,
    LIST_ITEM_TYPE : LIST_ITEM_TAG
}

TAGS = set({PARAGRAPH_TAG, LIST_TAG, LIST_ITEM_TAG})

def get_tree_from_html_text(text, listElemNumber=0):
    # print('NEW_CALL')
    tree = None
    first_idx = 0
    cur_tag = None
    # print('child tags:')
    # for child in text:
    #     print(child.tag, child.tag in TAGS)

    for index, child in enumerate(text):
        if child.name in TAGS:
            # print('DEBUG: ', 'first tag', child.name)
            root_vertex = Vertex(HTML_TYPE_NAMES[child.name])
            if child.name == LIST_ITEM_TAG:
                listElemNumber += 1
                root_vertex.number = listElemNumber
            tree = Tree(root_vertex)
            tree.innerEdge = get_tree_from_html_text(child.children)

            first_idx = index
            cur_tag = child
            # print(child)
            break

    cur_tree = tree

    if cur_tag:
        for child in cur_tag.next_siblings:
            tag = child.name
            if tag in TAGS:
                vertex = Vertex(HTML_TYPE_NAMES[tag])
                if tag == LIST_ITEM_TAG:
                    listElemNumber += 1
                    vertex.number = listElemNumber

                cur_tree.outerEdge = Tree(vertex)
                cur_tree = cur_tree.outerEdge
                # print('tag', tag)
                # print('add inner edge')

                # if child.name == LIST_TAG and CONTINUE_NUMBERING in text[index].attrib:
                #     cur_tree.innerEdge = get_tree_from_xml_text(text[index], listElemNumber + int(CONTINUE_NUMBERING in text[index].attrib))
                # else:
                cur_tree.innerEdge = get_tree_from_html_text(child.children)


    # for index in range(cur_idx, len(text)):
    #     for child in text[index]:
    #         print(child)
    # print('GO UP')
    return tree


f = open('/home/zhigan/Workspace/libre/5/sample.html')
html_doc = f.read()
f.close()

# print(html_doc)
# exit(0)

soup = BeautifulSoup(html_doc, 'html5lib')

# print(soup.body)

# print(soup.body.tags)
#
# for child in soup.body:
#     if child.name:
#         print(child.name, len(child))
#     print('_____________')
    # print(dir(child))

# print(dir(soup))




html_tree = get_tree_from_html_text(soup.body)
# print('__________________', 'Trace:')
# html_tree.trace()
