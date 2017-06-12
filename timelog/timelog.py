## coding=utf8
import re
import os
import time
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



# logfile = open("E:/work/测试环境和数据/oms.xtp-test-1.log.20170607")
logfile = open('oms.xtp-test-1.log.20170607')
output = open('output.txt','w+')

pattern_new_order_time = re.compile("\[(.*?)\]\[.*?recv new order",re.S)
pattern_new_order_xtpid = re.compile("xtp_id:(.*?),",re.S)
pattern_market=re.compile("market:(.*?),",re.S)

pattern_rsp_timer = re.compile("\[(.*?)\]\[.*?recv order_rsp",re.S)
pattern_rsp_xtpid = re.compile("order_id:(.*?),",re.S)
all = dict()
spanlist = list()
spanlist2=list()
numlist = list()
for line in logfile:
    if re.match(pattern_new_order_time,line):
        single = dict()
        item=re.findall(pattern_new_order_time,line)
        # time=item[0]
        single["req_time"]=item[0]
        req_time=item[0].split('.')[1]
        item=re.findall(pattern_new_order_xtpid,line)
        xtp_id=item[0]
        single["req"]=req_time
        single["xtp_id"]=xtp_id
        item=re.findall(pattern_market,line)
        single["mkt"]=item[0]
        # print single
        # print xtp_id
        all[xtp_id]=single
#        count = count + 1
        continue

    if re.match(pattern_rsp_timer,line):
        item=re.findall(pattern_rsp_timer,line)
        timestamp=item[0]
        rsp_time=item[0].split('.')[1]
        item=re.findall(pattern_rsp_xtpid,line)
        xtp_id=item[0]
        getsingle = all[xtp_id]
        getsingle["rsp_time"] = timestamp
        getsingle["rsp"]=rsp_time
        getsingle["span"]=int(rsp_time) - int(getsingle["req"])
        # if getsingle["span"] < 0:
        #     getsingle["span"] = getsingle["span"] + 1000
        datetime_obj=datetime.strptime("2017-06-07 " + getsingle["req_time"],"%Y-%m-%d %H:%M:%S.%f")
        req_stamp=time.mktime(datetime_obj.timetuple())*1000.0+ datetime_obj.microsecond/1000.0
        datetime_objb=datetime.strptime("2017-06-07 " + getsingle["rsp_time"],"%Y-%m-%d %H:%M:%S.%f")
        rsp_stamp=time.mktime(datetime_objb.timetuple())*1000.0 + datetime_objb.microsecond/1000.0
        span =int(rsp_stamp - req_stamp)
        getsingle["span"]=span

#        print getsingle
#        logstr="xtp_id:" + xtp_id + ",req_time:" + getsingle["req"] + ",rsp_time:" + rsp_time + ",span:" + str(getsingle["span"])
        logstr = xtp_id + "," + getsingle["req_time"] + "," + getsingle["rsp_time"]  + "," + str( getsingle["span"])
        output.write(logstr + '\n')
        if getsingle["span"] > 2000:
            continue
        if getsingle["mkt"] == "1":
            spanlist.append(getsingle["span"])
        else:
            spanlist2.append(getsingle["span"])
#        numlist.append(count)
        
        continue


logfile.close()
output.close()
# for v in all.itervalues():
#     logout = "xtp_id:" + ["xtp_id"] + ",req_time:" + v["req"] + ",rsp_time:" + v["rsp"] + ",span:" + str(v["span"])
#     print logout
# for ele in all:
     # logout="xtp_id:" + ele["xtp_id"] + ",req_time:" + ele["req"] + ",rsp_time:" + ele["rsp"] + ",span:" + str(ele["span"])
     # print logout
    # output.write(logout)
    # output.write("xtp_id:" + ele["xtp_id"] + ",req_time:" + ele["req"] + ",rsp_time:" + ele["rsp"] + ",span:" + str(ele["span"]))

fig1 = plt.figure("SZ")
plt.plot( spanlist, 'bo')
ax=fig1.gca()#获取当前图表坐标刻度
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
plt.ylabel('time:ms')
# ticker.MultipleLocator(5)
# plt.axis([0, 6, 0, 20])
fig1.show()


fig2 = plt.figure("SH")
plt.plot( spanlist2, 'bo')
# ticker.MultipleLocator(5)
ax=plt.gca()#获取当前图表坐标刻度
ax.yaxis.set_major_locator(ticker.MultipleLocator(50))
plt.ylabel('time:ms')
# plt.axis([0, 6, 0, 20])
plt.show()












