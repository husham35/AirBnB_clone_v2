#!/usr/bin/python3
"""
This is a module contains the definition of the DBStorage class
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """
    This class defines a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): SQLAlchemy engine.
        __session (sqlalchemy.Session): SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize a new database Storage instance.
        """
        USER = getenv("HBNB_MYSQL_USER")
        PWD = getenv("HBNB_MYSQL_PWD")
        HOST = getenv("HBNB_MYSQL_HOST")
        DB = getenv("HBNB_MYSQL_DB")
        URL = "mysql+mysqldb://{}:{}@{}:3306/{}".format(
            USER, PWD, str(HOST), DB)
        
        self.__engine = create_engine(URL, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the database session for all objects of a class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """
        Adds a new obj to the database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes to the database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an obj from the  database session.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database and initialize a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        session = scoped_session(session_factory)
        self.__session = session()

    def close(self):
        """
        Closes the working SQLAlchemy session.
        """
        self.__session.close()
