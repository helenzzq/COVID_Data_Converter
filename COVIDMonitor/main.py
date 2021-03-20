from werkzeug.datastructures import Headers
from .datapoint import DataPoint
from .dataparser import DataParser
from .outputfactory import OutputFactory

import os
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from werkzeug.utils import redirect, secure_filename
from http import HTTPStatus
from typing import List, Dict

UPLOAD_DIR = "COVIDMonitor/data"
# Check if upload dir exist
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

URL_PARAMS = ['start', 'end', 'country_region', 'province_state', 'combined_key', 'output_format']
URL_OUTPUT_FORMAT_PARAM = 'output'

TIME_SERIES_DATA_INDICATOR = "time_series"

NO_RESULT_MESSAGE = "Either no data file has been uploaded or query has no match found"

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


def parse_data(path, is_time_series) -> Dict[str, DataPoint]:
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

    path = None
    if extension.lower() == "csv":  # Check if the file is in  csv format
        # Duplicate file will be replaced directly
        path = os.path.join(app.config['DIR'], secure_filename(f.filename))
    else:
        return "file format not supported", HTTPStatus.BAD_REQUEST
    
    try:
        f.save(path)
    except:
        return "fail to store file in server", HTTPStatus.INTERNAL_SERVER_ERROR

    is_time_series = True if TIME_SERIES_DATA_INDICATOR in f.filename.lower() else False

    parsed_records = {}  # key: datetime, Value: datapoint
    try:
        parsed_records = parse_data(path, is_time_series)
    except:
        return "cannot parse data", HTTPStatus.INTERNAL_SERVER_ERROR

    for datetime in parsed_records:
        for dp in parsed_records[datetime]:
            # print(dp)
            update(datamap, dp)
            # for updated_dp in datamap[datetime]:
            #     if updated_dp.country_region == dp.country_region and updated_dp.province_state == dp.province_state:
            #         print("after update", updated_dp)
            #         break
            # break
    for datetime in datamap:
        for dp in datamap[datetime]:
            print(dp)

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
                curr_dp.sactive = dp.active
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


"""
Return whether date is in between start and end
"""
def is_between_two_dates(start, date, end) -> bool:
    # format into [MM, DD, YYYY], split empty string will result ['']
    start, date, end = start.split("-"), date.split("-"), end.split("-")
    # format into [YYYY, DD, MM]
    start = [start[-1]] + start[:-1]
    date = [date[-1]] + date[:-1]
    end = [end[-1]] + end[:-1]
    
    # no start date and no end date
    if not start[0] and not end[0]:
        return True

    # only start date is specified
    if start[0] and not end[0]:
        return start <= date
    
    # only end date is specified
    if not start[0] and end[0]:
        return date <= end

    # start and end is the same date
    if start == end:
        return date == start
    
    # check whether date is between start and end
    return start <= date <= end


"""
Return whether two country_region matches
"""
def is_same_country_region(cr1, cr2) -> bool:
    # no cr1 condition specified means country_region condition is always True
    return True if not cr1 else cr1.lower() == cr2.lower()

"""
Return whether two province_state matches
"""
def is_same_province_state(ps1, ps2) -> bool:
    #no ps1 condtion specified means province_state condition is always True
    return True if not ps1 else ps1.lower() == ps2.lower()

"""
Return whether two combined_key matches
"""
def is_same_combined_key(ck1, ck2) -> bool:
    # no ck1 specified means combined_key condition is always True
    return True if not ck1 else ck1.lower() == ck2.lower()

def parse_url_params(args) -> List[str]:
    return [args.get(p, "") for p in URL_PARAMS]

def get_query_results(args):
    start, end, country_region, province_state, combined_key, _dummy_output_format = parse_url_params(args)
    result_datapoints = []
    for date in datamap:
        if is_between_two_dates(start, date, end):
            for dp in datamap[date]:
                if (is_same_country_region(country_region, dp.country_region) and
                    is_same_province_state(province_state, dp.province_state) and
                    is_same_combined_key(combined_key, dp.combined_key)):
                    result_datapoints.append(dp)
    return result_datapoints

@app.route("/deaths", methods=['GET'])
def get_deaths():
    dp_list = get_query_results(request.args)
    output_format = request.args.get(URL_OUTPUT_FORMAT_PARAM, '')
    if not dp_list:
        return NO_RESULT_MESSAGE, HTTPStatus.NO_CONTENT
    else:
        out = OutputFactory()
        query_type = 'deaths'
        if output_format == 'json':
            return app.response_class(
                response = out.format_to_json(query_type, dp_list) ,
                mimetype = 'application/json'
            ), HTTPStatus.OK
        elif output_format == 'csv':
            return app.response_class(
                response = out.format_to_csv(query_type, dp_list),
                mimetype = 'text/csv',
                headers = {"Content-disposition": "attachment; filename=deaths.csv"}
            ), HTTPStatus.OK
        else: # default output is text
            return app.response_class(
                response = out.format_to_txt(query_type, dp_list),
                mimetype = 'text/plain'
            ), HTTPStatus.OK

@app.route("/confirmed", methods=['GET'])
def get_confirmed():
    dp_list = get_query_results(request.args)
    output_format = request.args.get(URL_OUTPUT_FORMAT_PARAM, '')
    if not dp_list:
        return NO_RESULT_MESSAGE, HTTPStatus.OK
    else:
        out = OutputFactory()
        query_type = 'confirmed'
        if output_format == 'json':
            return app.response_class(
                response = out.format_to_json(query_type, dp_list) ,
                mimetype = 'application/json'
            ), HTTPStatus.OK
        elif output_format == 'csv':
            return app.response_class(
                response = out.format_to_csv(query_type, dp_list),
                mimetype = 'text/csv',
                headers = {"Content-disposition": "attachment; filename=confirmed.csv"}
            ), HTTPStatus.OK
        else: # default output is text
            return app.response_class(
                response = out.format_to_txt(query_type, dp_list),
                mimetype = 'text/plain'
            ), HTTPStatus.OK


@app.route("/active", methods=['GET'])
def get_active():
    dp_list = get_query_results(request.args)
    output_format = request.args.get(URL_OUTPUT_FORMAT_PARAM, '')
    if not dp_list:
        return NO_RESULT_MESSAGE, HTTPStatus.OK
    else:
        out = OutputFactory()
        query_type = 'active'
        if output_format == 'json':
            return app.response_class(
                response = out.format_to_json(query_type, dp_list) ,
                mimetype = 'application/json'
            ), HTTPStatus.OK
        elif output_format == 'csv':
            return app.response_class(
                response = out.format_to_csv(query_type, dp_list),
                mimetype = 'text/csv',
                headers = {"Content-disposition": "attachment; filename=active.csv"}
            ), HTTPStatus.OK
        else: # default output is text
            return app.response_class(
                response = out.format_to_txt(query_type, dp_list),
                mimetype = 'text/plain'
            ), HTTPStatus.OK


@app.route("/recovered", methods=['GET'])
def get_recovered():
    dp_list = get_query_results(request.args)
    output_format = request.args.get(URL_OUTPUT_FORMAT_PARAM, '')
    if not dp_list:
        return NO_RESULT_MESSAGE, HTTPStatus.OK
    else:
        out = OutputFactory()
        query_type = 'recovered'
        if output_format == 'json':
            return app.response_class(
                response = out.format_to_json(query_type, dp_list) ,
                mimetype = 'application/json'
            ), HTTPStatus.OK
        elif output_format == 'csv':
            return app.response_class(
                response = out.format_to_csv(query_type, dp_list),
                mimetype = 'text/csv',
                headers = {"Content-disposition": "attachment; filename=recovered.csv"}
            ), HTTPStatus.OK
        else: # default output is text
            return app.response_class(
                response = out.format_to_txt(query_type, dp_list),
                mimetype = 'text/plain'
            ), HTTPStatus.OK


if __name__ == "__main__":
    app.run(debug=True)
