"""
This module contains the RentApartment class which is a subclass of Base class.
RentApartment class represents the rent_apartments table in the database.
"""

from sqlalchemy import Float, Integer, String, Column
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """ Base class for the SqlAlchemy models """

    pass


class RentApartment(Base):
    """
    RentApartment class is the model class to the rent_apartments table.

    Attributes:
        address: (String) primary key
        area: (Float)
        constraction_year: (Integer)
        rooms: (Integer)
        bedrooms: (Integer)
        bathrooms: (Integer)
        balcony: (String)
        storage: (String)
        parking: (String)
        furnished: (String)
        garage: (String)
        garden: (String)
        energy: (String)
        facilities: (String)
        zip: (String)
        neighborhood: (String)
        rent: (Integer)
    """

    __tablename__ = 'rent_apartments'

    address = Column(String, primary_key=True)
    area = Column(Float)
    constraction_year = Column(Integer)
    rooms = Column(Integer)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    balcony = Column(String)
    storage = Column(String)
    parking = Column(String)
    furnished = Column(String)
    garage = Column(String)
    garden = Column(String)
    energy = Column(String)
    facilities = Column(String)
    zip = Column(String)
    neighborhood = Column(String)
    rent = Column(Integer)
