#type 을 통해 어떤 데이터인지 구분? 사실 PORT 가 달라서 구분 할 필요 없을듯

from ast import literal_eval
from matplotlib.font_manager import json_load
from det import det
from sen import sen
from db import mysql_lib

import os, sys
import socket
import json
import re

import keyboard
import psutil

import multiprocessing
from multiprocessing.spawn import freeze_support

def exit_program():
    process = psutil.Process(parent_process_id)
    for proc in process.children(recursive=True):
        print(f"child process {proc.pid} terminate")
        proc.kill()
        
    print(f"Parent process {process.pid} terminate")
    process.kill()

def json_parser(data):
    json2dict = literal_eval(data)
    #json2dict = eval(data)
    li = json2dict.values()
    return list(map(str, li)) #SQL구문으로 써야해서 str으로 전부 변환  
    

def recv_sen(): #odyssey (센서통합임베디드 에서 들어오는 데이터 -- GNSS, lux, temp, humi, imu, rdsf)
    dbh = mysql_lib.DB_Handler()
    #sck = det.sock_server()
    while(1):
        #다중프로세스 에서 한 포트에 동시에 접근하기 때문에 소켓을 끊었다 연결했다 반복 (detect_data() 호출되면 소켓 연결후 대기하다가 받으면 데이터 출력후 __del__ ... 반복)
        recv_sck_data = sen.get_sensor_data()
        if(recv_sck_data != None):
            print(recv_sck_data)
            recv_data = json_parser(recv_sck_data)

            #쓰레드 처리 변경
            #type, [lat,lon], lux, temp, humi, time_stamp
            if(recv_data[0] == "00"):
                dbh.insert_gnss_tb(recv_data[1], recv_data[2], recv_data[3], recv_data[7]) #latitude, longtitude, speed, time_stamp
                dbh.insert_env_tb(recv_data[4], recv_data[5], recv_data[6], recv_data[7], dbh.select_last_id_gnss()) #lux, temp, humi, time_stamp, gnss_id
            
            #쓰레드 처리 변경
            #type, x, y, z, time_stamp
            if(recv_data[0] == "01"):
                dbh.insert_imu_tb(recv_data[1], recv_data[2], recv_data[3], recv_data[4], dbh.select_last_id_gnss()) #acc_x, acc_y, acc_z, time_stamp, gnss_id

            #쓰레드 처리 변경
            #if(recv_data[0] == "10"):
            #    dbh.insert_det_tb(recv_data[1],recv_data[2],recv_data[3],recv_data[4],recv_data[5],recv_data[6],recv_data[7],recv_data[8],recv_data[9])#img_detect, time_stamp, gnss_id
        ...

def recv_det(): #jetson-Xavier (영상처리서버에서 들어오는 데이터 -- Yolov5 data)
    dbh = mysql_lib.DB_Handler()
    #한 프로세스 하고만 연결되기때문에 소켓을 끊었다 연결했다 반복해서 리소스를 추가로 쓰는것보다 직접 소켓 데이터를 호출해서 한번만 연결하고 종료까지 유지해서 리소스를 줄이는게 좋을것 같다?
    sck = det.sock_server()
    while(1):
        print(1)
        recv_sck_data = sck.get_socket_udp()
        if(recv_sck_data != None):
            print(3)
            recv_data = json_parser(recv_sck_data)
            print(recv_data)
            dbh.insert_det_tb(recv_data, dbh.select_last_id_gnss())#img_detect, time_stamp, gnss_id#img_detect, time_stamp, gnss_id
        ...


if __name__ == "__main__":
    freeze_support()
    parent_process_id = os.getpid()

    p0 = multiprocessing.Process(target = recv_sen, args=())
    p1 = multiprocessing.Process(target = recv_det, args=())
    p0.start()
    print("p0 start...")    
    p1.start()
    print("p1 start...")
    
    keyboard.add_hotkey(('q'), lambda: exit_program())
    keyboard.add_hotkey(('ESC'), lambda: exit_program())
    keyboard.wait()
