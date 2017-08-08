import threading
import time

import Config
from tools import FilePaser
from tools.Helper import ShellHelpr, UsefulHelper


class DataTread(threading.Thread):

    def getPIDCpuTime(self):
        pid = UsefulHelper().getCurrentPID();
        return FilePaser.parsePIDCpuTime(ShellHelpr().exec('adb shell cat /proc/%s/stat'%pid));

    def getTotalCpuTime(self):
        return FilePaser.parsePIDCpuTime(ShellHelpr().exec('adb shell cat /proc/stat'));

    def getPSS(self):
        return FilePaser.parsePSS(ShellHelpr().exec('adb shell dumpsys meminfo %s'%Config.packageName));

    def __init__(self):
        threading.Thread.__init__(self);
        self.flag = True;
        self.name = 'men_cpu_'+UsefulHelper().getSaveCSVName();
        UsefulHelper().simpleWriteCSV(name=self.name, list=[Config.packageName]);
        UsefulHelper().simpleWriteCSV(name=self.name, list=['内存', '内存占用', 'CPU']);

    def run(self):
        while self.flag:
            s_pid = self.getPIDCpuTime();
            s_total = self.getTotalCpuTime();
            time.sleep(Config.sleepTime);
            e_pid = self.getPIDCpuTime();
            e_total = self.getTotalCpuTime();
            cpuUsage = str(round((e_pid - s_pid)/(e_total - s_total)*100,2))+'%';
            pss = self.getPSS();
            self.dataAfter(cpuUsage,pss);

    def stop(self):
        self.flag = False;

    def dataAfter(self,cpu,mem):
        if Config.largeHeap:
            heap = UsefulHelper().getPropValue('heapsize').strip('m');
        else :
            heap = UsefulHelper().getPropValue('heapgrowthlimit');
        memUsage = str(round(int(mem) / 10 / int(heap),2))+'%';
        print(mem + '||'+memUsage+'||'+cpu);
        UsefulHelper().simpleWriteCSV(name=self.name,list=[mem,memUsage,cpu]);

if __name__ == '__main__':
    t = DataTread();
    input('回车键开始测试，再次回车键停止测试');
    t.start();
    input();
    t.stop();
