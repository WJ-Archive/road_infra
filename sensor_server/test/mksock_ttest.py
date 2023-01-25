##### 센서통합 임베디드 보드에 올라갈 코드. () #####
#1. GNSS 와 env 센서는 1초에 한번씩 소켓 전송
#2. IMU 센서와 MARWIS 센서는 이벤트 발생시 소켓 전송.

#프로세스 2개로 구분. --> 더이상 올라가는 센서는 없을테니 2개정도면 충분한 퍼포먼스가 나올것으로 생각됨.
#   - 1초에 한번씩 소켓을 보내는 realtime p1,
#   - 이벤트 발생 감지시 센서속도에 맞춰 소켓을 보내는 event p2

from env import env
from imu import imu
from test import gnss_ttest
from rdsf import rdsf

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
UA_SER_PORT = "COM8" # USB Serial Device
HWT_SER_PORT = 6 #USB Serial CH340

SOCKET_PORT_NUM = 4040
SOCKET_TARGET_IP = "192.168.0.244" #메인서버 고정 IP (임시)
#SOCKET_TARGET_IP = "192.168.0.38" #메인서버 고정 IP (임시)
th_flag = 0
reset_timer = 0

class sock_client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ...

    def __del__(self):
        #self.sock.close()
        print("socket close")

    def send_socket_udp(self, msg):
        #여기서는 한 포트에 다중 프로세스가 접근하기 때문에 소켓연결 전송후 끊어 줘야함? 일단 보드오면 테스트 해봐야할듯.. 연결을 동시에 여러개 맺을수 있었나..?
        #젯슨자비어에서는 메인서버와 연결되는게 하나밖에 없어서 포트 하나 열어놓고 계속 쓰긴함..  
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(msg.encode(), (SOCKET_TARGET_IP, SOCKET_PORT_NUM))
        #self.sock.close()

def get_dates():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

def exit_program():
    process = psutil.Process(parent_process_id)
    for proc in process.children(recursive=True):
        print(f"child process {proc.pid} terminate")
        proc.kill()
        
    print(f"Parent process {process.pid} terminate")
    process.kill()

#env, gnss socket
def send_rt_sock(): #realtime  
    sock = sock_client()
    gnss_object = gnss_ttest.GNSS_Sensor(GNSS_ComNO=GNSS_SER_PORT)
    env_object = env.Env_Sensor(UAComNo=UA_SER_PORT)
    start_time = time.time()
    t1 = threading.Thread(target=gnss_object.get_gngga()) 
    t2 = threading.Thread(target=gnss_object.get_gnvtg()) 
    t1.setDaemon(True)
    t1.start()
    t2.setDaemon(True)
    t2.start()
    
    
    while(1):
        lux_data = env_object.get_lux()
        th_data = env_object.get_TH()[0:-1].split(',')
        print(gnss_object.gga_q.get())
        print(gnss_object.vtg_q.get())

        if (t1.join() != None):
            js_data = {
                'type' : '00', #gnss & env
                'lat' : gnss_data[0],
                'lon' : gnss_data[1],
                'speed' : speed,
                'lux' : lux_data,
                'temp' : float(th_data[0]),
                'humi' : float(th_data[1]),
                'time_stamp' : get_dates()
                #'time_stamp' : round(time.time() - start_time,1) #time_stamp 현재 날짜 or 가동 시간
            }
            json_data = json.dumps(js_data, ensure_ascii=False, indent="\t")
            sock.send_socket_udp(json_data)
            print(json_data)

#imu, rdsf
def send_imu_sock():
    global th_flag, reset_timer
    sock = sock_client()
    imu_object = imu.IMU_Sensor(HWT_ComNo=HWT_SER_PORT)
    start_time = time.time()
    pre_acc = [0,0,0]

    while(1):
        acc = imu_object.get_hwt()
        if((abs(acc[2])-1) >= 0.5):
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
                'time_stamp' : get_dates()
            }
            json_data = json.dumps(js_data, ensure_ascii=False, indent="\t")
            sock.send_socket_udp(json_data)
            print(json_data)

        pre_acc = acc


def send_rdsf_sock():

    ...

if __name__ == "__main__":
    freeze_support()
    parent_process_id = os.getpid()

    p0 = multiprocessing.Process(target = send_rt_sock, args=())
    p0.start()
    print("p0 start...")

    p1 = multiprocessing.Process(target = send_imu_sock, args=())
    p1.start()
    print("p1 start...")
    
    p2 = multiprocessing.Process(target = send_rdsf_sock, args=())
    p2.start()
    print("p2 start...")

    print("@@@@@@@@@@@@@@   종료 : Q or ESC   @@@@@@@@@@@@@@@@@")
    keyboard.add_hotkey(('q'), lambda: exit_program())
    keyboard.add_hotkey(('ESC'), lambda: exit_program())
    keyboard.wait()


