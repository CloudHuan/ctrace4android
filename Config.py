packageName='com.arashivision.insta360air'   #可以自己写入包名，也可以保持应用在前台运行 initPackageName自动填入!

scrollPoint = (800,300,200,300) #可以自定义滚动坐标，传入list[startX,startY,endX,endY]，为空则表示读取机型分辨率后计算

resultPath = 'output'  #测试报告存放的地方

sleepTime = 3       #单位秒，影响内存/cpu/耗电量值获取间隔

largeHeap = True    #计算pss占用分配的比例，androidmanifest如果打开了largetheapsize那么这个要置为true

maxBattery = 3000    #手机最大电量，会根据这个值计算出当前界面持续使用能用多久

scroll_time = 10    #自动屏幕滑动最大次数

degbugMode = False   #为true时会打印调试信息