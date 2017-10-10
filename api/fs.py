#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
from threading import Thread
import requests, json;
from multiprocessing.pool import ThreadPool
import request;
from request import *;

class SDBDfs(SDBDRequest):
    def __init__(self, tokenId):
        SDBDRequest.__init__(self, tokenId);

    def Read(self, repositorio,  path, driver, bus=None, parameters=None):
        envelope = {"operation": "read", "repositorio": repositorio, 'path' : path, "driver" : driver}
        if bus != None:
            envelope['bus'] = bus;
        return self.SendServers(self.servers, envelope=envelope);

    def List(self, repositorio, path, driver, bus=None, parameters=None):
        envelope = {"operation": "list", "repositorio": repositorio, 'path': path, "driver": driver}
        if bus != None:
            envelope['bus'] = bus;
        return self.SendServers(self.servers, envelope=envelope);

    def Write(self,repositorio, path, data, driver, bus=None, parameters=None):
        try:
            envelope = {"operation": "write","repositorio": repositorio, "path": path,
                        "version": 0, "data": data, "driver" : driver}
            if bus != None:
                envelope['bus'] = bus;
            return self.SendServers(self.servers, envelope=envelope);
        except Exception as e:
            print "Erro dentro TestInsert: " + str(e);

    def Find(self, repositorio, name, key, driver, bus=None, parameters=None):
        try:
            envelope = {"operation": "find", "repositorio": repositorio,
                        "version": 0, "name": name, "key" : key, "driver": driver}
            if bus != None:
                envelope['bus'] = bus;
            return self.SendServers(self.servers, envelope=envelope);
        except Exception as e:
            print "Erro dentro TestInsert: " + str(e);

# Exemplo....
#retorno = sdbd.Find("clima", "*_am", "_am", "fs", "home");
#print retorno;

#retorno = sdbd.Read("clima", "20170302/apui_am", "fs", bus="home");
#print retorno;

#retorno = sdbd.Write("clima", "20170302/teste", "Deu certo.", "fs", bus="home");
#print retorno;