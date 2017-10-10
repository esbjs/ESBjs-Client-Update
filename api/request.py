#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue, traceback, os;
from threading import Thread
import requests, json;
from multiprocessing.pool import ThreadPool
import uuid

from uuid import *;

class SDBDRequest:
    def __init__(self, tokenId, port=None):
        self.target = "";
        self.port = 5007
        if(port != None):
            self.port = port;
        self.timeout = 30;
        self.path = 'request'
        self.protocol = 'http'
        self.sessionId = str(uuid.uuid4());
        self.tokenId = tokenId;

    def SendServer(self, envelope):
        #print envelope;
        url = self.protocol + '://' + envelope['server'] + ':' + str(self.port) + '/' + self.path
        try:
            buffer_connection = requests.post(url, json=envelope, timeout=self.timeout);
            #print buffer_connection.text();
            buffer = buffer_connection.json();
            if buffer.get('version') and buffer['version'] == 2:
                if buffer['status']:
                    return envelope, buffer['data'];
                else:
                    return envelope, None;
            else:
                return envelope, buffer;
        except Exception as e:
            print e;
            return envelope, None;

    def SendServers(self,servers, envelope):
        try:
            envelope['sessionId'] = self.sessionId;
            envelope['trasactionId'] = str(uuid.uuid4());
            envelope['system'] = {
                'nome': os.uname()[1],
                'sistema': os.uname()[0]
            }

            envelope['tokenId'] = self.tokenId;
            que = Queue.Queue()
            threads_list = list();
            for server in servers:
                envelope['server'] = server;
                t = Thread(target=lambda q, arg1: q.put(self.SendServer(arg1)), args=(que, envelope))
                t.start()
                threads_list.append(t)
            # Join all the threads
            for t in threads_list:
                t.join()
            # Check thread's return value
            while not que.empty():
                envelope, result = que.get()
            return result;
        except Exception as e:
            traceback.print_exc();
            return None;

    def Select(self, table, key, driver, operand="=", orderby="", limit=0, bus="any", parameters=None):
        envelope = {"operation": "select", 'table' : table, 'key' : key, "driver" : driver}
        if limit > 0:
            envelope['limit'] = limit;

        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);

    def SelectV2(self, instance, table, key, limit=0, bus="any", parameters=None):
        envelope = {"operation": "select", "instancia" : instance ,'table': table, 'key': key, "driver": "mongo", "version" : 2}
        if limit > 0:
            envelope['limit'] = limit;
        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);

    def Remove(self, table, key, driver, bus="any", parameters=None):
        envelope = {"operation": "remove", 'table': table, 'key': key, "driver": driver}

        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);

    def Next(self, table, versao, driver, operand="=", orderby="", limit=1, bus="any", no_update=False, parameters=None):
        envelope = {"operation": "next", 'table': table, 'versao': versao, "driver" : driver, "no_update": no_update}
        envelope['limit'] = limit;

        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);

    def NextV2(self, name, sort, bus="any", parameters=None):
        envelope = {"operation": "next", 'name': name, 'version': 2,
                    "driver": "task", "sort" : sort}
        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);

    def GetV2(self, name, pos, bus="any", parameters=None):
        envelope = {"operation": "get", 'name': name, 'version': 2,
                    "driver": "task", "pos": pos}

        envelope['bus'] = bus;
        if parameters != None:
            envelope = dict(envelope.items() + parameters.items())

        return self.SendServers(self.servers, envelope=envelope);



    def TestInsert(self, table, key, driver, data, bus="any", parameters=None):
        try:
            envelope = {"operation": "testinsert", "table": table,
                        "version": 0, "key": key, "data": data, "driver" : driver}

            envelope['bus'] = bus;
            if parameters != None:
                envelope = dict(envelope.items() + parameters.items())

            return self.SendServers(self.servers, envelope=envelope);
        except Exception as e:
            print "Erro dentro TestInsert: " + str(e);

    def TestInsertV2(self,instance, table, key, data, bus="any", parameters=None):
        try:
            envelope = {"operation": "testinsert", "table": table,
                        "version": 2, "instancia" : instance, "key": key, "data": data, "driver": "mongo"}

            envelope['bus'] = bus;
            if parameters != None:
                envelope = dict(envelope.items() + parameters.items())

            return self.SendServers(self.servers, envelope=envelope);
        except Exception as e:
            print "Erro dentro TestInsert: " + str(e);

    def Drop(self, table, driver, bus="any", parameters=None):
        try:
            envelope = {"operation": "drop", "table": table,
                        "version": 0, "driver": driver}
            envelope['bus'] = bus;
            if parameters != None:
                envelope = dict(envelope.items() + parameters.items())

            return self.SendServers(self.servers, envelope=envelope);
        except Exception as e:
            print "Erro dentro TestInsert: " + str(e);

    def Ping(self, servers, testAll=False):
        for i in xrange(len(servers)):
            try:
                buffer = requests.get("http://" + servers[i]['ip'] + ":" + str(servers[i]['port']) + "/ping", timeout=5);
                if not testAll and buffer.status_code == 200:
                    print 'Servidor de tarefas achadoe em:', servers[i]['ip'];
                    return [ servers[i]['ip'] ];
            except Exception as e:
                print 'Ignorar:', servers[i]['ip']
        return None;

    #def MergeJson(self, default, buffer):


