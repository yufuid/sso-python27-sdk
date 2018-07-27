# -*- coding: utf-8 -*-
from error.VerifyException import VerifyException

class MissingKeyIdException(VerifyException):
    def __init__(self):
        VerifyException.__init__(self, "Missed key id")
