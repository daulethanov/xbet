import os
import random
import string
from flask import Blueprint, request, jsonify, send_file
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from config import allowed_file, db
from .model import User, ImageUpload
from .sh import UserSchema
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
            access_token = user.create_token(identity=user.id, id=user.id)
            return jsonify({"access_token": access_token, "user": user.id}), 200
    return jsonify(message="Invalid number, password, or role"), 401


@auth.route("/register", methods=["POST"])
def register():
    try:
        user_data = UserSchema(only=('email', 'password', 'full_name')).load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    pwd = User.password_hash(password=user_data['password'])

    user = User(
        email=user_data['email'],
        full_name=user_data['full_name'],
        password=pwd
    )

    if user:
        access_token = user.create_token(identity=user.id, id=user.id)
        user.create_user(user)
        code = "Вы зарегистрированы"
        send_password_reset_email(user, code)
        result = UserSchema().dump(user)
        return jsonify({"access_token": access_token, "user": user.id, "data": result}), 201


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
            access_token = user.create_token(identity=user.id, id=user.id)
            user.create_user(user)

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

