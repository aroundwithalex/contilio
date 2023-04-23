"""
Inserts data into the SQLite database

This module inserts data into the SQLite database. It
does this by using various aspects of the SQLAlchemy
API.

Typical Usage:
    >>> from src.insert import InsertData
    >>> insert = InsertData(engine)
    >>> insert_station_coords(station_data)
    True
"""

from hashlib import md5

from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.sqlite import insert


class InsertData:
    """
    Inserts data into the database

    This class contains methods to insert data into the database. It
    typically upserts data based on various unique characteristics.

    Attributes:
        self.engine -> Database engine
        self.coord_table -> Coordinates table
        self.journey_table -> Journey table
    """

    def __init__(self, engine):
        """
        Constructor for InsertData

        Builds the InsertData object by taking an engine and creating
        various table objects.

        Args:
            engine -> Database engine

        Returns:
            None

        Raises:
            None
        """
        self.engine = engine
        metadata = MetaData()

        self.coords_table = Table("station_coords", metadata, autoload_with=engine)

        self.journey_table = Table("journeys", metadata, autoload_with=engine)

    def insert_station_coords(self, code, long, lat):
        """
        Inserts data into station_coords table

        This method inserts data into the station_coords table. It
        takes a station code, longitude and latitute and upserts based
        on the station code.

        Args:
            code -> Station Code
            long -> Longitude
            lat -> Latitude

        Returns:
            True if the insert was successful

        Raises:
            None
        """
        stmt = insert(self.coords_table).values(station_code=code, long=long, lat=lat)
        stmt = stmt.on_conflict_do_nothing(index_elements=["station_code"])
        with self.engine.begin() as conn:
            conn.execute(stmt)

        return True

    def insert_journey_info(self, start_station, end_station, start_time, arrival_time):
        """
        Inserts data in the journey table

        This method inserts data into the journeys table. It takes
        a start_station, end_station, start_time and arrival_time and
        upserts based on a row hash.

        Args:
            start_station -> Start station for journey
            end_station -> End station for journey
            start_time -> Start time of journey
            arrival_time -> Arrival time of journey

        Return:
            True

        Raises:
            None
        """
        value_hash = md5(
            f"{start_station}{end_station}{start_time}{arrival_time}".encode("utf-8")
        ).hexdigest()
        stmt = insert(self.journey_table).values(
            journey_id=value_hash,
            start_station=start_station,
            end_station=end_station,
            start_time=start_time,
            arrival_time=arrival_time,
        )
        stmt = stmt.on_conflict_do_nothing(index_elements=(["journey_id"]))
        with self.engine.begin() as conn:
            conn.execute(stmt)

        return True
