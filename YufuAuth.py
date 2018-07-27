# -*- coding: utf-8 -*-
from auth.RSATokenGenerator import RSATokenGenerator
from error.YufuInitException import YufuInitException
from error.VerifyException import VerifyException
from error.GenerateException import GenerateException
from auth.RSATokenVerifier import RSATokenVerifier
from auth.key.OicKeySupplier import OicKeySupplier
import traceback
import YufuConstant


class YufuAuth(object):
    def __init__(self, issuer, role, privateKeyPath, publickKeyPath, tenant, password):
        """初始化Auth类"""
        try:
            self.__keySupplier = OicKeySupplier(publickKeyPath)
            if(role == YufuConstant._global_dict['IDP_ROLE']):
                self.__tokenGenerator = RSATokenGenerator(privateKeyPath, issuer, tenant, self.__keySupplier, password)
            elif role == YufuConstant._global_dict['SP_ROLE']:
                self.__tokenVerifier = RSATokenVerifier(self.__keySupplier)
            else:
                self.__tokenVerifier = RSATokenVerifier(self.__keySupplier)
                self.__tokenGenerator = RSATokenGenerator(privateKeyPath, issuer, tenant, self.__keySupplier, password)
            self.__tenant = tenant

        except Exception, e:
            traceback.print_exc()
            raise YufuInitException(e.message)

    def verify(self, token):
        try:
            return self.__tokenVerifier.verify(token)
        except Exception, e:
            traceback.print_exc()
            raise VerifyException(e.message)

    def generateToken(self, Claims):
        try:
            return self.__tokenGenerator.generate(Claims)
        except Exception, e:
            traceback.print_exc()
            raise GenerateException(e.message)

    def generateIDPRedirectUrl(self, Claims):
        try:
            loggingParams = self.__tenant is not None and "&tnt=" + self.__tenant or ""
            return YufuConstant.get_value('CONSUME_URL') + "?idp_token=" + self.__tokenGenerator.generate(
                Claims) + loggingParams
        except Exception, e:
            traceback.print_exc()
            raise GenerateException(e.message)

    def generateSPRedirectUrl(self, Claims):
        try:
            loggingParams = self.__tenant is not None and "&tnt=" + self.__tenant or ""
            return YufuConstant.get_value('AUTH_URL') + "?sp_token=" + self.__tokenGenerator.generate(
                Claims) + loggingParams
        except Exception, e:
            traceback.print_exc()
            raise GenerateException(e.message)

    class Builder(object):

        def __init__(self):
            self.__issuer = None
            self.__privateKeyPath = None
            self.__password = None
            self.__tenant = None
            self.__publicKeyPath = None
            self.__role = None

        def privateKeyPath(self, path):
            self.__privateKeyPath = path
            return self

        def publicKeyPath(self, path):
            self.__publicKeyPath = path
            return self

        def issuer(self, issuer):
            self.__issuer = issuer
            return self

        def password(self, password):
            self.__password = password
            return self

        def tenant(self, tnt):
            self.__tenant = tnt
            return self

        def role(self, role):
            self.__role = role
            return self

        def build(self):
            try:
                return YufuAuth(self.__issuer, self.__role, self.__privateKeyPath, self.__publicKeyPath, self.__tenant, self.__password)
            except Exception as e:
                traceback.print_exc()
                raise YufuInitException(e.message)
