from .datapoint import DataPoint

import jsonpickle
from typing import List, Dict


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

    def format_dp_list(self, query_type, dp_list):
        if query_type == 'deaths':
            return [OutputQuery.DeathDP(dp) for dp in dp_list]
        if query_type == 'confirmed':
            return [OutputQuery.ConfirmedDP(dp) for dp in dp_list]
        elif query_type == 'recovered':
            return [OutputQuery.RecoveredDP(dp) for dp in dp_list]
        else:  # query_type == 'active':
            return [OutputQuery.ActiveDP(dp) for dp in dp_list]

    def format_to_json(self, query_type, dp_list) -> str:
        dp_list = self.format_dp_list(query_type, dp_list)
        return jsonpickle.encode(dp_list, unpicklable=False)

    def format_to_txt(self, query_type, dp_list) -> str:
        dp_list = self.format_dp_list(query_type, dp_list)
        return "\n".join([str(dp) for dp in dp_list])

    def format_to_csv(self, query_type, dp_list) -> str:
        dp_list = self.format_dp_list(query_type, dp_list)
        attribute_line = ",".join(
            ["datetime",
             "country_region",
             "province_state",
             "combined_key",
             "admin",
             query_type]
        ) + "\n"
        return attribute_line + "\n".join([dp.to_csv() for dp in dp_list])

    class RawDP:
        """
        Degenerated datapoint with no count at all
        """

        def __init__(self, dp: DataPoint) -> None:
            self.datetime = dp.datetime
            self.country_region = dp.country_region
            self.province_state = dp.province_state
            self.combined_key = dp.combined_key
            self.admin = dp.admin

    class DeathDP(RawDP):
        """
        Degenerated datapoint with only death count
        """

        def __init__(self, dp: DataPoint) -> None:
            super().__init__(dp)
            self.deaths = dp.deaths

        def __str__(self) -> str:
            return str((self.datetime, self.country_region, self.province_state,
                        self.combined_key, self.admin, self.deaths))

        def to_csv(self) -> str:
            return ",".join(
                [self.datetime, self.country_region, self.province_state,
                 self.combined_key, self.admin, str(self.deaths)])

    class ConfirmedDP(RawDP):
        """
        Degenerated datapoint with only Confirmed count
        """

        def __init__(self, dp: DataPoint) -> None:
            super().__init__(dp)
            self.confirmed = dp.confirmed

        def __str__(self) -> str:
            return str((self.datetime, self.country_region, self.province_state,
                        self.combined_key, self.admin, self.confirmed))

        def to_csv(self) -> str:

            return ",".join(
                [self.datetime, self.country_region, self.province_state,
                 self.combined_key, self.admin, str(self.confirmed)])

    class ActiveDP(RawDP):
        """
        Degenerated datapoint with only Active count
        """

        def __init__(self, dp: DataPoint) -> None:
            super().__init__(dp)
            self.active = dp.active

        def __str__(self) -> str:
            return str((self.datetime, self.country_region, self.province_state,
                        self.combined_key, self.admin, self.active))

        def to_csv(self) -> str:
            return ",".join(
                [self.datetime, self.country_region, self.province_state,
                 self.combined_key, self.admin, str(self.active)])

    class RecoveredDP(RawDP):
        """
        Degenerated datapoint with only Recovered count
        """

        def __init__(self, dp: DataPoint) -> None:
            super().__init__(dp)
            self.recovered = dp.recovered

        def __str__(self) -> str:
            return str((self.datetime, self.country_region, self.province_state,
                        self.combined_key, self.admin, self.recovered))

        def to_csv(self) -> str:
            return ",".join(
                [self.datetime, self.country_region, self.province_state,
                 self.combined_key, self.admin, str(self.recovered)])
