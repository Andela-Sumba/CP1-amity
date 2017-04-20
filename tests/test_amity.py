# coding=utf-8
import os
import unittest
import sqlite3

from amity.amity import Amity
from amity.person import Person
from amity.room import Room

class TestAmity(unittest.TestCase):
    """
    Tests the amity system core functions
    """
    def setUp(self):
        self.amity = Amity()
        # creating office space
        self.amity.create_room(["void", "office"])
        # creating living space
        self.amity.create_room(["belta", "livingspace"])
        # adding fellows to amity
        self.amity.add_person("Daniel Sumba", "fellow", "y")
        self.amity.add_person("Roronoa Zoro", "fellow", "y")
        self.amity.add_person("Vinsmoke Sanji", "fellow", "n")
        # adding staff to amity
        self.amity.add_person("Roronoa Zoro", "staff")
        self.amity.add_person("Excalibur Teno", "staff")
        self.amity.add_person("Bosalino kizaru", "staff")

    def test_create_room(self):
        """Tests that amity creates rooms of either office or living space"""
        self.assertEqual(2, len(self.amity.rooms))
        self.assertEqual(1, len(self.amity.offices))
        self.assertEqual(1, len(self.amity.accommodations))
        self.assertEqual("void", self.amity.rooms[0])

    def test_amity_does_not_create_duplicte_rooms(self):
        """Test that amity does not create duplicate rooms"""
        self.amity.create_room(["void"])
        self.assertEqual(2, len(self.amity.rooms))

    def test_add_person(self):
        """Test that amity can add a person to a the amity system"""
        self.assertEqual(6, len(self.amity.employees))
        self.assertEqual(3, len(self.amity.fellows))
        self.assertEqual(3, len(self.amity.staff))

    def test_add_person_allocates_person_to_room(self):
        """Test that when a person is added to a room the person is allocated a room"""
        self.assertEqual(6, len(self.amity.offices["void"]))
        self.assertEqual(2, len(self.amity.accommodations["belta"]))

    def test_staff_cannot_be_allocated_accommodation(self):
        """Tests that a staff member can not be allocated to a living space"""
        response = self.amity.add_person("Sakazuki Akainu", "staff", "Y")
        self.assertEqual(response, "Staff can not be allocated a living space")

    def test_add_person_correct_accommodation_argument(self):
        """Test that amity accepts only Y and N as accommodation arguments"""
        response = self.amity.add_person("Monkey Garp", "staff", "P")
        self.assertEqual(response, "accommodation on accepts Y or N arguments")

    def test_amity_cannot_add_person_to_a_full_room(self):
        """Tests that amity does not add people to full rooms"""
        response = self.amity.add_person("Kuzan Aokiji", "staff")
        self.assertEqual(response, "there are no vacant rooms please create a new office")

    def test_unallocated_person(self):
        """Tests that people that have not been allocated space are stored somewhere"""
        self.amity.add_person("Kuzan Aokiji", "staff")
        self.assertEqual(1, len(self.amity.unallocated))

    def test_reallocate_person(self):
        """Test that amity can reallocate people to other rooms"""
        self.amity.create_room(["venus", "tent"])
        self.venus = self.amity.offices[1]
        self.person = self.amity.staff[1]
        self.amity.reallocate_person(self.person.id_no, "venus")
        self.assertEqual(1, len(self.amity.offices["venus"]))
        self.assertEqual(5, len(self.amity.offices["void"]))

    def test_print_room(self):
        response = self.amity.print_room("void")
        self.assertEqual(response, "The people in room void are:"
                                   "____________________________"
                                   "Daniel Sumba"
                                   "Roronoa Zoro"
                                   "Vinsmoke Sanji"
                                   "Roronoa Zoro"
                                   "Excalibur Teno"
                                   "Bosalino kizaru")

    def test_amity_print_empty_room(self):
        self.amity.create_room("livingspace", ["jupiter"])
        response = self.amity.print_room("jupiter")
        self.assertEqual(response, "The room jupiter is empty!!")

    def test_print_unallocated(self):
        """The that amity output to a file and that the file exists"""
        self.amity.print_unallocated({"--o": "test_unallocated.txt"})
        self.assertTrue(os.path.exists("test_unallocated.txt"))
        os.remove("test_unallocated.txt")

    def test_load_people(self):
        """Test that amity can add people from a .txt file"""
        self.amity.load_people({"<filename>": "test_people.txt"})
        self.assertEqual(13, len(self.amity.employees))
        self.assertEqual(7, len(self.amity.fellows))
        self.assertEqual(6, len(self.amity.staff))

    @unittest.skip("WIP")
    def test_save_state(self):
        pass

    @unittest.skip("WIP")
    def test_load_state(self):
        pass

    def test_print_allocation(self):
        self.amity.print_allocation({"--o": "test_allocation.txt"})
        self.assertTrue(os.path.exists("test_allocation.txt"))
        os.remove("test_allocation.txt")

    def tearDown(self):
        self.amity = None

if __name__ == '__main__':
    unittest.main()