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
        if (what == "*"):
            return observerTypeEnum.state

        elif (isinstance(what, str)):
            return observerTypeEnum.element

        elif (hasattr(what, "__len__")):
            return observerTypeEnum.listOfElements

        else:
            return observerTypeEnum.unknown
