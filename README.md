# ctrace4android
android端性能数据获取工具，支持python3和windows

流畅度
scroll_trace:自动化滑动屏幕，屏幕打印每次滑动低于60fps的次数，csv表格记录每次滑动绘制的ms。

流量总数
traffic_trace:屏幕打印流量总数，csv记录当前界面名称和流量总数

内存占用 && CPU
内存计算pss的值，和pss/heapsize的占比，CPU获取内存的同时会同步打印

耗电
读取电量消耗强度值，做粗略计算

内存泄漏 && 耗时
内存泄漏请使用leakcancy、耗时可以通过log日志打印，最精准，详细分析请使用traceview看函数调用时间