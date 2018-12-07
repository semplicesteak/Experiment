import numpy as np
import matplotlib.pyplot as plt
import math

# v我的平均步速
# t为检测的时间范围
# f为时间距离函数
def person_walk():
    v=1.25#(我的步速再4.0km/h-4.8km/h)
    t=np.linspace(float(0),float(8))
    f=[]
    for i in range(len(t)):
        f.append(v*t[i])
    plt.figure(figsize=(15,10))
    plt.plot(t,f,'o-',label='t - S')
    plt.xlabel('t (s)',fontsize=20)
    plt.ylabel('S (m)',fontsize=20)
    plt.title('t - S')
    plt.legend(loc='best')
    # plt.grid(True)
    plt.savefig('t-S',fontsize=20)
    plt.close()

#步频n=v*l/2s
# 身高h=183cm
# 步幅Sf=(h-155.911)/0.262 或 Sf=0.45h  所以这里取下这两种方法的平均值92，9cm
#躯干腿长指数= [ 身高(cm) - 坐高(cm) ] / 坐高(cm) ×100 ,腿长l=85cm
# 步频n=v*l/Sf
# 手摆动一个周期左右脚要分别走一次也就是两步，摆动周期T=2*Sf/v
# 振幅A假设0.15m，就是手摆出去的最大长度假设的不准
# f(t)=Asin(2Π*t/T)
def person_hand_Horizon():
    v=1.25
    Sf=0.929
    T=2*Sf/v
    t=np.linspace(0,T)#假设先从身体两侧向前摆，摆到最高点再往回摆，再摆到后侧的最高点向圣体两侧摆
    f=[]
    for i in range(len(t)):

        f.append(0.15*np.sin(2*math.pi*t[i]/T))
    plt.figure(figsize=(15, 10))
    plt.plot(t, f, 'o-', label='t - S')
    plt.xlabel('t (s)', fontsize=20)
    plt.ylabel('S (m)', fontsize=20)
    plt.title('t - S')
    plt.legend(loc='best')
    # plt.grid(True)
    plt.savefig('t-S-hand', fontsize=20)
    plt.close()

def Person_walking_horizon():
    v = 1.25
    Sf = 0.929
    T = 2 * Sf / v
    t = np.linspace(0, T)  # 假设先从身体两侧向前摆，摆到最高点再往回摆，再摆到后侧的最高点向圣体两侧摆
    f = []
    for i in range(len(t)):
        f.append(0.15*np.sin(2*math.pi*t[i]/T)+v*t[i])
    plt.figure(figsize=(15, 10))
    plt.plot(t, f, 'o-', label='t - S')
    plt.xlabel('t (s)', fontsize=20)
    plt.ylabel('S (m)', fontsize=20)
    plt.title('t - S')
    plt.legend(loc='best')
    # plt.grid(True)
    plt.savefig('t-S-Horizon', fontsize=20)
    plt.close()

#    O        d           A
#   ·-------------------·
#   \                α /
#   \                 /
#   \               /
# l \             /
#   \           /
#   \         /
# C ·      /
#   \     /
# x \   /
#   \ /
#   ·
# A为天线，d为天线与标签运动路径的垂直距离，O为垂点，l为起始位置与垂点的距离，C为运动一段时间后的点,α为天线与起始点的距离,seit为运动后的位置与天线的夹角
def RSSI_weak_module():
    l=2.5# 2.5m
    d=0.5# 0.5m
    α=math.atan(l/d)
    v = 1.25
    Sf = 0.929
    T = 2 * Sf / v
    t = np.linspace(float(0), float(2*l/v),num=200)  # 假设先从身体两侧向前摆，摆到最高点再往回摆，再摆到后侧的最高点向身体两侧摆
    P = -40  # 假设O点-30Hz
    p=np.linspace(float(-65),float(P),num=100)
    p2=np.linspace(float(P),float(-65),num=100)
    PC=[]
    for i in range(len(t)):
        x = 0.15 * np.sin(2 * math.pi * t[i] / T) + v * t[i]
        OC = l - x
        AC = math.sqrt(d ** 2 + OC ** 2)
        s = math.atan(OC / d)
        n = 2  # 与环境有关的常量
        if i<100:
            PC.append(p[i]-10*n*math.log10(AC/d))
        else:
            PC.append(p2[i-100] - 10 * n * math.log10(AC / d))
    plt.figure(figsize=(15, 10))
    plt.plot(t, PC, 'o-', label='t - S')
    plt.xlabel('t (s)', fontsize=20)
    plt.ylabel('PC (Hz)', fontsize=20)
    plt.title('t - PC')
    plt.legend(loc='best')
    # plt.grid(True)
    plt.savefig('t-PC', fontsize=20)
    plt.close()


if __name__ == '__main__':
    person_walk()
    person_hand_Horizon()
    Person_walking_horizon()
    RSSI_weak_module()
    print()