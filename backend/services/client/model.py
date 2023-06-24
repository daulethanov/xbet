from datetime import datetime
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from config import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String())
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    tg_token = db.Column(db.String(), unique=True)
    token = db.Column(db.String())
    active = db.Column(db.Boolean(), default=1)
    active_math = db.Column(db.Boolean(), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    number = db.Column(db.String())
    coin = db.Column(db.Integer(), default=999999)
    image = db.relationship('ImageUpload', backref='user')
    code_password = db.Column(db.String())
    capitan = db.Column(db.Boolean(), default=False)
    card = db.Column(db.String())
    age = db.Column(db.Integer())

    def __repr__(self):
        return self.email

    def password_hash(password):
        return generate_password_hash(password)

    def password_check_hash(self, password):
        return check_password_hash(self.password, password)

    def create_user(self, user):
        db.session.add(user)
        db.session.commit()

    def create_token(self, user_id):
        additional_claims = {'user_id': user_id}
        access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
        return access_token


class ImageUpload(db.Model):
    __tablename__ = 'image_upload'
    id = db.Column(db.Integer(), primary_key=True)
    fileName = db.Column(db.String())
    file = db.Column(db.String(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    hall_id = db.Column(db.Integer(), db.ForeignKey('hall.id'))

    def __repr__(self):
        return self.file
