import numpy as np
import matplotlib.pyplot as plt
import math,csv,os,time
import sympy
from scipy.optimize import fsolve,root

#环境量n=2
def rssi_distance_weak(p2,d1,d2):
    n=2
    P=p2-10*n*math.log10(d1/d2)
    return P

def rssi_angle_weak(p,r):
    p1=0.002014
    p2=0.0009455
    p3=0.3127
    P=p-p1*np.square(r)-p2*r-p3
    return P

def walk_model(t):
    v=1.25
    Sf=0.929#步幅
    T = 2 * Sf / v
    A=0.15#摆动幅度最大0.15m
    S=v*t+A*np.sin(2*math.pi*t/T)
    return S

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

#先画出d1和d2对应L的一个表然后查表,d的范围为0-2m，L范围为-4m到4m
def determine_a_point_model():
    angle_rssi=read_rssi_angel()#提供角度和rssi的关系
    p0=float(-35.0)#假设参考点p0=-35Hz,l0=0.6m
    d0=float(0.6)
    d=float(2)
    d1=np.linspace(float(0),float(2),num=1000).tolist()
    L=np.linspace(float(3),float(-3),num=1000).tolist()
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
    if (os.path.exists(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance.csv')):
        os.remove(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance.csv')
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance.csv', 'w') as file:
        csvfile = csv.writer(file)
        for i in range(len(rssi_distance)):
            csvfile.writerow(rssi_distance[i])
    return

#假设参考点p0=-35Hz,l0=0.6m,这种方法目前求不出非线性方程组的解暂时搁置
def first_point_model():
    x,y=sympy.symbols('x y')#x=d1,y=L
    n=float(2)
    p0=float(-35.0)
    d0=float(0.6)
    s1 = float(0.002014)
    s2 = float(0.0009455)
    s3 = float(0.3127)
    PA=float(-47.8)
    PB=float(-53)
    d=float(2)
    f=[p0-10*n*sympy.log(x/d0,10)-s1*sympy.root((180/sympy.pi)*sympy.atan(y/x),2)-s2*(180/sympy.pi)*sympy.atan(y/x)-s3-10*n*sympy.log(sympy.sqrt(sympy.root(x,2)+sympy.root(y,2))/x,10)-PA,
                        p0-10*n*sympy.log((d-x)/d0,10)-s1*sympy.root((180/math.pi)*sympy.atan(y/(d-x)),2)-s2*(180/sympy.pi)*sympy.atan(y/(d-x))-s3-10*n*sympy.log(sympy.sqrt(sympy.root((d-x),2)+sympy.root(y,2))/(d-x),10)-PB]
    p=sympy.expand(f[0])
    print(p)
    q=sympy.expand(f[1])
    print(q)
    result=sympy.nonlinsolve([p,q],[x,y])
    # result=fsolve(f,[1,1])
    print(result)
    return result


# def f(x):
#     x0,x1 = x.tolist()#0代表L，1代表d1
#     n = float(2.0)
#     p0 = float(-35.0)
#     d0 = float(0.6)
#     s1 = float(0.002014)
#     s2 = float(0.0009455)
#     s3 = float(0.3127)
#     PA = float(-45)
#     PB = float(-50)
#     d = float(1.0)
#     return [
#         p0 - 10 * n * sympy.log(x1 / d0, 10) - s1 * sympy.root((180 / sympy.pi) * sympy.atan(x0 / x1), 2) - s2 * (180 / sympy.pi) * sympy.atan(x0 / x1) - s3 - 10 * n * sympy.log(sympy.sqrt(sympy.root(x1, 2) + sympy.root(x0, 2)) / x1, 10) - PA,
#         p0 - 10 * n * sympy.log(d - x1 / d0, 10) - s1 * sympy.root((180 / math.pi) * sympy.atan(x0 / d - x1), 2) - s2 * (180 / sympy.pi) * sympy.atan(x0 / d - x1) - s3 - 10 * n * sympy.log(sympy.sqrt(sympy.root((d - x1), 2) + sympy.root(x0, 2)) / d - x1, 10) - PB,
#     ]

def no_block_model():
    return

# 该方法通过之前求出的表，用输入的点与表中所有点进行欧式距离计算找到距离最短的点
def detect_distance(rssi_distance,rssi):
    # rssi=[float(-60.5),float(-62)]#第四组
    # rssi=[float(-58.5),float(-64)]#第五组
    # rssi = [float(-61), float(-62.5)]  # 第六组
    d_min=float(1000)
    # distance=[]
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
    with open(r'G:\PycharmPython\RFID_Human_Detection\recorddata_baibi41.csv', 'r') as f:
        csv_content=csv.reader(f)
        headers = next(csv_content)
        i = 0
        all_row=[]
        distance_row=[]
        for row in csv_content:
            if i == 1 and row[7][:4] != "stop":
                all_row.append(row)
                if row[4]!=all_row[-2][4] :
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
                for p in range(2, len(distance)):  # 设置一个阈值，d1的波动范围在+-0.4之间
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
                plt.legend(loc='best')
                plt.grid(True)
                path = r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\picture\{0}.png'.format(q)
                plt.savefig(path)
                plt.close()
            else:
                distance.append(detect_distance(rssi_distance,[float(distance_row[q][0]),float(distance_row[q][1])]))



    return


if __name__ == '__main__':
    # no_block_model()
    # first_point_model()
    # determine_a_point_model()
    t1=time.time()
    rssi_distance=[]
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance.csv', 'r') as file:
        csvfile=csv.reader(file)
        for row in csvfile:
            if len(row)==0:
                continue
            rssi_distance.append(row)
    # print(rssi_distance)
    # detect_distance(rssi_distance)
    detect_path(rssi_distance)
    t2=time.time()
    t=t2-t1
    print(t)
