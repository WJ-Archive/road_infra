import requests
import json
def req_test():
    data = {
        "key1":"kkkttt",
        "key2":"test2",
        "to":"wj"
    }
    #d = json.dumps(data)
    #response = requests.get("http://192.168.0.244:4141/api/test",params=d)
    #response = requests.post("http://192.168.0.244:4141/api/test",data=d) #json 으로만 받을수 있음
    #response = requests.post("http://192.168.0.244:4141/api/test",json=data)
    response = requests.post("http://192.168.0.244:4141/pth",json=data)
    print(response)

req_test()