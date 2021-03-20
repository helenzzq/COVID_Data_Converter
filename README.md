# CSC301 Assignment 2

A RESTful API interface for the [JHU CSSE COVID-19 Dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data). User can query data and filter results by specifying URL parameters such as `start`, `end`, `country_region`, and `province_state`. 

Developed using `Flask`.

### Authors

Jefferson Zhong (*imJeffZ*)

Qi Zhu (*helenzzq*)

## Install

### Prerequisites

You must have Python-3 and a package manager [pip] installed on your computer

Additionally you will need to install the dependencies:

```bash
pip install -r requirements.txt
```
### Running the Code

To start the program,please run the bash command when you are in the *root project directory*.

```bash
python3 -m COVIDMonitor.main
```
### Running Tests

To run unit tests with coverage, run the following command:

```bash
pytest --cov-report term --cov=COVIDMonitor tests/unit_tests.py
```

## Usage

endpoint: *localhost:5000*

####  Sample Call
**Format**: `http://<endpoint>/<API Call>?[url parameters]`

```bash
curl http://localhost:5000/deaths?start=01-09-20&end=01-10-2021&country_region=us&province_state=wyoming&output=json
```

### URL parameters

- `start`

  The start date of the query.

  - If `start` is specified without `end`, then the query returns all possible entries with datetime equal to or after `start`.  

  - If both `start` and `end` are not specified, then the query returns all possible entries regardless of date.

- `end`

  The end date of the query.

  - If `end` is specified without `start`, then the query returns all possible entries with datetime equal or prior to `end`.

  - If both `start` and `end` are not specified, then the query returns all possible entries regardless of date.

- `country_region`

  The country/region of the  query.

  - If `country_region` is not specified, then the query returns all possible entries regardless of country/region.

- `province_state`

  The province/state of the  query.

  - If `province_state` is not specified, then the query returns all possible entries regardless of province/state.

- `combined_keys`

  The combined_keys of the query.

  - If `province_state` is not specified, then the query returns all possible entries regardless of province/state.
  
- `output`

  The output format of the query, can be one of `json`, `txt`, or `csv`. Defaults to be `txt`.
  
### API

Before sending a query, one must use a browser to visit `http://localhost:5000` to upload at least one data file from the [JHU CSSE COVID-19 Dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data), otherwise there will be no existing data to query, and a status code `204` along with the message "*Either no data file has been uploaded or query has no match found*" will be returned.

#### GET /deaths

Get COVID death case records in uploaded date set that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all death count entries will be returned.

#### GET /recovered

Get COVID recovered case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all recovered count entries will be returned.

#### GET /confirmed

Get COVID confirmed case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all confirmed count entries will be returned.

#### GET /active

Get COVID active case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all active count entries will be returned.

## Paired Programming 
We applied paired programming in both parsing data and 
## Code Craftsmanship

We use VS code built-in python extension IDE pack to format our code.
For paired coding, we use Live share extension in VS code so that we can code at the same time and any live changes will be reflected on both ends.