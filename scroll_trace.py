import subprocess,sys,threading

import Config
from Config import *;
from tools.FilePaser import parseGFX
from tools.Helper import UsefulHelper, ShellHelpr
import numpy

'''
dict['jank_count']  #绘制时间大于16.666ms那么+1
dict['fps']     #根据128帧的绘制时间计算帧数
dict['variance']  #128帧的时间计算稳定性
'''
class ScrollThread(threading.Thread):

    all_fps = []

    def __init__(self):
        threading.Thread.__init__(self);
        self.flag = True;
        self.screen = UsefulHelper().getScreenSize();
        self.name = 'fps_'+UsefulHelper().getSaveCSVName();
        UsefulHelper().simpleWriteCSV(name=self.name, list=[Config.packageName,UsefulHelper().getPropValue('model')]);

    def run(self):
        if Config.scroll_time < 0:
            run_time = 999999999;
        else:
            run_time = Config.scroll_time;
        for i in range(run_time):
            _shell = 'adb shell input swipe %s'%self.way;
            ShellHelpr().exec(_shell);
            d_result = parseGFX(ShellHelpr().exec('adb shell dumpsys gfxinfo %s'%Config.packageName));
            self.dataAfter(d_result);
            if i == run_time - 1:
                self.last_run();

    def stop(self):
        print('stop!!!!!')
        self.flag = False;

    def scroll_position(self,position):
        if position == '1':
            self.way = '%d %d %d %d' % (self.screen[0]/2,self.screen[1]*3/5,self.screen[0]/2,self.screen[1]/5);
        if position == '2':
            self.way = '%d %d %d %d' % (self.screen[0]/2,self.screen[1]/4,self.screen[0]/2,self.screen[1]*3/4);
        if position == '3':
            if Config.scrollPoint == [] or len(Config.scrollPoint) < 4:
                print('路径未定义,请到config处定义');
                exit(-1)
            self.way = '%d %d %d %d' % Config.scrollPoint;

    #取到测试数据的处理函数
    def dataAfter(self,data_resp):

        fps = str(data_resp['fps']);
        variance = str(data_resp['variance']);
        jank = str(data_resp['jank_count']);
        UsefulHelper().simpleWriteCSV(name=self.name, list=[fps,jank,variance]);
        self.all_fps.append(data_resp['fps']);
        print("fps:"+fps+"|jank:"+jank+'|variance:'+variance);

    '''最后一次运行,作为总的统计'''
    def last_run(self):
        variance_fps = numpy.var(self.all_fps);
        argv = numpy.mean(self.all_fps);
        UsefulHelper().simpleWriteCSV(name=self.name, list=['fps平均值:',argv]);
        UsefulHelper().simpleWriteCSV(name=self.name, list=['fps方差',variance_fps]);
        print('-------------summary------------');
        print("fps avg:" + str(argv) + "|fps variance:" + str(variance_fps));

if __name__ == '__main__':
    s = ScrollThread();
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