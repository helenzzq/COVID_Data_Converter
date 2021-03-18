from COVIDMonitor.dataparser import DataParser

from flask import Flask, request, render_template, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from http import HTTPStatus

UPLOAD_DIR = "data"

# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app = Flask(__name__)
app.config['DIR'] = UPLOAD_DIR

data =DataParser()

app.secret_key = 'csc301/team1'

# Data records
records = []

@app.route("/")
def main():
    return render_template('index.html'),200

def parse_data(path, isUSData, isTimeSeries):
    
    parser = dataparser.DataParser()
    parsed_records = []

    # COVID data in TimeSeries csv file format
    if isTimeSeries:
        parsed_records = parser.parse_covid_timeseries(path)


    # COVID data in Daily Report csv file format
    else:
        parsed_records = parser.parse_covid_daily_report(path)

    records.extend(parsed_records)


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        # Check if the extension is valid
        if '.' in f.filename:
            extension = f.filename.rsplit('.', 1)[1]
            # Check if the file is in  csv format
            if extension.lower() == "csv":
                # Duplicate file will be replaced directly
                f.save(os.path.join(app.config['DIR'], secure_filename(f.filename)))
                flash("File is uploaded successfully")
            else:
                flash("This uploaded file is not in csv format. Please upload in the right format")
            return render_template('index.html'),200

    return render_template('index.html'),400


if __name__ == "__main__":
    app.run(debug=True)
