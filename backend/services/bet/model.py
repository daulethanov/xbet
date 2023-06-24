from datetime import datetime
from config import db


class Hall(db.Model):
    __tablename__ = "hall"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    image = db.relationship('ImageUpload', backref='hall')
    users = db.relationship('Command', secondary='hall_command', backref=db.backref('hall', lazy='dynamic'))
    hall_start = db.Column(db.DateTime())
    hall_finish = db.Column(db.DateTime())
    leisure_time = db.Column(db.DateTime())
    square = db.Column(db.Integer())
    address = db.Column(db.String())
    city = db.Column(db.String())
    price = db.Column(db.Integer())


class Command(db.Model):
    __tablename__ = "command"

    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    name = db.Column(db.String())
    description = db.Column(db.String())
    users = db.relationship('User', secondary='commands_users', backref=db.backref('command', lazy='dynamic'))
    win_math = db.Column(db.Boolean())
    goal = db.Column(db.Integer())

    def __repr__(self):
        return self.name


class Math(db.Model):
    __tablename__ = "math"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    kind_of_sport = db.Column(db.String())
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.now())
    start_math = db.Column(db.DateTime())
    finish_math = db.Column(db.DateTime())
    closed_match = db.Column(db.Boolean(), default=False)
    commands = db.relationship(Command, secondary='maths_commands', backref=db.backref('math', lazy='dynamic'))
    command1_id = db.Column(db.Integer, db.ForeignKey('command.id'))
    command2_id = db.Column(db.Integer, db.ForeignKey('command.id'))

    command1 = db.relationship("Command", foreign_keys=[command1_id])
    command2 = db.relationship("Command", foreign_keys=[command2_id])
    audience = db.relationship("User", secondary="math_audience", backref=db.backref('math', lazy='dynamic'))

    def __repr__(self):
        return self.name


commands_users = db.Table(
    'commands_users',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('command_id', db.Integer, db.ForeignKey('command.id'))
)

maths_commands = db.Table(
    "maths_commands",
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('math_id', db.Integer, db.ForeignKey('math.id')),
    db.Column('command_id', db.Integer, db.ForeignKey('command.id'))
)

math_audience = db.Table(
    "math_audience",
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('math_id', db.Integer, db.ForeignKey('math.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)


hall_command = db.Table(
    "hall_command",
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('hall_id', db.Integer, db.ForeignKey('hall.id')),
    db.Column('command_id', db.Integer, db.ForeignKey('command.id'))
)

