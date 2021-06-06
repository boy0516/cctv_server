from views import app
from flask import Flask
from flask_restful import Api
import views


app.run(debug=True, host='0.0.0.0', port=15003)
