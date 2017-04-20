# coding=utf-8
import os
import random
import sqlite3 as db
import sys
from termcolor import colored
from person import Person,Fellow,Staff
from room import Room, LivingSpace, Office


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

    def add_person(self, role, name, accommodate="N"):
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
        self.allocated = False
        if role.upper() == "FELLOW":
            new_employee = Fellow(name)
            new_id_no = str(id(new_employee))
            self.employees[new_id_no] = name
            self.fellows[new_id_no] = name
            self.allocate_office(new_id_no)

            if accommodate == "Y":
                self.allocate_accommodation(new_id_no)

            if not self.allocated:
                self.unallocated.append(new_id_no)

            if new_id_no in self.employees.keys() and self.fellows.keys():
                return "The fellow " + name + " has been added successfully to the system"
            else:
                return "error!!! person not add properly"

        elif role.upper() == "STAFF":
            new_employee = Staff(name)
            new_id_no = str(id(new_employee))
            self.employees[new_id_no] = name
            self.staff[new_id_no] = name
            self.allocate_office(new_id_no)

            if accommodate == "Y":  # check that amity does not allocate staff accommodation
                print("staff can not be allocated accommodation")

            if not self.allocated:
                self.unallocated.append(new_id_no)

            if new_id_no in self.employees.keys() and self.staff.keys():
                return "The staff " + name + " has been added successfully to the system"
            else:
                return "error!!! person not add properly"

        else:
            return "Please specify the persons role"

    def allocate_office(self, new_id_no):
        """

        :param new_id_no:
        :return:
        """
        if len(self.rooms) == 0:
            msg = "The system has no available rooms"
            return msg

        vacant_offices = []
        for room in self.rooms:
            if room in self.offices.keys() and len(self.offices[room]) < 6:
                vacant_offices.append(room)
        if len(vacant_offices) == 0:
            print("The system has no available office space")
        else:
            workspace = random.choice(vacant_offices)
            self.offices[workspace].append(new_id_no)
            self.allocated = True
            if new_id_no in self.offices[workspace]:
                print("office allocated successfully")

    def allocate_accommodation(self, new_id_no):
        """
        :param new_id_no:
        :return:
        """
        if len(self.rooms) == 0:
            msg = "The system has no available rooms"
            return msg

        vacant_accommodation = []
        for room in self.rooms:
            if room in self.accommodations.keys() and len(self.accommodations[room]) < 4:
                vacant_accommodation.append(room)
        if len(vacant_accommodation) == 0:
            print("The system has no available accommodations")
        else:
            workspace = random.choice(vacant_accommodation)
            self.accommodations[workspace].append(new_id_no)
            self.allocated = True
            if new_id_no in self.accommodations[workspace]:
                print("allocated accommodation successfully")

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
        if room_name not in self.rooms:
            return "There is no search room in system!"
        else:
            print("The members of room " + room_name + ":")
            if room_name in self.rooms:
                if room_name in list(self.offices.keys()):
                    for item in self.offices[room_name]:
                        print(self.employees[item])
                elif room_name in self.accommodations.keys():
                    for item in self.accommodations[room_name]:
                        print(self.employees[item])

    def load_people(self, args):
        """
        Load people from a text file to amity
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        txtfile = arg["<filename>"]
        with open('data/inputs/' + txtfile, 'r') as loadfile:
            people = loadfile.readlines()
            for msee in people:
                msee = msee.split()
                role = msee[0]
                name = msee[1]
                name += " " + msee[2]
                if len(msee) == 4:
                    accommodate = msee[3]
                else:
                    accommodate = "N"
                self.add_person(role, name, accommodate)



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
        if len(self.unallocated) == 0:
            return "There are no unallocated people"
        else:
            output = "UNALLOCATED PEOPLE"
            output += "________________________________"
            for item in self.unallocated:
                output += item
            print(output)
            if arg["--o"]:
                with open(args["--o"], 'wt') as file:
                    file.write(output)
                    print("Unallocated saved to: {}".format(args["--o"])


    def load_state(self, args):
        """
        Load application state that was saved in the database
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass