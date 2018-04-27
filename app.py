import csv
import io
import urllib.request as urllib_request
from flask import Flask, render_template, request, redirect, jsonify, make_response
from werkzeug.datastructures import ImmutableMultiDict
from util import parse_and_format_csv
from negExImplementation import evaluate_reports
from flask.ext.login import current_user, LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager()
login_manager.init_app(app)

class AppUser:
    def __init__(self, kerberos):
        self.kerberos = kerberos
        self.active = True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
    	return self.kerberos

@login_manager.user_loader
def load_user(kerberos):
    return AppUser(kerberos)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

@app.route('/login')
def login():
	return render_template('index.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/login-request', methods=['POST'])
def login_request():
	kerberos = request.get_json()['kerberos']
	password = request.get_json()['password']
	request_url = 'http://puff.med.nyu.edu/ProxyAuth/authUser?type=SOMwithSquareSpecial&user=' + kerberos + '&password=' + password
	response = urllib_request.urlopen(request_url)
	response_string = response.read().decode('utf-8')
	if response_string == "SUCCESS":
		login_user(AppUser(kerberos))
	return jsonify({'login_status': response_string})

@app.route('/is-logged-in', methods=['GET'])
def is_logged_in():
	is_logged_in = current_user.is_authenticated and current_user.is_authenticated()
	print(current_user.is_authenticated)
	return jsonify({'logged_in': is_logged_in})
	

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/negex_implementation')
@login_required
def neg_ex():
  return render_template('index.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
	f = request.files['file']
	stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
	csv_input = csv.reader(stream)
	[start_phrase, target_phrases, skip_phrases, reports, config_rows] = parse_and_format_csv(csv_input)
	evaluations = evaluate_reports(target_phrases, start_phrase, skip_phrases, reports)
	new_csv_rows = config_rows
	for i in range(len(reports)):
		new_csv_rows.append([reports[i], str(evaluations[i])])
	si = io.StringIO()
	cw = csv.writer(si)
	cw.writerows(new_csv_rows)
	output = make_response(si.getvalue())
	print(si.getvalue())
	output.headers["Content-Disposition"] = "attachment; filename=export.csv"
	output.headers["Content-type"] = "text/csv"
	return output

if __name__ == '__main__':
  app.run(debug=True)

