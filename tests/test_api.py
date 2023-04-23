from unittest import TestCase
from src.api import TransportAPI
import responses

class TestAPI(TestCase):

    def setUp(self):
        self.transport_api = TransportAPI("some_id", "some_key")
    
    @responses.activate
    def test_get_station_co_ordinates(self):
        responses.add(
            responses.GET,
            "https://transportapi.com/v3/uk/places.json?",
            json={"member": [{'longitude': 0.00, "latitude": 0.00}]},
            status=200
        )
        data = self.transport_api.get_station_co_ordinates("LBG")
        self.assertTrue("long" in data.keys())
    
    @responses.activate
    def test_get_journey_data(self):
        responses.add(
            responses.GET,
            "https://transportapi.com/v3/uk/public_journey.json?",
            json={"response": {"arrival_time": "10:00:00"}}
        )

        data = self.transport_api.get_journey_data (
            from_coords = {"long": 0.00, "lat": 0.00},
            to_coords = {"long": 0.00, "lat": 0.00},
            start_time="2022-02-02 00:00:00"
        )

        self.assertTrue("response" in data.keys())
