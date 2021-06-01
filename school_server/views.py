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


class SchoolList(Resource):
    def get(self):
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT 학교명 FROM school"
        cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_header, result)))
        conn.close()
        return Response(dumps({"school_list": json_data}), status=200, mimetype='application/json')


class SchoolDataAll(Resource):
    def get(self):
        school = request.args.get('school')
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        if school:
            sql = "SELECT * from school where 학교명 = '{}'".format(
                school)
            cursor.execute(sql)
        else:
            sql = "SELECT * from school"
            cursor.execute(sql)
        result_set = cursor.fetchall()
        row_header = [x[0] for x in cursor.description]
        json_data = []
        for result in result_set:
            json_data.append(dict(zip(row_header, result)))

        data = dumps({"school_data": json_data})
        conn.close()
        return Response(data, status=200, mimetype='application/json')


