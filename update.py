#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, inspect, sys, json, traceback;
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,currentdir)
sys.path.insert(0,currentdir + '/api/')

from update import *;

CONFIG = json.loads(open(currentdir + '/data/config.json', 'r').read());


# ----------------------------------------------     FUNÇOES AQUI DENTRO ---------------------------------------------------

def AdicionarArquivosRaiz(dir):
    lista = os.listdir(dir);
    arquivos = [];
    for i in xrange(len(lista)):
        path = dir + '/' + lista[i];
        if (not os.path.isdir(path)):
            arquivos.append( '/' + lista[i]);
    return arquivos;


def listarRecursivo(dir):
    print dir;
    if not os.path.exists(dir):
        return [];

    lista = os.listdir(dir);
    arquivos = [];
    for i in xrange(len(lista)):
        path = dir + '/' + lista[i];
        if (os.path.isdir(path)):
            arquivos = arquivos + listarRecursivo(path);
        else:
            arquivos.append( path[len(currentdir):]);
    return arquivos;


def CriarDir(path):
    elementos = path.split('/');
    del elementos[-1];
    buffer_path = '';
    for item in elementos:
        buffer_path = buffer_path + '/' + item;
        if not os.path.exists(buffer_path):
            os.mkdir(buffer_path);


def KeyFile(str):
    key = 0;
    i = 0;
    for charitem in str:
        i = i + 1;
        key = key + (ord(charitem) * i);
    return key;


def KeyFilePath(path):
    return KeyFile(open(currentdir + path, 'r').read())

    # -------------------------------------------------------------------------------------------------------------------------



if (os.path.isdir(currentdir + '/atualizando')):
    print 'Em atualização.'
    exit(0);
else:
    try:
        open(currentdir + '/atualizando', 'a').close()

        esbjs = SDBDupdate(CONFIG['tokenId'], CONFIG['servers'][0]['port']);
        esbjs.servers = None;
        esbjs.servers = [CONFIG['servers'][0]["ip"]];
        #print esbjs.servers

        projetos = esbjs.Projects(CONFIG['projects'], bus="home");

        for j in xrange(len(projetos)):
            #print projetos[j];
            diretorios = projetos[j]['directories'];
            arquivos = [];       # temporário até criar arquivos_valor
            ignores = ['config.json', 'node_modules', '.idea', ".pyc"]

            #print diretorios;
            for dir in xrange(len(diretorios)):
                #print dir;
                arquivos += listarRecursivo(currentdir + "/" + diretorios[dir]);
            #print arquivos;
            for epos in xrange(len(arquivos) - 1, -1, -1):
                #print epos
                arquivo = arquivos[epos];
                for ignore in ignores:
                    posicao = arquivo.find(ignore);
                    if posicao >= 0:
                        arquivos.pop(epos);
            arquivos += AdicionarArquivosRaiz(currentdir);
            arquivos_valor = [];  #vai conter nome do arquivo e sua chave para consulta no servidor....
            for arquivo in arquivos:
                key = KeyFilePath(arquivo);
                arquivos_valor.append({'path' : arquivo, 'key' : key});
            #print arquivos;
            retorno = esbjs.List(arquivos_valor, bus=CONFIG['servers'][0]["name"], project=projetos[j]['name']); # o retorno é o que devo baixar.
            #print 'Mandei:', arquivos_valor;
            print 'Foi retornado:', retorno;


            for buffer_elemento in retorno:
                elemento = currentdir  + buffer_elemento;
                ignorar_arquivo = False;
                for ignore in ignores:

                    posicao = elemento.find(ignore);
                    if posicao >= 0:
                        ignorar_arquivo = True;

                if not ignorar_arquivo:
                    #print elemento
                    arquivo = esbjs.Read(buffer_elemento, project=projetos[j]['name'], bus=CONFIG['servers'][0]["name"]);
                    #print arquivo;
                    if arquivo != None and arquivo['data'] != None and arquivo['data'] != '':
                        print 'Path:', elemento
                        CriarDir(elemento);
                        arquivofs = open(elemento, 'w');
                        arquivofs.writelines(arquivo['data'].encode('utf-8').strip());
                        arquivofs.close();
    except Exception as ex:
        print ex;
        traceback.print_exc()
    #os.remove(currentdir + '/atualizando');

