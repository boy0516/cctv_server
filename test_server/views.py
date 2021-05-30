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

# cctvdb api 호출

def get_cctv_list():
    # cctv 목록 가져오기
    try:
        cctv_list_res = requests.get(cctv_server_host+"chart")
        if cctv_list_res.status_code == 200:
            return cctv_list_res.json()['cctv_list']
    except:
        return []


def get_cctv_logs_all(cctv):
    # cctv log 가져오기
    print(cctv)
    print(type(cctv))
    if cctv:
        try:
            cctv_log_res = requests.get(cctv_server_host+"log/all?cctv="+cctv)
            if cctv_log_res.status_code == 200:
                return cctv_log_res.json()
        except:
            return []
    else:
        try:
            cctv_log_res = requests.get(cctv_server_host+"log/all")
            if cctv_log_res.status_code == 200:
                return cctv_log_res.json()
        except:
            return []

# db사용


def get_cctv_logs_month(dbjson):
    json_data = []
    log_count = 0
    for db_log in dbjson:
        if datetime.datetime.now().strftime('%m') == db_log["log_time"][5:7]:
            json_data.append(db_log)
            log_count += 1
    return {"cctv_logs": json_data, "log_count": log_count}


def get_cctv_logs_day(dbjson):
    json_data = []
    log_count = 0
    for db_log in dbjson:
        if datetime.datetime.now().strftime('%m-%d') == db_log["log_time"][5:10]:
            json_data.append(db_log)
            log_count += 1
    return {"cctv_logs": json_data, "log_count": log_count}


def get_cctv_logs_week(dbjson):
    week_count = [0]*7
    for db_log in dbjson:
        week_count[datetime.datetime.strptime(
            db_log["log_time"], '%Y-%m-%d %H:%M:%S').weekday()] += 1

    return {"log_count": week_count}


@app.route('/')
def main_page():
    cctv = None
    
    values = {
        "cctv_server_host":cctv_server_host,
        "school": ""
        }

    return render_template('index.html', values=values)


@app.route('/school_detail')
def school_detail():
    school = request.args.get('school')
    
    values = {
        "cctv_server_host":cctv_server_host,
        "school": school
    }

    return render_template('school_detail.html', values=values)


@app.route('/streaming')
def streaming():
    cctv = request.args.get('cctv')

    values = {
        "cctv_name": cctv
    }

    return render_template('streaming.html', values=values)


@app.route('/cctvmap')
def cctvmap():
    cctv = request.args.get('cctv')

    values = {
        "cctv_name": cctv,
        "cctv_list": get_cctv_list()
    }

    return render_template('cctvmap.html', values=values)


@app.route('/cctvpost')
def cctvpost():
    cctv = request.args.get('cctv')

    values = {
        "cctv_name": cctv
    }

    return render_template('cctvpost.html', values=values)


@app.route('/postdetail')
def postdetail():
    url = request.args.get('url')

    values = {
        "url": url
    }

    return render_template('postdetail.html', values=values)

@app.route('/first_map')
def first_map():

    return render_template('first_map.html')