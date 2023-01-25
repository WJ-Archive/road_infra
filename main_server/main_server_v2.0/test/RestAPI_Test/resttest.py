from flask import Flask
from flask import request
import json

app = Flask(__name__)

@app.route('/api/<params>', methods=['GET','POST']) 
def api(params):
    print("params : ",params)
    d = request.get_json(silent=True, force=True)
    #d = request.json
    print("d : ",d)
    k = d['key1']
    print("key1 ",k)
    d = {"text": "Hello {}".format(k)}
    print(d)
    return json.dumps(d)

if __name__ == "__main__":
    app.run(host='192.168.0.244', port=4141, debug=True)