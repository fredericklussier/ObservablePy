#!/usr/bin/python3
# -*- coding: utf-8 -*-

from enum import Enum, unique


@unique
class observerTypeEnum(Enum):
    unknown = 0
    state = 1
    element = 2
    listOfElements = 3

    @classmethod
    def typeOf(cls, what):

        isString = isinstance(what, str)
        isList = hasattr(what, "__len__")

        if (what == "*"):
            return observerTypeEnum.state

        elif (isString):
            return observerTypeEnum.element

        elif (isList):
            return observerTypeEnum.listOfElements

        else:
            return observerTypeEnum.unknown
