#UDP 송수신
from model.sck_connect import udp_connect
import socket
import json

SCK_SERVER_IP = '192.168.0.244'
SCK_SERVER_PORT = 4141          
SCK_BUF = 2048

def get_lineprofiler_data():
    try:
        sck = udp_connect.UDP_Sock(SCK_SERVER_IP, SCK_SERVER_PORT, SCK_BUF)
        lpf_data = sck.get_socket_udp()
        print(lpf_data)
        
        #데이터 예시
        '''
        lpf_data = {
                    "msg_uuid" : "12345678-1234-5678-1234-567812345678",
                    "obj_id" : 1794,
                    "obj_type" : 20,
                    "obj_image" : "0000000000142.png", #실시간 X
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
        
        #json_data = json.dumps(lpf_data, ensure_ascii=False, indent="\t")
        #return json_data
        return lpf_data
    
    finally:
        ...#print("sen close....")
        


"""
#REST API 로 송수신
from flask import Flask
from flask import request
import json

from model.db.mysql_lib import DB_Handler

'''
app = Flask(__name__)
class pth_server:
    def __init__(self, dq):
        _dq = dq
        app.run(host='192.168.0.244', port=4141, debug=False)

    @app.route('/pth', methods = ['GET','POST'])
    def api():
        d = request.get_json(silent=True, force=True)
        print(d)
        return json.dumps(d)
'''

dbh = DB_Handler()
app = Flask(__name__)
def p_run():
    app.run(host='192.168.0.244', port=4141, debug=False)

@app.route('/pth', methods = ['GET','POST'])
def pth():
    print("dbn",dbh.select_last_id_gnss())
    d = request.get_json(silent=True, force=True)
    print(d)
    return json.dumps(d)

"""