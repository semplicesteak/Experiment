import csv,os

def compute_average(path,name):
    with open(path, 'r') as f:
        csvfile=csv.reader(f)
        headers = next(csvfile)
        rssi=0.0
        i=0
        for row in csvfile:
            rssi+=float(row[1])
            i+=1
        p=rssi/i
        print("{0}".format(name)+str(p))
    return p

if __name__ == "__main__":
    path=[r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\recorddata_an1_0.9.csv',
          r'G:\PycharmPython\RFID_Human_Detection\RFID_Go_Out\recorddata_an2_0.9.csv']
    name=["天线1在正对天线0.9m时的平均天线强度为：",
          "天线2在正对天线0.9m时的平均天线强度为："]
    result=[]
    for i in range(len(path)):
        result.append(compute_average(path[i],name[i]))
    print((result[0]+result[1])/2)