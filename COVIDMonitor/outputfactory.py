import numpy as np
from .datapoint import DataPoint

import jsonpickle

jsonpickle.set_encoder_options('simplejson',
                               use_decimal=True)
jsonpickle.set_decoder_options('simplejson',
                               use_decimal=True)


class NumpyFloatHandler(jsonpickle.handlers.BaseHandler):
    """
    Automatic conversion of numpy float to python floats
    Required for jsonpickle to work correctly
    """
    def flatten(self, obj, data):
        """
        Converts and rounds a Numpy.float* to Python float
        """
        return round(obj, 6)

class NumpyIntHandler(jsonpickle.handlers.BaseHandler):
    """
    Automatic conversion of numpy int to python int.
    Required for jsonpickle to work correctly
    """
    def flatten(self, obj, data):
        return int(obj)

# https://stackoverflow.com/questions/23793884/jsonpickle-encoding-floats-with-many-decimals-as-null
jsonpickle.handlers.registry.register(np.int64, NumpyIntHandler)
jsonpickle.handlers.registry.register(np.float32, NumpyFloatHandler)
jsonpickle.handlers.registry.register(np.float64, NumpyFloatHandler)


class OutputFactory:
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
            return [OutputFactory.DeathDP(dp) for dp in dp_list]
        if query_type == 'confirmed':
            return [OutputFactory.ConfirmedDP(dp) for dp in dp_list]
        elif query_type == 'recovered':
            return [OutputFactory.RecoveredDP(dp) for dp in dp_list]
        else:  # query_type == 'active':
            return [OutputFactory.ActiveDP(dp) for dp in dp_list]

    def format_to_json(self, query_type, dp_list) -> str:
        dp_list = self.format_dp_list(query_type, dp_list)
        return jsonpickle.encode(dp_list, unpicklable=False, use_decimal=True)

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

    class RawDPInterface:
        """
        Degenerated datapoint interface with no count at all
        """

        def __init__(self, dp: DataPoint) -> None:
            self.datetime = dp.datetime
            self.country_region = dp.country_region
            self.province_state = dp.province_state
            self.combined_key = dp.combined_key
            self.admin = dp.admin
        
        def __str__(self) -> str:
            pass
        
        def to_csv(self) -> str:
            pass

    class DeathDP(RawDPInterface):
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

    class ConfirmedDP(RawDPInterface):
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

    class ActiveDP(RawDPInterface):
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

    class RecoveredDP(RawDPInterface):
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
