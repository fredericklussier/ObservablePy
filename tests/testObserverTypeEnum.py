#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from observablePy.ObserverTypeEnum import observerTypeEnum


class ObserverStoreTests(unittest.TestCase):

    """
    typeOf
    """

    def testTypeOf_State_ShouldReturnStateEnumValue(self):
        # Arrange

        # Action
        actualValue = observerTypeEnum.typeOf("*")

        # Assert
        self.assertEqual(actualValue, observerTypeEnum.state)

    def testTypeOf_Element_ShouldReturnElementEnumValue(self):
        # Arrange

        # Action
        actualValue = observerTypeEnum.typeOf("voltage")

        # Assert
        self.assertEqual(actualValue, observerTypeEnum.element)

    def testTypeOf_ListOfElements_ShouldReturnListOfElementsEnumValue(self):
        # Arrange

        # Action
        actualValue = observerTypeEnum.typeOf(["voltage", "level"])

        # Assert
        self.assertEqual(actualValue, observerTypeEnum.listOfElements)

    def testTypeOf_Unknown_ShouldReturnUnknownEnumValue(self):
        # Arrange

        # Action
        actualValue = observerTypeEnum.typeOf(10)

        # Assert
        self.assertEqual(actualValue, observerTypeEnum.unknown)
