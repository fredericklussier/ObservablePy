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
        result = observerTypeEnum.unknown

        if isinstance(what, str):
            result = (observerTypeEnum.state
                      if (what == "*")
                      else observerTypeEnum.element)

        elif hasattr(what, "__len__"):
            result = observerTypeEnum.listOfElements

        return result
