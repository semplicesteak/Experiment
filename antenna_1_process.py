import csv,os,pywt
import numpy as np
import matplotlib.pyplot as plt

#1根天线
class one_antenna():
    # 分组
    def distribute_group(self,path):
        IW=intial_write_csv()
        file_name = path.split('.')
        path_clear = file_name[0] + "_clear.csv"
        with open(path, 'r') as f:
            csv_content = csv.reader(f)
            headers = next(csv_content)
            headers_clear = [headers[1], headers[5], headers[6]]
            IW.initial_file(path_clear, headers_clear)
            clear_row = []
            clear_RSSI=[]
            clear_time=[]
            clear_group=[]
            i=0
            j=0
            for row in csv_content:
                if i == 1 and row[7][:4] != "stop":
                    clear_row = (str(row[1]), row[5], row[6])
                    clear_RSSI.append(clear_row[0])
                    clear_time.append(clear_row[1])
                    clear_group.append(clear_row)
                if row[7][:5] == "start":
                    i = 1
                    clear_row = (str(row[1]), row[5], row[6])
                    clear_RSSI.append(clear_row[0])
                    clear_time.append(clear_row[1])
                    clear_group.append(clear_row)
                if row[7][:4] == "stop":
                    i = 0
                    clear_row = (str(row[1]), row[5], row[6])
                    clear_RSSI.append(clear_row[0])
                    clear_time.append(clear_row[1])
                    clear_group.append(clear_row)
                    self.origin_picture(clear_RSSI,clear_time,j,file_name[0])#画原始图像
                    self.denoising_picture(clear_RSSI,clear_time,j,file_name[0])#画去噪后的图像
                    row_stop = {'next'}
                    j=j+1
                    clear_group.append(row_stop)
                    IW.write_file(path_clear, clear_group)
                    clear_RSSI = []
                    clear_time = []
                    clear_group = []

    #画原图
    def origin_picture(self,data,time,picturename,picturedir):
        data[0]='-80'
        data[-1]='-80'
        for i in range(len(data)):#将str类型变成float型
            data[i]=float(data[i])
        DP=draw_picture()
        DP.visualization(data, time, picturename, picturedir)

    #画小波图
    def denoising_picture(self,data,time,picturename,picturedir):
        data=data[1:-1]
        for i in range(len(data)):
            data[i]=float(data[i])#将str类型变成float型
        WD=wavelet_denoising()
        meta=WD.wavelet_denosing_7_levels(data)
        meta=meta.tolist()
        meta.insert(0,float('-80'))
        meta.insert(len(meta),float('-80'))
        picturedir=picturedir+"_denosing"
        DP = draw_picture()
        DP.visualization(meta, time, picturename, picturedir)

#2根天线
class double_antenna():
    #分组
    def distribute_group(self,path):
        file_name=path.split('.')
        path_clear1=file_name[0]+'_clear1.csv'
        path_clear2=file_name[0]+'_clear2.csv'
        with open(path,'r') as f:
            csv_content = csv.reader(f)
            headers = next(csv_content)
            headers_clear = [headers[1], headers[5], headers[6]]
            IW=intial_write_csv()
            IW.initial_file(path_clear1,headers_clear)
            IW.initial_file(path_clear2,headers_clear)
            clear_row=[]
            clear_row1=[]
            clear_row2=[]
            clear_RSSI1=[]
            clear_RSSI2=[]
            clear_time1=[]
            clear_time2=[]
            clear_group1=[]
            clear_group2=[]
            i=0
            j=0
            for row in csv_content:
                if i == 1 and row[7][:4] != "stop":
                    if row[4] == "1":#天线1数据
                        clear_row1=(str(row[1]), row[5], row[6])
                        clear_RSSI1.append(clear_row1[0])
                        clear_time1.append(clear_row1[1])
                        clear_group1.append(clear_row1)
                    if row[4] == "2":#天线2数据
                        clear_row2 = (str(row[1]), row[5], row[6])
                        clear_RSSI2.append(clear_row2[0])
                        clear_time2.append(clear_row2[1])
                        clear_group2.append(clear_row2)
                if row[7][:5] == "start":
                    i = 1
                    clear_row = (str(row[1]), row[5], row[6])
                    clear_RSSI1.append(clear_row[0])
                    clear_time1.append(clear_row[1])
                    clear_group1.append(clear_row)
                    clear_RSSI2.append(clear_row[0])
                    clear_time2.append(clear_row[1])
                    clear_group2.append(clear_row)
                if row[7][:4] == "stop":
                    i = 0
                    clear_row = (str(row[1]), row[5], row[6])
                    clear_RSSI1.append(clear_row[0])
                    clear_time1.append(clear_row[1])
                    clear_group1.append(clear_row)
                    clear_RSSI2.append(clear_row[0])
                    clear_time2.append(clear_row[1])
                    clear_group2.append(clear_row)
                    self.origin_picture(clear_RSSI1,clear_time1,clear_RSSI2,clear_time2,j,file_name[0])#原图
                    self.denoising_picture(clear_RSSI1,clear_time1,clear_RSSI2,clear_time2,j,file_name[0])#小波图
                    row_stop = {'next'}
                    j=j+1
                    clear_group1.append(row_stop)
                    clear_group2.append(row_stop)
                    IW.write_file(path_clear1, clear_group1)
                    IW.write_file(path_clear2, clear_group2)
                    clear_RSSI1 = []
                    clear_RSSI2 = []
                    clear_time1 = []
                    clear_time2 = []
                    clear_group1 = []
                    clear_group2 = []

    #画原图
    def origin_picture(self,data1,time1,data2,time2,picturename,picturedir):
        if len(time1)==0 or len(time2)==0:
            return
        else:
            data1[0]='-80'
            data1[-1]='-80'
            data2[0]='-80'
            data2[-1]='-80'
            for i in range(len(data1)):  # 将str类型变成float型
                data1[i] = float(data1[i])
            for i in range(len(data2)):  # 将str类型变成float型
                data2[i] = float(data2[i])
            DP = draw_picture()
            DP.visualization_double_antenna(data1,time1,data2,time2,picturename,picturedir)

    #画小波去噪图
    def denoising_picture(self,data1,time1,data2,time2,picturename,picturedir):
        if len(time1)==0 or len(time2)==0:
            return
        else:
            data1=data1[1:-1]
            data2=data2[1:-1]
            for i in range(len(data1)):  # 将str类型变成float型
                data1[i] = float(data1[i])
            for i in range(len(data2)):  # 将str类型变成float型
                data2[i] = float(data2[i])
            WD=wavelet_denoising()
            meta1=WD.wavelet_denosing_7_levels(data1)
            meta2=WD.wavelet_denosing_7_levels(data2)
            meta1=meta1.tolist()
            meta2=meta2.tolist()
            meta1.insert(0, float('-80'))
            meta1.insert(len(meta1), float('-80'))
            meta2.insert(0, float('-80'))
            meta2.insert(len(meta2), float('-80'))
            picturedir = picturedir + "_denosing"
            DP=draw_picture()
            DP.visualization_double_antenna(meta1,time1,meta2,time2,picturename,picturedir)

#初始化文件及文件写入
class intial_write_csv():
    #初始化存储分好组的文件
    def initial_file(self,path, headers):
        if (os.path.exists(path)):
            os.remove(path)
        with open(path, 'w') as f:
            csvfile = csv.writer(f)
            csvfile.writerow(headers)

    #文件写入
    def write_file(self,path, content):
        with open(path, 'a') as f:
            csvfile = csv.writer(f)
            for i in range(len(content)):
                csvfile.writerow(content[i])

    #画图
class draw_picture():
    # 判断文件夹是否存在
    def detect_dir(self, dirpath):
        if (os.path.isdir(dirpath)):
            return
        else:
            os.mkdir(dirpath)

    def visualization(self,data,time,name,picturedir):#1根天线
        time_list=[0]
        for i in range(1,len(time)):
            time_list.append((int(time[i])-int(time[i-1])+time_list[i-1])/1000)
        x=np.array(time_list)
        self.draw_pic(x,data,name,picturedir)

    def visualization_double_antenna(self,data1, time1, data2, time2, name,picturedir):  # 2根天线
        time_list1 = [0]
        for i in range(1, len(time1)):
            time_list1.append(int(time1[i]) - int(time1[i - 1]) + time_list1[i - 1])
        x1 = np.array(time_list1)

        time_list2 = [0]
        for i in range(1, len(time2)):
            time_list2.append(int(time2[i]) - int(time2[i - 1]) + time_list2[i - 1])
        x2 = np.array(time_list2)

        self.draw_pic_double_antenna(x1,data1,x2,data2,name,picturedir)

    def draw_pic(self,x,y,name,picturedir):
        plt.figure(figsize=(15,10))
        plt.plot(x,y,'o-',label='antenna')
        plt.xlabel('Time difference between every two points (ms)')
        plt.ylabel('RSSI (Hz)')
        plt.title('group:{0}'.format(name))
        plt.legend(loc='best')
        plt.grid(True)
        # plt.gca().invert_yaxis()#将外轴坐标安从大到小排列
        self.detect_dir(picturedir)
        path=picturedir+'/{0}.png'.format(name)
        plt.savefig(path)
        plt.close()

    def draw_pic_double_antenna(self,x1, y1, x2, y2, name,picturedir):
        plt.figure(figsize=(15, 10))
        plt.plot(x1, y1, '^-', color='b', label='antenna-1')
        plt.plot(x2, y2, 'o-', color='r', label='antenna-2')
        plt.xlabel('Time difference between every two points (ms)')
        plt.ylabel('RSSI (Hz)')
        plt.title('group:{0}'.format(name))
        plt.legend(loc='best')
        plt.grid(True)
        self.detect_dir(picturedir)
        path=picturedir+'/{0}.png'.format(name)
        plt.savefig(path)
        plt.close()

#小波去噪
class wavelet_denoising():
    def wavelet_denosing_7_levels(self,data):
        coeffs = pywt.wavedec(data, 'coif5', mode='symmetric',
                              level=7)  # 将波分为7层，这行代码是一个参数是数据，第二个参数选择小波基这里选coif5，第三个点是模型默认是symmetric，第四个参数是分的层数
        cA7, cD7, cD6, cD5, cD4, cD3, cD2, cD1 = coeffs
        sD7 = pywt.threshold(cD7, 0.014, 'soft')
        sD6 = pywt.threshold(cD6, 0.014, 'soft')
        sD5 = pywt.threshold(cD5, 0.014, 'soft')
        sD4 = pywt.threshold(cD4, 0.014, 'soft')
        sD3 = np.zeros(len(cD3))
        sD2 = np.zeros(len(cD2))
        sD1 = np.zeros(len(cD1))
        coeffs2 = [cA7, sD7, sD6, sD5, sD4, sD3, sD2, sD1]
        meta = pywt.waverec(coeffs2, 'coif5')
        if len(meta) > len(data):
            meta = meta[:-1]
        return meta

if __name__ == '__main__':
	#path1=r'seven_exp\recorddata_out1.csv'
	#path2=r'sixth_exp\360测试.csv'
	#path3=r'sixth_exp\360测试2.csv'
	#path4=r'sixth_exp\半圆环垂直.csv'
	#path5=r'sixth_exp\单天线摆手出门.csv'
	#path6=r'sixth_exp\单天线不摆臂水平.csv'
	#path7=r'sixth_exp\单天线非出门横走.csv'
	#path8=r'sixth_exp\单天线水平摆手出门.csv'
	#A1=one_antenna()
	#A1.distribute_group(path1)
	#A1.distribute_group(path2)
	#A1.distribute_group(path3)
	#A1.distribute_group(path4)
	#A1.distribute_group(path5)
	#A1.distribute_group(path6)
	#A1.distribute_group(path7)
	#A1.distribute_group(path8)
	path1=r'F:\2018\行为识别实验\姿势无关的出入检测\Picture\eight_exp\recorddata_baibi4.csv'
	A2=double_antenna()
	A2.distribute_group(path1)