from flask_admin.contrib.sqla import ModelView
from services.client.model import User, ImageUpload
from services.bet.model import Command, Math, Hall, DopHall
from config import admin, db


class CommandAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["users", "name", "id"]


class MathAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["commands", "name", "hall"]


class UserAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["command", "email"]


class ImageAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ["user_id", "hall_id"]


class HallAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ['id', 'name', 'image', 'users', 'hall_start', 'hall_finish', 'leisure_time',
                   'square', 'address', 'city', 'price', 'dop_hall']


class DopHallAdmin(ModelView):
    column_hide_backrefs = False
    column_list = ('id', )


admin.add_view(UserAdmin(User, db.session))
admin.add_view(CommandAdmin(Command, db.session))
admin.add_view(MathAdmin(Math, db.session))
admin.add_view(ImageAdmin(ImageUpload, db.session))
admin.add_view(HallAdmin(Hall, db.session))
admin.add_view(DopHallAdmin(DopHall, db.session))