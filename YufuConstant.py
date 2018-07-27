# -*- coding: utf-8 -*-

global _global_dict
_global_dict = {}
_global_dict['RUNTIME_URL'] = "https://idp.yufuid.com"
_global_dict['CONSUME_URL'] = _global_dict['RUNTIME_URL'] + "/sso/v1/consume"
_global_dict['AUTH_URL'] = _global_dict['RUNTIME_URL'] + "/sso/v1/authorize"
_global_dict['KEY_SERVICE_URL'] =_global_dict['RUNTIME_URL'] + "/api/v1/public/keys"

_global_dict['DEFAULT_AUDIENCE'] = "cidp"
_global_dict['DEFAULT_SUB'] = "test"
_global_dict['DEFAULT_VALID_TIME_IN_MS'] = 300000   #5min
_global_dict['DEFAULT_KEY_ID'] = "defaultKeyId"

_global_dict['IDP_ROLE'] = "IDP"
_global_dict['SP_ROLE'] = "SP"




def get_value(key,defValue=None):
    """ 获得全局变量，不存在则返回默认值 """
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

