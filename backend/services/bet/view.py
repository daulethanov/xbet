import random
import string
from datetime import datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from sqlalchemy import func

from config import db
from services.bet.sh import HallSchema, MathSchema, CommandSchema, MatchCreateSchema, MatchSchemaView
from services.bet.model import Hall, Math, Command
from services.client.model import User
from services.client.sh import UserSchema
from services.mail import send_notification_email, send_invitation_notification, send_mail

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
    current_user_id = get_jwt_identity()
    user_schema = UserSchema()

    try:
        command_data = CommandSchema().load(request.json)
        command_name = command_data['name']

        command = Command.query.filter_by(name=command_name).first()
        if not command:
            return jsonify(error=f"Command '{command_name}' does not exist."), 404

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

        db.session.commit()

        return jsonify(message='Пользователи добавлены в команду успешно.'), 200
    except ValidationError as e:
        return jsonify(error=e.messages), 400


@bet.route("/math/create/first", methods=["POST"])
@jwt_required()
def create_mathes():
    user_id = get_jwt_identity()
    data = request.get_json()
    errors = MatchSchemaView().validate(data)
    if errors:
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

    name = data['name']
    active_math=data['active_math']
    hall_ids = data.get('hall_ids', [])
    halls = Hall.query.filter(Hall.id.in_(hall_ids)).all()

    math = Math(
        user_id=user_id,
        name=name,
        active_math=active_math,
        start_math=datetime.now(),
        hall=halls,
    )

    db.session.add(math)
    db.session.commit()

    return jsonify({"message": "Math created successfully", "math_id": math.id}), 201


@bet.route('/math/create/<int:id>', methods=["PUT"])
def update_math(id):
    data = request.get_json()

    errors = MatchCreateSchema().validate(data)
    if errors:
        return jsonify({"message": "Invalid request data", "errors": errors}), 400

    command1_id = data['command1_id']
    command2_id = data['command2_id']

    hall_ids = data.get('hall_ids', [])
    halls = Hall.query.filter(Hall.id.in_(hall_ids)).all()
    command1 = Command.query.get(command1_id)
    command2 = Command.query.get(command2_id)

    if not command1 or not command2:
        return jsonify({"message": "Invalid command1_id or command2_id"}), 404

    math = Math.query.get(id)
    if not math:
        return jsonify({"message": "Invalid math_id"}), 404

    total_price = sum(hall.total_price for hall in halls)
    participants_count = (
        db.session.query(func.count(func.distinct(User.id)))
        .filter(User.id.in_(user.id for user in command1.users))
        .scalar()
        + db.session.query(func.count(func.distinct(User.id)))
        .filter(User.id.in_(user.id for user in command2.users))
        .scalar()
    )
    if participants_count > 0:
        total_price_per_participant = total_price / participants_count
    else:
        total_price_per_participant = 0

    math.command1 = command1
    math.command2 = command2
    math.hall = halls
    math.price = total_price

    db.session.commit()
    divided_number = total_price_per_participant / participants_count

    for user in command1.users:
        if user.active_math:
            user.coin -= divided_number
            send_mail(user.email, "Матч", f"{math.name}, Дата начала: {math.start_math}, Счет за оплату в размере "
                                          f"{divided_number}\n У вас списалось {divided_number}\n"
                                          f"Остаток на счету {user.coin}")

    for user in command2.users:
        if user.active_math:
            user.coin -= divided_number
            send_mail(user.email, "Матч", f"{math.name}, Дата начала: {math.start_math}, Счет за оплату в размере "
                                          f"{divided_number}\n У вас списалось {divided_number}\n"
                                          f"Остаток на счету {user.coin}")

    return jsonify({"message": "Math updated successfully", "math_id": math.id}), 200


@bet.route('/math/<int:math_id>/cancel', methods=["POST"])
def cancel_math(math_id):
    math = Math.query.get(math_id)
    if not math:
        return jsonify({"message": "Math not found"}), 404

    if math.active_math:
        math.active_math = False
        db.session.commit()

        total_winning_users = len(math.audience)
        if total_winning_users > 0:
            share_amount = math.price / total_winning_users
            for winning_user in math.audience:
                winning_user.coin += share_amount
            db.session.commit()

        return jsonify({"message": "Math canceled successfully"}), 200
    else:
        return jsonify({"message": "Math is already canceled"}), 400


@bet.route('/math/<int:id>/place_bet', methods=["POST"])
@jwt_required()
def place_bet(id):
    user_id = get_jwt_identity()
    data = request.get_json()

    selected_command = data['command']
    bet_amount = data.get('bet_amount')  # Retrieve the bet_amount field from the JSON data

    if bet_amount is None:
        return jsonify({"message": "bet_amount field is missing"}), 400

    math = Math.query.get(id)
    user = User.query.filter_by(id=user_id).first()

    if user in math.audience or user in math.command1.users or user in math.command2.users:
        if selected_command == 1:
            if math.command1 is not None:
                command = math.command1
                math.command1_bet = (math.command1_bet or 0) + bet_amount
            else:
                return jsonify({"message": "Command 1 is not available for this match"}), 400
        elif selected_command == 2:
            if math.command2 is not None:
                command = math.command2
                math.command2_bet = (math.command2_bet or 0) + bet_amount
            else:
                return jsonify({"message": "Command 2 is not available for this match"}), 400
        else:
            return jsonify({"message": "Invalid command selection"}), 400

        if user.coin >= bet_amount:
            user.coin -= bet_amount
            db.session.add(user)  # Add the user to the session for updating the coin value
            db.session.commit()

            return jsonify({"message": "Bet placed successfully", "new_coin_balance": user.coin}), 200
        else:
            return jsonify({"message": "Insufficient balance"}), 400
    else:
        return jsonify({"message": "Unauthorized to place bets for this match"}), 403


@bet.route('/confirm/<email>', methods=["GET"])
def confirm_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        user.active_math = True
        db.session.commit()
        return "Email verification successful. You can now log in."
    return "Email verification failed. Invalid email or user not found."


@bet.route('/math/<int:id>/end_match', methods=["POST"])
def end_match(id):
    math = Math.query.get(id)

    if math.closed_match:
        return jsonify({"message": "Match has already been closed"}), 400

    # current_time = datetime.now()
    # if current_time < math.finish_math:
    #     return jsonify({"message": "Match has not finished yet"}), 400

    if math.command1_goal > math.command2_goal:
        winning_command = math.command1
    elif math.command2_goal > math.command1_goal:
        winning_command = math.command2
    else:
        return handle_draw(math)

    total_bet_amount = math.command1_bet + math.command2_bet

    winning_users = winning_command.audience.all()
    total_winning_users = len(winning_users)

    if total_winning_users > 0:
        share_amount = total_bet_amount / total_winning_users
        for winning_user in winning_users:
            winning_user.coin += share_amount

    math.active_math = False
    db.session.commit()

    return jsonify({"message": "Match ended successfully"}), 200


def handle_draw(math):
    command1_users = math.command1.audience.all()
    command2_users = math.command2.audience.all()

    for user in command1_users:
        user.coin += math.command1_bet

    for user in command2_users:
        user.coin += math.command2_bet

    total_bet_amount = math.command1_bet + math.command2_bet

    math.closed_match = True
    db.session.commit()

    return jsonify({"message": "Match ended in a draw. Bet amount returned to all users."}), 200

@bet.route('/math/<int:id>/add_goal', methods=["POST"])
def add_goal(id):
    math = Math.query.get(id)
    data = request.get_json()
    goal = data.get('goal')
    command_id = data.get('command_id')

    if not command_id:
        return jsonify({"message": "Invalid data provided"}), 400

    if command_id == 1:
        if math.command1_goal is None:
            math.command1_goal = 0
        math.command1_goal += goal
    elif command_id == 2:
        if math.command2_goal is None:
            math.command2_goal = 0
        math.command2_goal += goal
    else:
        return jsonify({"message": "Invalid command ID"}), 400

    db.session.commit()

    return jsonify({"message": "Goal added successfully"}), 200
