# 부산 실측 후 변경사항
#   - 현재 사용하는  GNSS 센서의 속도가 느려서 Lux 값이 제대로 나오지 않아 가로등 탐지가 제대로 이루어지지 않음
#   - lux, temp, humi 는 ent_tb 라는곳에 따로 저장하니 그냥 나오는대로 보내는게 좋을것 같다. 따라서 앞에 구분을 '02'로 하여 전송
#   - marwis 센서 전송 X

from env import env
from imu import imu
from gnss import gnss

import os, sys
import socket
import json
import time, datetime
import numpy as np

import multiprocessing, threading
from multiprocessing.spawn import freeze_support

import psutil
import keyboard
import logging

GNSS_SER_PORT = "COM7" #USB Seraial Port
UA_SER_PORT = "COM9" # USB Serial Device
HWT_SER_PORT = 5 #USB Serial CH340

SOCKET_PORT_NUM = 4040
SOCKET_TARGET_IP = "192.168.0.244" #메인서버 고정 IP 
#SOCKET_TARGET_IP = "192.168.0.38" #메인서버 고정 IP 
th_flag = 0
reset_timer = 0

class sock_client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ...

    def __del__(self):
        self.sock.close()
        print("socket close")

    def send_socket_udp(self, msg):
        self.sock.sendto(msg.encode(), (SOCKET_TARGET_IP, SOCKET_PORT_NUM))

#메인서버 SQL에서 now()로 시간 저장 하도록 통일
#def get_dates(): 
#    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#진동 이벤트 발생시 5초 카운터 쓰레드 
def th_intr_timer():
    global th_flag, reset_timer
    th_flag = 1
    TIMER = 10
    tid = threading.get_native_id()
    num_of_secs = TIMER
    while (num_of_secs):
        if(reset_timer == 1):
            reset_timer = 0
            num_of_secs = TIMER
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@{:02d}:{:02d}@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'.format(m, s)
        print("")
        print(min_sec_format)
        print("")
        time.sleep(1)
        num_of_secs -= 1
    th_flag = 0

    sys.exit(0)

#q or exit 클릭시 프로세스 kill
def exit_program():
    process = psutil.Process(parent_process_id)
    for proc in process.children(recursive=True):
        print(f"child process {proc.pid} terminate")
        proc.kill()
        
    print(f"Parent process {process.pid} terminate")
    process.kill()

#gnss socket
def send_gnss_sock(): #realtime  
    sock = sock_client()
    gnss_object = gnss.GNSS_Sensor(GNSS_ComNO=GNSS_SER_PORT)
    while(1):
        gnss_data = gnss_object.get_gnss_serial()
        if (gnss_data != None):
            js_data = {
                'type' : '00', #gnss
                'lat' : gnss_data[0],
                'lon' : gnss_data[1],
                'speed' : gnss_data[2],
            }
            json_data = json.dumps(js_data, ensure_ascii=False, indent="\t")
            sock.send_socket_udp(json_data)
            print(json_data)

#imu
def send_imu_sock():
    global th_flag, reset_timer
    sock = sock_client()
    imu_object = imu.IMU_Sensor(HWT_ComNo=HWT_SER_PORT)
    pre_acc = [0,0,0]

    while(1):
        acc = imu_object.get_hwt()
        if((abs(acc[2])-1) >= 0.3):
            reset_timer = 1
            if not th_flag:
                t = threading.Thread(target = th_intr_timer)
                t.setDaemon(True)
                t.start()
        
        if(pre_acc != acc and th_flag):
            js_data = {
                'type' : '01', #imu
                'acc_x' : acc[0],
                'acc_y' : acc[1],
                'acc_z' : acc[2],
            }
            json_data = json.dumps(js_data, ensure_ascii=False, indent="\t")
            sock.send_socket_udp(json_data)
            print(json_data)
            pre_acc = acc

def send_env_sock():
    sock = sock_client()
    env_object = env.Env_Sensor(UAComNo=UA_SER_PORT)
    
    while(1):
        time.sleep(0.1)
        lux_data = env_object.get_lux()
        th_data = env_object.get_TH()[0:-1].split(',')
        js_data = {
            'type' : '02', #gnss & env
            'lux' : lux_data,
            'temp' : float(th_data[0]),
            'humi' : float(th_data[1]),
        }
        json_data = json.dumps(js_data, ensure_ascii=False, indent="\t")
        sock.send_socket_udp(json_data)
        print(json_data)
    ...


if __name__ == "__main__":
    freeze_support()
    parent_process_id = os.getpid()

    p0 = multiprocessing.Process(target = send_gnss_sock, args=())
    p0.start()
    print("p0 start...")

    p1 = multiprocessing.Process(target = send_imu_sock, args=())
    p1.start()
    print("p1 start...")

    p2 = multiprocessing.Process(target = send_env_sock, args=())
    p2.start()
    print("p2 start...")
    
    print("@@@@@@@@@@@@@@   종료 : Q or ESC   @@@@@@@@@@@@@@@@@")
    keyboard.add_hotkey(('q'), lambda: exit_program())
    keyboard.add_hotkey(('ESC'), lambda: exit_program())
    keyboard.wait()

    os.system('pause')
