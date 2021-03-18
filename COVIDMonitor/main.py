from datapoint import DataPoint
from dataparser import DataParser

import os
from flask import Flask, request, render_template, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
from typing import List, Dict

UPLOAD_DIR = "data"
US_DATA_INDICATOR = "us"
TIMESERIES_DATA_INDICATOR = "timeseries"

# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
app = Flask(__name__)
app.config['DIR'] = UPLOAD_DIR

data =DataParser()

app.secret_key = 'csc301/team1'

# Data map: key=date, value=datapoint
datamap = dict()

@app.route("/")
def main():
    #TODO: Clear local cached files
    return render_template('index.html')

def parse_data(path, is_us_data, is_time_series):
    
    parser = DataParser()
    parsed_records = []

    if is_us_data and is_time_series: # US COVID data in TimeSeries csv file format
        parsed_records = parser.parse_us_covid_timeseries(path)
    elif is_us_data and not is_time_series: # US COVID data in regular csv file format
        parsed_records = parser.parse_us_covid_regular_data(path)
    elif not is_us_data and is_time_series: # Global COVID data in TimeSeries csv file format
        parsed_records = parser.parse_global_covid_timeseries(path)    
    else: # Global COVID data in regular csv file format
        parsed_records = parser.parse_global_covid_regular_data(path)

    return parsed_records


@app.route("/upload", methods=['POST'])
def upload():
    f = request.files['file']
    
    # Check if the file extension is valid
    extension = ""
    if '.' in f.filename:
        extension = f.filename.rsplit('.', 1)[1]
    else:
        return "invalid filename", HTTPStatus.BAD_REQUEST
    
    path = ""
    if extension.lower() == "csv": # Check if the file is in  csv format
        # Duplicate file will be replaced directly
        path = os.path.join(app.config['DIR'], secure_filename(f.filename))
    else:
        return "file format not supported", HTTPStatus.BAD_REQUEST

    try:
        f.save(path)
    except:
        return "cannot save file", HTTPStatus.INTERNAL_SERVER_ERROR

    is_us_data = True if US_DATA_INDICATOR in f.filename else False
    is_time_series = True if TIMESERIES_DATA_INDICATOR else False

    parsed_records = []
    # try:
    #     parsed_records = parse_data(path, is_us_data, is_time_series)
    # except:
    #     return "cannot parse data", HTTPStatus.INTERNAL_SERVER_ERROR
    
    for dp in parsed_records:
        update(datamap, dp)

    flash("File is uploaded successfully")
    return render_template('index.html'), HTTPStatus.CREATED


def update(datamap: Dict[str, DataPoint], dp: DataPoint) -> None:
    return

if __name__ == "__main__":
    app.run(debug=True)
