#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Send UDP broadcast packets
import sys, time, inspect, os, json, select
from socket import *
from api import *;

class Broadcast:
    def __init__(self):
        self.target = "";
        self.port = 6400
        self.timeout = 5;
        self.servers_address = [];
        print 'Port: ', self.port, "Target:", self.target;

    def Discovery(self, currentdir):
        # primeiro vamos olhar o arquivo de configura;áo
        print currentdir + '/data/config.json'
        if os.path.exists(currentdir + '/data/config.json'):
            print open(currentdir + '/data/config.json', 'r').read();
            js = json.loads(open(currentdir + '/data/config.json', 'r').read());
            for server in js['servers']:
                self.servers_address.append(server['ip']);
            return self.servers_address;

        #nao tem, entao vamos fazer o dscover na rede
        s = socket(AF_INET, SOCK_DGRAM)
        s.bind(('', 0))
        s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        s.settimeout(7);
        envelope = {"operation": "who"}
        data = json.dumps(envelope) + '  \n'
        s.sendto(data, ('<broadcast>', self.port))

        try:
            while True:
                data, addr = s.recvfrom(1024)
                self.servers_address.append(addr[0]);
        except Exception as e:
            print("DISCOVERY, OK", e);
        return self.servers_address;