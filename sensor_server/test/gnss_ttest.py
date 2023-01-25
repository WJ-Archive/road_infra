import serial
import queue
import threading


#python thread is not parallel processing. so not use semaphore
class GNSS_Sensor:
    def __init__(self, GNSS_ComNO, Baudrate = 115200,  latitude=37.58070125, longtitude=126.88811022):
        self.GNSS_ComNo = GNSS_ComNO    
        self.baudrate = Baudrate
        self.latitude = latitude
        self.longtitude = longtitude
        self.speed = '0.0'
        self.ser = serial.Serial(self.GNSS_ComNo, self.baudrate, timeout = 1)
        self.gga_q = queue.Queue()
        self.vtg_q = queue.Queue()
        self.sem = threading.Semaphore(10)
    
    def __del__(self):
        self.ser.close()
        print(self.GNSS_ComNo," Port Close (GNSS)")
    
    def get_gngga(self):
        
        try:
            self.sem.acquire()
            res = self.ser.readline()    
            res_packet = res.decode('utf-8')[:len(res)-1]
            nmea_data = res_packet.split(',')
            print("gga",res_packet)
            if(nmea_data[0] == '$GNGGA'):
                if (nmea_data[2] == '' and nmea_data[4] == ''): 
                    print("cant detect satellite")
                    self.latitude = 0.0
                    self.longtitude = 0.0
                    self.gga_q.put([self.latitude,self.longtitude])
                else:
                    self.latitude = str(round(float(nmea_data[2][0:2]) + (float(nmea_data[2][2:])/60),6))[0:11]
                    self.longtitude = str(round(float(nmea_data[4][0:3]) + (float(nmea_data[4][3:])/60),6))[0:12]
                    print([self.latitude,self.longtitude])
                    self.gga_q.put([self.latitude,self.longtitude])
            self.sem.release()

        except(UnicodeDecodeError):
            self.sem.release()
            ...

    def get_gnvtg(self):

        try:
            self.sem.acquire()
            res = self.ser.readline()
            res_packet = res.decode('utf-8')[:len(res)-1]
            nmea_data = res_packet.split(',')
            print("vtg",res_packet)
            if(nmea_data[0] == '$GNVTG'):
                self.speed = nmea_data[5]
                print(self.speed)
                self.vtg_q.put(self.speed)
            self.sem.release()

        except(UnicodeDecodeError):
            self.sem.release()
            ...
