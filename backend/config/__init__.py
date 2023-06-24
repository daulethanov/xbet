from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_security import Security
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
cors = CORS(resources={r"*": {"origins": "*"}})
security = Security()
jwt = JWTManager()
admin = Admin(url="/api/admin")


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif',"PNG"}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS