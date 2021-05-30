from json import dumps, loads
from flask import Response, jsonify, request, wrappers
from flask_restful import Resource, Api
from flask_jwt_extended import *
import pymysql
import datetime
import consul
import time
import threading


c = consul.Consul(host='34.199.237.253', port=8500)
index = None

index, data = c.kv.get('db_config', index=index)
db_config = loads(data['Value'])


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

# cctv 목록 조회 API


class CctvList(Resource):
    def get(self):
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT *" \
              "FROM cctv "
        cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_header, result)))
        conn.close()
        return Response(dumps({"cctv_list": json_data}), status=200, mimetype='application/json')


class CctvLogAll(Resource):
    def get(self):
        cctv = request.args.get('cctv')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if cctv:
            sql = "SELECT * from cctvlog where cctvname = '{}'".format(
                cctv)
            cursor.execute(sql)
        else:
            sql = "SELECT * from cctvlog"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_header, result)))

        data = dumps({"cctv_logs": json_data},
                     default=myconverter)
        conn.close()
        return Response(data, status=200, mimetype='application/json')


class CctvLogMonth(Resource):
    def get(self):
        cctv = request.args.get('cctv')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if cctv:
            sql = "SELECT * from cctvlog where (cctvname = '{}') AND (date_format(log_time, '%m') = date_format(now(), '%m'))".format(cctv)
            cursor.execute(sql)
        else:
            sql = "SELECT * from cctvlog where date_format(log_time, '%m') = date_format(now(), '%m')"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        log_count = 0
        for result in result_set:
            log_count += 1
            json_data.append(dict(zip(row_header, result)))

        data = dumps({"cctv_logs": json_data, "log_count": log_count},
                     default=myconverter)
        conn.close()
        return Response(data, status=200, mimetype='application/json')


class CctvLogDay(Resource):
    def get(self):
        cctv = request.args.get('cctv')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if cctv:
            sql = "SELECT * from cctvlog where (cctvname = '{}') AND (date_format(log_time, '%d') = date_format(now(), '%d'))".format(cctv)
            cursor.execute(sql)
        else:
            sql = "SELECT * from cctvlog where date_format(log_time, '%d') = date_format(now(), '%d')"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        log_count = 0
        for result in result_set:
            log_count += 1
            json_data.append(dict(zip(row_header, result)))

        data = dumps({"cctv_logs": json_data, "log_count": log_count},
                     default=myconverter)
        conn.close()
        return Response(data, status=200, mimetype='application/json')


class CctvLogWeek(Resource):
    def get(self):
        cctv = request.args.get('cctv')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if cctv:
            sql = "SELECT log_time from cctvlog where (cctvname = '{}') AND (DATE(log_time) >= DATE_SUB(NOW(), INTERVAL 6 DAY))".format(
                cctv)
            cursor.execute(sql)
        else:
            sql = "SELECT log_time from cctvlog where DATE(log_time) >= DATE_SUB(NOW(), INTERVAL 6 DAY)"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        week_count = [0]*7
        for result in result_set:
            week_count[result[0].weekday()] += 1

        data = dumps({"log_week": week_count})
        conn.close()
        return Response(data, status=200, mimetype='application/json')


class CctvLogCount(Resource):
    def get(self):
        cctv = request.args.get('cctv')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if cctv:
            sql = "SELECT * from cctvlog where (cctvname = '{}') AND (date_format(log_time, '%m') = date_format(now(), '%m'))".format(cctv)
            cursor.execute(sql)
        else:
            sql = "SELECT * from cctvlog where date_format(log_time, '%m') = date_format(now(), '%m')"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        log_count = 0
        for result in result_set:
            log_count += 1
            json_data.append(dict(zip(row_header, result)))

        assault = 0
        smoke = 0

        for logs in json_data:
            if logs['situation'] == 'assault':
                assault += 1
            if logs['situation'] == 'smoke':
                smoke += 1
        

        data = dumps({"assault": assault, "smoke": smoke},
                     default=myconverter)
        conn.close()
        return Response(data, status=200, mimetype='application/json')
        
        
