#dll (hwt_905)
#IMU센서 코드는 c언어로 작성되있기 때문에 동적라이브러리파일로 컴파일 후 로드 (dll/gyro_dll.cpp)
from ctypes import *

class IMU_Sensor: #진동 Event 발생시 활성화 되야하는것들 : GNSS, IMU1, IMU2

    def __init__(self, HWT_ComNo, Baudrate = 9600, x=255, y=255, z=255):
        self.HWT_ComNo = HWT_ComNo        #IMU  PORT
        self.Baudrate = Baudrate

        #Load DLL into memory
        self.hwt_Dll = cdll.LoadLibrary("imu\\dll\\gyro_dll.dll")
       
        #open hwt Serial Port in DLL
        self.open_hwt()

    def __del__(self):
        print(self.HWT_ComNo," Port Close (HWT)")

    #hwt-905 open Serial (in dll)
    def open_hwt(self):
        open_gport = self.hwt_Dll['open_port']
        open_gport.argtypes = [c_ulong, c_ulong, c_int]
        open_gport(self.HWT_ComNo, self.Baudrate, 1)
        open_gport.restype = None

    #hwt-905 get value 
    def get_hwt(self):
        #hwt buff
        ret_buff = []
        get_gVal = self.hwt_Dll['get_gValue']
        get_gVal.argtypes = [c_int, c_int]
        get_gVal.restype = c_float
        for i in range(0,3):
            ret_buff.append(get_gVal(self.HWT_ComNo, i))
        
        return ret_buff
"""
imu = IMU_Sentsor() #def __init__(self, GNSS_ComNo ="COM10", Baudrate = 115200):
pre_imu_data = [0,0,0]
dbh = mysql_lib.DB_Handler()

while(1):
    imu_data = imu.get_hwt() #pitch(x,y), roll
    if pre_imu_data != imu_data: 
        print(imu_data) 
        dbh.insert_imu_tb(imu_data[0], imu_data[1], imu_data[2], 0, 0)
    pre_imu_data = imu_data

"""
