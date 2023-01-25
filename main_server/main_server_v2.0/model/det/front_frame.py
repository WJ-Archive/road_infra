import numpy
from model.sck_connect import tcp_connect
#import cv2

# front frame 은 packages/utils/video.py 에서 사용.
SCK_SERVER_IP = "192.168.0.244"
SCK_SERVER_PORT = 3838
FRAME_WITDH = 640
FRAME_HEIGHT = 480

class Frame:
    def __init__(self):
        self._keep_running = True
        self._det_event = False
        self._s = b''
        self.connect_socket()
        ...

    def connect_socket(self):
        self.tcp_sck = tcp_connect.TCP_Sock(SCK_SERVER_IP, SCK_SERVER_PORT)
        self.sck = self.tcp_sck.tcp_connect()
        self.conn_sock, addr = self.sck.accept()
        print(str(addr),"에서 접속")

    def get_frame(self):
        
        if self._keep_running:

            data, addr = self.conn_sock.recvfrom((FRAME_WITDH * FRAME_HEIGHT * 3)) 
            self._s += data
            if(len(self._s) == (FRAME_WITDH * FRAME_HEIGHT * 3)): #921600 (width x height x rgb(3) )
                frame = numpy.fromstring(self._s, dtype=numpy.uint8)
                frame = frame.reshape(FRAME_HEIGHT, FRAME_WITDH, 3)
                self._det_event = False
                self._s = b''
                #cv2.imshow("imagename", frame)
                #cv2.waitKey()
                return frame

            elif(len(self._s)> (FRAME_WITDH * FRAME_HEIGHT * 3)): #921600
                #참고 : 이더넷 스위치 속도 느리면 제대로 전송 안됨
                print("초과", len(self._s))
                self._s = b''
                
                