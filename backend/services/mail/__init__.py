from urllib.parse import urljoin

from flask import current_app
from flask_mail import Message, Mail

mail = Mail()


def send_password_reset_email(user, codes):
    code = str(codes)
    msg = Message(subject='OSI.HElP УВЕДОМЛЕНИЕ О РЕГИСТРАЦИИ',
                  sender='OSI.HELP',
                  recipients=[user.email],
                  body=f'''Уведомление о  регистрации {code} ''')
    mail.send(msg)


def send_email_register(user, random_password, token):
    msg = Message(subject='OSI.HElP УВЕДОМЛЕНИЕ О РЕГИСТРАЦИИ',
                  sender='OSI.HELP',
                  recipients=[user.email],
                  body=f'''Уведомление о регистрации, ваш пароль: {random_password}. Быстрый код для досупа в систему 
{token}''')
    mail.send(msg)


def send_notification_email(email, random_password, code):
    msg = Message(subject='OSI.HElP УВЕДОМЛЕНИЕ О РЕГИСТРАЦИИ',
                  sender='OSI.HELP',
                  recipients=[email],
                  body=f'''Ваш логин {email}. Уведомление о регистрации, ваш пароль: {random_password}. Быстрый код для доступа в систему: {code}.''')
    mail.send(msg)


def send_invitation_notification(email, command_name):
    confirmation_link = generate_confirmation_link(email)  # Сгенерировать уникальную ссылку для подтверждения

    # Составить сообщение электронной почты
    subject = "Приглашение присоединиться к команде"
    body = f"Вас пригласили присоединиться к команде: {command_name}.\n" \
           f"Пожалуйста, перейдите по следующей ссылке, чтобы принять или отклонить приглашение:\n" \
           f"{confirmation_link}\n" \
           f"Дата начала матча: \n"\
           f"Если не хотите участвовать не переходите по ссылке"

    mail = current_app.extensions.get('mail')
    message = Message(subject=subject, body=body, recipients=[email])
    mail.send(message)


def send_mail(email, command_name, match_start_date):
    confirmation_link = generate_confirmation_link(email)  # Generate a unique confirmation link

    # Compose the email message
    subject = "Оплата"
    body = f"Ваш счет за игру {command_name}.\n" \
           f"Пожалуйста, перейдите по следующей ссылке, чтобы принять или отклонить приглашение:\n" \
           f"Дата начала матча: {match_start_date}\n" \
           f"Ссылка для подтверждения: {confirmation_link}"

    # Send the email notification
    msg = Message(subject=subject, body=body, recipients=[email])
    mail.send(msg)


def generate_confirmation_link(email):
    base_url = "http://0.0.0.0:5000"
    confirmation_url = urljoin(base_url, f"/api/bet/confirm/{email}")
    return confirmation_url



