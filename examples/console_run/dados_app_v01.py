#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit environment
# https://cortix.org
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/cortix/blob/master/COPYRIGHT.txt
#
# Licensed under the University of Massachusetts Lowell LICENSE:
# https://github.com/dpploy/cortix/blob/master/LICENSE.txt
'''
Cortix: a program for system-level modules coupling, execution, and analysis.

Cortix is a library and it is used by means of a driver. This file is a simple example
of a driver. Many Cortix objects can be ran simultaneously; a single object
may be sufficient since many simulation/tasks can be ran via one object.

As Cortix evolves additional complexity may be added to this driver and/or other
driver examples can be created.
'''
#*********************************************************************************
import os, sys, multiprocessing, time, threading, datetime
from cortix import Cortix

sys.path.append("../..")
from rs_232 import RS_232
from mcc_118 import MCC_118
#*********************************************************************************

def start_rs232():
    rsworker=threading.Thread(target=RS_232, args=('ir-7040','/tmp/dados'),name='rs232')
    rsworker.daemon=True
    rsworker.start()
    return

def start_mcc118():
    mccworker=threading.Thread(target=MCC_118, args=('analog-input','/tmp/dados'),name='mcc118')
    mccworker.daemon=True
    mccworker.start()
    return
def read_display(filelist):
    global string
    form='.4f'
    oldstring=''
    time.sleep(1)
    while True:
        vallist=[]
        for file in filelist:
            if file=='/tmp/dados/ir_temp.csv':
                with open(file) as f:
                    line = f.read()
                    if len(line)<5:
                        continue
                    spline=line.split(',')
                    try:
                        ch1='Ch1: {}'.format(format(float(spline[2]),form))
                        ch2='Ch2: {}'.format(format(float(spline[4]),form))
                        vallist.append(ch1)
                        vallist.append(ch2)
                    except ValueError or IndexError:
                        continue
            if file=='/tmp/dados/mcc_118_data.csv':
                with open(file) as f:
                    line=f.read()
                    try:
                        v1='Ch1 (Volts): {}'.format(format(float(line),form))
                        vallist.append(v1)
                    except ValueError:
                        continue
        vallist.append(' select a command: ')
        string='\r'+', '.join(vallist)
        #string = '\rCh1: {}, ch2: {}, Ch1(Volt): {}'.format(ch1,ch2,v1)
        if string==oldstring:
            time.sleep(0.1)
            continue
        oldstring=string
        length = len(string)
        print(string,end='')
        sys.stdout.flush()

        time.sleep(.1)


def main():
    global string
    string=''
    length=42
    pwd = os.path.dirname(__file__)
    full_path_config_file = os.path.join(pwd, '../input/cortix-config-dados.xml')
    print('main')
    timestamp=str(datetime.datetime.now())
    timeID=timestamp[:4]+timestamp[5:7]+timestamp[8:10]+timestamp[11:13]+timestamp[14:16]+timestamp[17:19]
    oldline=''
    print('')
    print('''1) RS_232
2) MCC_118
3) Start Display
Press anything else to save Datapoint
''')
    filelist=[]
    while True:
        length = len(string)
        word=input('\r{}'.format(' '*length))
        namelist=[f.getName() for f in threading.enumerate()]
        timestamp=datetime.datetime.now()
        if word=='1' and 'rs232' not in namelist:
            start_rs232()
            if '/tmp/dados/ir_temp.csv' not in filelist:
                filelist.append('/tmp/dados/ir_temp.csv')
        elif word=='2' and 'mcc118' not in namelist:
            try:
                check2==True
                continue
            except:
                pass
            check2=True
            start_mcc118()
            if '/tmp/dados/mcc_118_data.csv' not in filelist:
                filelist.append('/tmp/dados/mcc_118_data.csv')
        elif word=='3' and 'display' not in namelist:
            worker=threading.Thread(target=read_display,args=(filelist,),daemon=True,name='display')
            worker.start()
        else:
            with open('/tmp/dados/experiment_{}.csv'.format(timeID),'a') as f:
                f.write('{}, {}, {}\n'.format(timestamp, string, word))
        time.sleep(.3)

if __name__ == "__main__":
    main()
