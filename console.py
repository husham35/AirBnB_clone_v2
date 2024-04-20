#!/usr/bin/python3
""" 
This module is the entry point of the command line interpreter for the
program
"""

import sys
import cmd

from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = "(hbnb) " if sys.__stdin__.isatty() else ""

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "Place": Place,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Review": Review,
    }

    data_types = {
        "number_rooms": int,
        "number_bathrooms": int,
        "max_guest": int,
        "price_by_night": int,
        "latitude": float,
        "longitude": float,
    }
    
    obj_cmds = ["all", "count", "show", "destroy", "update"]
    
    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("(hbnb)")

    def precmd(self, line):
        """
        Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ""  # initialize line elements

        # scan for general formatting - i.e '.', '(', ')'
        if "." not in line or "(" not in line or ")" not in line:
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[: pline.find(".")]

            # isolate and validate <command>
            _cmd = pline[pline.find(".") + 1:pline.find("(")]
            if _cmd not in HBNBCommand.obj_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find("(") + 1:pline.find(")")]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(", ")  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('"', "")
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
            if pline:
                # check for *args or **kwargs
                if (
                    pline[0] == "{" and pline[-1] == "}" and
                        type(eval(pline)) is dict
                ):
                    _args = pline
                else:
                    _args = pline.replace(",", "")
                    # _args = _args.replace('\"', '')
            line = " ".join([_cmd, _cls, _id, _args])

        except Exception:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print("(hbnb) ", end="")
        return stop

    def do_quit(self, command):
        """Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """Prints the help documentation for quit"""
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help documentation for EOF"""
        print("Exits the program without formatting\n")

    def emptyline(self):
        """Overrides the empty line method of CMD"""
        pass


    def do_create(self, line):
        """Create an object of any class"""
        if not line:
            print("** class name missing **")
            return

        # split the line string into args list
        args = line.split()
        class_name = args[0]
        if class_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        # slice the args list to drop the class_name
        args = args[1:]

        # create a dictionary for instatiating a new object from a class
        kwargs = {}

        # iterate over every parameter in the args list
        # and parse each parameter
        for param in args:
            param = param.split("=")

            if len(param) != 2:
                # skip this 'bad' parameter
                continue

            key = param[0]
            value = param[1]

            # check if value of param starts & ends with double quotes
            # we have a string value
            # strip starting and ending double quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
                value = value.replace("_", " ")
                # replace all escaped quotes with quotes
                value = value.replace('\\"', '"')
            # check if value is a float
            elif "." in value:
                # cast it into a float
                try:
                    value = float(value)
                # if cast fails, skip curr param
                except Exception:
                    continue
            # for any other format of value
            else:
                # try to cast it into an int
                try:
                    value = int(value)
                # if cast fails, skip curr param    
                except Exception:
                    continue

            # add the key and parsed value to the kwargs dictionary
            kwargs[key] = value

        # instantiate the new object using the class_name &
        # provided params stored in the kwargs dictionary
        new_obj_instance = HBNBCommand.classes[class_name](**kwargs)
        new_obj_instance.save()
        print(new_obj_instance.id)


    def help_create(self):
        """Help information for the create method"""
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """Method to show an individual object"""
        new = args.partition(" ")
        cmd_name = new[0]
        cmd_id = new[2]

        # guard against trailing args
        if cmd_id and " " in cmd_id:
            cmd_id = cmd_id.partition(" ")[0]

        if not cmd_name:
            print("** class name missing **")
            return

        if cmd_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cmd_id:
            print("** instance id missing **")
            return

        key = f"{cmd_name}.{cmd_id}"
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Help information for the show command"""
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """Destroys a specified object"""
        new = args.partition(" ")
        cmd_name = new[0]
        cmd_id = new[2]
        if cmd_id and " " in cmd_id:
            cmd_id = cmd_id.partition(" ")[0]

        if not cmd_name:
            print("** class name missing **")
            return

        if cmd_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not cmd_id:
            print("** instance id missing **")
            return

        key = f"{cmd_name}.{cmd_id}"

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Help information for the destroy command"""
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(" ")[0]  # remove possible trailing args
            if args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for key, value in storage.all(args).items():
                if key.split(".")[0] == args:
                    print_list.append(str(value))
        else:
            for key, value in storage.all().items():
                print_list.append(str(value))

        print(print_list)

    def help_all(self):
        """Help information for the all command"""
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        count = sum(
            1
            for k, v in storage._FileStorage__objects.items()
            if args == k.split(".")[0]
        )
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """Updates a certain object with new info"""
        cmd_name = cmd_id = attr_name = attr_val = kwargs = ""

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.partition(" ")
        if args[0]:
            cmd_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if cmd_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # isolate id from args
        args = args[2].partition(" ")
        if args[0]:
            cmd_id = args[0]
        else:  # id not present
            print("** instance id missing **")
            return

        # generate key from class and id
        key = f"{cmd_name}.{cmd_id}"

        # determine if key is present
        if key not in storage.all():
            print("** no instance found **")
            return

        # first determine if kwargs or args
        if "{" in args[2] and "}" in args[2] and type(eval(args[2])) is dict:
            kwargs = eval(args[2])
            args = []
            for key, value in kwargs.items():
                args.extend((key, value))
        else:  # isolate args
            args = args[2]
            if args and args[0] == '"':  # check for quoted arg
                second_quote = args.find('"', 1)
                attr_name = args[1:second_quote]
                args = args[second_quote + 1:]

            args = args.partition(" ")

            # if attr_name was not quoted arg
            if not attr_name and args[0] != " ":
                attr_name = args[0]
            # check for quoted val arg
            if args[2] and args[2][0] == '"':
                attr_val = args[2][1:args[2].find('"', 1)]

            # if attr_val was not quoted arg
            if not attr_val and args[2]:
                attr_val = args[2].partition(" ")[0]

            args = [attr_name, attr_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for i, attr_name in enumerate(args):
            # block only runs on even iterations
            if i % 2 == 0:
                attr_val = args[i + 1]  # following item is value
                if not attr_name:  # check for attr_name
                    print("** attribute name missing **")
                    return
                if not attr_val:  # check for attr_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if attr_name in HBNBCommand.data_types:
                    attr_val = HBNBCommand.data_types[attr_name](attr_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({attr_name: attr_val})
        # save updates to file
        new_dict.save()
        storage.save()

    def help_update(self):
        """Help information for the update class"""
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
