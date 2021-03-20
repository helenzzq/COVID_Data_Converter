import json
import os
import random
import string
import jsonpickle
from .datapoint import DataPoint
from typing import List, Dict
from pandas import DataFrame

COL = ["Date", "Country_Region", "Province_State", "Combined_Key"]
OUTPUT_DIR = 'COVIDMonitor/output'


class OutputQuery:
    """
    A class that output the data based on user query.
    Strategy pattern for outputing the following types of data:
      - US COVID time_series
      - GLOBAL COVID time_series
      - US COVID regular data
      - GLOBAL COVID regular data
    The data can be any of the following:
      - Deaths
      - Confirmed
      - Active
      - Recovered
    Support returning the data in multiple formats:
      - JSON
      - CSV
      - Text (printed)
    """

    def __init__(self):
        super().__init__()

    @classmethod
    def output_data(cls, query: List[DataPoint], data_type: str, formats: str) \
            -> Dict[str, List]:
        """Output the query data given specified format"""
        col = []
        col.extend(COL)
        col.append(data_type)
        result = dict()
        for c in col:
            result[c] = []
        for dp in query:
            result["Date"].append(dp.datetime)
            result[col[1]].append(dp.country_region)
            result[col[2]].append(dp.province_state)
            result[col[3]].append(dp.combined_key)
            result[data_type].append(dp.confirmed)
        output = cls.format_switcher(formats, result, col)
        return output

    @classmethod
    def output_confirmed(cls, query: List[DataPoint], formats: str) \
            -> Dict[str, List]:
        """Output Confirmed data in specified format"""
        if formats == 'json':
            return cls.format_switcher(formats, query, [])
        else:
            return cls.output_data(query, 'Confirmed', formats)

    @classmethod
    def output_death_data(cls, query: List[DataPoint], formats: str):
        """Output deaths data in specified format"""
        if formats == 'json':
            return cls.format_switcher(formats, query, [])
        return cls.output_data(query, 'Deaths', formats)

    @classmethod
    def output_active_data(cls, query: List[DataPoint], formats: str):
        """Output active data in specified format"""
        if formats == 'json':
            return cls.format_switcher(formats, query, [])
        return cls.output_data(query, 'Active', formats)

    @classmethod
    def output_recovered_data(cls, query: List[DataPoint], formats: str):
        """Output recovered data"""
        if formats == 'json':
            return cls.format_switcher(formats, query, [])
        return cls.output_data(query, 'Recovered', formats)

    @classmethod
    def format_switcher(cls, formats: str, data: Dict or List[DataPoint],
                        col: List[str]):
        """Convert data to specified format"""
        output = None
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        letters = string.ascii_lowercase
        random_str = ''.join(random.choice(letters) for _ in range(3))
        file_path = OUTPUT_DIR + '/output_' + random_str + '.' + formats

        if formats == 'json':
            output = jsonpickle.encode(data, unpicklable=False)
        else:
            df = DataFrame.from_dict(data)
            if formats == 'csv':
                output = DataFrame(data).to_csv(file_path)
            elif formats == 'txt':
                    output = df.to_csv(file_path, header=False, index=False,
                                       sep=' ', mode='a')
        return output
