import re
from _functools import reduce

import Config
from tools import log
from tools.Helper import UsefulHelper
import numpy

'''
解析gfxinfo文件，通过dict返回,每次执行命令返回一个dict对象
dict['jank_count']  #绘制时间大于16.666ms那么+1
dict['fps']     #根据128帧的绘制时间计算帧数
dict['varance']  #128帧的时间计算稳定性
'''
def parseGFX(result=''):
    if result == '' or 'No process found' in result:
        print('no data find!is your current pkg is'+Config.packageName);
        exit(-1)
    if result.strip().lower() == '' or result.strip().lower() == None:
        return -1;
    if '6' in UsefulHelper().getPropValue('ro.build.version.release').lower():
        result = result.split('Stats since')[1].split('View hierarchy:')[0];
        data = result[result.index('Execute'):result.rfind('Stats since')].strip();
        data_lines = data.split('\n\n')[1:-1];
    else:
        result = result.split('Execute')[-1].split('View hierarchy:')[0]
        data = result;
        data_lines = data.split('\n')[1:-2];
    log.debug('parse gfx ok');
    frame_times = [];
    dict = {};
    jank_count = 0;
    frame_count = data_lines.__len__();
    frame_timeout = 0;
    #数据提取
    for datas in data_lines:
        l = datas.split('\t')
        frame_time = round(float(l[1])+float(l[2])+float(l[3])+float(l[4]),2);
        frame_times.append(frame_time);
        if frame_time > 16.67:
            jank_count += 1;
            log.debug("frame_time:"+str(frame_time))
            if frame_time % 16.67 == 0:
                frame_timeout += frame_time / 16.67 -1;
            else:
                frame_timeout += int(frame_time / 16.67);
                log.debug("frame_timeout:" + str(frame_timeout))
    try:
        _fps = frame_count * 60 / (frame_count + frame_timeout);
    except:
        print('parse error!no frame data!do you keep move?');
        exit(-1)
    #数据计算
    dict['jank_count'] = jank_count;
    dict['variance'] = round(numpy.var(frame_times),2);
    dict['fps'] = round(_fps,2);
    log.debug('jank:'+str(jank_count)+'   varance:'+str(dict['variance']));
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