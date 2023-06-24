import random
import string
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from config import db
from services.bet.sh import HallSchema, MathSchema, CommandSchema, MatchCreateSchema
from services.bet.model import Hall, Math, Command
from services.client.model import User
from services.client.sh import UserSchema
from services.mail import send_notification_email, send_invitation_notification

bet = Blueprint('bet', __name__, url_prefix="/api/bet")


@bet.route('/hall/list', methods=["GET"])
def hall_list():
    hall = Hall.query.all()
    hall_data = HallSchema(many=True).dump(hall)
    return jsonify(hall_data)


@bet.route('/hall/<int:id>', methods=["GET"])
def get_hall(id):
    hall = Hall.query.get(id)
    if hall:
        hall_data = HallSchema().dump(hall)
        return jsonify(hall_data)
    else:
        return jsonify({"message": "Hall not found"}), 404


@bet.route('/math/list', methods=["GET"])
def math_list():
    math = Math.query.all()
    math_data = MathSchema(many=True).dump(math)
    return jsonify(math_data)


@bet.route('/math/<int:id>', methods=["GET"])
def get_math(id):
    math = Math.query.get(id)
    if math:
        math_data = MathSchema().dump(math)
        return jsonify(math_data)
    else:
        return jsonify({"message": "Math not found"}), 404


@bet.route('/command/list', methods=["GET"])
def command_list():
    command = Command.query.all()
    command_data = CommandSchema(many=True).dump(command)
    return jsonify(command_data)


@bet.route('/command/<int:id>', methods=["GET"])
def get_command(id):
    command = Command.query.get(id)
    if command:
        command_data = CommandSchema().dump(command)
        return jsonify(command_data)
    else:
        return jsonify({"message": "Command not found"}), 404


@bet.route('/command/create', methods=["POST"])
@jwt_required()
def create_command():
    current_user_id = get_jwt_identity().get("id")
    user_schema = UserSchema()

    try:
        command_data = CommandSchema().load(request.json)
        command = Command(name=command_data['name'])

        users = command_data.get("users")
        if users:
            for user in users:
                email = user.get("email")
                if email:
                    try:
                        user_data = user_schema.load({'email': email})
                        existing_user = User.query.filter_by(email=user_data['email']).first()
                        if existing_user:
                            command.users.append(existing_user)
                            send_invitation_notification(existing_user.email, command.name)
                        else:
                            random_password = ''.join(random.choices(string.ascii_lowercase, k=8))
                            new_user = User(email=user_data['email'], password=random_password)
                            command.users.append(new_user)
                            send_invitation_notification(new_user.email, command.name)
                            db.session.add(new_user)

                    except ValidationError as e:
                        return jsonify(error='Ошибка: Некорректный адрес электронной почты.'), 400

        db.session.add(command)
        db.session.commit()

        return jsonify(message='Команда создана успешно.'), 200
    except ValidationError as e:
        return jsonify(error=e.messages), 400

@bet.route('/math/create', methods=["POST"])
def create_math():
    data = request.get_json()

    errors = MatchCreateSchema().validate(data)
    if errors:
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

    name = data['name']
    kind_of_sport = data['kind_of_sport']
    description = data.get('description')
    start_math_str = data['start_math']
    command1_id = data['command1_id']
    command2_id = data['command2_id']

    start_math = datetime.fromisoformat(start_math_str)

    command1 = Command.query.get(command1_id)
    command2 = Command.query.get(command2_id)

    if not command1 or not command2:
        return jsonify({"message": "Invalid command1_id or command2_id"}), 404

    math = Math(
        name=name,
        kind_of_sport=kind_of_sport,
        description=description,
        start_math=start_math,
        command1=command1,
        command2=command2
    )

    db.session.add(math)
    db.session.commit()

    return jsonify({"message": "Math created successfully", "math_id": math.id}), 201


@bet.route('/confirm/<email>', methods=["GET"])
def confirm_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.email_verified = True
        db.session.commit()
        return "Email verification successful. You can now log in."

    return "Email verification failed. Invalid email or user not found."





