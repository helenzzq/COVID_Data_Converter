from .datapoint import DataPoint
from typing import List, Dict
import pandas as pd
import ntpath

# Combined_Key only appear in time_series us
TIME_SERIES_US = ["Country_Region", "Province_State"]
TIME_SERIES = ["Country/Region", "Province/State"]
DETAILED_GLOBAL = ["Country_Region", "Province_State", "Active", "Confirmed",
                   "Deaths", "Recovered", "Combined_Key",
                   "Admin2"]
DETAILED_US = ["Country_Region", "Province_State",
               "Active", "Confirmed", "Deaths", "Recovered"]
US_DATA_INDICATOR = "us"
ADMIN = "Admin2"
DEATHS = "deaths"
RECOVERED = "recovered"
ACTIVE = "active"
CONFIRMED = "confirmed"
COMBINED_KEY = "Combined_Key"


def convert_date_format(date):
    """Return the date in format MM-DD-YYYY"""
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
    func_lst = [dp.set_death, dp.set_recovered,
                dp.set_active, dp.set_confirmed]
    data = check_null_entry(data, 'int')
    func_lst[index](int(data))
    if is_us:
        dp.set_combined_key(data)


def check_null_entry(entry, expected_type):
    """
    Return default empty value of the expected type
    of the column entry if the original entry
    in csv is null
    """

    if pd.isna(entry):
        if expected_type == 'int':
            return 0
        else:
            return ''
    return entry


class DataParser:
    """
    Strategy pattern for parsing the following types of data:
      - US COVID time_series
      - GLOBAL COVID time_series
      - US COVID regular data
      - GLOBAL COVID regular data
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def parse_covid_time_series(self, path) -> Dict[str, List[DataPoint]]:
        """Return Parsed Time series data as a Hashmap"""
        # Read csv and extract column data
        csv_name = ntpath.basename(path)
        is_us = US_DATA_INDICATOR in csv_name.lower()
        covid_data = pd.read_csv(path)
        col = list(covid_data.columns)
        # Check csv data is global or us
        country_prov_cols = TIME_SERIES
        if is_us:
            country_prov_cols = TIME_SERIES_US
        df = pd.read_csv(path, usecols=country_prov_cols)
        date_col = [c for c in col if c[0].isnumeric()]
        row_num = df.shape[0]
        hash_map = dict()
        for date in date_col:
            data = covid_data[date]
            new_date = convert_date_format(date)
            hash_map[new_date] = []
            for i in range(row_num):
                province = df[country_prov_cols[1]][i]
                # Check if the province entry is none
                if pd.isna(province):
                    province = ''
                # Create data point based on data
                dp = DataPoint(new_date, df[country_prov_cols[0]][i], province)
                # Check csv data type and update corresppnding data type column
                check_data_catego(dp, csv_name, data[i], is_us)

                if is_us:
                    admin = '' if pd.isna(
                        covid_data[ADMIN][i]) else covid_data[ADMIN][i]
                    dp.set_admin(admin)
                hash_map[new_date].append(dp)
        return hash_map

    @classmethod
    def parse_covid_daily_report(self, path) -> Dict[str, List[DataPoint]]:
        """Return Parsed Daily report data as a Hashmap"""
        # Read csv and extract column data
        csv_name = ntpath.basename(path)
        covid_data = pd.read_csv(path)
        col = list(covid_data.columns)
        is_us = COMBINED_KEY not in col
        target_col = DETAILED_GLOBAL
        if is_us:
            target_col = DETAILED_US
        df = pd.read_csv(path, usecols=target_col)

        date = csv_name.split(".")[0].split('-')
        date[2] = date[2][2:]
        date = '-'.join(date)
        row_num = df.shape[0]
        hash_map = dict()
        hash_map[date] = []
        for i in range(row_num):
            # Check if each column entry is null
            # If so update corresponding column value to default empty value
            dp_value = [check_null_entry(
                df[target_col[k]][i], 'str') for k in range(2)]
            dp_value.extend(
                [check_null_entry(df[target_col[k]][i], 'int') for k in
                 range(2, 6)])
            # Create data point based on data
            dp = DataPoint(date, dp_value[0], dp_value[1], '',
                           '', dp_value[2], dp_value[3], dp_value[4],
                           dp_value[5])
            # If us, no combined key column
            if not is_us:
                combined = '' if pd.isna(
                    df[COMBINED_KEY][i]) else df[COMBINED_KEY][i]
                admin = '' if pd.isna(df[ADMIN][i]) else df[ADMIN][i]
                dp.set_combined_key(combined)
                dp.set_admin(admin)
            # Add to hashmap
            hash_map[date].append(dp)

        return hash_map
