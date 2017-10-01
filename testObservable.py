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
    Init
    """

    def testInit_ShouldInitiateValue(self):
        # Arrange
        # See Battery class

        # Action
        # See setup

        # Assert
        self.assertFalse(self.battery.hasObservers())

    """
    observeState
    """

    def testObserveState_ShouldAppendObserver(self):
        # Arrange
        # Battery class, plus
        def changeStatehandle():
            print("voltageChange")

        # Action
        self.battery.observeState(changeStatehandle)

        # Assert
        self.assertEqual(self.battery.getObservers(), [
            {"fields": "*", "call": changeStatehandle}])

    def observeState_WhenObserveLinkToBadFunction_ShouldRaiseValueError(self):
        # Arrange
        # Battery class, plus
        def changeStatehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(TypeError):
            # Error call should be a function not a string
            self.battery.observeState("changeStatehandle")

    """
    observeElements
    """

    def testobserveElements_ShouldAppendObserver(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action
        self.battery.observeElements("voltage", voltagehandle)

        # Assert
        self.assertEqual(self.battery.getObservers(), [
                         {"fields": "voltage", "call": voltagehandle}])

    def testobserveElements_WhenUsingDecorator_ShouldAppendObserver(self):
        # Arrange
        # Battery class

        # Action
        @self.battery.observeElement("voltage")
        def voltagehandle():
            print("voltageChange")

        # Assert
        self.assertEqual(self.battery.getObservers(), [
                         {"fields": "voltage", "call": voltagehandle}])

    def testobserveElements_WhenUsingDecoratorAndArray_ShouldAppendObserver(self):
        # Arrange
            # Battery class

        # Action
        @self.battery.observeElements(["voltage", "level"])
        def voltagehandle():
            print("voltageChange")

        # Assert
        self.assertEqual(self.battery.getObservers(), [
            {"fields": ["voltage", "level"], "call": voltagehandle}])

    def testObserve_WhenObserveNoneExistingField_ShouldRaiseValueError(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(ValueError):
            # Error weight does not exist in state
            self.battery.observeElements("weight", voltagehandle)

    def testObserve_WhenObserveNoneExistingFieldInArray_ShouldRaiseValueError(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(ValueError):
            # Error weight does not exist in state
            self.battery.observeElements(["voltage", "weight"], voltagehandle)

    def testObserve_WhenObserveLinkToBadFunction_ShouldRaiseValueError(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(TypeError):
            # Error call should be a function not a string
            self.battery.observeElements("voltage", "voltagehandle")

    """
    unObserve
    """

    def testUnObserve_ShouldRemoveObserver(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        self.battery.observeElements("voltage", voltagehandle)
        self.battery.observeElements("level", voltagehandle)

        # Action
        self.battery.unObserve("level", voltagehandle)

        # Assert
        self.assertEqual(self.battery.getObservers(), [
                         {"fields": "voltage", "call": voltagehandle}])

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

    def testDiffuse_WhenFieldsObservedChange_ShouldEmitChanges(self):
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


if __name__ == '__main__':
    unittest.main()
