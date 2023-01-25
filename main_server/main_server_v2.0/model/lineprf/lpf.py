#UDP 송수신
from model.sck_connect import udp_connect
import socket

SCK_SERVER_IP = '192.168.0.244'
SCK_SERVER_PORT = 4040          
SCK_BUF = 2048

def get_lineprofiler_data():
    try:
        sck = udp_connect.UDP_Sock(SCK_SERVER_IP, SCK_SERVER_PORT, SCK_BUF)
        lpf_data = sck.get_socket_udp()
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