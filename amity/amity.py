# coding=utf-8
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

    def create_room(self, room_name, room_type):
        """
        create rooms in amity that are either of type offices or accommodations
        ________________________________________________________________________
        :param room_name: the unique name of the room
        :param room_type: the type of the room (either offices or accommodations)
        :return: success message
        """
        pass

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