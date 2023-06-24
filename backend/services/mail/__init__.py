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