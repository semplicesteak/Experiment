import math,csv
import matplotlib.pyplot as plt

#返回一个具有十个点的点集
def detect_distance(rssi):
    rssi_distance = read_rssi_distance_index()
    distance_set=[]#记录输入的点到所有点的距离以及对应的距离
    for i in range(len(rssi_distance)):
        rssi_distance[i] = [float(rssi_distance[i][0]), float(rssi_distance[i][1]), float(rssi_distance[i][2]),
                            float(rssi_distance[i][3])]#str转换成float做计算
        d = math.sqrt((rssi_distance[i][0] - rssi[0]) ** 2 + (rssi_distance[i][1] - rssi[1]) ** 2)
        distance_set.append([d,rssi_distance[i][2],rssi_distance[i][3]])
    distance_set.sort(key=lambda x:x[0])
    distance_point_set = []
    q=10
    if len(distance_set)<10:
        q=len(distance_set)
    for i in range(q):
        distance_point_set.append([distance_set[i][1],distance_set[i][2]])
    return distance_point_set


def detect_start_path():
    with open(r'G:\PycharmPython\RFID_Human_Detection\第九次实验\第九次实验\recorddata_out1 先中间 后靠近2 最后靠近1.csv', 'r') as f:
        csv_content = csv.reader(f)
        headers = next(csv_content)
        i = 0
        all_row = []
        distance_row = []
        for row in csv_content:
            if i == 1 and row[7][:4] != "stop":
                all_row.append(row)
                if row[4] != all_row[-2][4]:
                    if all_row[-2][5] != '\\Z' and all_row[-1][5] != '\\Z':
                        if row[4] == "1" and abs(int(row[5]) - int(all_row[-2][5])) < 40000:  # 判断两个强度之间间隔时间不能太大
                            distance_row.append([row[1], all_row[-2][1]])
                        elif row[4] == "2" and abs(int(row[5]) - int(all_row[-2][5])) < 40000:
                            distance_row.append([all_row[-2][1], row[1]])
            if row[7][:5] == "start":
                i = 1
                all_row.append(row)
                distance_row.append(['start', 'start'])
            if row[7][:4] == "stop":
                i = 0
                all_row.append(row)
                distance_row.append(['stop', 'stop'])
        distance_group=[]
        for q in range(len(distance_row)):
            distance=[]
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
            else:
                distance.append(detect_distance([float(distance_row[q][0]), float(distance_row[q][1])]))

def read_rssi_distance_index():
    rssi_distance = []
    with open(r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\RSSI_Distance_index_-37.52_0.9_100点.csv',
              'r') as file:
        csvfile = csv.reader(file)
        for row in csvfile:
            if len(row) == 0:
                continue
            rssi_distance.append(row)
    return  rssi_distance

if __name__ == "__main__":
    detect_start_path()