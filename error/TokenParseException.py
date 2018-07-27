# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException


class TokenParseException(VerifyException):
    def __init__(self, msg):
        VerifyException.__init__(self, "Unable to parse token: " + msg)