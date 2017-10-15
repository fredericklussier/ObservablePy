#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from observablePy.ObserverStore import ObserverStore
from observablePy.ObserverTypeEnum import observerTypeEnum


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

    def testAdd_UsingSingleElement_ShouldAdd(self):
        # Arrange
        def changeHandle():
            print("Changes")

        # Action
        self.observers.add("voltage", changeHandle)

        # Assert
        self.assertTrue(self.observers.hasObservers())
        self.assertEqual(
            self.observers._observers,
            [{"observing": "voltage",
              "type": observerTypeEnum.element,
              "call": changeHandle}])

    def testAdd_UsingMultiElements_ShouldAdd(self):
        # Arrange
        def changeHandle():
            print("Changes")

        # Action
        self.observers.add(["voltage", "level"], changeHandle)

        # Assert
        self.assertTrue(self.observers.hasObservers())
        self.assertEqual(
            self.observers._observers,
            [{"observing": ["voltage", "level"],
              "type": observerTypeEnum.listOfElements,
              "call": changeHandle}])

    def testAdd_UsingAllElements_ShouldAdd(self):
        # Arrange
        def changeHandle():
            print("Changes")

        # Action
        self.observers.add("*", changeHandle)

        # Assert
        self.assertTrue(self.observers.hasObservers())
        self.assertEqual(
            self.observers._observers,
            [{"observing": "*",
              "type": observerTypeEnum.state,
              "call": changeHandle}])

    def testAdd_UsingUnknowElement_ShouldRaiseError(self):
        # Arrange
        def changeHandle():
            print("Changes")

        # Actionand Assert
        with self.assertRaises(TypeError):
            self.observers.add(12, changeHandle)

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
            [{
                "observing": "voltage",
                "call": changeHandle
            }, {
                 "observing": "level",
                 "call": changeHandle
            }])

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
    iteration generator
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
        observers = self.observers.iterationGenerator()
        for observer in observers:
            # Assert
            self.assertEqual(
                observer["observing"],
                ["voltage", "level", "plugged"][index])
            index += 1

    def testIteration_UsingArray_ShouldIter(self):
            # Arrange
        def changeHandle():
            print("Changes")

        self.observers.add("voltage", changeHandle)
        self.observers.add(["level", "voltage"], changeHandle)
        self.observers.add("plugged", changeHandle)
        # Action
        actualResult = len(list(self.observers.iterationGenerator("voltage")))

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
        actualResult = len(list(self.observers.iterationGenerator("voltage")))

        # Assert
        self.assertEqual(actualResult, 3)
