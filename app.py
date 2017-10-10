#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Wellington Pinto de Oliveira

import os, sys, time, inspect, traceback, json;
from socket import *
from random import randint

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)
sys.path.insert(0,currentdir + '/api/')

from subprocess import Popen, PIPE, STDOUT
from task import *;                          #API do barramento

CONFIG = json.loads(open(currentdir + '/data/config.json', 'r').read());

esbjs = SDBDtask(CONFIG['tokenId'], CONFIG['servers'][0]['port']);
esbjs.servers = None;
esbjs.servers = [ CONFIG['servers'][0]["ip"] ];
print esbjs.servers


erros = 0;
execucoes = 0;
while True:
    try:
        if (os.path.isdir(currentdir + '/atualizando')):
            print 'Em atualização.'
            exit(0);

        if erros > 15 or execucoes > 50 :
            print 'Total de erros excedidos ou execuções excedidas.'
            exit(0);

        work = esbjs.HasworkV2(bus=CONFIG['servers'][0]['name'], parameters=CONFIG['task']['parameters']);
        if work == None or work['instance'] == '':
            print 'Sem trbalhos agendados.';
            exit(0);

        tarefa = esbjs.NextV2(work['name'], 'sequencia');
        if tarefa != None :
            if os.path.isfile(currentdir + '/' + tarefa['item']['rotina']):
                p = Popen(['python2.7', currentdir + '/' + tarefa['item']['rotina']], stdout=PIPE, stdin=PIPE,stderr=STDOUT)
                grep_stdout = p.communicate(input=json.dumps(tarefa) + "\n");
                print(grep_stdout);
            else:
                print 'Em atualização'
                p = Popen(['python2.7', currentdir + '/update.py'])
                grep_stdout = p.communicate(input=json.dumps(tarefa) + "\n");
                exit(0);

            time.sleep(randint(1, 4))
        else:
            print 'Nenhuma atividade, dormir por 10 segundos.'
            time.sleep(10);
        execucoes += 1;
    except Exception as e:
        traceback.print_exc();
        erros += 1;
        time.sleep(5)
