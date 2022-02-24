import os

from flask import Flask, request, make_response
from forms_validations import (
    RegistrationForm,
    OptinalForm,
    get_errors_wtforms,
    UploadForm,
    SelectedForm,
    CustomValidateForm
)

# init config
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'
headers_json = {'Content-Type': 'application/json'}

# initialize our Flask application
app = Flask(__name__)


@app.route("/", methods=["POST"])
def request_test():
    form = RegistrationForm(request.form)

    if form.validate() and form.custom_validate_accept_tos(request.form, 'accept_tos'):
        return make_response({"Successfully_stored": str(request.form)}, 200, headers_json)
    else:
        return make_response({'status_code': 400, 'erros': get_errors_wtforms(form)}, 400, headers_json)


@app.route("/upload", methods=["POST"])
def request_upload():
    form = UploadForm(request.files)
    print(request.files)

    if form.validate() and form.validate_file_extesion(request.files, 'uploa'):
        return make_response({"Successfully_stored": str(request.files)}, 200, headers_json)
    else:
        return make_response({'status_code': 400, 'erros': get_errors_wtforms(form)}, 400, headers_json)


@app.route("/field", methods=["POST"])
def request_field():
    form = OptinalForm(request.form)
    print(request.form)

    if form.validate():
        return make_response({"Successfully_stored": str(request.form)}, 200, headers_json)
    else:
        return make_response({'status_code': 400, 'erros': get_errors_wtforms(form)}, 400, headers_json)


@app.route("/select", methods=["POST"])
def request_custom():
    form = SelectedForm(request.form)
    print(request.form)

    if form.validate():
        return make_response({"Successfully_stored": str(request.form)}, 200, headers_json)
    else:
        return make_response({'status_code': 400, 'erros': get_errors_wtforms(form)}, 400, headers_json)


@app.route("/custom", methods=["POST"])
def request_select():
    form = CustomValidateForm(request.form)
    print(request.form)

    if form.validate_custom():
        return make_response({"Successfully_stored": str(request.form)}, 200, headers_json)
    else:
        return make_response({'status_code': 400, 'erros': get_errors_wtforms(form)}, 400, headers_json)


if __name__ == '__main__':
    app.run(debug=True)
