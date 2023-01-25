import serial

class GNSS_Sensor:
    def __init__(self, GNSS_ComNO, Baudrate = 115200,  latitude=37.58070125, longtitude=126.88811022):
        self.GNSS_ComNo = GNSS_ComNO    
        self.baudrate = Baudrate
        self.latitude = latitude
        self.longtitude = longtitude
        self.speed = '0.0'
        self.ser = serial.Serial(self.GNSS_ComNo, self.baudrate, timeout = 1)
    
    def __del__(self):
        self.ser.close()
        print(self.GNSS_ComNo," Port Close (GNSS)")
    
    def get_gnss_serial(self):
        res = self.ser.readline()
        try:
            res_packet = res.decode('utf-8')[:len(res)-1]
            nmea_data = res_packet.split(',')
            if(nmea_data[0] == '$GNGGA'):
                if (nmea_data[2] == '' and nmea_data[4] == ''): 
                    print("cant detect satellite")
                    self.latitude = 0.0
                    self.longtitude = 0.0
                    self.speed = 0.0
                    return [self.latitude, self.longtitude, self.speed]
                else:
                    self.latitude = str(round(float(nmea_data[2][0:2]) + (float(nmea_data[2][2:])/60),6))[0:11]
                    self.longtitude = str(round(float(nmea_data[4][0:3]) + (float(nmea_data[4][3:])/60),6))[0:12]
                    return [self.latitude, self.longtitude, self.speed] #speed synchronization lat,lon --> speed delay occur
                    
            if(nmea_data[0] == '$GNVTG'):
                self.speed = nmea_data[5]
            
            #return [self.latitude, self.longtitude, self.speed] # gnvtg and gngga return

        except(UnicodeDecodeError):
            #NMEA 데이터중 UTF-8로 인코딩이 안되는 값이 출력됨...위도 경도 결과값에 영향을 끼치진 않는데 가끔 떠서 에러난다. 뭔지 몰라서 그냥 예외처리
            ...