import socket

class UDP_Sock:
    def __init__(self, ip, port, buf):

        self._SCK_SERVER_IP = ip
        self._SCK_SERVER_PORT = port
        self._SCK_BUF = buf
        self.data = ''
        self.udp_connect()

    def udp_connect(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sck.settimeout(10.0)
        self.sck.bind((self._SCK_SERVER_IP,  self._SCK_SERVER_PORT))
        
    def get_socket_udp(self):
        try:
            data, addr = self.sck.recvfrom(self._SCK_BUF)
            data = data.decode()
        except socket.timeout:
            data = None

        return data