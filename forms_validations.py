import os
import re
from pprint import pprint

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.sansio import request
from wtforms import Form, BooleanField, StringField, PasswordField, validators, FileField, ValidationError

list_extensions_allowed = ['pdf', 'doc', 'docx', 'odt', 'png', 'jpeg', 'jpg',
                           'PDF ', 'DOC', 'DOCX', 'ODT', 'PNG', 'JPEG', 'JPG']


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address',
                        [validators.Length(min=6, max=35), validators.Email(message='Precisa de email pow!')])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


class OptinalForm(Form):
    username = StringField(
        'Username',
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25)
        ])
    email = StringField(
        'Email Address',
        [
            validators.Optional(),
            validators.Length(min=6, max=35),
            validators.Email(message='Precisa de email pow!'),
        ])


class UploadForm(Form):
    upload = FileField(label=u'Image File', validators=[validators.DataRequired(message='Field upload empty file')])

    def validate_file_extesion(self, file: ImmutableMultiDict, name: str):
        try:
            field = file[name]
        except KeyError:
            raise ValueError('Set corret name file field')

        mimetype = field.mimetype.split('/')[1]
        if mimetype not in list_extensions_allowed:
            self.upload.errors.append(
                "This is field upload not extesion allowed. Allowed: " + ', '.join(list_extensions_allowed))
            return False
        return True


def get_errors_wtforms(form) -> list:
    validation_fields = []
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            validation_fields.append({'field': fieldName, 'message': err})
    return validation_fields


def check_upload(cls):
    fields = []
    for name in dir(cls):  # look at the names on the class
        if not name.startswith('_'):  # ignore names with leading _
            unbound_field = getattr(cls, name)  # get the value
            if hasattr(unbound_field, '_formfield'):  # make sure it's a field
                fields.append((name, unbound_field))  # record it
    return fields
