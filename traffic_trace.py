import Config
from tools.Helper import ShellHelpr, UsefulHelper
import re


def getTraffic():
    s = ShellHelpr();
    userID = s.exec('adb shell dumpsys package %s |findstr %s'%(Config.packageName,'userId'));
    userID = re.findall(u'userId=(\d+)', userID)[0];
    result = s.exec( "adb shell cat /proc/net/xt_qtaguid/stats |findstr %s"%userID);
    result = result.split('\n');
    count_rx = 0  # 接收流量
    count_tx = 0  # 发送流量
    for items in result:
        itemss = items.split()
        if itemss[3] == userID and itemss[1] != 'lo':    #过滤第4列uid为选择的uid，避免统计其他的
            count_rx = count_rx + int(itemss[5]);
            count_tx = count_tx + int(itemss[7]);
    #print("rx:"+str(count_rx)+"\ntx"+str(count_tx)+"\nsum:"+str(count_rx+count_tx));
    dict = {};
    dict['rx_kb'] = str(round(count_rx/1000,2));
    dict['tx_kb'] = str(round(count_tx/1000,2));
    dict['sum'] = str(round((count_rx+count_tx)/1000,2));
    return dict;

if __name__ == '__main__':
    u = UsefulHelper();
    name = 'traffic_'+u.getSaveCSVName();
    u.simpleWriteCSV(name=name, list=[Config.packageName]);
    u.simpleWriteCSV(name=name, list=['current','cost','rx','tx']);
    while True:
        command = input("点击任意键键打印当前流量，输入0退出\n")
        if command == '0':
            exit(1)
        dict = getTraffic();
        _list = []
        u.simpleWriteCSV(name=name,list=[u.getCurrentActivity(),dict.get('sum'),dict.get('rx_kb'),dict.get('tx_kb')]);
        print('总流量:' + dict['sum']+'kb');