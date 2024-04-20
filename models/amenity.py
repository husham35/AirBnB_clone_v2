#!/usr/bin/python3
"""
This is the definition of the `amenity class` module
"""

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from models.base_model import Base, BaseModel


class Amenity(BaseModel, Base):
    """
    Defines the class Amenity for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table amenities.

    Attributes:
        __tablename__ (str): the MySQL table to store Amenities.
        name (sqlalchemy String): amenity name.
        place_amenities (sqlalchemy relationship): Place-Amenity relationship.
    """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship(
        "Place", secondary="place_amenity", viewonly=False
    )
