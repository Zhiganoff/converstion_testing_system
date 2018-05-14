#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

from vertex import *
from tree import *
from util import *

import xml.etree.ElementTree as etree

PREFIX = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'

PARAGRAPH_TAG = PREFIX + 'p'
LIST_TAG = PREFIX + 'list'
LIST_ITEM_TAG = PREFIX + 'list-item'

XML_TYPE_NAMES = {
    PARAGRAPH_TAG : PARAGRAPH_TYPE,
    LIST_TAG      : LIST_TYPE,
    LIST_ITEM_TAG : LIST_ITEM_TYPE
}

XML_TAGS_FROM_TYPE_NAMES = {
    PARAGRAPH_TYPE : 'p',
    LIST_TYPE : 'list',
    LIST_ITEM_TYPE : 'list-item'
}

CONTINUE_NUMBERING = PREFIX + 'continue-numbering'
LIST_HEADER_TAG = PREFIX + 'list-header'

TAGS = set({PARAGRAPH_TAG, LIST_TAG, LIST_ITEM_TAG})

tree = etree.parse('/home/zhigan/Workspace/libre/5/example.odt_FILES/content.xml')
root = tree.getroot()
# print(len(root))

body = tree.find('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}body')
text = body[0]
# print('body: ', body, len(text))


def get_tree_from_xml_text(text, listElemNumber=0):
    if len(text) == 1 and text[0].tag == LIST_HEADER_TAG:
        return get_tree_from_xml_text(text[0])
    # print('NEW_CALL')
    tree = None
    first_idx = 0

    # print('child tags:')
    # for child in text:
    #     print(child.tag, child.tag in TAGS)

    for index, child in enumerate(text):
        if child.tag in TAGS:
            # print('DEBUG: ', 'first tag', child.tag)
            root_vertex = Vertex(XML_TYPE_NAMES[child.tag])
            if child.tag == LIST_ITEM_TAG:
                listElemNumber += 1
                root_vertex.number = listElemNumber
            tree = Tree(root_vertex)

            tree.innerEdge = get_tree_from_xml_text(child)

            first_idx = index
            break

    cur_tree = tree

    for index in range(first_idx + 1, len(text)):
        tag = text[index].tag
        # print('cur_tag', tag)
        if tag in TAGS:
            # print('add outer tag', tag)
            vertex = Vertex(XML_TYPE_NAMES[tag])
            if tag == LIST_ITEM_TAG:
                listElemNumber += 1
                vertex.number = listElemNumber

            cur_tree.outerEdge = Tree(vertex)
            cur_tree = cur_tree.outerEdge

            if text[index].tag == LIST_TAG and CONTINUE_NUMBERING in text[index].attrib:
                cur_tree.innerEdge = get_tree_from_xml_text(text[index], listElemNumber + int(CONTINUE_NUMBERING in text[index].attrib))
            else:
                cur_tree.innerEdge = get_tree_from_xml_text(text[index])


    # for index in range(cur_idx, len(text)):
    #     for child in text[index]:
    #         print(child)
    # print('GO UP')
    return tree

# for child1 in text:
#     print(child1.tag, len(child1), child1.attrib, child1.text)
#     for child2 in child1:
#         print('   ', child2.tag, len(child2), child2.attrib, child2.text)
#         for child3 in child2:
#             print('       ', child3.tag, len(child3), child3.attrib, child3.text)

# print('________________________________')
# print('get_tree_from_xml_text')

xml_tree = get_tree_from_xml_text(text)
# print('__________________', 'Trace:')
# xml_tree.trace()
