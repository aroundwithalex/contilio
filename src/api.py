"""
Fetches data from the Transportation API

This module fetches data from the Transportation API, and returns
within a generator.

Typical Usage:
    >>> from api import get_arrival_data
    >>> get_arrival_data()
    "2022-09-12 00:00:00
"""

import requests


class TransportAPI:
    """
    Fetches data from the Transportation API

    This object fetches data from the Transportation API. It returns
    the data within a generator.

    Attributes:
        app_id: App authentication for the API
        app_key: Key for accessing the app
    """

    def __init__(self, app_id, app_key):
        """
        Constructor for Transport API class

        Takes the two keys required to access the API and saves as
        instance variables. Includes the URL for the API.

        Args:
            app_id -> App ID key
            app_key -> App Key for authentication

        Returns:
            None

        Raises:
            None
        """

        self.app_id = app_id
        self.app_key = app_key

        self.base_url = (
            "https://developer.transportapi.com/v3/uk/train/station_actual_journeys"
        )

    def get_station_co_ordinates(self, station_code):
        """
        Gets co-ordinates of a train station

        This method gets the co-ordinates of a train station. It is then
        used in the journey planner API to get relevant data points.

        Args:
            station_code -> Code of station to look up

        Returns:
            Station co-ordinates

        Raises:
            None
        """

        params = {
            "query": station_code,
            "type": "train_station",
            "app_id": self.app_id,
            "app_key": self.app_key,
        }

        response = requests.get(
            "https://transportapi.com/v3/uk/places.json?", params=params
        )
        latitude = response.json()["member"][0]["latitude"]
        longtitude = response.json()["member"][0]["longitude"]
        return {"lat": latitude, "long": longtitude}

    def get_journey_data(self, from_coords, to_coords, start_time):
        """
        Prepares URL for HTTP request

        This method constructs a URL for an HTTP request. It
        does this by adding a station code and start time, along
        with authentication parameters.

        Args:
            station_code -> Station code to add to URL
            start_time -> Start time to add to URL

        Returns:
            Formatted URL

        Raises:
            None
        """

        date, time = start_time.split()

        params = {
            "from": f"lonlat:{from_coords['long']},{from_coords['lat']}",
            "to": f"lonlat:{to_coords['long']},{to_coords['lat']}",
            "date": date[1::],
            "time": time,
            "app_key": self.app_key,
            "app_id": self.app_id,
        }

        response = requests.get(
            f"https://transportapi.com/v3/uk/public_journey.json?",
            params=params,
        )

        return response.json()
