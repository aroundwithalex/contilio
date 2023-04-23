"""
Queries the database and returns data

This module contains methods to query the database and return
data contained within it. It is typically used to speed up
runs of code.

Typical Usage:
    >>> from src.query import QueryDB
    >>> query = QueryDB(engine)
    >>> query.check_journey_exists()
    True
"""

from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy import Table
from sqlalchemy import and_


class QueryDB:
    """
    Queries the database and returns results

    This class queries the database and returns relevant database results. It
    looks up both station and journey data and returns for usage.

    Attributes:
        self.engine -> Database Engine
        self.metadata -> Metadata object
    """
    def __init__(self, engine):
        """
        Constructor for QueryDB

        This method is the constructor for the QueryDB object. It instantiates
        two variables: engine and metadata, for later use in the program.

        Args:
            engine -> Database engine
        
        Returns:
            None
        
        Raises:
            None
        """
        self.engine = engine
        self.metadata = MetaData()

    def lookup_station(self, station_code):
        """
        Lookups up station codes

        This method looks up station codes and returns for use within
        the program. This should be used when trying to avoid making
        API calls.

        Args:
            station_code -> Station code to look up
        
        Returns:
            Dictionary of returned data
        
        Raises:
            None
        """
        coords_table = Table("station_coords", self.metadata, autoload_with=self.engine)
        with Session(self.engine) as session:
            query = session.query(coords_table).filter(
                coords_table.c.station_code.like(station_code)
            )
            result = session.execute(query)
        
        data = result.fetchall()
        
        return_value = {}
        if len(data) >= 1:
            return_value["long"] = data[0][1]
            return_value["lat"] = data[0][2]

        return return_value

    def lookup_journey(self, start_station, end_station, start_time):
        """
        Looks up journey data

        This method looks up journey data by utilising the start
        and end station data, along with a start time. It then returns
        data within a dictionary, which can be empty if no matches are
        found.

        Args:
            start_station -> Three letter station code
            end_station -> Three letter end station code
            start_time -> Start time of the journey
        
        Returns:
            Dictionary of data
        
        Raises:
            None
        """
        journey_table = Table("journeys", self.metadata, autoload_with=self.engine)
        with Session(self.engine) as session:
            query = session.query(journey_table).filter(
                and_(
                    journey_table.c.start_station.like(start_station),
                    journey_table.c.end_station.like(end_station),
                    journey_table.c.start_time.like(start_time),
                )
            )
            result = session.execute(query)
        
        data = result.fetchall()

        return_value = {}
        if len(data) >= 1:
            return_value["start_station"] = data[0][1]
            return_value["end_station"] = data[0][2]
            return_value["start_time"] = data[0][3]
            return_value["arrival_time"] = data[0][4]

        return return_value
