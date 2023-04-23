from unittest import TestCase
from src.tables import Tables
from sqlalchemy import create_engine
from src.insert import InsertData

class TestInsertData(TestCase):

    def setUp(self):
        tables = Tables("sqlite:///./tests/test_db.db")
        engine = create_engine("sqlite:///./tests/test_db.db")
        tables.define_station_coords_table()
        tables.define_journey_table()
        tables.create_tables()

        self.insert = InsertData(engine)
    
    def test_insert_station_data(self):
        result = self.insert.insert_station_coords("LBG", 0.12, 0.13)
        self.assertTrue(result)
    
    def test_insert_journey_info(self):
        result = self.insert.insert_journey_info("LBG", "HYK", "2022-02-02", "2022-02-02")
        self.assertTrue(result)


