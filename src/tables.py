"""
Creates and manages a SQLite database

This method creates and manages a SQLite database. This means
it both creates tables and inserts data as required.

Typical Usage:
    >>> from src.db import Database
    >>> db = Database()
    >>> db.create_tables()
"""

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String


class Tables:
    """
    Creates database tables

    This object contains various methods to define database
    tables. It also includes a method to create these tables.

    Attributes:
        self.engine -> Database engine
        self.metadata -> Metadata object
    """
    def __init__(self, db_url):
        """
        Constructor for Tables object

        This method is the constructor for the Table object. It takes
        a database URL and creates a database engine.

        Args:
            db_url -> Database URL
        
        Returns:
            None
        
        Raises:
            None
        """
        self.engine = create_engine(db_url)
        self.metadata = MetaData()

    def define_station_coords_table(self):
        """
        Defines station_coords table

        This method defines the station_coords table. It can then
        be created by a later method.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        station_coords_table = Table(
            "station_coords",
            self.metadata,
            Column("station_code", String(3), primary_key=True),
            Column("long", String(10), nullable=False, unique=True),
            Column("lat", String(10), nullable=False, unique=True),
        )

        return True

    def define_journey_table(self):
        """
        Defines the journeys table

        This method defines the journeys table. It can then be created
        by a later method.

        Args: 
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        jouney_table = Table(
            "journeys",
            self.metadata,
            Column("journey_id", String(32), primary_key=True),
            Column("start_station", String(3), nullable=False),
            Column("end_station", String(3), nullable=False),
            Column("start_time", String(16), nullable=False),
            Column("arrival_time", String(20), nullable=False),
        )

        return True

    def create_tables(self):
        """
        Creates database tables

        This method creates database tables. It takes the
        schema definitions and utilises the create_all method
        within SQLAlchemy to create the table.

        Args:
            None
        
        Returns:
            None
        
        Raises:
            None
        """
        self.metadata.create_all(self.engine)
        return True
