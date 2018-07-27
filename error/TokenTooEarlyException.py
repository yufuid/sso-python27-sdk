# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException

class TokenTooEarlyException(VerifyException):
    def __init__(self):
        VerifyException.__init__(self, "Token is used too early")
