import subprocess
import re
import csv
import os
import time
import sys

import Config


class ShellHelpr():

    def exec(self,_shell):
        result = subprocess.getoutput('adb devices');
        if result.split('\n').__len__() == 2:
            print('no connect phone');
            input()
            exit(-1)
        return subprocess.getoutput(_shell);

class ADBHelper():
    pass

class UsefulHelper():

    #return [1080.0, 2040.0]
    def getScreenSize(self):
        result = ShellHelpr().exec('adb shell wm size');
        tuplee = re.findall('(\d+)x(\d+)', result)[0];
        return [float(tuplee[0]),float(tuplee[1])];

    def simpleWriteCSV(self,path=Config.resultPath,name='test.csv',list=[]):
        realPath = os.path.join(sys.path[0],path);
        if not os.path.exists(realPath):
            os.mkdir(path)
        with open(os.path.join(realPath,name),'a+') as f:
            _writer = csv.writer(f,delimiter=',');
            _writer.writerow(list);

    def getCurrentActivity(self):
        cur = ShellHelpr().exec('adb shell dumpsys activity top|findstr ACTIVITY');
        return cur.split()[1];

    def getCurrentPackageName(self):
        cur = ShellHelpr().exec('adb shell dumpsys activity top|findstr ACTIVITY');
        return cur.split()[1].split('/')[0];

    def getCurrentPID(self):
        cur = ShellHelpr().exec('adb shell dumpsys activity top|findstr ACTIVITY');
        return cur.split()[3].split('=')[1];

    def getSaveCSVName(self):
        return time.strftime('%y%m%d%H%M', time.localtime())+'.csv';

    def getPropValue(self,key):
        result = ShellHelpr().exec('adb shell getprop | findstr %s'%key);
        return result.split(']')[1].split('[')[1]

if __name__ == '__main__':
    #print(UsefulHelper().getScreenSize());
    UsefulHelper().simpleWriteCSV("C:/Users/Administrator/Desktop",'justtest.csv',['1001.1','102.5']);
    print(UsefulHelper().getCurrentActivity());
    print(UsefulHelper().getPropValue('heapgrowthlimit'))