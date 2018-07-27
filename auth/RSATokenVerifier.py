# -*- coding: utf-8 -*-
import YufuConstant
from error.InvalidTokenException import InvalidTokenException
from error.CannotRetrieveKeyException import CannotRetrieveKeyException
from error.MissingKeyIdException import MissingKeyIdException
from jose import jwt
from auth.token.JWT import JWT


def convert(token):
    payload = jwt.get_unverified_claims(token)
    claims = JWT(iss=payload.get('iss'), aud=payload.get('aud'), sub=payload.get('sub'), jwtId=payload.get('jwtId'),
                 exp=payload.get('exp'), issueAt=payload.get('issueAt'), nbf=payload.get('nbf'))
    return claims


class RSATokenVerifier:
    def __init__(self, keySupplier):
        self.__keySupplier = keySupplier

    def verify(self, token):
        if token is None:
            raise InvalidTokenException("Token could not be empty")

        keyId = str(jwt.get_unverified_header(token).get('kid'))
        if keyId is None:
            raise MissingKeyIdException

        try:
            key = self.__keySupplier.keyMap[keyId]
        except Exception:
            key = self.__keySupplier.keyMap[YufuConstant._global_dict['DEFAULT_KEY_ID']]

        if key is None:
            raise CannotRetrieveKeyException

        try:
            claims = convert(token)
            jwt.decode(token, key, ['RS256'], {'leeway': 300}, audience=claims.getAudience(),
                       issuer=claims.getIssueAt(),
                       subject=claims.getSubject())
        except Exception, e:
            raise InvalidTokenException(e)
        return claims
