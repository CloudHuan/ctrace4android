import threading
import time

import Config
from tools.Helper import ShellHelpr, UsefulHelper


class Battery_Thread(threading.Thread):

    def getBatteryCost(self):
        return str(int(ShellHelpr().exec('adb shell cat /sys/class/power_supply/battery/current_now'))/1000);

    def __init__(self):
        threading.Thread.__init__(self);
        self.flag = True;
        self.name = 'bat_' + UsefulHelper().getSaveCSVName();
        UsefulHelper().simpleWriteCSV(name=self.name, list=[Config.packageName]);
        UsefulHelper().simpleWriteCSV(name=self.name, list=['电量消耗mA','估算时间']);

    def run(self):
        while self.flag:
            b = self.getBatteryCost();
            leaveTime = str(round(Config.maxBattery/float(b),2));
            print(b + 'mA||'+ leaveTime);
            time.sleep(Config.sleepTime);
            self.after([b,leaveTime]);

    def stop(self):
        self.flag = False;

    def after(self,l):
        UsefulHelper().simpleWriteCSV(name=self.name,list=l);

if __name__ == '__main__':
    input('点击回车开始打印当前整机电量消耗(ms)');
    b = Battery_Thread();
    b.start();
    input();
    b.stop();