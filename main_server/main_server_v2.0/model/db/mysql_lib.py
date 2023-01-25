#############################################################################

# TODO : ORM 지원가능 패키지로 변경, 순서도, configuration , 정보중의적ㅍ표현, 데이터플로우다이어그램, 전체프로그램 동작, 데이터명세서 + DB에들어있는 데이터 

import pymysql
import re
import time, datetime
#from db import configuration

#Connect DB, DB Handler : db_conn, curs
class DB_Handler:
    def __init__(self):
        self.db_conn, self.curs = self.connect_DB()

    def __del__(self):
        self.db_conn.close()
        self.curs.close()
        ...#print("DB Close....")
    
    #Connect DB (mysql dbdb)
    def connect_DB(self):
        #database connect
        self.db_conn = pymysql.connect(
            user = 'root',
            passwd = 'keti1234',
            host = '127.0.0.1',
            db = 'dbdb',
            charset = 'utf8'
        )
        if self.db_conn:
            print("Connected Successfully")
        else:
            ...#print("Connection Not Established")

        self.curs = self.db_conn.cursor()

        return self.db_conn, self.curs

    def select_last_id_imu(self): 
        sql = "select id from imu_tb ORDER BY id DESC LIMIT 1"
        self.curs.execute(sql)
        last_seq = self.curs.fetchone()  
        if(last_seq != None):
            return last_seq[0]
        else:
            return '0'

    def select_last_id_env(self):
        sql = "select id from env_tb ORDER BY id DESC LIMIT 1"
        self.curs.execute(sql)
        last_seq = self.curs.fetchone()  
        if(last_seq != None):
            return last_seq[0]
        else:
            return '0'

    def select_last_id_det(self):
        sql = "select id from det_tb ORDER BY id DESC LIMIT 1"
        self.curs.execute(sql)
        last_seq = self.curs.fetchone()  
        if(last_seq != None):
            return last_seq[0]
        else:
            return '0'

    def select_last_id_gnss(self): 
        sql = "select id from gnss_tb ORDER BY id DESC LIMIT 1"
        self.curs.execute(sql)
        last_id = self.curs.fetchone()  
        if(last_id != None):
            return str(last_id[0])
        else:
            ...#print("NOTHING")
            return '1'


    #############################################################################
    #선택한 센서값(JSON)의 마지막값 return 
    def select_gnss_seq_tb(self, data):
        sql = "SELECT "+data+" FROM gnss_tb ORDER BY seq DESC LIMIT 1"
        self.curs.execute(sql)
        row = self.curs.fetchone()
        if row is not None:
            return row
        else:
            print("no data")
            exit()

    def select_env_seq_tb(self, data):
        sql = "SELECT "+data+" FROM env_tb ORDER BY seq DESC LIMIT 1"
        self.curs.execute(sql)
        row = self.curs.fetchone()
        if row is not None:
            return row
        else:
            print("no data")
            exit()

    def select_imu_seq_tb(self, data):
        sql = "SELECT "+data+" FROM imu_tb ORDER BY seq DESC LIMIT 1"
        self.curs.execute(sql)
        row = self.curs.fetchone()
        if row is not None:
            return row
        else:
            print("no data")
            exit()

    def select_det_seq_tb(self, data):
        sql = "SELECT "+data+" FROM det_tb ORDER BY id DESC LIMIT 1"
        self.curs.execute(sql)
        row = self.curs.fetchone()
        if row is not None:
            return row
        else:
            print("no data")
            exit()



    #### INSERT
    #시간값 여기서 통합하는걸로 변경
    def insert_gnss_tb(self, data):
        sql = "INSERT INTO gnss_tb (gp_lat, gp_lon, speed, time_stamp)"\
            "VALUES('" + data[1] + "','" + data[2] + "','" + data[3] + "',now())"
        
        self.curs.execute(sql)
        self.db_conn.commit()
        print("gnss_tb Insert Success : ",data)

    def insert_env_tb(self, data, gnss_id):
        sql = "INSERT INTO env_tb (ev_lux, ev_temp, ev_hum, time_stamp, gnss_id)"\
            "VALUES('" + data[1] + "','" + data[2] + "','" + data[3] + "',now(),'" + gnss_id + "')"

        self.curs.execute(sql)
        self.db_conn.commit()
        print("env_tb Insert Success : ",data)

    def insert_imu_tb(self, data, gnss_id):
        sql = "INSERT INTO imu_tb (ev_imu_x, ev_imu_y, ev_imu_z, time_stamp, gnss_id)"\
            "VALUES('" + data[1] + "','" + data[2] + "','" + data[3] + "',now(),'" + gnss_id + "')"
        
        self.curs.execute(sql)
        self.db_conn.commit()
        print("imu_tb Insert Success : ",data)

    def insert_det_tb(self, data, gnss_id):
        print(data)
        re_txt = re.sub('[-:]','',str(time.time())).replace(' ','_')
        sql = "INSERT INTO det_tb (sign_name, sign_class, recog, x, y, w, h, frame,  img_path, time_stamp, gnss_id)"\
            "VALUES('" + data[1] + "','" + data[2] + "','" + data[3] + "','" + data[4] + "','" \
                + data[5] +"','" + data[6] + "','" + data[7] + "','" + data[8]+ "','" + "C:/_workspace/doro/_det/front_cam/"+re_txt+".jpg"\
                 + "',now(),'" + gnss_id +"')"
    
        self.curs.execute(sql)
        self.db_conn.commit()
        print("det_tb Insert Success : ",sql)

    def insert_road_tb(self, data, gnss_id):
        sql = "INSERT INTO road_tb (recv_num, rd_temp, rd_dewp, rd_hum, waterfilm_h, rd_status, rd_ice_per,  rd_fric, rd_status_str, battV, ptemp, time_stamp, gnss_id)"\
            "VALUES('" + data[1] + "','" + data[3] + "','" + data[4] + "','" + data[5] +"','" \
                + data[6] + "','" + data[7]+"','" + data[8]+"','" + data[9] + "','" + data[10] \
                    + "','" + data[11] + "','" + data[12] + "','" + "'now()'" + "','"  + gnss_id +"')"
        self.curs.execute(sql)
        self.db_conn.commit()
        print("road_tb Insert Success : ",data)
    
    def insert_road_tb(self, data, gnss_id):
        sql = "INSERT INTO road_tb (msg_uuid, obj_id, obj_type, obj_image, obj_time, size)"\
            "VALUES('" + data[1] + "','" + data[3] + "','" + data[4] + "','" + data[5] +"','" \
                + data[6] + "','" + data[7]+"','" + data[8]+"','" + data[9] + "','" + data[10] \
                    + "','" + data[11] + "','" + data[12] + "','" + "'now()'" + "','"  + gnss_id +"')"
        self.curs.execute(sql)
        self.db_conn.commit()
        print("road_tb Insert Success : ",data)

    def insert_pthole_tb(self, data, gnss_id):
        sql = "INSERT INTO pthole_tb (msg_uuid, obj_id, obj_type, obj_image, obj_time, pt_h_max, time_stamp, gnss_id)"\
            "VALUES('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] +"','" \
                + data[4] + "','" + data[5]+"','"  + "'now()'" + "','"  + gnss_id +"')"
        self.curs.execute(sql)
        self.db_conn.commit()
        print("pthole_tb Insert Success : ",data)

    def insert_pt_frame_tb(self, data, pth_id):
        sql = "INSERT INTO pt_frame_tb (pt_x, pt_w, pth_h_avg, pthole_id)"\
            "VALUES('" + data[0] + "','" + data[1] + "','" + data[2] + "','" + data[3] +"','" \
                + data[4] + "','" + data[5]+"','"  + "'now()'" + "','"  + pth_id +"')"
        self.curs.execute(sql)
        self.db_conn.commit()
        print("pthole_tb Insert Success : ",data)


    ### 검색 ###

    def search(self, lat_q="", lon_q=""):
        sql = \
        "SELECT \
            imu.ev_imu_x, imu.ev_imu_y,imu.ev_imu_z,\
            env.ev_lux, env.ev_temp, env.ev_hum, \
            det.sign_name, det.sign_class, det.recog, \
            gps.* \
        FROM gnss_tb gps \
            left outer join imu_tb imu on gps.id = imu.gnss_id \
            left outer join env_tb env on gps.id = env.gnss_id \
            left outer join det_tb det on gps.id = det.gnss_id \
        WHERE gp_lat LIKE '%"+str(lat_q)+"%' AND gp_lon LIKE '%"+str(lon_q)+"%'"

        self.curs.execute(sql)
        search_row = self.curs.fetchall()  
        #print(f"search result{search_row}")
        search_dict = {}
        if(search_row != None):
            for i,search_d in enumerate(search_row):
                #print("TTT",i,search_d)
                search_dict[i] = {
                    "latitude": search_d[10],
                    "longitude": search_d[11],
                    "acc_x":search_d[0],
                    "acc_y":search_d[1],
                    "acc_z":search_d[2],
                    "lux":search_d[3],
                    "temp":search_d[4],
                    "humi":search_d[5],
                    "sign_name":search_d[6],
                    "sign_class":search_d[7],
                    "recog":search_d[8]
                }
            #print(search_dict)
            return search_dict
        else:
            print("NOTHING")
            return None
        ...

    def sql_insert(self, sql):
        print("SQL : ",sql)
        self.curs.execute(sql)
        row = self.curs.fetchall()
        if row is not None:
            return row
        else:
            print("no data")
            return None
    

















































"""
try:
    db_conn = pymysql.connect(
        user = 'keti',
        passwd = '1234',
        host = '127.0.0.1',
        db = 'dbdb',
        charset = 'utf8'
    )

    if db_conn:
        print("Connected Successfully")
    else:
        print(" Connection Not Established")

    #curs = db_conn.cursor()
    #insert_tb(db_conn, curs, val)
    #sql_sort_seq(curs)
    #select_tb(curs)

finally:
    db_conn.close()

"""
#val = (json.dumps(sensor_data1))

"""
sql ="CREATE TABLE IF NOT EXISTS data_tb(\
    seq			INT NOT NULL AUTO_INCREMENT,\
    lux         VARCHAR(10),\
    temp		VARCHAR(10),\
    humidity	VARCHAR(10),\
    g_x			VARCHAR(10),\
    g_y			VARCHAR(10),\
    g_z			VARCHAR(10),\
    t			datetime,\
    PRIMARY KEY (seq)\
    )ENGINE=MyISAM CHARSET=utf8;"
"""
#sql = 'INSERT INTO data_tb(lux, temp, humidity, g_x, g_y, g_z, t)'\
#    'VALUES (%s, %s, %s, %s, %s, %s, now())'
#curs.execute(sql, ('11.11', '22.11', '33.11', '44.11', '55.11', '66.11'))
#curs.execute(sql, ('11.22', '22.22', '33.22', '44.22', '55.22', '66.22'))
#curs.execute(sql, ('11.33', '22.33', '33.33', '44.33', '55.33', '66.33'))

"""
def insert_tb(db_conn, curs, val):
    #db에서 json 형식은 글자수가 적은수대로 sorting 되서 들어가게된다. ex) g_x, g_y, g_z, lux, temp, humidty 순서 
    sql = "INSERT INTO data_tb(sensor_data, t)"\
        "VALUES('" + val + "',now(3))"
    print("str ::: ", str(sql))
    curs.execute(sql)
    db_conn.commit()
    print("SUCCESS")

"""

"""
temp_sensor_data = {
    "id" : "real_time",
    "device" : "env_sensor",
    "origin" : "timestamp",
    "runtime" : "runtime",
    "readings" : {
        "device" : "UA10",
        "name" : "temp",
        "value" : "11.11",
        "valueType" : "float"
    }
}
humi_sensor_data = {
   
    "device" : "UA10",
    "name" : "humidity",
    "value" : "22.11",
    "valueType" : "float"
    
"""