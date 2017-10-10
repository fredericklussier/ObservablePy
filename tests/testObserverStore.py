#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from observablePy.ObserverStore import ObserverStore

"""
Battery is the class used for testing the observer
"""


class ObserverStoreTests(unittest.TestCase):

    """
    setUp each test
    """

    def setUp(self):
        self.observers = ObserverStore()

    """
    tearDown each test
    """

    def tearDown(self):
        self.observers = None

    """
    Init
    """

    def testInit_ShouldInitiateValue(self):
        # Arrange see setUp

        # Action see setUp

        # Assert
        self.assertFalse(self.observers.hasObservers())

    """
    add
    """
    def testAdd_ShouldAdd(self):
        # Arrange
        def changeHandle():
            print("Changes")

        # Action
        self.observers.add("voltage", changeHandle)

        # Assert
        self.assertTrue(self.observers.hasObservers())
        self.assertEqual(
            self.observers.getObservers(),
            [{"observing": "voltage", "call": changeHandle}])

    def testAdd_WhenNotCallable_ShoulRaiseError(self):
        # Arrange
        def changeHandle():
            print("Changes")
        
        # Action and Assert
        with self.assertRaises(TypeError):
            # str is not callable
            self.observers.add("voltage", "changeHandle")  

    """
    remove
    """
    def testRemove_ShouldRemove(self):
        # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add("level", changeHandle)
        self.observers.add("plugged", changeHandle)

        # Action
        self.observers.remove("plugged", changeHandle)

        # Assert
        self.assertTrue(self.observers.hasObservers())
        self.assertEqual(
            self.observers.getObservers(),
            [{"observing": "voltage", "call": changeHandle},
            {"observing": "level", "call": changeHandle}])

    """
    removeAll
    """
    def testRemoveAll_ShouldRemoveAll(self):
        # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add("level", changeHandle)
        self.observers.add("plugged", changeHandle)

        # Action
        self.observers.removeAll()

        # Assert
        self.assertFalse(self.observers.hasObservers())

    """
    iteration
    """
    def testIteration_ShouldIter(self):
        # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add("level", changeHandle)
        self.observers.add("plugged", changeHandle)
        # Action

        index = 0
        for observer in self.observers:
            # Assert
            self.assertEqual(
                observer["observing"], ["voltage", "level", "plugged"][index])
            index += 1

    def testIteration_UsingArray_ShouldIter(self):
            # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add(["level", "voltage"], changeHandle)
        self.observers.add("plugged", changeHandle)
        # Action
        actualResult = len(list(self.observers.__iter__("voltage")))

        # Assert
        self.assertEqual(actualResult, 2)

    def testIteration_UsingAll_ShouldIter(self):
            # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add(["level", "voltage"], changeHandle)
        self.observers.add("*", changeHandle)
        self.observers.add("plugged", changeHandle)
        # Action
        actualResult = len(list(self.observers.__iter__("voltage")))

        # Assert
        self.assertEqual(actualResult, 3)
