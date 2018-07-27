# -*- coding: utf-8 -*-

class VerifyException(Exception):
    def __init__(self, arg):
        Exception.__init__(self, arg)
