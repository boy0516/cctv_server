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

school = '/school'
api.add_resource(views.SchoolList, school + '/chart')  # cctv 위치 이름 정보 API
api.add_resource(views.SchoolDataAll, school + '/data')



app.run(debug=True, host='0.0.0.0', port=15002)
