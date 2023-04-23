from unittest import TestCase
from src.tables import Tables

class TestTables(TestCase):
    
    def setUp(self):

        self.tables = Tables("sqlite:///./tests/test_db.db")
    
    def test_define_station_coords(self):

        result = self.tables.define_station_coords_table()
        self.assertTrue(result)
    
    def test_define_journey_table(self):

        result = self.tables.define_journey_table()
        self.assertTrue(result)
    
    def test_create_tables(self):

        result = self.tables.create_tables()
        self.assertTrue(result)
