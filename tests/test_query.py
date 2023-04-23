from unittest import TestCase
from src.tables import Tables
from src.insert import InsertData
from src.query import QueryDB
from sqlalchemy import create_engine

class TestQueryDB(TestCase):
    def setUp(self):
        tables = Tables("sqlite:///./tests/test_db.db")
        self.engine = create_engine("sqlite:///./tests/test_db.db")
        tables.define_station_coords_table()
        tables.define_journey_table()
        tables.create_tables()

        self.insert_data = InsertData(self.engine)
        self.query_db = QueryDB(self.engine)
    
    def test_lookup_station(self):
        
        self.insert_data.insert_station_coords("LBG", 0.12, 0.13)
        result = self.query_db.lookup_station("LBG")

        self.assertTrue("long" in result.keys())
    
    def test_lookup_journey(self):

        self.insert_data.insert_journey_info("LBG", "HKY", "2022-01-01", "2022-04-03")

        result = self.query_db.lookup_journey("LBG", "HKY", "2022-01-01")
        self.assertTrue("start_station" in result)
    