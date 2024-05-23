#!/usr/bin/python3
"""
This is a module that contains the BaseModel class,
it contains all the definitions for methods/attributes of
the BaseModel class that will be inherited by other classes
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

import models

Base = declarative_base()


class BaseModel:
    """
    Definition for the BaseModel class

    Attributes:
        id (sqlalchemy String): BaseModel id.
        created_at (sqlalchemy DateTime): datetime at creation.
        updated_at (sqlalchemy DateTime): datetime of last update.
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize the BaseModel class.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
        if "id" not in kwargs:
            self.id = str(uuid4())
        if "created_at" not in kwargs:
            self.created_at = datetime.utcnow()
        if "updated_at" not in kwargs:
            self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def save(self):
        """
        Updates the public instance attribute updated_at
        with the current datetime
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Makes a dictionary containing all the key/values of __dict__
        of the instance:
            -by using `self.__dict__`, only instance attributes set will
              be returned
            -a key __class__ must be added to this dictionary with the
              of the object
            -created_at/updated_at must be converted to string object
              in ISO formatr
        Returns:
            a dictionary containing all keys/values of __dict__ of the instance
        """
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = str(type(self).__name__)
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """
        Deletes the current instance from storage.
        """
        models.storage.delete(self)

    def __str__(self):
        """
        Returns the print/str representation of the BaseModel instance.
        """
        return "[{}] ({}) {}".format(
            {type(self).__name__}, ({self.id}), {self.__dict__})
