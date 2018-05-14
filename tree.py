#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

class Tree:
    """ Graph tree class """

    def __init__(self, vertex):
        self.vertex = vertex
        self.innerEdge = None
        self.outerEdge = None

    def generateDocuments(self, invariants):
        pass

    def trace(self, n_spaces = 0):
        self.vertex.trace(n_spaces)
        print(' ' * n_spaces, 'inner:')
        if self.innerEdge:
            self.innerEdge.trace(n_spaces + 4)
        else:
            print(' ' * (n_spaces + 4), 'None')

        print(' ' * n_spaces, 'outer:')
        if self.outerEdge:
            self.outerEdge.trace(n_spaces)
        else:
            print(' ' * n_spaces, 'None')

    def equal_trees(first, second):
        if first == None and second == None:
            return True
        elif first == None:
            return False
        elif second == None:
            return False
        else:
            return first.vertex.vType == second.vertex.vType and \
                   first.vertex.number == second.vertex.number and \
                   Tree.equal_trees(first.innerEdge, second.innerEdge) and \
                   Tree.equal_trees(first.outerEdge, second.outerEdge)
