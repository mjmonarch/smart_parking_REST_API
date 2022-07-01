import os

from flask import Flask
from flask_restful import Api

from resources.fact import Fact

from db import db

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pi:$ecretP2nda@192.168.0.112:5432/pi'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mjmonarch'
api = Api(app)


routes = ['/facts', '/facts/<string:vrp_no>']
api.add_resource(Fact, *routes)


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
