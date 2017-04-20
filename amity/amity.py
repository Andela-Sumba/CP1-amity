# coding=utf-8
import os
import random
import sqlite3 as db

from amity.person import Person,Fellow,Staff
from amity.room import Room, LivingSpace, Office


class Amity(object):
    """
        Amity class:
        ________________________________________________________________________________
        Amity class models a room allocation system for one of
        Andela's facilities called Amity. Amity creates rooms which can
        be offices or living spaces. An office has maximum of 6
        people allocated to it. A living space can accommodate maximum of 4 people.
        Amity also creates and allocates a person rooms. A person to be allocated
        could be a fellow or staff. Staff cannot be allocated living
        spaces. Fellows have a choice to choose a living space or not.
        This system will be used to automatically allocate spaces to
        people at random.

        Data structures:
        ______________________
        rooms(list): contains a list of all rooms in the system
        office(dict): This is a dict of all IDs of offices in the amity system
        accommodations(dict): This is a dict of all IDs of accommodations in the amity system
        employees(dict): This is a dict of all IDs of employees in the amity system
        fellows(dict): This is a dict of all IDs of fellows in the amity system
        staff(dict): This is a dict of all IDs of staff in the amity system
        unallocated(list): This a list of all unallocated people
        allocated(list): List of all allocated people

    """
    def __init__(self):
        self.rooms = []
        self.offices = {}
        self.accommodations = {}
        self.employees = {}
        self.fellows = {}
        self.staff = {}
        self.unallocated = []
        self.allocated = []

    def create_room(self, room_list):
        """
        create rooms in amity that are either of type offices or accommodations
        ________________________________________________________________________
        :param room_list: the unique list of room names
        :return: success message
        """
        total_rooms = len(self.rooms)
        for name in room_list:
            if name in self.rooms:
                name_index = self.rooms.index(name)
                self.rooms.pop(name_index)
                print("The room " + name + " already exists cannot create duplicate rooms")
        if "office" in room_list:
            room_list.pop()
            for room_name in room_list:
                Office(room_name)
                self.rooms.append(room_name)
                self.offices[room_name] = []
            new_total_rooms = len(self.rooms)
            if new_total_rooms-total_rooms > 1:
                return str(new_total_rooms-total_rooms) + " offices have been successfully created"
            else:
                return " The office has been created successfully!"

        elif "livingspace" in room_list:
            room_list.pop()
            for room_name in room_list:
                LivingSpace(room_name)
                self.rooms.append(room_name)
                self.accommodations[room_name] = []
            new_total_rooms = len(self.rooms)
            if new_total_rooms - total_rooms > 1:
                return str(new_total_rooms - total_rooms) + " living spaces have been successfully created"
            else:
                return "The living space has been created successfully!"
        else:
            for room_name in room_list:
                Office(room_name)
                self.rooms.append(room_name)
                self.offices[room_name] = []
            new_total_rooms = len(self.rooms)
            if new_total_rooms-total_rooms > 1:
                return str(new_total_rooms-total_rooms) + " offices have been successfully created"
            else:
                return " The office has been created successfully!"

    def add_person(self, name, role, accommodate="N"):
        """
        adds people to amity that are either fellows or staff and the person has
        a choice to either want accommodation or not
        __________________________________________________________________________
        :param name: name of the person to be added to system
        :param role: role of the person in Andela (fellow|staff)
        :param accommodate: Y or N
        :return: success messages that person added successfully, added to office
                 successfully, and added to living space successfully
        """
        pass

    def reallocate_person(self, id_no, room_name):
        """
        Reallocates person use the person id number from a certain room to another room
        ______________________________________________________________________________
        :param id_no: unique identifier for the person to be reallocated
        :param room_name: name of the room person to be relocated to
        :return: Success message that person has be successfully reallocate
        """
        pass

    def print_room(self, room_name):
        """
        Prints out the members or occupants in the room
        _______________________________________________________________________________
        :param room_name: name of room to print
        :return: prints a list of all occupants in the room
        """
        pass

    def load_people(self, args):
        """
        Load people from a text file to amity
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass

    def save_state(self, args):
        """
        save all data in amity to a specified database
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass

    def print_allocation(self, args):
        """
        Prints out list of all people who have been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass

    def print_unallocated(self, args):
        """
        Prints out list of all people who have not been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass

    def load_state(self, args):
        """
        Load application state that was saved in the database
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass