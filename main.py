import os

from dateparser import parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

from src.api import TransportAPI
from src.insert import InsertData
from src.query import QueryDB
from src.tables import Tables

DB_URL = "sqlite:///./trains.db"

def get_journey_data(stations, start_time, max_wait):
    """
    Calculates journey times and returns

    This function calcultes journey times and prints the arrival
    time of a train to the console. If the arrival time is longer
    than the maximum wait time, an error is raised.

    Args:
        stations -> Stations to wait at
        start_time -> Start time of journey
        max_wait -> Maximum wait time
    
    Returns:
        None
    
    Raises:
        None
    """
    load_dotenv()
    engine = create_engine(DB_URL)

    app_id = os.environ.get("APP_ID")
    app_key = os.environ.get("APP_KEY")
    api = TransportAPI(app_id, app_key)

    insert_data = InsertData(engine)
    query_data = QueryDB(engine)

    start_coords = query_data.lookup_station(stations[0])
    if not start_coords:
        start_coords = api.get_station_co_ordinates(stations[0])
        insert_data.insert_station_coords(stations[0], start_coords["long"], start_coords["lat"])

    end_coords = query_data.lookup_station(stations[-1])
    if not end_coords:
        end_coords = api.get_station_co_ordinates(stations[-1])
        insert_data.insert_station_coords(stations[0], start_coords["long"], start_coords["lat"])
    
    item = query_data.lookup_journey(stations[0], stations[-1], start_time)
    if not item:
        journey_data = api.get_journey_data(start_coords, end_coords, start_time)
        arrival_time = journey_data["routes"]["arrival_time"]
        insert_data.insert_journey_info(stations[0], stations[-1], start_time, arrival_time)
    else:
        arrival_time = item["arrival_time"]

    first_date = parse(start_time)
    second_date = parse(arrival_time)
    
    minutes_diff = (second_date - first_date).total_seconds() / 60.0
    if minutes_diff > max_wait:
        raise Exception("The wait times are too long")

    print(arrival_time)

if __name__ == "__main__":
    stations = [ 'LBG' , 'SAJ' , 'NWX' , 'BXY' ]
    start_time = "2022-02-09 14:17"
    get_journey_data(stations, start_time, max_wait=60)
