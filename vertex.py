#!/usr/local/bin/python3

# -*- coding: utf-8 -*-

class Vertex:
    """Graph vertice class"""

    cnt = 0
    vType = None
    number = None

    def __init__(self, vType=None, number=None):
        self.vType = vType
        self.number = number
        Vertex.cnt += 1

    def trace(self, n_spaces = 0):
        print(' ' * n_spaces, 'type = {}, number = {}'.format(self.vType, self.number))
