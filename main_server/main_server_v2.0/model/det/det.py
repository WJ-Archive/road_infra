#Jetson Xavier (Yolov5s) detect Data
import socket
from model.sck_connect import udp_connect

SCK_SERVER_IP = '192.168.0.244'
SCK_SERVER_PORT = 3939
SCK_BUF = 2048

def get_detect_data():
    try:
        sck = udp_connect.UDP_Sock(SCK_SERVER_IP, SCK_SERVER_PORT, SCK_BUF)
        detect_data = sck.get_socket_udp()
        return detect_data

    finally:
        ...
        #print("det close....")