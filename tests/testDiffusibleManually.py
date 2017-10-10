#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import unittest
from observablePy import Observable

"""
Battery is the class used for testing the Observable
"""


class Battery(Observable):
    def __init__(self):
        super(Battery, self).__init__()
        self.state = {
            "voltage": 0,
            "level": 0.0,
            "plugged": False
        }

        self.addObservableElement("voltage")
        self.addObservableElement("level")
        self.addObservableElement("plugged")

    def update(self, voltage, plugged):
        previousState = copy.deepcopy(self.state)

        self.state["voltage"] = voltage
        self.state["level"] = voltage / 5000
        self.state["plugged"] = plugged

        self.diffuse(previousState, self.state)


class testDiffusibleManuallyTests(unittest.TestCase):

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
    Diffuse
    """

    def testDiffuse_WhenFieldObservedChange_ShouldEmitChanges(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousVoltage, voltage):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(previousVoltage, 0)
            self.assertEqual(voltage, 3392)

        self.battery.observeElement("voltage", voltagehandle)

        # Action
        self.battery.update(3392, False)

        # Assert
        self.assertTrue(called)

    def testDiffuse_WhenElementsObservedChange_ShouldEmitChanges(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousBatteryState, batteryState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(previousBatteryState, {
                             "voltage": 0, "level": 0.0})
            self.assertEqual(batteryState, {"voltage": 3392, "level": 0.6784})

        self.battery.observeElements(["voltage", "level"], voltagehandle)

        # Action
        self.battery.update(3392, False)

        # Assert
        self.assertTrue(called)

    def testDiffuse_UsingDecoratorState_ShouldEmitEvent(self):
        # Arrange
        # Battery class, plus
        called = False

        @self.battery.observeState()
        def voltagehandle(previousSate, actualState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(
                previousSate,
                {"voltage": 0, "level": 0.0, "plugged": False})
            self.assertEqual(
                actualState,
                {"voltage": 3392, "level": 0.6784, "plugged": False})

        # Action
        self.battery.update(3392, False)

        # Assert
        self.assertTrue(called)

    def testDiffuse_UsingState_ShouldEmitEvent(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousSate, actualState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(
                previousSate,
                {"voltage": 0, "level": 0.0, "plugged": False})
            self.assertEqual(
                actualState,
                {"voltage": 3392, "level": 0.6784, "plugged": False})

        self.battery.observeState(voltagehandle)

        # Action
        self.battery.update(3392, False)

        # Assert
        self.assertTrue(called)

    def testDiffuse_BadDiffusingArguments_ShoulRaiseError(self):
        # Arrange

        # Action + Assert
        with self.assertRaises(TypeError):
            # str is not callable
            self.battery.diffuse("*")

if __name__ == '__main__':
    unittest.main()
