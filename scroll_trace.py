import subprocess,sys,threading

import Config
from Config import *;
from tools.FilePaser import parseGFX
from tools.Helper import UsefulHelper, ShellHelpr

class ScrollThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self);
        self.flag = True;
        self.screen = UsefulHelper().getScreenSize();
        self.name = 'fps_'+UsefulHelper().getSaveCSVName();
        UsefulHelper().simpleWriteCSV(name=self.name, list=[Config.packageName]);

    def run(self):
        while self.flag:
            _shell = 'adb shell input swipe %s'%self.way;
            ShellHelpr().exec(_shell);
            d_result = parseGFX(ShellHelpr().exec('adb shell dumpsys gfxinfo %s'%Config.packageName));
            self.dataAfter(d_result);

    def stop(self):
        print('stop!!!!!')
        self.flag = False;

    def scroll_position(self,position):
        if position == '1':
            self.way = '%d %d %d %d' % (self.screen[0]/2,self.screen[1]*3/4,self.screen[0]/2,self.screen[1]/4);
        if position == '2':
            self.way = '%d %d %d %d' % (self.screen[0]/2,self.screen[1]/4,self.screen[0]/2,self.screen[1]*3/4);
        if position == '3':
            if Config.scrollPoint == [] or len(Config.scrollPoint) < 4:
                print('路径未定义,请到config处定义');
                exit(-1)
            self.way = '%d %d %d %d' % Config.scrollPoint;

    #取到测试数据的处理函数
    def dataAfter(self,data_resp):
        print(data_resp['outcount']);
        UsefulHelper().simpleWriteCSV(name=self.name,list=data_resp['fps']);
        UsefulHelper().simpleWriteCSV(name=self.name, list=[data_resp['outcount'],]);

if __name__ == '__main__':
    s = ScrollThread();
    while True:
        command = input('输入:\n1-->上滑\n 2-->下滑\n 3-->自定义滑动\n0--> 停止测试\n');
        if command == '1':
            s.scroll_position('1');
            s.start();
        if command == '2':
            s.scroll_position('2');
            s.start();
        if command == '3':
            s.scroll_position('3');
            s.start();
        if command == '0':
            s.stop();
            exit(1);