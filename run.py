import base64

from app import app
from db import db
from models.user import UserModel

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all(app=app)

    admin = UserModel('admin', b'c3Ryb25nX3Bhc3N3b3Jk')
    db.session.add(admin)
    db.session.commit()