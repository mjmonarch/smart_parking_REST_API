import hmac
import base64
from models.user import UserModel

def authentificate(username, password):
    user = UserModel.find_by_username(username)
    _password = base64.b64decode(user.password).decode("utf-8")
    if user and hmac.compare_digest(_password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)