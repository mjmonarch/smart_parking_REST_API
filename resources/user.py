import base64

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Mandatory parameter: username"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Mandatory parameter: password"
    )

    @jwt_required()
    def post(self):
        username = current_identity.username

        if username != 'admin':
             return {'message': 'Only admin can create new users.'}, 401

        data = UserRegister.parser.parse_args()

        #check whether user already exists
        if UserModel.find_by_username(data['username']):
            return {'message': 'User already exists.'}, 400

        user = UserModel(data['username'], base64.b64encode(data['password'].encode("utf-8")))
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201