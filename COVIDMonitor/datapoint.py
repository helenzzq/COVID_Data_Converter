class DataPoint:
    """A datapoint of covid data.

    === Private Attributes ===
    datetime: str
      The datetime this datapoint is created.
    
    country_region: str
      Country/Region of this data.
    
    province_state: str
      Province/State of this data.
    
    combined_key: str
      Combines province_state and country_region.
      Format: "[province_state, ]<country_region>"
    
    active: int
      Active cases.
    
    confirmed: int
      Active cases.
    
    deaths: int
      Death cases.

    recovered: int
      Recovered cases.
    """
    datetime: str
    country_region: str
    province_state: str
    combined_key: str
    active: int
    confirmed: int
    deaths: int
    recovered: int

    def __init__(
            self, datetime  ="",
            country_region  ="",
            province_state  ="",
            combined_key    ="",
            active      =0,
            confirmed   =0,
            deaths      =0,
            recovered   =0
        ) -> None:
        self.datetime       = datetime
        self.country_region = country_region
        self.province_state = province_state
        self.combined_key   = combined_key
        self.active         = active
        self.confirmed      = confirmed
        self.deaths         = deaths
        self.recovered      = recovered
