#Yocto-Light-V3 import
import os,sys
import serial

# add ./Sources to the PYTHONPATH
sys.path.append(os.path.join("env\\Sources"))
from yocto_api import *
from yocto_lightsensor import *


class Env_Sensor:
    def __init__(self, UAComNo, Baudrate = 9600):
        #port                       #light sensor 는 YAPI API 내부에서 잡는다.
        self.UAComNo = UAComNo            #UA10 PORT
        self.Baudrate = Baudrate

        #port setting
        self.ser = serial.Serial(self.UAComNo, self.Baudrate, timeout = 1)
        
        self.errmsg = YRefParam()
        
        # Setup the API to use local USB devices
        if YAPI.RegisterHub("usb", self.errmsg) != YAPI.SUCCESS:
            sys.exit("init error"+self.errmsg.value)

        # retreive any Light sensor
        self.sensor = YLightSensor.FirstLightSensor()

        if self.sensor is None :
            self.die('No module connected')

        if not(self.sensor.isOnline()): self.die('device not connected')

    def __del__(self):
        print("ENV Sensor Serial Close(UA, YOCTO)")
        self.ser.close()
    
    def die(self, msg):
        sys.exit(msg+'(check USB cable)')

    #UA10 get value (Temp, Humidity)
    def get_TH(self):
        #write AT Commands
        self.ser.write(b"ATCD\r\n")       
        #read serial
        res = self.ser.readline()
        #packet decode
        res_packet = res.decode()[:len(res)-1].split(" ")
        return res_packet[1]

    #Yocto-light-V3 get Value (lux)
    def get_lux(self):
        lx = self.sensor.get_currentValue()
        return lx
