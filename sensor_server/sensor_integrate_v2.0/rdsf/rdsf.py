#road_surface (Marwis)

#DATA Logger : Socket Server , odyssey : Socket_client
#request url   python request to this url & parsing,,, (rest api communication)
#http://169.254.67.85/tables.html?command=DataQuery&mode=most-recent&format=json&uri=dl:marwis&p1=25
#http://169.254.67.85/tables.html
#https://www.campbellsci.in/forum?forum=1&l=thread&tid=16477
#MARWIS_IP = '169.254.67.85'
#MARWIS_PORT = 6785

import requests
def marwis_data_parsing(js_data):
    mws_data = list(js_data.values())
    return mws_data
    ...

def marwis_requests():
    #response = requests.get("http://169.254.67.85/tables.html?command=DataQuery&mode=most-recent&format=json&uri=dl:marwis&p1=25")
    response = requests.get("http://192.168.0.100/tables.html?command=DataQuery&mode=most-recent&format=json&uri=dl:marwis&p1=25")
    return marwis_data_parsing(response.json()['data'][-1])
    
"""
pre_data = 0
data = 1

while(1):
    data = marwis_requests()
    if(pre_data != data):
        print(data)
        pre_data = data
"""
    #print(response.json())
    #print(response.json()['head']['fields'][1])
    #print(response.json()['head']['fields'][2]['name'] , response.json()['head']['fields'][2]['type'])
    #print(response.json()['head']['fields'][3]['name'] , response.json()['head']['fields'][3]['type'])
    #print(response.json()['head']['fields'][4]['name'] , response.json()['head']['fields'][4]['type'])
    #print(response.json()['head']['fields'][5]['name'] , response.json()['head']['fields'][5]['type'])
    #print(response.json()['head']['fields'][6]['name'] , response.json()['head']['fields'][6]['type'])
    #print(response.json()['head']['fields'][7]['name'] , response.json()['head']['fields'][7]['type'])
    #print(response.json()['head']['fields'][8]['name'] , response.json()['head']['fields'][8]['type'])
    #print(response.json()['head']['fields'][9]['name'] , response.json()['head']['fields'][9]['type'])
    #print(response.json()['data'][-1])