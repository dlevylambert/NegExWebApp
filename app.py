import csv
import io
from flask import Flask, render_template, request, jsonify, make_response
from werkzeug.datastructures import ImmutableMultiDict
from util import parse_and_format_csv
from negExImplementation import evaluate_reports

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/negex_implementation')
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

