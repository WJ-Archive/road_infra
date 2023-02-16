
from ast import literal_eval
import threading

from model.dq import Data_Queue
from model.db import mysql_lib
from model.sen import sen
from model.det import det
from model.lineprf import lpf

from model.rdsf import rdsf
from pymysql import IntegrityError

import time

#import cv2
def mmfps(speed, fps=900): #mm
    print("mmfps",)
    return speed * (1000000/3600) / fps
    ...

def pthxy():

    ...


class Data_Model():
    def __init__(self):
        self.d = Data_Queue()

    def json_parser(self, data):
        json2dict = literal_eval(data)
        print(type(json2dict))
        print(json2dict)
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
            speed = dbh.select_gnss_seq_tb("speed")[0]
            print("gnss_현재 속도(lpf 계산용) : ",speed)
            print("gnss_현재 속도(lpf 계산용) : ",type(speed))

            if(lpf_data != None):
                
                lpf_data_parse = self.json_parser(lpf_data)
                pthole_data = literal_eval(lpf_data_parse[5])
                pthole_hmax = abs(pthole_data['h_max'])
                pthole_info = pthole_data['frame_info']
                
                lpf_d = list(map(str,lpf_data_parse[0:5]))+[str(pthole_hmax)]                
                dbh.insert_pthole_tb(lpf_d, dbh.select_last_id_gnss())

                #TODO :pthole info 데이터를 이용해 pt_frame_tb에 들어갈 값 구하기
                #1) 현재 속도값을 이용해서 포트홀 높이 측정 알고리즘 짜기 
                #2) 라인프로파일 frame_info 에서 들어오는 데이터 합쳐서 포트홀의 전체 크기 구하기 (pothole_tb, pt_frame_tb)
                #view 에서 출력하는 모델 없으니 바로 DB로 전달         
                #단위 : mm
                #x : 화면 비율 (포트홀 첫번째 지점)
                #w : 측정된 포트홀 길이
                #h : 깊이 평균. 
                #속도로 높이 구하는법 : 70km/h 라고할때 프레임당 거리.
                #카메라 fps
                #1) 단위 환산 mm x 1000 x 1000 (km) / sec x 60 x 60 (h)
                #카메라 FPS : 900프레임 918
                # n km x (1000000/3600) / fps = 간격(mm)

                last_lpf_id = dbh.select_last_id_pthole()

                p_res = 0
                line_gap = mmfps(speed)

                for d in pthole_info:
                    print(d)
                    dbh.insert_pt_frame_tb(list(map(str,[d['x'], d['w'], d['h_avg']])), str(last_lpf_id))
                    p_res += d['w']
                    ...
               
                res = p_res * line_gap * pthole_hmax
                print("res",res)

                #print("hmax::::",pthole_hmax)
                #print("info::::",pthole_info[0])
                #print("info::::",type(pthole_info[0]))


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

