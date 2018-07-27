# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException

class InvalidTokenException(VerifyException):
    def __init__(self, msg):
        VerifyException.__init__(self, msg)
