from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import requests
import numpy as np
from yoyoweather import secret

import sys


class WeatherApi(object):

    def city2coord(self, city):
        """
        Get latitude and longitude for a given city from geopy
        """
        geolocator = Nominatim()
        location = geolocator.geocode(city)
        if location is None:
            raise CityNotFoundError(city)
            return None, None
        return location.longitude, location.latitude

    def forecastio_query(self, query):
        """
        Use api.forecast.io to get weather data for a specific
        lat,long and time.
        Returns 24 hours data from a given start point.
        """
        r = requests.get(query)
        htemp = np.empty(shape=24)
        hhumi = np.empty(shape=24)
        try:
            for i, v in enumerate(r.json()['hourly']['data']):
                htemp[i] = v['temperature']
            for i, v in enumerate(r.json()['hourly']['data']):
                hhumi[i] = v['humidity']
        except KeyError as e:
            raise KeyError("No " + str(e) +
                           " field for given place and period")
        dtempavg = np.average(htemp)
        dhumiavg = np.average(hhumi)
        dtempmedian = np.median(np.array(htemp))
        dhumimedian = np.median(np.array(hhumi))
        return htemp, hhumi, dtempavg, dhumiavg, dtempmedian, dhumimedian

    def get_api_response(self, city, from_date, to_date):
        """
        convert timestamp string into datetime object
        """
        from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M')
        to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M')
        date_diff = to_date - from_date
        str_fromdate = datetime.strftime(from_date, '%Y-%m-%dT%H:%M')
        nobs = date_diff.seconds/3600
        nobs += date_diff.days*24
        try:
            temps = np.empty(shape=(nobs, 24))
            humis = np.empty(shape=(nobs, 24))
        except ValueError as e:
            raise ValueError("from_date is after to_date!")
        lon, lat = self.city2coord(city)
        for i in xrange(nobs):
            iterdate = from_date + timedelta(hours=i)
            nextdate = datetime.strftime(iterdate, '%Y-%m-%dT%H:%M:%S')
            querystring = ('https://api.forecast.io/forecast/' +
                           secret.forecastkey +
                           str(lat) +
                           ',' + str(lon) + ',' + nextdate)
            res = self.forecastio_query(querystring)
            assert res is not None, "api.forecast.io returned empty result"
            temps[i] = res[0]
            humis[i] = res[1]
        res = {
            'Temp. Min': str(np.min(temps)) +' deg. Celsius',
            'Temp. Max': str(np.max(temps)) + ' deg. Celsius',
            'Temp. Avg.': str(np.average(temps)) + ' deg. Celsius',
            'Temp. Median': str(np.median(temps)) + ' deg. Celsius',
            'Humidity Min': str(np.min(humis)) + '%',
            'Humidity Max': str(np.max(humis)) + '%',
            'Humidity Avg.': str(np.average(humis)) + '%',
            'Humidity Median': str(np.median(humis)) + '%'
        }
        return res


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class CityNotFoundError(Error):
    """Exception raised if city name not found"""
    def __init__(self, city):
        Error.__init__(self, city + " not found by geopy")


def api_call(city, from_date, to_date):
    api = WeatherApi()
    return api.get_api_response(city, from_date, to_date)
