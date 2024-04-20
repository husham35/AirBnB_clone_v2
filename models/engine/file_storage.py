#!/usr/bin/python3
"""
This is a module contains the definition of the FileStorage class
"""

import json
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """
    This class serializes instances to a JSON file and desrializes
    JSON file to instances
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns: the dictionary `__objects`
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            return {
                key: value
                for key, value in self.__objects.items()
                if isinstance(value, cls)
            }
        return self.__objects

    def new(self, obj):
        """
        Sets in `__objects` the `obj` with key <obj class name>.id
        """
        self.all().update({obj.to_dict()["__class__"] + "." + obj.id: obj})

    def save(self):
        """
        Serializes `__objects` to the JSON file `__file_path`
        """
        with open(FileStorage.__file_path, "w", encoding="UTF-8") as file:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, file)

    def reload(self):
        """
        Deserializes the JSON file to `__objects` if `__file_path`
        exists, else nothing
        """
        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
        }
        try:
            temp = {}
            with open(FileStorage.__file_path, "r", encoding="UTF-8") as file:
                temp = json.load(file)
                for key, val in temp.items():
                    self.all()[key] = classes[val["__class__"]](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        try:
            del self.__objects["{}.{}".format(type(obj).__name__, obj.id)]
        except (AttributeError, KeyError):
            pass

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
