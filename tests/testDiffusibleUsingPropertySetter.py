#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from observablePy import Observable
from observablePy import observable_property

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
        self.__voltage = None

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


class DiffusibleUsingPropertySetterTests(unittest.TestCase):

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
        self.battery.voltage = 3392

        # Assert
        self.assertTrue(called)

    def testDiffuse_WhenelementsObservedChange_ShouldEmitChanges(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousBatteryState, batteryState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(previousBatteryState, {
                             "voltage": 0, "level": 0.0})
            self.assertEqual(batteryState, {"voltage": 3392, "level": 0.0})

        self.battery.observeElements(["voltage", "level"], voltagehandle)

        # Action
        self.battery.voltage = 3392

        # Assert
        self.assertTrue(called)

    def testDiffuse_WhenelementsObservedDelete_ShouldEmitChanges(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousBatteryState, batteryState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(previousBatteryState, {
                             "voltage": 0, "level": 0.0})
            self.assertEqual(batteryState, {"voltage": None, "level": 0.0})

        self.battery.observeElements(["voltage", "level"], voltagehandle)

        # Action
        del(self.battery.voltage)

        # Assert
        self.assertTrue(called)

    def testDiffuse_UsinDecoratorState_ShouldEmitEvent(self):
        # Arrange
        # Battery class, plus
        called = False

        @self.battery.observeState()
        def voltagehandle(previousSate, actualState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(
                previousSate, {"voltage": 0, "level": 0.0, "plugged": 0})
            self.assertEqual(
                actualState, {"voltage": 3392, "level": 0.0, "plugged": 0})

        # Action
        self.battery.voltage = 3392

        # Assert
        self.assertTrue(called)

    def testDiffuse_WhenStateChange_ShouldEmitEvent(self):
        # Arrange
        # Battery class, plus
        called = False

        def voltagehandle(previousSate, actualState):
            # Assert
            nonlocal called
            called = True
            self.assertEqual(
                previousSate, {"voltage": 0, "level": 0.0, "plugged": 0})
            self.assertEqual(
                actualState, {"voltage": 3392, "level": 0.0, "plugged": 0})

        self.battery.observeState(voltagehandle)

        # Action
        self.battery.voltage = 3392

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
                previousSate, {"voltage": 0, "level": 0.0, "plugged": 0})
            self.assertEqual(
                actualState, {"voltage": 3392, "level": 0.0, "plugged": 0})

        self.battery.observeState(voltagehandle)

        # Action
        self.battery.voltage = 3392

        # Assert
        self.assertTrue(called)

if __name__ == '__main__':
    unittest.main()
