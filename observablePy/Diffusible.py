#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
from functools import singledispatch
import typing
from .ObserverStore import ObserverStore


class Diffusible(object):
    def __init__(self):
        self.__observers = {}

    def getObservableElements(self):
        raise NotImplementedError(
            'subclasses must override getObservableElements()!')

    def getObserversIter(self, filter=None):
        raise NotImplementedError(
            'subclasses must override __getObserversIter()!')

    def diffuse(self, what, previousValue, value):
        """
        diffuse an element change to the observers

        :param str what: element name to diffuse
        :param any previousValue: value before change of the element
        :param any value: actual value of the element
        """

        def _buildState(elements=None):
            state = {}
            previousState = {}

            if elements is None:
                observableElements = self.getObservableElements()
            else:
                observableElements = elements

            for observableElement in observableElements:
                state[observableElement] = getattr(self, observableElement)

            previousState = copy.deepcopy(state)
            previousState[what] = previousValue

            return previousState, state

        def _diffuse(call, element=None):
            if (element is None):
                previousStateValue, statevalue = _buildState()
                call(previousStateValue, statevalue)
            else:
                call(previousValue, value)

        def _diffuseManyFields(call, elements):
            previousValues, values = _buildState(elements)
            call(previousValues, values)

        for observer in self.getObserversIter(what):
            if (observer['observing'] == "*"):
                _diffuse(observer['call'])

            elif (isinstance(observer['observing'], str)):
                _diffuse(observer['call'], observer['observing'])

            else:
                _diffuseManyFields(observer['call'], observer['observing'])

    def diffuseState(self, previousState, actualState):
        """
        diffuse state changes.

        :param dict previousValue: state values before change
        :param dict value: actual state values
        """

        def _buildState(elements=None):
            if elements is None:
                return previousState, actualState
            else:
                subState = {}
                previousSubState = {}
                for element in elements:
                    subState[element] = actualState[element]
                    previousSubState[element] = previousState[element]

                return previousSubState, subState

        def _diffuse(call, element=None):
            if (element is None):
                previousStateValue, stateValue = _buildState()
                call(previousStateValue, actualState)
            else:
                call(previousState[element], actualState[element])

        def _diffuseManyFields(call, elements):
            previousSubState, subState = _buildState(elements)
            call(previousSubState, subState)

        for observer in self.getObserversIter():
            if (observer['observing'] == "*"):
                _diffuse(observer['call'])

            elif (isinstance(observer['observing'], str)):
                _diffuse(observer['call'], observer['observing'])

            else:
                _diffuseManyFields(observer['call'], observer['observing'])
