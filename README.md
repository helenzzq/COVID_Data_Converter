# Assignment 2 Starter Template 

## Getting Started 

These instructions will get a copy of the assignment starter template up and running on your local machine. 

### Prerequisites

You must have Python-3 and a package manager [pip] installed on your computer 

Additionally you will need to install the dependencies: 

```bash
pip install -r requirements.txt
```

### Data constraints
- Must specify date in "MM-DD-YY"
- If timeseries data, must contain "time_series" in filename

### Running The Code

You can start by running main.py, which is in the folder COVIDMonitor. main.py has the main method that will start the program. 

```bash
python main.py
```

## Running Tests 

A starter template for unit tests can be found under tests/unit_tests.py

To run unit tests with coverage, run the following command:

```bash
pytest --cov-report term --cov=COVIDMonitor tests/unit_tests.py
```

## Assignment Instructions

Assignment instructions can be found here: https://drive.google.com/file/d/1CX_c29slK1TyUvEOiolSzuugnRGCRp8A/view?usp=sharing

## Code Crafstmanship
We use VS code built-in python extension IDE pack to format our code.
For paired coding, we use Live share extension in VS code so that we can code at the same time and any live changes will be reflected on both ends.
