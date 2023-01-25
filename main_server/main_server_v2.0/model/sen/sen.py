#Sensor Integrated Embedded Board
from model.sck_connect import udp_connect
import socket

SCK_SERVER_IP = '192.168.0.244'
SCK_SERVER_PORT = 4040
SCK_BUF = 2048

def get_sensor_data():
    try:
        sck = udp_connect.UDP_Sock(SCK_SERVER_IP, SCK_SERVER_PORT, SCK_BUF)
        sensor_data = sck.get_socket_udp()
        return sensor_data
    
    
    finally:
        ...#print("sen close....")
        