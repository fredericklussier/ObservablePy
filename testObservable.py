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


class ObservableTests(unittest.TestCase):

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
    getObservableElements
    """
    def testGetObservableElements_ShouldGiveObservableElements(self):
        # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.getObservableElements()

        # Assert
        self.assertEqual(actualValue, ['level', 'plugged', 'voltage'])

    """
    hasObservableElements
    """
    def testHasObservableElements_ShouldBeTrue(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.hasObservableElements()

        # Assert
        self.assertTrue(actualValue)

    """
    addObservableElement
    """
    def testAddObservableElement_ShouldBeTrue(self):
        # Arrange
        # Battery class, plus
        
        # Action
        self.battery.addObservableElement("statup")

        # Assert
        actualValue = self.battery.isObservableElement("statup")
        self.assertTrue(actualValue)

    """
    removeObservableElement
    """
    def testremoveObservableElement_ShouldBeTrue(self):
        # Arrange
        # Battery class, plus
        
        # Action
        self.battery.removeObservableElement("level")

        # Assert
        actualValue = self.battery.isObservableElement("level")
        self.assertFalse(actualValue)

    """
    isObservableElement
    """
    def testIsObservableElement_ShouldBeTrue(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.isObservableElement("voltage")

        # Assert
        self.assertTrue(actualValue)

    def testIsObservableElement_UsingArray_ShouldBeTrue(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.isObservableElement(["voltage", "level"])

        # Assert
        self.assertTrue(actualValue)

    def testIsObservableElement_UsingState_ShouldBeTrue(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.isObservableElement("*")

        # Assert
        self.assertTrue(actualValue)

    def testIsObservableElement_UsingArrayAndNotObsElement_ShouldBeFalse(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.isObservableElement(["voltage", "model"])

        # Assert
        self.assertFalse(actualValue)

    def testIsObservableElement_WhenNotObservableElement_ShouldBeFalse(self):
            # Arrange
        # Battery class, plus

        # Action
        actualValue = self.battery.isObservableElement("model")

        # Assert
        self.assertFalse(actualValue)

    def testIsObservableElement_WhenBadType_ShouldRaiseError(self):
        # Arrange
        # Battery class, plus

        # Action and assert
        with self.assertRaises(TypeError):

            # Error call should be a function not a string
            self.battery.isObservableElement(10)

    """
    getObservers
    """
    def testGetObservers_ShouldGiveObservers(self):
        # Arrange
        # Battery class, plus
        def changeStatehandle():
            print("voltageChange")

        self.battery.observeElement("voltage", changeStatehandle)

        # Action
        actualResult = self.battery.getObservers()

        # Assert
        self.assertEqual(actualResult, [
            {"observing": "voltage", "call": changeStatehandle}])

    def testGetObservers_WhenNoOne_ShouldGiveObservers(self):
        # Arrange
        # Battery class

        # Action
        actualResult = self.battery.getObservers()

        # Assert
        self.assertEqual(actualResult, [])

    """
    hasObservers
    """
    def testHasObservers_ShouldTrue(self):
        # Arrange
        # Battery class, plus
        def changeStatehandle():
            print("voltageChange")

        self.battery.observeElement("voltage", changeStatehandle)

        # Action
        actualResult = self.battery.hasObservers()

        # Assert
        self.assertTrue(actualResult)
    
    def testHasObservers_WhenNoOne_ShouldFalse(self):
        # Arrange
        # Battery class

        # Action
        actualResult = self.battery.hasObservers()

        # Assert
        self.assertFalse(actualResult)

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
            {"observing": "*", "call": changeStatehandle}])

    def testObserveState_UsingDecorator_ShouldAppendObserver(self):
        # Arrange
        # Battery class, plus

        # Action
        @self.battery.observeState()
        def changeStatehandle():
            print("voltageChange")

        # Assert
        self.assertEqual(self.battery.getObservers(), [
            {"observing": "*", "call": changeStatehandle}])

    def testObserveState_WhenObserveLinkToBadFunction_ShouldRaiseValueError(self):
        # Arrange
        # Battery class, plus
        def changeStatehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(TypeError):
    
            # Error call should be a function not a string
            self.battery.observeState("changeStatehandle")

    """
    observeElement
    """

    def testObserveElement_ShouldAppendObserver(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action
        self.battery.observeElement("voltage", voltagehandle)

        # Assert
        self.assertEqual(self.battery.getObservers(), [
                         {"observing": "voltage", "call": voltagehandle}])

    def testObserveElement_UsingDecorator_ShouldAppendObserver(self):
        # Arrange
        # Battery class

        # Action
        @self.battery.observeElement("voltage")
        def voltagehandle():
            print("voltageChange")

        # Assert
        self.assertEqual(self.battery.getObservers(), [
                         {"observing": "voltage", "call": voltagehandle}])

    def testObserveElement_WhenObserveNoneExistingField_ShouldRaiseValueError(self):
        # Arrange
        # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(ValueError):
            # Error weight is not an observable element
            self.battery.observeElements("weight", voltagehandle)

    def testObserveElement_WhenObserveLinkToBadFunction_ShouldRaiseValueError(self):
            # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(TypeError):
            # Error call should be a function not a string
            self.battery.observeElement("voltage", "voltagehandle")

    """
    observeElements
    """

    def testObserveElements_ShouldAppendObserver(self):
        # Arrange
        # Battery class

        # Action
        @self.battery.observeElements(["voltage", "level"])
        def voltagehandle():
            print("voltageChange")

        # Assert
        self.assertEqual(self.battery.getObservers(), [
            {"observing": ["voltage", "level"], "call": voltagehandle}])

    def testObserveElements_UsingDecorator_ShouldAppendObserver(self):
        # Arrange
            # Battery class

        # Action
        def voltagehandle():
            print("voltageChange")

        self.battery.observeElements(["voltage", "level"], voltagehandle)

        # Assert
        self.assertEqual(self.battery.getObservers(), [
            {"observing": ["voltage", "level"], "call": voltagehandle}])

    def testObserveElements_WhenNotExistInObserverArray_ShouldRaiseValueError(self):
        # Arrange
            # Battery class, plus
        def voltagehandle():
            print("voltageChange")

        # Action and assert
        with self.assertRaises(ValueError):
            # Error weight is not an observable element
            self.battery.observeElements(["voltage", "weight"], voltagehandle)

    def testObserveElements_WhenObserveLinkToBadFunction_ShouldRaiseValueError(self):
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
                         {"observing": "voltage", "call": voltagehandle}])

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


if __name__ == '__main__':
    unittest.main()
