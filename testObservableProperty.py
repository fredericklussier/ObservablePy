#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from Observable import Observable
from ObservableProperty import observable_property

"""
Battery is the class used for testing the Observable
"""


class Battery(Observable):
    def __init__(self):
        super().__init__()
        self.__voltage = 0
        self.__capacity = 0
        self.__level = 0.0
        self.__plugged = False

    @observable_property
    def voltage(self):
        return self.__voltage

    @voltage.setter
    def voltage(self, value):
        self.__voltage = value

    @voltage.deleter
    def voltage(self):
        self.__voltage = 0

    @observable_property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @observable_property
    def plugged(self):
        return self.__plugged

    @plugged.setter
    def plugged(self, value):
        self.__plugged = value


class ObservableTest(unittest.TestCase):

    """
    setUp each test
    """

    def setUp(self):
        self.battery = Battery()

    """
    tearDown each test
    """

    def tearDown(self):
        self.battery = None

    """
    Observable Decoration
    """

    def testObservableDecoration_ShouldSetObservableElement(self):
        # Arrange
        # See Battery class

        # Action and Assert
        self.assertTrue(self.battery.hasObservableElements())
        self.assertTrue(self.battery.isObservableElement("voltage"))
        self.assertTrue(self.battery.isObservableElement("level"))
        self.assertTrue(self.battery.isObservableElement("plugged"))

    def testObservableDecoration_UsingNotObservableElement_ShouldNotExist(self):
        # Arrange
        # See Battery class

        # Action and Assert
        self.assertTrue(self.battery.hasObservableElements())
        self.assertFalse(self.battery.isObservableElement("capacity"))


if __name__ == '__main__':
    unittest.main()
