import os
import random
import string
from flask import Blueprint, request, jsonify, send_file
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from config import allowed_file, db
from .model import User, ImageUpload
from .sh import UserSchema
from ..bet.model import Hall
from ..mail import send_password_reset_email, send_email_register
from flask_jwt_extended import get_jwt_identity, jwt_required

auth = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth.route('/login', methods=["POST"])
def login():
    try:
        user_data = UserSchema(only=('email', 'password')).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    email = user_data.get('email')
    password = user_data.get('password')

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and user.password_check_hash(password):
            access_token = user.create_token(user_id=user.id)
            return jsonify({"access_token": access_token, "user": user.id}), 200
    return jsonify(message="Invalid number, password, or role"), 401


def create_mathes():
    user_id = get_jwt_identity()
    data = request.get_json()
    errors = MatchCreateSchema(only=("name", 'start_math', "finish_math", "hall",)).validate(data)
    if errors:
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

    name = data['name']
    start_math_str = data['start_math']
    hall_ids = data.get('hall_ids', [])
    halls = Hall.query.filter(Hall.id.in_(hall_ids)).all()
    start_math = datetime.fromisoformat(start_math_str)
    finish_math = datetime.fromisoformat(data['finish_math'])
    math = Math(
        user_id=user_id,
        name=name,
        start_math=start_math,
        hall=halls,
        finish_math=finish_math
    )

    db.session.add(math)
    db.session.commit()

    return jsonify({"message": "Math created successfully", "math_id": math.id}), 201





@auth.route("/register/players", methods=["POST"])
def register_players():
    try:
        user_data = UserSchema(only=('email',)).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    email = user_data.get('email')

    if email:
        token = str(random.randint(10000000, 99999999))
        random_password = ''.join(random.choices(string.ascii_lowercase, k=8))
        pwd = User.password_hash(password=random_password)

        user = User(
            token=token,
            email=email,
            password=pwd,
        )

        send_email_register(user, random_password, token)

        if user:
            user.create_user(user)
            access_token = user.create_token(user_id=user.id)
            result = UserSchema().dump(user)

            return jsonify({"access_token": access_token, "user": user.id, "data": result}), 201

    return jsonify({"message": "Email is required"}), 400


@auth.route("/account", methods=["GET"])
@jwt_required()
def account():
    try:
        user_id = get_jwt_identity()
        if user_id is None:
            return jsonify(error='Неверные учетные данные'), 401

        user = User.query.get(user_id)
        if user is None:
            return jsonify(error='Пользователь не найден'), 404

        user_schema = UserSchema()
        return jsonify(user=user_schema.dump(user))
    except ValidationError:
        return jsonify(error='Неверный токен авторизации'), 401


@auth.route("/account/edit", methods=["PUT"])
@jwt_required()
def account_edit():
    user_id = get_jwt_identity()
    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify(error='Пользователь не найден'), 404

        # Update fields if provided in the request
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        number = request.form.get("number")
        tg_token = request.form.get('tg_token')
        age = request.form.get('age')
        card = request.form.get('card')

        # Update the user's fields
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if number:
            user.number = number
        if tg_token:
            user.tg_token = tg_token
        if card:
            user.card = card
        if age:
            user.age = age

        images = request.files.getlist('images')
        if images:
            image_uploads = []
            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    from app import app
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(file_path)

                    image_upload = ImageUpload(fileName=filename, file=file_path)
                    db.session.add(image_upload)
                    image_uploads.append(image_upload)

            user.image.extend(image_uploads)

        db.session.commit()

        return jsonify(message='Информация об аккаунте успешно обновлена.')
    else:
        return jsonify(error='Ошибка: Неверные учетные данные.')


@auth.route('/images/<fileName>', methods=['GET'])
def get_image(fileName):
    image_upload = ImageUpload.query.filter_by(fileName=fileName).first()
    if image_upload is None:
        return 'Файл не найден', 404
    from app import app
    image_path = os.path.join(app.root_path, "..", 'uploads', fileName)
    return send_file(image_path)

