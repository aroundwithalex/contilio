from main import DB_URL
from src.tables import Tables


def build_database():
    """
    Builds database tables

    This method builds database tables. It should be used
    when initialising the database.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        None
    """
    tables = Tables(DB_URL)
    tables.define_station_coords_table()
    tables.define_journey_table()
    tables.create_tables()
