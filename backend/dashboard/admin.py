from flask_admin.contrib.sqla import ModelView
from services.client.model import User, ImageUpload
from services.bet.model import Command, Math
from config import admin, db


class CommandAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["users", "name"]


class MathAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["commands", "name"]


class UserAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["command", "email"]


class ImageAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["user_id", "hall_id"]


admin.add_view(UserAdmin(User, db.session))
admin.add_view(CommandAdmin(Command, db.session))
admin.add_view(MathAdmin(Math, db.session))
admin.add_view(ImageAdmin(ImageUpload, db.session))