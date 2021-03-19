import os,shutil
from .datapoint import DataPoint
from .dataparser import DataParser
from flask import Flask, request, render_template, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from http import HTTPStatus
from typing import List, Dict

UPLOAD_DIR = "COVIDMonitor/data"
# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

TIME_SERIES_DATA_INDICATOR = "time_series"

app = Flask(__name__)
app.config['DIR'] = UPLOAD_DIR
app.secret_key = 'csc301/team1'

# Data map: key=date, value=datapoint
datamap = dict()
if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

@app.route("/")
def main():
    # Clear Cashed Data
    for file in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, file)
        if os.path.isfile(path) or os.path.islink(path):
            os.unlink(path)
    return render_template('index.html')


def parse_data(path, is_time_series):
    parser = DataParser()

    if is_time_series:  # COVID data in time series csv file format
        parsed_records = parser.parse_covid_time_series(path)
    else:  # Global COVID data in regular csv file format
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
    if extension.lower() == "csv":  # Check if the file is in  csv format
        # Duplicate file will be replaced directly
        path = os.path.join(app.config['DIR'], secure_filename(f.filename))
    else:
        return "file format not supported", HTTPStatus.BAD_REQUEST

    try:
        f.save(path)
    except:
        return "cannot save file", HTTPStatus.INTERNAL_SERVER_ERROR

    is_time_series = True if TIME_SERIES_DATA_INDICATOR in f.filename.lower() else False

    parsed_records = {}  # key: datetime, Value: datapoint
    try:
        parsed_records = parse_data(path, is_time_series)
    except:
        return "cannot parse data", HTTPStatus.INTERNAL_SERVER_ERROR

    for datetime in parsed_records:
        for dp in parsed_records[datetime]:
            update(datamap, dp)

    # for datetime in datamap:
    #     for dp in datamap[datetime]:
    #         print(dp)
    flash("File is uploaded successfully")
    return render_template('index.html'), HTTPStatus.CREATED


def update(datamap: Dict[str, List[DataPoint]], dp: DataPoint) -> None:
    if not dp.datetime:
        return
    if dp.country_region == dp.province_state:
        print("repeated", dp)
        return

    # same_day_recs = datamap.setdefault(dp.datetime, [])
    if dp.datetime not in datamap:
        datamap[dp.datetime] = []

    for curr_dp in datamap[dp.datetime]:
        if (curr_dp.country_region == dp.country_region and
                curr_dp.province_state == dp.province_state):
            if dp.active != -1:
                curr_dp.active = dp.active
            if dp.confirmed != -1:
                curr_dp.confirmed = dp.confirmed
            if dp.deaths != -1:
                curr_dp.deaths = dp.deaths
            if dp.recovered != -1:
                curr_dp.recovered = dp.recovered
            return  # Updated the datapoint

    # dp is a completely new entry
    datamap[dp.datetime].append(dp)
    return


if __name__ == "__main__":
    app.run(debug=True)
