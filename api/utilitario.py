#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import re;
import unicodedata
from datetime import timedelta

class Utilitario(object):
    def Data(data, formato, incrementoHH=0):
        if data == None:
            data = datetime.datetime.now();
        if incrementoHH > 0:
            data = data + timedelta(hours=incrementoHH);
        if formato == 'YYYYMDH':
            return data.strftime("%Y%m%d%H")
        if formato == 'YYYYMMDDHH':
            return data.strftime("%Y%m%d%H")
        if formato == 'YYYY_MM_DD':
            return str(data.year) + '_' + '{0:02d}'.format(data.month ) + '_' + '{0:02d}'.format(data.day);
        if formato == 'YYYY_MM_DD_HH':
            return str(data.year) + '_' + '{0:02d}'.format(data.month) + '_' + '{0:02d}'.format(data.day) + '_' + '{0:02d}'.format(data.hour);
        if formato == 'YYYYMMDDHHMM':
            return str(data.year) + '' + '{0:02d}'.format(data.month) + '' + '{0:02d}'.format(
                data.day) + '' + '{0:02d}'.format(data.hour) + '{0:02d}'.format(data.minute);
        if formato == 'YYYYMM':
            return str(data.year) + '{0:02d}'.format(data.month);
        if formato == 'YYYYMMDD':
            return str(data.year) + '{0:02d}'.format(data.month ) + '{0:02d}'.format(data.day);
        print formato;
    Data = staticmethod(Data)

    def RetornaNumero(texto):
        #print type(texto);
        #print 'Sera procurado numeros em: ' + texto;
        regex = r"[0-9]+"
        return re.findall(regex, texto);

    RetornaNumero = staticmethod(RetornaNumero);

    def RemoveAcentos(input_str):
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    RemoveAcentos = staticmethod(RemoveAcentos)

    def RemoveNoAlfabeto(texto):
        p2 = re.compile('\W+');
        return p2.sub('', texto);
    RemoveNoAlfabeto = staticmethod(RemoveNoAlfabeto)

    def KeyFile(str):
        key = 0;
        i = 0;
        for charitem in str:
            i = i + 1;
            key = key + (ord(charitem) * i);
        return key;
    KeyFile = staticmethod(KeyFile)