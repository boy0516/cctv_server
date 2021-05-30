from flask import Flask
from flask_restful import Api
from flask_jwt_extended import *
from flask_cors import CORS
from json import loads
import views
import pymysql
import consul
import time

app = Flask(__name__)

api = Api(app)
CORS(app)

cctv = '/cctv'
api.add_resource(views.CctvList, cctv + '/chart')  # cctv 위치 이름 정보 API
api.add_resource(views.CctvLogAll, cctv + '/log/all')
api.add_resource(views.CctvLogMonth, cctv + '/log/month')  # cctv 위치 이름 정보 API
api.add_resource(views.CctvLogDay, cctv + '/log/day')
api.add_resource(views.CctvLogWeek, cctv + '/log/week')  # cctv 위치 이름 정보 API
api.add_resource(views.CctvLogCount, cctv + '/log/count')


app.run(debug=True, host='0.0.0.0', port=15001)
