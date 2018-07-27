# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from jose import jwt
from jose import JWTError
import YufuConstant
from error.YufuInitException import YufuInitException
from error.GenerateException import GenerateException
import traceback
import time


class RSATokenGenerator:
    def __init__(self, *args):
        self.__privateKeyPath = args[0]
        self.__issuer = args[1]
        self.__tenant = args[2]
        self.__keySupplier = args[3]
        self.__cipher = None
        if args[4] is None:
            self.__password = None
        else:
            self.__password = args[4]
        try:
            if self.__privateKeyPath is None:
                raise YufuInitException("key filename cannot be blank")
            try:
                with open(str(self.__privateKeyPath), 'r') as keyFile:
                    key = keyFile.read()
                    self.__privateKey = RSA.importKey(key)
            except Exception:
                traceback.print_exc()
                if self.__password is None:
                    raise YufuInitException("password is required")
                with open(str(self.__privateKeyPath), 'r') as keyFile:
                    key = keyFile.read()
                    self.__privateKey = RSA.importKey(key, passphrase=self.__password)
            # finally:
            #     if self.__keySupplier.getOneKey() is not None:
            #         try:
            #             self.__cipher = Cipher_pkcs1_v1_5.new(self.__keySupplier.getOneKey())
            #         except Exception:
            #             traceback.print_exc()
        except IOError, e:
            raise YufuInitException(
                "Can not find private key file in given path or Private key file can not be read" + e.message)

    def generate(self, payload):

        header = {'alg': 'RS256', 'kid': self.__issuer, 'typ': "JWT"}
        audience = payload.get("aud") is not None and str(payload.get("aud")) or YufuConstant._global_dict['DEFAULT_AUDIENCE']
        sub = payload.get('sub') is not None and str(payload.get("sub")) or YufuConstant._global_dict['DEFAULT_SUB']
        now = time.time()

        claims = {'aud': audience, 'exp': now + YufuConstant._global_dict['DEFAULT_VALID_TIME_IN_MS'], 'iat': now - 1,
                  'iss': self.__issuer, 'sub': sub, 'nbf': now - 1}

        if self.__tenant is not None:
            claims['tnt'] = self.__tenant
        for rns in payload:
            try:
                if claims[rns] is None:
                    claims[rns] = payload[rns]
            except KeyError:
                claims[rns] = payload[rns]
        try:
            signedJWT = jwt.encode(claims, self.__privateKey, algorithm='RS256', headers=header)
        except JWTError:
            raise GenerateException
        return signedJWT
