# -*- coding: utf-8 -*-
from VerifyException import VerifyException

class CannotRetrieveKeyException(VerifyException):
    def __init__(self):
        VerifyException.__init__(self, "Can not retrieve key for token")
