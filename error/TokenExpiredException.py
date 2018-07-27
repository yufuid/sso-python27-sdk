# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException

class TokenExpiredException(VerifyException):
    def __init__(self):
        VerifyException.__init__(self, "Token is expired")
