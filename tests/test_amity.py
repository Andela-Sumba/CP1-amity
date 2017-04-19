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
        self.amity.create_room("office", ["void"])
        # creating living space
        self.amity.create_room("livingspace", ["belta"])
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

    def test_amity_does_not_create_duplicte_rooms(self):
        """Test that amity does not create duplicate rooms"""
        response = self.amity.create_room("office", ["void"])
        self.assertEqual(response, "Amity cannot add duplicate rooms")

    def test_amity_does_not_accept_other_room_types(self):
        """ Test that amity only accepts room types either office or livingspace"""
        response = self.amity.create_room("tent", ["Tsavo"])
        self.assertEqual(response, "Amity only accepts room type of office or livingspace")

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
        self.amity.create_room("office", ["venus"])
        self.venus = self.amity.offices[1]
        self.person = self.amity.staff[1]
        self.amity.reallocate_person(self.person.id_no, "venus")
        self.assertEqual(1, len(self.amity.offices["venus"]))
        self.assertEqual(5, len(self.amity.offices["void"]))

    @unittest.skip("WIP")
    def test_print_room(self):
        pass

    @unittest.skip("WIP")
    def test_print_unallocated(self):
        pass

    @unittest.skip("WIP")
    def test_save_state(self):
        pass

    @unittest.skip("WIP")
    def test_load_state(self):
        pass

    @unittest.skip("WIP")
    def test_print_allocation(self):
        pass

    def tearDown(self):
        self.amity = None

if __name__ == '__main__':
    unittest.main()