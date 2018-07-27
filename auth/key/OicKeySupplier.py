# -*- coding:utf-8 -*-
import threading
from time import sleep
import YufuConstant
import json
import urllib2
import collections
import traceback
from error.CannotRetrieveKeyException import CannotRetrieveKeyException

fetchKey_mutex = threading.Lock()

class Scheduler(threading.Thread):
    def __init__(self, supplier, interval):
        super(Scheduler, self).__init__()
        self.__supplier = supplier
        self.__interval = interval
        self.__MAX_RETRY_TIMES = 5
        self.__RETRY_INTERVAL_IN_SEC = 10

    def renewKeys(self, publicKeyPath):
        retryTime = 0
        interval = self.__RETRY_INTERVAL_IN_SEC
        while retryTime < self.__MAX_RETRY_TIMES:
            try:
                self.__supplier.fetchKeys(publicKeyPath)
                break
            except CannotRetrieveKeyException:
                interval <<= 1
                retryTime += 1
                sleep(interval)

    def run(self):
        var = 1
        while var == 1:
            try:
                sleep(self.__interval * 3600)
                self.renewKeys()
            except Exception:
                traceback.print_exc()


class OicKeySupplier(object):
    def __init__(self, publicKeyPath):
        try:
            self.__publicKeyPath = publicKeyPath
            self.keyMap = collections.OrderedDict()
            self.__RENEW_INTERVAL_IN_HOUR = 24
            self.sch = Scheduler(self, self.__RENEW_INTERVAL_IN_HOUR)
            self.sch.renewKeys(publicKeyPath)
            self.sch.start()

        except:
            traceback.print_exc()
            raise CannotRetrieveKeyException


    def fetchKeys(self, publicKeyPath):
        global fetchKey_mutex
        fetchKey_mutex.acquire()

        try:
            if publicKeyPath is not None:
                publicKey = open(publicKeyPath, "r").read()
                self.keyMap[YufuConstant._global_dict['DEFAULT_KEY_ID']] = publicKey
            else:
                data = urllib2.urlopen(YufuConstant._global_dict['KEY_SERVICE_URL']).read()
                value = json.loads(data)
                rootlist = value.keys()

                for self.fingerprint in rootlist:
                    pass
                publicKey = value[self.fingerprint]
                self.keyMap[self.fingerprint] = publicKey

        except Exception:
            traceback.print_exc()
            raise CannotRetrieveKeyException()
            pass
        finally:
            fetchKey_mutex.release()

    def getOneKey(self):
        try:
            if self.keyMap is None:
                self.fetchKeys()
            return self.keyMap.values()[self.keyMap.__len__() - 1]
        except Exception:
            traceback.print_exc()
            raise CannotRetrieveKeyException()

    def getKey(self, keyId):
        try:
            if keyId is None or keyId.trim().length() == 0:
                raise CannotRetrieveKeyException

            if self.keyMap is None:
                self.fetchKeys()

            return self.keyMap.keys()[self.keyMap.__len__() - 1]
        except Exception:
            traceback.print_exc()
            raise CannotRetrieveKeyException()
