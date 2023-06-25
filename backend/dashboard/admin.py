import os
import random

from flask_admin.contrib.sqla import ModelView
from flask_admin import form

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

    base_path = os.path.join(os.getcwd(), 'uploads')
    form_extra_fields = {
        'file': form.FileUploadField('File', base_path=base_path)
    }

    def _change_path_data(self, form):
        try:
            if form.file.data:
                storage_file = form.file.data
                ext = storage_file.filename.split('.')[-1]
                hash_value = random.getrandbits(128)
                filename = f'{hash_value}.{ext}'
                file_path = os.path.join(self.base_path, filename)

                # Save the uploaded image
                storage_file.save(file_path)

                # Update the form fields
                form.fileName.data = storage_file.filename
                form.file.data = filename

                # Generate thumbnail if it's an image
                if ext.lower() in ['jpg', 'jpeg', 'png', 'gif']:
                    thumbnail_path = os.path.join(self.base_path, 'thumbnails', filename)
                    thumbnail_size = (100, 100)  # Set your desired thumbnail size

                    # Open the uploaded image
                    image = ImageUpload.open(file_path)
                    image.thumbnail(thumbnail_size)
                    image.save(thumbnail_path)

        except Exception as ex:
            pass

        return form

    def create_model(self, form):
        form = self._change_path_data(form)
        return super().create_model(form)

    def update_model(self, form, model):
        form = self._change_path_data(form)
        return super().update_model(form, model)

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