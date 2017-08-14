import re
from _functools import reduce

from tools.Helper import UsefulHelper
import numpy

'''
解析gfxinfo文件，返回一个绘制时长的list
'''
def parseGFX(result=''):
    if result.strip().lower() == '' or result.strip().lower() == None:
        return -1;
    if 'mi' in UsefulHelper().getPropValue('manufacturer').lower():
        result = result.split('Stats since')[1].split('View hierarchy:')[0];
        data = result[result.index('Execute'):result.rfind('Stats since')].strip();
        data_lines = data.split('\n\n')[1:-1];
    else:
        result = result.split('Execute')[-1].split('View hierarchy:')[0]
        data = result;
        data_lines = data.split('\n')[1:-2];
    count_time = [];
    for datas in data_lines:
        l = datas.split('\t')
        sum = float(l[1])+float(l[2])+float(l[3])+float(l[4]);
        sum = round(sum,2);
        count_time.append(sum);
        if count_time == []:
            return -2;
    #对数据进行解析，返回dict = {'orginal':[xxx],'fps':[xxx],'outcount':5}
    dict = {}
    dict['original'] = count_time;
    dict['fps'] = list(map(lambda x:round(1000/x,2),count_time));
    dict['outcount'] = list(filter(lambda x:x>16.66,count_time)).__len__();
    dict['variance'] = numpy.var(dict['fps']);
    return dict;

def parsePIDCpuTime(result=''):
    _result = re.findall(u'(\d+)', result)
    _result = reduce(lambda x, y: x + y, [int(_result[11]), int(_result[12]), int(_result[13]), int(_result[14])]);
    return _result

def parseTotalCpuTime(result=''):
    _result = result.split('\n')[0]
    _result = re.findall(u'(\d+)', _result)
    _result = reduce(lambda x, y: int(x) + int(y), _result)
    return _result

def parsePSS(result=''):
    try:
        resp = result.split('TOTAL')[2].split()[1];
    except:
        return -1;
    return resp;

if __name__ == '__main__':
    with open('C:\\Users\\Administrator\\Desktop\\gfxinfo.txt','r+') as f:
        result = f.read();
    print(parseGFX(result));