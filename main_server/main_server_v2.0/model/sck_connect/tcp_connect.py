# -*- coding: utf-8 -*-
import socket

FRAME_WITDH = 640
FRAME_HEIGHT = 480

class TCP_Sock():
    def __init__(self, ip, port):
        self._SCK_SERVER_IP = ip
        self._SCK_SERVER_PORT = port

        self._capture = None
        self._WIDTH = FRAME_WITDH
        self._HEIGHT = FRAME_HEIGHT

    def tcp_connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self._SCK_SERVER_IP, self._SCK_SERVER_PORT))
            #self.sock.settimeout(20.0)
            self.sock.listen(1)
            print("연결대기")
            return self.sock
                 
        except socket.timeout:
            print("tcp timeout")
            data = None
            return data

        except KeyboardInterrupt:
            print("Keyboard Interrupt. socket close")
            self.sock.close()

        except Exception as e:
            print(e)
            raise
