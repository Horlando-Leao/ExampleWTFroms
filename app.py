import os

from flask import Flask, jsonify, request, make_response
from forms_validations import RegistrationForm, OptinalForm, get_errors_wtforms, UploadForm

# init config
os.environ['FLASK_APP'] = 'app.py'
os.environ['FLASK_ENV'] = 'development'
headers_json = {'Content-Type': 'application/json'}

# initialize our Flask application
app = Flask(__name__)


@app.route("/", methods=["POST"])
def request_test():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        body = request.form
        return jsonify(str("Successfully stored  " + str(body)))
    else:
        # for fieldName, errorMessages in form.errors.items():
        #     for err in errorMessages:
        #         print(fieldName, err)
        erros = get_errors_wtforms(form)
        return make_response({'status_code': 400, 'erros': erros}, 400, headers_json)


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


if __name__ == '__main__':
    app.run(debug=True)
