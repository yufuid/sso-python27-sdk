# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException

class InvalidFormatException(VerifyException):
    def __init__(self, msg):
        VerifyException.__init__(self, "Unexpected token format: " + msg)
