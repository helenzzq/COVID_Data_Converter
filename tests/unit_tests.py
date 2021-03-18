from COVIDMonitor.main import app
from COVIDMonitor.dataparser import DataParser
from COVIDMonitor.dataparser import DataPoint
import unittest, random, ntpath


def test_monitor():
    response = app.test_client().get('/')

    assert response.status_code == 200


parser = DataParser()
TS_GLOBAL = "tests/test_data/time_series_covid19_confirmed_global.csv"
TS_US = "tests/test_data/time_series_covid19_deaths_US.csv"
DR_GLOBAL = "tests/test_data/01-01-2021.csv"
DR_US = "tests/test_data/01-02-2021.csv"
TS_DATE = ['01-22-20', '01-23-20', '01-24-20', '01-25-20', '01-26-20', '01-27-20', '01-28-20', '01-29-20', '01-30-20',
           '01-31-20', '02-1-20', '02-2-20', '02-3-20', '02-4-20', '02-5-20', '02-6-20', '02-7-20', '02-8-20',
           '02-9-20', '02-10-20', '02-11-20', '02-12-20', '02-13-20', '02-14-20', '02-15-20', '02-16-20', '02-17-20',
           '02-18-20', '02-19-20', '02-20-20', '02-21-20', '02-22-20', '02-23-20', '02-24-20', '02-25-20', '02-26-20',
           '02-27-20', '02-28-20', '02-29-20', '03-1-20', '03-2-20', '03-3-20', '03-4-20', '03-5-20', '03-6-20',
           '03-7-20', '03-8-20', '03-9-20', '03-10-20', '03-11-20', '03-12-20', '03-13-20', '03-14-20', '03-15-20',
           '03-16-20', '03-17-20', '03-18-20', '03-19-20', '03-20-20', '03-21-20', '03-22-20', '03-23-20', '03-24-20',
           '03-25-20', '03-26-20', '03-27-20', '03-28-20', '03-29-20', '03-30-20', '03-31-20', '04-1-20', '04-2-20',
           '04-3-20', '04-4-20', '04-5-20', '04-6-20', '04-7-20', '04-8-20', '04-9-20', '04-10-20', '04-11-20',
           '04-12-20', '04-13-20', '04-14-20', '04-15-20', '04-16-20', '04-17-20', '04-18-20', '04-19-20', '04-20-20',
           '04-21-20', '04-22-20', '04-23-20', '04-24-20', '04-25-20', '04-26-20', '04-27-20', '04-28-20', '04-29-20',
           '04-30-20', '05-1-20', '05-2-20', '05-3-20', '05-4-20', '05-5-20', '05-6-20', '05-7-20', '05-8-20',
           '05-9-20', '05-10-20', '05-11-20', '05-12-20', '05-13-20', '05-14-20', '05-15-20', '05-16-20', '05-17-20',
           '05-18-20', '05-19-20', '05-20-20', '05-21-20', '05-22-20', '05-23-20', '05-24-20', '05-25-20', '05-26-20',
           '05-27-20', '05-28-20', '05-29-20', '05-30-20', '05-31-20', '06-1-20', '06-2-20', '06-3-20', '06-4-20',
           '06-5-20', '06-6-20', '06-7-20', '06-8-20', '06-9-20', '06-10-20', '06-11-20', '06-12-20', '06-13-20',
           '06-14-20', '06-15-20', '06-16-20', '06-17-20', '06-18-20', '06-19-20', '06-20-20', '06-21-20', '06-22-20',
           '06-23-20', '06-24-20', '06-25-20', '06-26-20', '06-27-20', '06-28-20', '06-29-20', '06-30-20', '07-1-20',
           '07-2-20', '07-3-20', '07-4-20', '07-5-20', '07-6-20', '07-7-20', '07-8-20', '07-9-20', '07-10-20',
           '07-11-20', '07-12-20', '07-13-20', '07-14-20', '07-15-20', '07-16-20', '07-17-20', '07-18-20', '07-19-20',
           '07-20-20', '07-21-20', '07-22-20', '07-23-20', '07-24-20', '07-25-20', '07-26-20', '07-27-20', '07-28-20',
           '07-29-20', '07-30-20', '07-31-20', '08-1-20', '08-2-20', '08-3-20', '08-4-20', '08-5-20', '08-6-20',
           '08-7-20', '08-8-20', '08-9-20', '08-10-20', '08-11-20', '08-12-20', '08-13-20', '08-14-20', '08-15-20',
           '08-16-20', '08-17-20', '08-18-20', '08-19-20', '08-20-20', '08-21-20', '08-22-20', '08-23-20', '08-24-20',
           '08-25-20', '08-26-20', '08-27-20', '08-28-20', '08-29-20', '08-30-20', '08-31-20', '09-1-20', '09-2-20',
           '09-3-20', '09-4-20', '09-5-20', '09-6-20', '09-7-20', '09-8-20', '09-9-20', '09-10-20', '09-11-20',
           '09-12-20', '09-13-20', '09-14-20', '09-15-20', '09-16-20', '09-17-20', '09-18-20', '09-19-20', '09-20-20',
           '09-21-20', '09-22-20', '09-23-20', '09-24-20', '09-25-20', '09-26-20', '09-27-20', '09-28-20', '09-29-20',
           '09-30-20', '10-1-20', '10-2-20', '10-3-20', '10-4-20', '10-5-20', '10-6-20', '10-7-20', '10-8-20',
           '10-9-20', '10-10-20', '10-11-20', '10-12-20', '10-13-20', '10-14-20', '10-15-20', '10-16-20', '10-17-20',
           '10-18-20', '10-19-20', '10-20-20', '10-21-20', '10-22-20', '10-23-20', '10-24-20', '10-25-20', '10-26-20',
           '10-27-20', '10-28-20', '10-29-20', '10-30-20', '10-31-20', '11-1-20', '11-2-20', '11-3-20', '11-4-20',
           '11-5-20', '11-6-20', '11-7-20', '11-8-20', '11-9-20', '11-10-20', '11-11-20', '11-12-20', '11-13-20',
           '11-14-20', '11-15-20', '11-16-20', '11-17-20', '11-18-20', '11-19-20', '11-20-20', '11-21-20', '11-22-20',
           '11-23-20', '11-24-20', '11-25-20', '11-26-20', '11-27-20', '11-28-20', '11-29-20', '11-30-20', '12-1-20',
           '12-2-20', '12-3-20', '12-4-20', '12-5-20', '12-6-20', '12-7-20', '12-8-20', '12-9-20', '12-10-20',
           '12-11-20', '12-12-20', '12-13-20', '12-14-20', '12-15-20', '12-16-20', '12-17-20', '12-18-20', '12-19-20',
           '12-20-20', '12-21-20', '12-22-20', '12-23-20', '12-24-20', '12-25-20', '12-26-20', '12-27-20', '12-28-20',
           '12-29-20', '12-30-20', '12-31-20', '01-1-21', '01-2-21', '01-3-21', '01-4-21', '01-5-21', '01-6-21',
           '01-7-21', '01-8-21', '01-9-21', '01-10-21', '01-11-21', '01-12-21', '01-13-21', '01-14-21', '01-15-21',
           '01-16-21', '01-17-21', '01-18-21', '01-19-21', '01-20-21', '01-21-21', '01-22-21', '01-23-21', '01-24-21',
           '01-25-21', '01-26-21', '01-27-21', '01-28-21', '01-29-21', '01-30-21', '01-31-21', '02-1-21', '02-2-21',
           '02-3-21', '02-4-21', '02-5-21', '02-6-21', '02-7-21', '02-8-21', '02-9-21', '02-10-21', '02-11-21',
           '02-12-21', '02-13-21', '02-14-21', '02-15-21', '02-16-21', '02-17-21', '02-18-21', '02-19-21', '02-20-21',
           '02-21-21', '02-22-21', '02-23-21', '02-24-21', '02-25-21', '02-26-21', '02-27-21', '02-28-21', '03-1-21',
           '03-2-21', '03-3-21', '03-4-21', '03-5-21', '03-6-21', '03-7-21', '03-8-21', '03-9-21', '03-10-21',
           '03-11-21', '03-12-21', '03-13-21', '03-14-21', '03-15-21', '03-16-21']
TS_GLOBAL_CONF = parser.parse_covid_time_series(TS_GLOBAL)
TS_US_Deaths = parser.parse_covid_time_series(TS_US)
DR_GLOBAL_PARSED = parser.parse_covid_daily_report(DR_GLOBAL)
DR_US_PARSED = parser.parse_covid_daily_report(DR_US)


class TestParser(unittest.TestCase):
    """A unitTest class for testing parsing csv data"""

    def test_time_series_parsing_date(self):
        """Test if we extract the correct date entry for time series data"""
        self.assertEqual(TS_DATE, list(TS_US_Deaths.keys()))
        self.assertEqual(TS_DATE, list(TS_GLOBAL_CONF.keys()))

    def test_time_series_combined_key(self):
        """Test if we input the write combined_key value for each type of time series
        Global time series data has no combined_key column
        """
        index = random.randint(0, 28)
        random_date = TS_DATE[index]
        dp_us = TS_US_Deaths[random_date][1]
        dp_global = TS_GLOBAL_CONF[random_date][1]
        self.assertEqual(dp_global.combined_key, '', "Combined_Key Column should not be in Global time series data")
        self.assertNotEqual(dp_us.combined_key, '', "Combined_Key Column should be in US time series data")

    def test_time_series_incorrect_data_type_entry(self):
        """Test if we extract the wrong data type [Confirmed,Deaths,Active,Recovered] of corresponding csv"""
        index = random.randint(0, 28)
        random_date = TS_DATE[index]
        self.assertNotEqual(TS_US_Deaths[random_date][0].deaths, -1)
        self.assertNotEqual(TS_GLOBAL_CONF[random_date][0].confirmed, -1)

    def test_daily_report_combined_key(self):
        """Test if we input the write combined_key value for each type of time series
        Global time series data has no combined_key column
        """
        index = random.randint(0, 2)
        dp_global = list(DR_GLOBAL_PARSED.values())[0][index]
        dp_us = list(DR_US_PARSED.values())[0][index]
        self.assertNotEqual(dp_global.combined_key, '', "Combined_Key Column should be in in Global Daily report data")
        self.assertEqual(dp_us.combined_key, '', "Combined_Key Column should not be in US Daily report data")

    def test_time_series_confirmed(self):
        expected_dp = [DataPoint('01-22-20', "Afghanistan", "", confirmed=0),
                       DataPoint('01-22-20', "Albania", "", confirmed=0),
                       DataPoint('01-22-20', "Algeria", "", confirmed=0)]
        data_entry = TS_GLOBAL_CONF['01-22-20']
        for k in range(3):
            self.assertEqual(expected_dp[k].confirmed,
                             data_entry[k].confirmed, "Number of Confirmed cases does not match")
            self.assertEqual(expected_dp[k].country_region, data_entry[k].country_region, "Province  does not match")
            self.assertEqual(expected_dp[k].combined_key, data_entry[k].combined_key, "Combined Key  does not match")
            self.assertEqual(expected_dp[k].province_state, data_entry[k].province_state, "Province  does not match")
            # Should not have other category entry other than confirmed
            self.assertEqual(data_entry[k].active, -1)
            self.assertEqual(data_entry[k].recovered, -1)
            self.assertEqual(data_entry[k].deaths, -1)

    def test_parse_daily_report_global(self):
        expected_dp = [DataPoint('01-01-21', "Australia", "Australian Capital Territory",
                                 "Australian Capital Territory, Australia", "Capital Territory", 1, 118, 3, 114),
                       DataPoint('01-01-21', "Australia", "New South Wales",
                                 "New South Wales, Australia", "South Wales", 1696, 4947, 54, 0),
                       DataPoint('01-01-21', "Australia", "Northern Territory",
                                 "Northern Territory, Australia", "Northern Territory", 4, 75, 0, 71)]
        dp = list(DR_GLOBAL_PARSED.values())[0]
        for k in range(3):
            self.assertEqual(expected_dp[k].confirmed, dp[k].confirmed, "Number of Confirmed cases does not match")
            self.assertEqual(expected_dp[k].active, dp[k].active, "Number of Recovered cases does not match")
            self.assertEqual(expected_dp[k].deaths, dp[k].deaths, "Number of Death cases does not match")
            self.assertEqual(expected_dp[k].recovered, dp[k].recovered, "Number of Recovered cases does not match")
            self.assertEqual(expected_dp[k].admin, dp[k].admin, "Administration district does not match")
            self.assertEqual(expected_dp[k].province_state, dp[k].province_state, "Province  does not match")
            self.assertEqual(expected_dp[k].country_region, dp[k].country_region, "Country  does not match")
            self.assertEqual(expected_dp[k].combined_key, dp[k].combined_key, "Combined Key  does not match")

    def test_daily_report_us(self):
        expected_dp = [DataPoint('01-02-21', "US", "Alabama",
                                 "", '', 162449, 369458, 4872, 202137),
                       DataPoint('01-02-21', "US", "Alaska",
                                 "", "", 40421, 47801, 215, 7165),
                       DataPoint('01-02-21', "US", "American Samoa",
                                 "", "", 0, 0, 0, 0)]
        dp = list(DR_US_PARSED.values())[0]
        for k in range(3):
            self.assertEqual(expected_dp[k].confirmed, dp[k].confirmed, "Number of Confirmed cases does not match")
            self.assertEqual(expected_dp[k].active, dp[k].active, "Number of Recovered cases does not match")
            self.assertEqual(expected_dp[k].deaths, dp[k].deaths, "Number of Death cases does not match")
            self.assertEqual(expected_dp[k].recovered, dp[k].recovered, "Number of Recovered cases does not match")
            self.assertEqual(expected_dp[k].admin, dp[k].admin, "Administration district does not match")
            self.assertEqual(expected_dp[k].province_state, dp[k].province_state, "Province  does not match")
            self.assertEqual(expected_dp[k].country_region, dp[k].country_region, "Country  does not match")
            self.assertEqual(expected_dp[k].combined_key, dp[k].combined_key, "Combined Key  does not match")
