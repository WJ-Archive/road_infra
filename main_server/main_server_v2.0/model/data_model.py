
from ast import literal_eval
import threading

from model.dq import Data_Queue
from model.db import mysql_lib
from model.sen import sen
from model.det import det
from model.lineprf import lpf

from model.rdsf import rdsf
from pymysql import IntegrityError

#import cv2

class Data_Model():
    def __init__(self):
        self.d = Data_Queue()

    def json_parser(self, data):
        json2dict = literal_eval(data)
        li = json2dict.values()
        return list(map(str, li))
    
    def t_sen(self, sem):
        dbh = mysql_lib.DB_Handler()
        while True:
            sem.acquire()
            sen_data = sen.get_sensor_data()
            print(sen_data)
            if(sen_data != None):
                
                sen_data_parse = self.json_parser(sen_data)
                
                #gnss sock parsing
                if(sen_data_parse[0] == "00"):
                    self.d.latlon_buf.append(sen_data_parse[1])
                    self.d.latlon_buf.append(sen_data_parse[2])
                    dbh.insert_gnss_tb(sen_data_parse)
                    
                #imu sock parsing
                if(sen_data_parse[0] == "01"):
                    try:
                        self.d.acc_x_buf.appendleft(sen_data_parse[1])
                        self.d.acc_y_buf.appendleft(sen_data_parse[2])
                        self.d.acc_z_buf.appendleft(sen_data_parse[3])
                        dbh.insert_imu_tb(sen_data_parse, dbh.select_last_id_gnss())
                    except IntegrityError:
                        print("no gnss_id : 외래키(gnss_id)없음 .. 참조무결성 위배 GNSS_대기")

                #env sock parsing
                if(sen_data_parse[0] == "02"):
                    try:
                        self.d.lux_buf.appendleft(sen_data_parse[1])
                        self.d.temp_buf.appendleft(sen_data_parse[2])
                        self.d.humi_buf.appendleft(sen_data_parse[3])
                        dbh.insert_env_tb(sen_data_parse, dbh.select_last_id_gnss()) 
                    
                    except IntegrityError:
                        print("no gnss_id : 외래키(gnss_id)없음 .. 참조무결성 위배 GNSS_대기")

            sem.release()

    #
    def t_det(self, sem):
        dbh = mysql_lib.DB_Handler()
        while True:
            sem.acquire()
            det_data = det.get_detect_data()
            if(det_data != None):
                det_data_parse = self.json_parser(det_data)
                if(det_data_parse[0] =='11'):
                    try:
                        print(det_data_parse)
                        self.d.det_buf.append(det_data_parse[1:])
                        dbh.insert_det_tb(det_data_parse, dbh.select_last_id_gnss())
                    except IntegrityError:
                        print("no gnss_id : 외래키(gnss_id)없음 .. 참조무결성 위배 GNSS_대기")    
            sem.release()
    
    #마위스 센서 데이터 (도로노면 road_surface)
    def t_rdsf(self, sem):
        dbh = mysql_lib.DB_Handler()
        pre_mws_data = ''
        while True:
            sem.acquire()
            mws_data = rdsf.marwis_requests()
            if(pre_mws_data != mws_data):
                try:
                    #view 에서 출력하는 모델 없으니 바로 DB로 전달
                    #데이터 파싱은 DB SQL 문에서 수행
                    dbh.insert_road_tb(mws_data, dbh.select_last_id_gnss())
                    pre_mws_data = mws_data
                except IntegrityError:
                    print("no gnss_id : 외래키(gnss_id)없음 .. 참조무결성 위배 GNSS_대기")
            
            sem.release()

    #라인프로파일러 센서 데이터 
    def t_lpf(self, sem):
        dbh = mysql_lib.DB_Handler()
        speed = 0.0
        while True:
            sem.acquire()
            lpf_data = lpf.get_lineprofiler_data()
            #속도값은 GNSS 센서의 NMEA데이터중 $GNVPS 에서 파싱한 값 사용
            speed = dbh.select_gnss_seq_tb("speed")
            print("현재 속도 : ",speed)

            if(lpf_data != None):
                print(lpf_data)
                #TODO : 현재 속도값을 이용해서 포트홀 높이 측정 알고리즘 짜기
                #TODO : 라인프로파일 frame_info 에서 들어오는 데이터 합쳐서 포트홀의 전체 크기 구하기 (pothole_tb, pt_frame_tb)
                #데이터 예시
                '''
                {
                    "msg_uuid" : "12345678-1234-5678-1234-567812345678",
                    "obj_id" : 1794,
                    "obj_type" : 20,
                    "obj_image" : "0000000000142.png",
                    "obj_time" : "2022-06-20 09:25:59",
                    "size" : {
                        "h_max" : -63.84,
                        "frame_info" : [
                            {
                                "x" : 20.16,
                                "w" : 195.42,
                                "h_avg" : -16.33
                            },
                            {
                                "x" : 5.1,
                                "w" : 305.42,
                                "h_avg" : -59.99
                            },
                            {
                                "x" : 14.61,
                                "w" : 261.42,
                                "h_avg" : -37.41
                            },
                            {
                                "x" : 35.64,
                                "w" : 53.66,
                                "h_avg" : -8.1
                            }
                        ]
                    }
                }
                '''
                #view 에서 출력하는 모델 없으니 바로 DB로 전달
                #데이터 파싱은 DB SQL 문에서 수행         
                #dbh.insert_gnss_tb(lpf_data) 
            sem.release()


    #Process 1
    def run(self): 
        sem = threading.Semaphore(4)
        t1 = threading.Thread(target = self.t_sen, args = (sem,))
        t1.start()
        t2 = threading.Thread(target = self.t_det, args = (sem,))
        t2.start()
        t3 = threading.Thread(target = self.t_rdsf, args = (sem,))
        t3.start()
        t4 = threading.Thread(target = self.t_lpf, args = (sem,))
        t4.start()

