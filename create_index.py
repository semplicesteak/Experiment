import csv,math,os
import numpy as np

#读取不同角度对应的信号强度值以及归一化
def read_rssi_angel():
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\925HzE_total_90.csv','r') as f:
        csvfile=csv.reader(f)
        angle=[]
        rssi=[]
        i=0
        for row in csvfile:
            if len(row)!=0:
                if i==0:
                    angle=row
                    for i in range(len(angle)):
                        angle[i]=int(angle[i])
                    i=1
                else:
                    rssi=row
                    for i in range(len(rssi)):
                        rssi[i]=float(rssi[i])
                    m=max(rssi)
                    for i in range(len(rssi)):
                        rssi[i]=rssi[i]-m
        angle_rssi=dict(zip(angle,rssi))
        return angle_rssi

#先画出d1和d2对应L的一个表然后查表,d的范围为0-1.8m，L范围为0m到3m
def create_index():
    angle_rssi=read_rssi_angel()#提供角度和rssi的关系
    p0=float(-37.52)#参考点天线1p0,l0
    d0=float(0.9)
    d=float(1.8)
    d1=np.linspace(float(0),float(1.8),num=1000).tolist()
    L=np.linspace(float(0),float(-3),num=1000).tolist()
    P=[]
    Q=[]
    rssi_distance=[]
    for i in range(len(d1)):
        if d1[i]==0 or d1[i]==d:
            continue
        else:
            P.append(p0-10*2*math.log10(d1[i]/d0))
            Q.append(p0 - 10 * 2 * math.log10((d-d1[i]) / d0))
        for j in range(len(L)):
            a=float(180)*math.atan(L[j]/d1[i])/math.pi#得到角度之后与angle_rssi中的数据进行匹配
            b=-float(180)*math.atan(L[j]/(d-d1[i]))/math.pi
            if isinstance(a,int):
                if a%2==0:
                    Pap=P[-1]+angle_rssi[a]
                else:
                    Pap=P[-1]+(angle_rssi[a-1]+angle_rssi[a+1])/2
            else:
                a=round(a)
                if a%2==0:
                    Pap=P[-1]+angle_rssi[a]
                else:
                    Pap=P[-1]+(angle_rssi[a-1]+angle_rssi[a+1])/2
            Pam=Pap-10*2*math.log10(math.sqrt(d1[i]**2+L[j]**2)/d1[i])
            if isinstance(b,int):
                if b%2==0:
                    Pbq=Q[-1]+angle_rssi[b]
                else:
                    Pbq=Q[-1]+(angle_rssi[b-1]+angle_rssi[b+1])/2
            else:
                b=round(b)
                if b%2==0:
                    Pbq=Q[-1]+angle_rssi[b]
                else:
                    Pbq=Q[-1]+(angle_rssi[b-1]+angle_rssi[b+1])/2
            Pbm = Pbq - 10 * 2 * math.log10(math.sqrt((d-d1[i])**2+L[j]**2)/(d-d1[i]))
            rssi_distance.append([Pam,Pbm,d1[i],L[j]])
    if (os.path.exists(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance_index_-37.52_0.9_1000点.csv')):
        os.remove(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance_index_-37.52_0.9_1000点.csv')
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance_index_-37.52_0.9_1000点.csv', 'w') as file:
        csvfile = csv.writer(file)
        for i in range(len(rssi_distance)):
            csvfile.writerow(rssi_distance[i])
    return

if __name__ == "__main__":
    create_index()