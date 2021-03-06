from app import app
from flask import render_template, request, jsonify

import requests
import json

BASE_URL = "http://127.0.0.1:6500/"

@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = {
            'username':request.form['username'],
            'password':request.form['password']
        }
        headers = {'content-type':'application/json'}
        res = requests.post(BASE_URL+'/user', data=json.dumps(data), headers=headers)
        print(res.json())
        return res.json()
    return render_template("index.html")

@app.route("/current_user", methods=['POST', 'GET'])
def get_current_user():
    res = requests.get(BASE_URL+'/user')
    print(res.json())
    return res.json()