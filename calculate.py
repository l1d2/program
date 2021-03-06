
# coding: utf-8

# In[2]:


import numpy as np
import csv
import time as tm
import string as str
import matplotlib.pyplot as plt
import pandas as pd
import re
import xlwt
import os
#读入包含功率的中转表格，可视化并计算

#修改matlab middle表格
#data=pd.read_csv(r"D:\redianliangong\12.csv")  #csv文件读入，不能有中文路径；excel转csv的文件需要重新选择编码格式（UTF8）
     #with open(_file_,'D:\redianliangong\middle.xlsx') as f:
     #data=pd.read_excel(f,sheetname=1)
          
#excel文件sheetname读入
io=r'D:\redianliangong\middle.xlsx'
data0=pd.read_excel(io,sheet_name=None,header=None)#data包括列名
sheetname=list(data0.keys())
#list_sheetname=sheetname.tolist()
sheet=np.array(sheetname)
#print(sheet)
#data.head()
#print(sheet)


#公共def函数创建
#持续时间处理
def time_continue1(a):
    if a<5:
        a=5*a
    elif a==5:
        a=30
    else:
        a=45
    return(a)    
#print(b)
def time_continue2(a):
    if a<7:
        a=5*a
    elif 7<=a<10:
        a=30+10*(a-6)
    elif a==10:
        a=90
    else:
        a=(2+a-11)*60
    return(a)
#频率处理
#用电设备
def data_f2(a):
    if a<6:
        a=6-a
    elif a==6:
        a=0.5
    else:
        a=1/(a-4+(a-7))
    return(a)
#用热行为
#洗碗
def data_f1_1(a):
    if a==1:
        a=0
    elif 2<=a<=3:
        a=1/(5-a)
    else:
        a=a-3
    return(a)
#洗脸
def data_f1_2(a):
    if a==1:
        a=0.5
    else:
        a=a-1
    return(a)
#洗澡
def data_f1_3(a):
    if a==1:
        a=1/7
    elif 2<=a<=3:
        a=1/(5-a)
    else:
        a=a-3
    return(a)



#初始时刻处理
def time_start(a):
    if'24:00'==a:
        t1=0
    else:
        start_time=tm.strptime(a,"%H:%M")
    #print(start_time)
        hour=tm.strftime("%H",start_time)
        minute=tm.strftime("%M",start_time)
        hour=int(hour)
        minute=int(minute)
    #print(hour,minute)#整数类型
        t1=60*hour+minute
    return(t1)



def show_curve1(Nh):  # 画图用的
    plt.subplot(2, 1, 1)
    plt.title('Power of heat')
    plt.xlabel("Time(Hour)")
    plt.ylabel("Power(w)")
    plt.xticks(range(0, 1441, 60), list(range(0, 25)))
    plt.plot(Nh, color='r')
    plt.show()       
    
def show_curve2(Ne):  # 画图用的
    plt.subplot(2, 1, 1)
    plt.title('Power of electricity')
    plt.xlabel("Time(Hour)")
    plt.ylabel("Power(w)")
    plt.xticks(range(0, 1441, 60), list(range(0, 25)))
    plt.plot(Ne, color='r')
    plt.show()       
    

#指定sheetname的数据导入
c=1
print(sheet.shape[0])
g=sheet.shape[0]+1
while(c<g):
    data=pd.read_excel(io,sheet_name=np.str(c),header=None)
    #print('测试1')
    data=np.array(data)
    #print(data)

#按列提取数据
    data1_pattern=(data[1:,0])#用能设备
#print(data1_pattern)
    data2_f=data[1:,1]
    list_data2_f=data2_f.tolist()
#print(data2_f)
    data3_starttime=data[1:,2]#开始时刻
#print(data3_starttime)
    data4_continue=data[1:,3]#持续时间
    list_data4_continue=data4_continue.tolist()
#print(data4_continue)
    data5_P=data[1:,4]
    list_data5_P=data5_P.tolist()
#print(data5_P)
    data6_season_heat=data[0:2,19]
    #print(data6_season_heat)
    data7_week_heat=data[0:2,18]
    #print(data7_week_heat)
    data8_week_ele=data[0:2,20]
    #print( data8_week_ele)

#优化excel
    data33_starttime=data[1:,2]
#类型名称处理
    n=0
    #print(data.shape[0])
    while(n<data.shape[0]-1):
        if pd.isna(data1_pattern[n]):
            data1_pattern[n]=' '
            n=n+1
            #print(n)
            #print(data1_pattern[n])
        elif '空调'in data1_pattern[n]or'其他'in data1_pattern[n]:
            n=n+1
        elif '请选择'in data1_pattern[n]:
            a=data1_pattern[n].index(' ')
        #print(x)
            data1_pattern[n]=data1_pattern[n][a+1:]
            b=data1_pattern[n].index(' ')
            data1_pattern[n]=data1_pattern[n][:b+3]
            data1_pattern[n]=data1_pattern[n].replace(data1_pattern[n][b:b+3],'(电)')
       # print(data1_pattern[n])
            n=n+1
       # print(n)
        else:
            a=data1_pattern[n].index('的')
        #print(x)
            data1_pattern[n]=data1_pattern[n][a+1:]
            b=data1_pattern[n].index('频率')
            data1_pattern[n]=data1_pattern[n][:b+3]
            data1_pattern[n]=data1_pattern[n].replace(data1_pattern[n][b:b+3],'(热)')
        #print(data1_pattern[n])
            n=n+1
    #print(n)
#print(data1_pattern)
    list_data1_pattern=data1_pattern.tolist()
#初始时间处理
    i=0
    #print()
    #print(data.shape[0])
    while(i<data.shape[0]-1):
    #print('第几行：',i+1)
    #print('共几行：',data.shape[0])
        if pd.isna(data3_starttime[i]):
            data3_starttime[i]=' '
            i=i+1
        else:
            x=data3_starttime[i].index('(')
    #print(x)
            if  '-'in data3_starttime[i]:
                y=data3_starttime[i].index('-')
            else:
                y=data3_starttime[i].index(')')
            
            start_time=data3_starttime[i][x+1:y]#取括号内的时间
    #print(start_time)
            data33_starttime[i]=start_time
            i=i+1
    #print(i)
    list_data3_starttime=data33_starttime.tolist()


    
#频率、持续时间处理
    i=0
    while(i<data.shape[0]-1):
        if ' 'in data3_starttime[i]:
            i=i+1
        else:
            if'(电)'in data1_pattern[i]:
                f=data_f2(data2_f[i])
                t=time_continue2(data4_continue[i])
                i=i+1
        #print(i)
            elif'(热)'in data1_pattern[i]:
                if '洗澡'in data1_pattern[i]: 
                    f=data_f1_3(data2_f[i])
                elif '洗脸'in data1_pattern[i]:
                    f=data_f1_2(data2_f[i])
                else:
                    f=data_f1_1(data2_f[i])
                t=time_continue1(data4_continue[i])
                i=i+1
           # print(i)
            else:
                m=i
                while(' 'in data1_pattern[m]):
                    m=m-1
                if'(电)'in data1_pattern[m]:
                    f=data_f2(data2_f[i])
                    t=time_continue2(data4_continue[i])
                    i=i+1
                #print(i)
                elif'(热)'in data1_pattern[m]:
                    if '洗澡'in data1_pattern[m]: 
                        f=data_f1_3(data2_f[i])
                    elif '洗脸'in data1_pattern[m]:
                        f=data_f1_2(data2_f[i])
                    else:
                        f=data_f1_1(data2_f[i])
                    t=time_continue1(data4_continue[i])
                i=i+1
            #print(i)
            data2_f[i-1]=f
            data4_continue[i-1]=t
            
            
            
    #计算过程
    '''print(data1_pattern)
    print(data2_f)
    print(data3_starttime)
    print(data4_continue)
    print(data5_P)
    '''
    Nh=np.zeros(1440)#初始化
    Ne=np.zeros(1440)
    q=0
    while(q<100):#100可以换成最长数据长度data1_pattern.shape[0]
        if' 'in data3_starttime[q]:
            break
        else:
            #n1=time_start(data3_starttime[q])
            #while(i<data.shape[0]):
        #f=data2_f[i]
            #print(data3_starttime[q])
            n1=time_start(data3_starttime[q])
        #P1=np.array([data5_P[i]*f])
            if'(电)'in data1_pattern[q]:
                #f=data_f2(data2_f[i])
                f=data2_f[q]
                P1=data5_P[q]*f
                t=data4_continue[q]
                n2=n1+t
                N2=Ne[n1:n2]
                Ne[n1:n2]=N2+P1
                #print('计算后的数组为:\n',Nh)
                #q=q+1
            #print(i)
            elif'(热)'in data1_pattern[q]:
                f=data2_f[q]##可以与上文合并
                P1=data5_P[q]*f
                t=data4_continue[q]
                n2=n1+t
                N2=Nh[n1:n2]
                Nh[n1:n2]=N2+P1
            #print(i)
            else:
                a=data1_pattern[i-1]
                if'(电)'in a:
                    f=data2_f[q]
                    P1=data5_P[q]*f
                    t=data4_continue[q]
                    n2=n1+t
                    N2=Ne[n1:n2]
                    Ne[n1:n2]=N2+P1 
                elif'(热)'in a:
                    f=data2_f[q]##可以与上文合并
                    P1=data5_P[q]*f
                    t=data4_continue[q]
                    n2=n1+t
                    N2=Nh[n1:n2]
                    Nh[n1:n2]=N2+P1
                else:
                    m=q
                    while(' 'in data1_pattern[m]):
                        m=m-1
                    if'(电)'in data1_pattern[m]:
                        f=data2_f[q]
                        P1=data5_P[q]*f
                        t=data4_continue[q]
                        n2=n1+t
                        N2=Ne[n1:n2]
                        Ne[n1:n2]=N2+P1 
                    elif'(热)'in data1_pattern[m]:
                        f=data2_f[q]##可以与上文合并
                        P1=data5_P[q]*f
                        t=data4_continue[q]
                        n2=n1+t
                        N2=Nh[n1:n2]
                        Nh[n1:n2]=N2+P1    
        q=q+1 
        #print(q)
    

                
#画图
    if c==15:
        show_curve1(Nh)
        #show_curve2(Ne)
        
    c=c+1


print('循环结束')

