#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from ObservableStore import ObservableStore


class ObserverStoreTests(unittest.TestCase):

    """
    setUp each test
    """

    def setUp(self):
        self.observables = ObservableStore([])

    """
    tearDown each test
    """

    def tearDown(self):
        self.observables = None

    """
    Init
    """

    def testInit_ShouldInitiateValue(self):
        # Arrange

        # Action
        actualResult = self.observables.hasObservableElements()

        # Assert
        self.assertFalse(actualResult)

    def testInit_UsingParam_ShouldInitiateValue(self):
        # Arrange

        # Action
        observables = ObservableStore(["voltage", "level"])

        # Assert
        self.assertTrue(observables.hasObservableElements())

    """
    add
    """
    def testAdd_ShouldAdd(self):
        # Arrange

        # Action
        self.observables.add("voltage")

        # Assert
        self.assertTrue(self.observables.hasObservableElements())
        self.assertEqual(
            self.observables.getObservableElements(),
            ["voltage"])

    def testAdd_WhenDouble_ShoulRaiseError(self):
        # Arrange
        self.observables.add("voltage")

        # Action + Assert
        with self.assertRaises(RuntimeError):
            # str is not callable
            self.observables.add("voltage")

    """
    remove
    """ 
    def testRemove_ShouldRemove(self):
        # Arrange
        self.observables.add("voltage")

        # Action
        self.observables.remove("voltage")

        # Assert
        self.assertFalse(self.observables.hasObservableElements())

    def testRemove_whenTryingNotExisting_ShouldRemove(self):
        # Arrange
        self.observables.add("voltage")

        # Action
        self.observables.remove("level")

        # Assert
        self.assertTrue(self.observables.hasObservableElements())

    """
    isObservableElement
    """
    def testIsObservableElement_ShouldTrue(self):
        # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action
        actualResult = observables.isObservableElement("voltage")

        # Assert
        self.assertTrue(actualResult)

    def testIsObservableElement_UsingArray_ShouldTrue(self):
        # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action
        actualResult = observables.isObservableElement(["voltage", "plugged"])

        # Assert
        self.assertTrue(actualResult)

    def testIsObservableElement_WhenNotExisting_ShouldFalse(self):
        # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action
        actualResult = observables.isObservableElement(["model"])

        # Assert
        self.assertFalse(actualResult)

    def testIsObservableElement_WhenArrayAndNotExisting_ShouldFalse(self):
        # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action
        actualResult = observables.isObservableElement(["voltage", "model"])

        # Assert
        self.assertFalse(actualResult)

    def testIsObservableElement_WhenAll_ShouldTrue(self):
        # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action
        actualResult = observables.isObservableElement("*")

        # Assert
        self.assertTrue(actualResult)
    
    def testIsObservableElement_UsingBadType_ShouldRaiseError(self):
            # Arrange
        observables = ObservableStore(["voltage", "level", "plugged"])

        # Action and Assert
        with self.assertRaises(TypeError):
            actualResult = observables.isObservableElement(14)