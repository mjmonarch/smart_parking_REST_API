import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authentificate, identity
from resources.fact import Fact
from resources.user import UserRegister

from db import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:$ecretP2nda@192.168.0.112:5432/pi'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_C_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'mjmonarch'
api = Api(app)

jwt = JWT(app, authentificate, identity) # /auth

routes = ['/facts', '/facts/<string:vrp_no>']
api.add_resource(Fact, *routes)

api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
