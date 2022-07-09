import base64

from app import app
from db import db
from models.user import UserModel

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all(app=app)

    admin = UserModel('admin', 'strong_password')
    db.session.add(admin)
    db.session.commit()

    
