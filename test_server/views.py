from json import dumps, loads
from flask import Response, jsonify, request, render_template, redirect, url_for, make_response
import requests
from __init__ import app
import pymysql
import datetime
import consul


c = consul.Consul(host='34.199.237.253', port=8500)
index = None

index, data = c.kv.get('cctv_server_host', index=index)
cctv_server_host = loads(data['Value'])["cctv_server_host"]

index = None
index, data = c.kv.get('school_server_host', index=index)
school_server_host = loads(data['Value'])["school_server_host"]

index = None
index, data = c.kv.get('kakaokey', index=index)
kakaokey = loads(data['Value'])["kakaokey"]



@app.route('/')
def main_page():
    cctv = None
    
    values = {
        "cctv_server_host":cctv_server_host,
        "school_server_host":school_server_host,
        "school": ""
        }

    return render_template('index.html', values=values)


@app.route('/school_detail')
def school_detail():
    school = request.args.get('school')
    
    values = {
        "cctv_server_host":cctv_server_host,
        "school_server_host":school_server_host,
        "school": school,
        "kakaokey":kakaokey
    }

    return render_template('school_detail.html', values=values)

