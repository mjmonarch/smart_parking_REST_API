from flask import Flask
from flask_restful import Api

from resources.fact import Fact

app = Flask(__name__)
app.secret_key = 'mjmonarch'
api = Api(app)


routes = ['/facts', '/facts/<string:vrp_no>']
api.add_resource(Fact, *routes)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
