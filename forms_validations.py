from werkzeug.datastructures import ImmutableMultiDict

from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    validators,
    FileField,
    SelectField,
    IntegerField
)

list_extensions_allowed = ['pdf', 'doc', 'docx', 'odt', 'png', 'jpeg', 'jpg',
                           'PDF ', 'DOC', 'DOCX', 'ODT', 'PNG', 'JPEG', 'JPG']


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address',
                        [validators.Length(min=6, max=35), validators.Email(message='Precisa de email pow!')])
    age = IntegerField(
        'age',
        [
            validators.number_range(min=1, max=99),
            validators.DataRequired(message='This field is required. Is Integer')
        ])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

    def custom_validate_accept_tos(self, form: ImmutableMultiDict, name: str):
        try:
            field = form[name]
        except KeyError:
            raise ValueError('Set correct name field')

        my_validation = ['yes', 'OK', 'VERY NICE', 'GOOD', 'NO', 'NOT']
        if field not in my_validation:
            self.accept_tos.errors.append("This is field accept_tos do no accept. Allowed: " + ', '.join(my_validation))
            return False
        return True


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


class SelectedForm(Form):
    username = StringField(
        'Username',
        [
            validators.DataRequired(),
            validators.Length(min=4, max=25)
        ])
    age = SelectField(label='Age', choices=['+18', '>18', '-18', '<18'], validate_choice=True)
    print(age)


class CustomValidateForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.Email()])

    def valida_gmail(self):
        server: int = str(self.email.data).find('gmail')
        if server != -1:
            self.email.errors.append('email needs to be different from gmail')
            return False
        else:
            return True

    def validate_custom(self) -> bool:
        validate = self.validate()
        valida_gmail = self.valida_gmail()

        if validate and valida_gmail:
            return True
        else:
            return False


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
