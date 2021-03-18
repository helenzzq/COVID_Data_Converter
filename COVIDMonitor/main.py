from datapoint import DataPoint
from dataparser import DataParser

import os
from flask import Flask, request, render_template, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
from typing import List, Dict

UPLOAD_DIR = "data"
# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

TIME_SERIES_DATA_INDICATOR = "time_series"



app = Flask(__name__)
app.config['DIR'] = UPLOAD_DIR
app.secret_key = 'csc301/team1'

# Data map: key=date, value=datapoint
datamap = dict()

@app.route("/")
def main():
    #TODO: Clear local cached files
    return render_template('index.html')

def parse_data(path, is_time_series):
    
    parsed_records = []
    parser = DataParser()

    if is_time_series:  # COVID data in time series csv file format
        parsed_records = parser.parse_covid_time_series(path) 
    else:               # Global COVID data in regular csv file format
        parsed_records = parser.parse_covid_daily_report(path)

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

    is_time_series = True if TIME_SERIES_DATA_INDICATOR in f.filename.lower() else False

    parsed_records = []
    try:
        parsed_records = parse_data(path, is_time_series)
    except RuntimeError as err:
        print(err)
        return "cannot parse data", HTTPStatus.INTERNAL_SERVER_ERROR
    
    for dp in parsed_records:
        print("dp", dp)
        update(datamap, dp)

    print(datamap)
    flash("File is uploaded successfully")
    return render_template('index.html'), HTTPStatus.CREATED


def update(datamap: Dict[str, DataPoint], dp: DataPoint) -> None:
    if not dp.datetime:
        return
    if dp.country_region == dp.province_state:
        return
    
    same_day_recs = datamap.setdefault(dp.datetime, [])
    

    for curr_dp in same_day_recs:
        if (curr_dp.country_region == dp.country_regionand and
            curr_dp.province_state == dp.province_state):
            if dp.active != -1:
                curr_dp.active = dp.active
            if dp.confirmed != -1:
                curr_dp.confirmed = dp.confirmed
            if dp.deaths != -1:
                curr_dp.deaths = dp.deaths
            if dp.recovered != -1:
                curr_dp.recovered = dp.recovered
            return # Updated the datapoint
    
    # dp is a completely new entry
    same_day_recs.append(dp)
    return

if __name__ == "__main__":
    app.run(debug=True)
