from marshmallow import Schema, fields as f
from services.client.sh import UserSchema


class ImageUploadSchema(Schema):
    id = f.Int()
    fileName = f.Str()
    file = f.Str()
    user_id = f.Int()
    hall_id = f.Int()


class CommandSchema(Schema):
    id = f.Int()
    created_at = f.DateTime()
    name = f.Str()
    description = f.Str()
    win_math = f.Boolean()
    goal = f.Int()
    users = f.List(f.Nested("UserSchema"))

class HallSchema(Schema):
    id = f.Int()
    name = f.Str()
    image = f.Nested(ImageUploadSchema(many=True))
    users = f.Nested(CommandSchema(many=True))
    hall_start = f.DateTime()
    hall_finish = f.DateTime()
    leisure_time = f.DateTime()
    square = f.Int()
    address = f.Str()
    city = f.Str()
    price = f.Int()


class MathSchema(Schema):
    id = f.Int()
    name = f.Str()
    kind_of_sport = f.Str()
    description = f.Str()
    created_at = f.DateTime()
    start_math = f.DateTime()
    finish_math = f.DateTime()
    closed_match = f.Boolean()
    commands = f.Nested(CommandSchema(many=True))
    audience = f.Nested(UserSchema(many=True))


class MatchCreateSchema(Schema):
    name = f.Str(required=True)
    kind_of_sport = f.Str(required=True)
    description = f.Str(required=True)
    start_math = f.DateTime(required=True)
    finish_math = f.DateTime()
    command1_id = f.Int(required=True)
    command2_id = f.Int(required=True)