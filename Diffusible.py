#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
from ObserverStore import ObserverStore


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
        diffuse changes to the observers

        what: (string) state fields to diffuse

        """

        def _buildState(useField=None):
            state = {}
            previousState = {}

            if useField is None:
                observableElements = self.getObservableElements()
            else:
                observableElements = useField

            for observableElement in observableElements:
                state[observableElement] = getattr(self, observableElement)

            previousState = copy.deepcopy(state)
            previousState[what] = previousValue

            return previousState, state

        def _diffuse(call, field=None):
            if (field is None):
                previousStateValue, statevalue = _buildState()
                call(previousStateValue, statevalue)
            else:
                call(previousValue, value)

        def _diffuseManyFields(call, fields):
            previousFieldsValue, fieldsValue = _buildState(fields)
            call(previousFieldsValue, fieldsValue)

        for observer in self.getObserversIter(what):
            if (observer['observing'] == "*"):
                _diffuse(observer['call'])

            elif (isinstance(observer['observing'], str)):
                _diffuse(observer['call'], observer['observing'])

            else:
                _diffuseManyFields(observer['call'], observer['observing'])
