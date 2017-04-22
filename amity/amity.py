# coding=utf-8
import os
import random
import sqlite3
import sys

from person import Person, Fellow, Staff
from room import Room, LivingSpace, Office

if os.path.exists('amity'):
    os.chdir('amity')


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
        if len(room_list) != 0:
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
            Fellow(name)
            new_id_no = str(id(name))
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
            Staff(name)
            new_id_no = str(id(name))
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
        Allocates office to staff and fellows
        _______________________________________________________
        :param new_id_no: id number of the person
        :return: success or failure message
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
                print("successfully allocated the office: " + workspace)

    def allocate_accommodation(self, new_id_no):
        """
        Allocates random living space to fellows only
        ______________________________________________________________________________
        :param new_id_no: id number of fellow being allocated:
        :return: success or failure message
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
                print("successfully allocated the living space: " + workspace)

    def get_person_id(self, search_name):
        """
        The function receive a search name and prints out the id number of person
        ___________________________________________________________
        :param search_name: Name of person you want to get the id
        :return: prints out id_no of the person being searched
        """
        if search_name not in list(self.employees.values()):
            print("The person is not in system")
        else:
            for id_no, name in self.employees.items():
                if name == search_name:
                    print(id_no)

    def reallocate_person(self, id_no, room_name):
        """
        Reallocates person use the person id number from a certain room to another room
        ______________________________________________________________________________
        :param id_no: unique identifier for the person to be reallocated
        :param room_name: name of the room person to be relocated to
        :return: Success message that person has be successfully reallocate
        """
        vacant_room = []
        new_room = room_name.capitalize()
        if new_room not in self.rooms:
            return "The room " + new_room + " does not exist in amity"
        if new_room in self.accommodations.keys() and len(self.accommodations[new_room]) < 4:
            vacant_room.append(new_room)
        elif new_room in self.offices.keys() and len(self.offices[new_room]) < 6:
            vacant_room.append(new_room)
        for room in vacant_room:
            if id_no in self.staff.keys():
                if room in self.accommodations.keys():
                    return "Staff can not be allocated a living space"
                else:
                    self.offices[room].append(id_no)
                    if id_no in self.offices[room]:
                        print("The person has been successfully moved to: " + room)
            if id_no in self.fellows.keys():
                if room in self.accommodations.keys():
                    self.accommodations[room].append(id_no)
                    if id_no in self.accommodations[room]:
                        print(self.employees[id_no] + " has been successfully moved to: " + room)
                else:
                    self.offices[room].append(id_no)
                    if id_no in self.offices[room]:
                        print(self.employees[id_no] + " has been successfully moved to: " + room)

    def print_room(self, room_name):
        """
        Prints out the members or occupants in the room
        _______________________________________________________________________________
        :param room_name: name of room to print
        :return: prints a list of all occupants in the room
        """
        print_name = room_name.capitalize()
        if print_name not in self.rooms:
            return "There is no room " + print_name + " in system!"
        else:
            print("The members of room " + print_name + ":")
            if print_name in self.rooms:
                if print_name in list(self.offices.keys()):
                    for item in self.offices[print_name]:
                        print(self.employees[item].upper())
                elif print_name in self.accommodations.keys():
                    for item in self.accommodations[print_name]:
                        print(self.employees[item].upper())

    def load_people(self, textfile):
        """
        Load people from a text file to amity
        ____________________________________________________________________________________
        :param textfile:
        :return:
        """
        if not isinstance(textfile, str):
            return TypeError("Amity on accepts string as input")
        elif textfile is not None:
            if os.path.exists('data/input/' + textfile):
                with open('data/input/' + textfile, 'r') as file:
                    people = file.readlines()
                    for person in people:
                        p_details = person.split()
                        role = p_details[0]
                        name = p_details[1] + " " + p_details[2]
                        if len(p_details) > 3:
                            accommodate = p_details[3]
                        else:
                            accommodate = "N"
                        self.add_person(role, name, accommodate)
            else:
                return "The file does not exist!"
        return "People have been successfully load to amity!"

    def print_allocations(self, filename=None):
        """
        Prints out list of all people who have been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param filename:
        :return:
        """
        occupied_rooms = []
        output = "ROOM ALLOCATIONS\n"
        if len(occupied_rooms) == 0:
            return "There are no occupied rooms in amity!"
        for room in self.rooms:
            if room in self.accommodations.keys() and len(self.accommodations[room]) != 0:
                occupied_rooms.append(room)
            elif room in self.offices.keys() and len(self.offices[room]) != 0:
                occupied_rooms.append(room)
        for room_name in occupied_rooms:
            if room_name in self.accommodations.keys():
                output += room_name.upper() + "\n"
                output += "-----------------------------------------------\n"
                output += ", ".join(self.accommodations[room_name]) + "\n"
            elif room_name in self.offices.keys():
                output += room_name.upper() + "\n"
                output += "-----------------------------------------------\n"
                output += ", ".join(self.offices[room_name]) + "\n"
        print(output)
        if filename is not None:
            with open('data/output/' + filename, 'w') as outfile:
                outfile.write(output)
                print("Allocations saved to: {}".format(filename))

    def print_unallocated(self, filename):
        """
        Prints out list of all people who have not been allocated a room and save it to an external .txt file
        ___________________________________________________________________________________________________
        :param filename:
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
            if filename is not None:
                with open('data/output/' + filename, 'w') as outfile:
                    outfile.write(output)
                    print("Allocations saved to: {}".format(filename))

    def save_state(self, args):  # work in progress
        """
        save all data in amity to a specified database
        _____________________________________________________________________________________
        :param args:
        :return:
        """
        if args["--db"]:
            database_name = args["--db"]
        else:
            database_name = "kuokoa.db"
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE IF EXISTS Employees")
        self.cur.execute("DROP TABLE IF EXISTS Rooms")
        self.cur.execute("DROP TABLE IF EXISTS State")
        self.create_table(database_name)

        self.conn.commit()

    def create_table(self, database_name):
        """
        Creates table in the database
        _______________________
        :param database_name:
        :return:
        """
        self.conn = sqlite3.connect(database_name)
        self.cur = self.conn.cursor()

        try:
            self.cur.execute('''CREATE TABLE IF NOT EXISTS Employees(
                                id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Role TEXT, id_no TEXT)''')

            self.cur.execute('''CREATE TABLE IF NOT EXISTS Rooms(
                                        id INTEGER PRIMARY KEY AUTOINCREMENT, Room_Name TEXT, Room_Type TEXT)''')

            self.cur.execute('''CREATE TABLE IF NOT EXISTS State(State BLOB)''')
        except sqlite3.IntegrityError:
            return False

    def load_state(self, args):
        """
        Load application state that was saved in the database
        ___________________________________________________________________________________________________
        :param args:
        :return:
        """
        pass