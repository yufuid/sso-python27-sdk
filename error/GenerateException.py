# -*- coding: utf-8 -*-

class GenerateException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
