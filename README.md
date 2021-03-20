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

Before sending a query, one must use a browser to visit `http://localhost:5000` to upload at least one data file from the [JHU CSSE COVID-19 Dataset](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data), otherwise there will be no existing data to query, and a status code `404` along with the message "*Either no data file has been uploaded or query has no match found*" will be returned.

#### GET /deaths

Get COVID death case records in uploaded date set that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all death count entries will be returned.

#### GET /recovered

Get COVID recovered case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all recovered count entries will be returned.

#### GET /confirmed

Get COVID confirmed case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all confirmed count entries will be returned.

#### GET /active

Get COVID active case records that satisfies the conditions specified in URL parameters. By default, if no URL parameters are given, all active count entries will be returned.

## Paired Programming 
In this assignment, we design the solutions the solution together and paired programmed for most of the features. In the initial meeting, we discuss possible features and decide on a subset of tasks to implement.

### Feature Breakdown
We implement mainly 4 features in the assignment:
- Upload file
  - Front-End UI (Qi Zhu)
  - Routing  (Jefferson Zhong , Qi Zhu)
  - Exception Handle (Jefferson Zhong)
- Parsing Data(Jefferson Zhong,Qi Zhu)
  - DataParser Structure (Jefferson Zhong)
  - DataParser Routing (Jefferson Zhong)
  - DataParser Implementation: (Qi Zhu)
  - DataParser Testing:(Qi Zhu)
- Query Data & Routing (Paired Programmed)
  - Driver:(Jefferson Zhong)
  - Navigator: Qi Zhu
- Output Query & Routing(Paired Programmed)
  - Driver: Qi Zhu
  - Navigator: Jefferson Zhong
### Paired Programming  Reflection
We strictly followed the paired programming requirement in implementing the last two features:1. Query Data & Routing; 2. Output Query & Routing.

We set up an approximate 2 hours limit for each feature. 
Indeed, paired programming profoundly enhanced the efficiency of coding and debugging.  For example, since the feature 'Output Query' is tightly related to Output Query, playing as the navigator of the querying data helped the driver of implementing the next feature in understanding the code more thoroughly.  Additionally, while playing as the navigator for the second feature,  the driver for the first feature, Jefferson, can quickly identify the source of the bug that is caused by his previous implementation.  Switching roles in paired programming contributes to that.

However, paired programming is a bit challenging for teams like us that live in different time zone. It's a little bit hard for us to meet for a long time. We can only break our implementation into several steps and then meet several times to complete a feature. So the gap between the commits in the last feature is a little bit longer compared to other branches.




## Code Craftsmanship
We use VS code built-in python extension IDE pack to format our code.
For paired coding, we use Live share extension in VS code so that we can code at the same time and any live changes will be reflected on both ends.