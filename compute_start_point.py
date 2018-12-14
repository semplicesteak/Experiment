import numpy as np
import matplotlib.pyplot as plt
import math,csv,os

# 该方法通过之前求出的表，用输入的点与表中所有点进行欧式距离计算找到距离最短的点
def detect_distance(rssi_distance,rssi):
    # rssi=[float(-60.5),float(-62)]#第四组
    # rssi=[float(-58.5),float(-64)]#第五组
    # rssi = [float(-61), float(-62.5)]  # 第六组
    d_min=float(1000)
    for i in range(len(rssi_distance)):
        rssi_distance[i]=[float(rssi_distance[i][0]),float(rssi_distance[i][1]),float(rssi_distance[i][2]),float(rssi_distance[i][3])]
        d=math.sqrt((rssi_distance[i][0]-rssi[0])**2+(rssi_distance[i][1]-rssi[1])**2)
        if d<d_min:
            d_min=d
            distance=rssi_distance[i]
    print(distance)
    distance2=[distance[2],distance[3]]
    return distance2

# 当数据中出现天线1和天线2交替出现时记录下两个天线的读数，带入上面求出的表查找距离，当有三个连续点的d1再+-0.4之间波动时认定他们走在一条直线上
def detect_path(rssi_distance):
    with open(r'G:\PycharmPython\RFID_Human_Detection\第九次实验\第九次实验\recorddata_out1 先中间 后靠近2 最后靠近1.csv', 'r') as f:
        csv_content=csv.reader(f)
        headers = next(csv_content)
        i = 0
        all_row=[]
        distance_row=[]
        for row in csv_content:
            if i == 1 and row[7][:4] != "stop":
                all_row.append(row)
                if row[4]!=all_row[-2][4] :
                    if all_row[-2][5]!='\\Z' and all_row[-1][5]!='\\Z':
                        if row[4]=="1" and abs(int(row[5])-int(all_row[-2][5]))<50000:#判断两个强度之间间隔时间不能太大
                            distance_row.append([row[1],all_row[-2][1]])
                        elif row[4]=="2" and abs(int(row[5])-int(all_row[-2][5]))<50000:
                            distance_row.append([all_row[-2][1],row[1]])
            if row[7][:5] == "start":
                i = 1
                all_row.append(row)
                distance_row.append(['start','start'])
            if row[7][:4] == "stop":
                i = 0
                all_row.append(row)
                distance_row.append(['stop', 'stop'])
        distance=[]
        distance_group=[]

        j=0
        for q in range(len(distance_row)):
            if distance_row[q]==["start","start"]:
                continue
            elif distance_row[q]==["stop","stop"]:
                distance_group.append(distance)
                plt.figure(figsize=(15, 10))
                for p in range(2, len(distance)//2):  # 设置一个阈值，d1的波动范围在+-0.4之间
                    if abs(distance[p][0] - distance[p - 1][0]) <= 0.4:
                        if abs(distance[p][0] - distance[p - 2][0]) <= 0.4:
                            if abs(distance[p - 1][0] - distance[p - 2][0]) <= 0.4:

                                x=[distance[p-2][0],distance[p-1][0],distance[p][0]]
                                y=[abs(distance[p-2][1]),abs(distance[p-1][1]),abs(distance[p][1])]
                                plt.plot(x,y,'o-',label=j)
                                plt.xlabel("d1")
                                plt.ylabel("L")
                                plt.title('lalala')
                                j=j+1
                # plt.legend(loc='best')
                plt.grid(True)
                path = r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\picture_第九次实验_100点\{0}.png'.format(q)
                plt.savefig(path)
                plt.close()
                distance=[]
            else:
                distance.append(detect_distance(rssi_distance,[float(distance_row[q][0]),float(distance_row[q][1])]))
    return

if __name__ == '__main__':
    rssi_distance = []
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance_index_-37.52_0.9_100点.csv', 'r') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            if len(row) == 0:
                continue
            rssi_distance.append(row)
    detect_path(rssi_distance)