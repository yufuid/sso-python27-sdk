# -*- coding: utf-8 -*-
import collections


class JWT:
    def __init__(self, **args):
        self.__issuer = args['iss']
        self.__audience = args['aud']
        self.__subject = args['sub']
        self.__jwtId = args['jwtId']
        self.__expiration = args['exp']
        self.__issueAt = args['issueAt']
        self.__notBefore = args['nbf']
        self.__claims = collections.OrderedDict()

    def getAudience(self):
        return self.__audience

    def getSubject(self):
        return self.__subject

    def getExpiration(self):
        return self.__expiration

    def getIssueAt(self):
        return self.__issueAt

    def getNotBefore(self):
        return self.__notBefore

    def build(self):
        pass
