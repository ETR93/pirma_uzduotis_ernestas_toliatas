import requests
import pandas as pd
import datetime
from helpers import check_amount_of_requests

class GetData:

    def __init__(self, place_code):
        self.place_code = place_code

    def historical_data(self):
        """
        This method returns the historical data as pandas dataFrame from the meteo.lt API.
        :return:
        """
        data_frame_list = []
        requests_count = 0
        response_data = {}
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")
        if len(start_date.split('-')) != 3:
            return "Invalid start date"
        if  len(end_date.split('-')) != 3:
            return "Invalid end date"
        dates = list(pd.date_range(start=start_date, end=end_date, tz='UTC'))
        for date in dates:
            response = requests.get("https://api.meteo.lt/v1/stations/{0}-ams/observations/{1}".format(
                self.place_code, date.strftime('%Y-%m-%d')
            ))
            if response.status_code == 404:
                return "Invalid place code"
            response_data.update({date.strftime('%Y-%m-%d'): response.json()})
            requests_count = check_amount_of_requests(requests_count)
        for date, data in response_data.items():
            station = data['station']
            for obs in data["observations"]:
                row = {
                    "date": date,
                    "station_code": station["code"],
                    "station_name": station["name"],
                    "latitude": station["coordinates"]["latitude"],
                    "longitude": station["coordinates"]["longitude"],
                    **obs
                }
                data_frame_list.append(row)
        response_data = pd.DataFrame(data_frame_list)
        response_data["observationTimeUtc"] = pd.to_datetime(response_data["observationTimeUtc"])
        return response_data

    def get_forecast_date(self):
        """
        This method returns forecast data as pandas dataFrame from the meteo.lt API.
        :return:
        """
        response_data = {}
        now = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        date_after_week = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(7), '%Y-%m-%d')
        dates = pd.date_range(start=now, end=date_after_week, tz='UTC')
        for date in dates:
            response = requests.get("https://api.meteo.lt/v1/places/{0}/forecasts/long-term".format(self.place_code))
            if response.status_code == 404:
                return "Invalid place code"
            response_data.update({date.strftime('%Y-%m-%d'): response.json()})
        response_data = pd.DataFrame(response_data)
        return response_data