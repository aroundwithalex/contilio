from src.api import TransportAPI
from src.tables import Tables
from src.insert import InsertData
from src.query import QueryDB
from sqlalchemy import create_engine

from dateparser import parse

DB_URL = "sqlite:///./trains.db"

def build_database():

    tables = Tables(DB_URL)
    tables.define_station_coords_table()
    tables.define_journey_table()
    tables.create_tables()

def get_journey_data(stations, start_time, max_wait):
    engine = create_engine(DB_URL)

    api = TransportAPI("ec2d4066", "ed0a241765e5f6c57b5668779041b319")

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
