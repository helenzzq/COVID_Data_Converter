from datapoint import DataPoint
from typing import Dict
import pandas as pd
import ntpath

# Combined_Key only appear in time_series us

TIME_SERIES = ["Province/State", "Country/Region"]
DETAILED = ["Province/State", "Country/Region", "Combined_Key", "Active", "Confirmed", "Deaths", "Recovered"]

DEATHS = "deaths"
RECOVERED = "recovered"
ACTIVE = "active"
CONFIRMED = "confirmed"
COMBINED_KEY = "Combined_Key"


def convert_date_format(date):
    """Return the date in format MM-DD-YY"""
    date = date.split('/')
    if int(date[0]) < 10:
        date[0] = '0' + date[0]

    return '-'.join(date)


def check_data_catego(dp, csv_name, data, is_us) -> None:
    """Check the type of the time series and update the
    corresponding value in data point
    """
    type_lst = [DEATHS, RECOVERED, ACTIVE, CONFIRMED]
    index = [i for i in range(4) if type_lst[i] in csv_name][0]
    func_lst = [dp.set_death, dp.set_recovered, dp.set_active, dp.set_confirmed]
    func_lst[index](data)
    if is_us:
        dp.set_combined_key(data)


class DataParser:
    """
    Strategy pattern for parsing the following types of data:
      - US COVID Timeseries
      - GLOBAL COVID Timeseries
      - US COVID regular data
      - GLOBAL COVID regular data
    """

    @classmethod
    def parse_covid_timeseries(self, path) -> Dict[str, DataPoint]:
        """Return Parsed Time series data as a Hashmap"""
        csv_name = ntpath.basename(path)
        is_us = "us" in csv_name
        covid_data = pd.read_csv(path)
        col = list(covid_data.columns)
        df = pd.read_csv(path, TIME_SERIES)
        date_col = [convert_date_format(c) for c in col if c[0].isnumeric()]
        row_num = df.shape[0]
        hash_map = dict()
        for date in date_col:
            data = covid_data[date]
            for i in range(row_num):
                dp = DataPoint(date, df["Country/Region"][i], df["Province/State"][i])
                check_data_catego(dp, csv_name, data[i], is_us)
                hash_map[date].append(dp)
        return hash_map

    @classmethod
    def parse_covid_daily_report(self, path) -> Dict[str, DataPoint]:
        """Return Parsed Daily report data as a Hashmap"""
        csv_name = ntpath.basename(path)
        covid_data = pd.read_csv(path)
        col = list(covid_data.columns)
        is_us = COMBINED_KEY in col
        if is_us:
            DETAILED.remove(COMBINED_KEY)
        df = pd.read_csv(path, DETAILED)
        temp = csv_name.split(".")[0].split("-")
        temp[2] = temp[2][2:]
        date = '-'.join(temp)
        row_num = df.shape[0]
        hash_map = dict()
        for i in range(row_num):
            dp = DataPoint(date, df[DETAILED[0]][i], df[DETAILED[1]][i], df[DETAILED[2]][i],
                           df[DETAILED[3]][i], df[DETAILED[4]][i], df[DETAILED[5]][i])
            # If us, no combined key column
            if not is_us:
                dp.set_combined_key(df[DETAILED[6]][i])
            hash_map[date].append(dp)
        return hash_map
