#!/usr/bin/env python3
#encoding:utf-8  
import numpy as np 
import matplotlib.pyplot as plt
import math


#position keeping点 或path following点
lon_set = [109.07462746,109.080167,109.0844,109.090533,109.0957667]
lat_set = [18.2445389,18.243766,18.243766,18.241,18.243233]
plt.plot(lon_set, lat_set,  color='r',markerfacecolor='blue',marker='o')  
for a, b in zip(lon_set, lat_set):  
    plt.text(a, b, (a,b),ha='center', va='bottom', fontsize=10)  

#waveglider实时位置
file=open("/home/wp/waveglider_new/position_real.json",'r')
next(file)
lon=[]
lat=[]
with file as file_obj:
    lines=file_obj.readlines()
for line in lines:
    line=line.rstrip()
    line=line.split(',')
    lat_data=line[-1].replace("]","")
    lon_data=line[1]
    lat.append(float(lat_data))
    lon.append(float(lon_data))

plt.plot(lon,lat)
#设置坐标轴名称
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.show()
plt.xlim(109.074,109.10)
plt.ylim(18.241,18.245)