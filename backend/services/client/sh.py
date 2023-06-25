from marshmallow import Schema, fields as f


class UserSchema(Schema):
    id = f.Integer(dump_only=True)
    full_name = f.String()
    email = f.Email()
    password = f.String()
    token = f.String()
    tg_token = f.String()
    active = f.Boolean()
    active_math = f.Boolean()
    created_at = f.DateTime()
    number = f.Number()
    coin = f.Integer()
    role = f.String()
    capitan = f.Boolean()
    image = f.Nested('ImageUploadSchema', many=True, only=("fileName", ))
    card = f.String()
    age = f.Integer()





