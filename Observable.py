#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
from ObservableProperty import observable_property

"""
Implement the observable behaviour to a class.

Observable property:
The property of an observable class that have the
@observable_property decorator is an observable property.

refer to ObservableProperty to set a property observable

Observer:
An Observer is a function that will be called, when the specified
observable element change.

=================
How to use it
=================

.. code-block:: python
from Observable import Observable, observable_property

class Battery(Observable):
def __init__(self):
    super().__init__()
    self.__voltage = 0

@observable_property
def voltage(self):
    return self.__voltage

@voltage.setter
def voltage(self, value):
    self.__voltage = value

@voltage.deleter
def voltage(self):
    self.__voltage = None

"""


class Observable():
    # for execution speed, I store the Observable Elements as a
    #  class variable since the definition of a class is not changing.
    # TODO: let add or remove observable element dynamically
    __ObservableElements = {}

    def __init__(self):
        self.__observers = []
        # build the list of observable element.
        if self.hasObservableElements() == 0:
            Observable.__ObservableElements = self.getObservableElements()

    @classmethod
    def getObservableElements(cls):
        """
        get the list of properties that have observable decoration

        :return: list of observable properties.
        :rtype: Array
        """
        return [p for p in dir(cls)
                if isinstance(getattr(cls, p), observable_property)]

    @classmethod
    def hasObservableElements(cls):
        """
        Mention if class has observable element.

        :return: true if have observable element, otherwise false.
        :rtype: bool
        """
        return cls.__ObservableElements.__len__() > 0

    @classmethod
    def isObservableElement(cls, ElementNames):
        """
        Mention if an element is an observable element.

        :param str ElementNames: the element name to evaluate
        :ElementNames Type: (str | Array of strings)
        :return: true if is an observable element, otherwise false.
        :rtype: bool
        """
        def _evaluateString():
            if (ElementNames in cls.__ObservableElements):
                return True
            return False

        def _evaluateArray():
            if set(ElementNames).issubset(cls.__ObservableElements):
                return True
            return False

        if (ElementNames == "*"):
            return True
        else:
            if (isinstance(ElementNames, str)):
                return _evaluateString()

            elif (hasattr(ElementNames, "__len__")):
                return _evaluateArray()

            else:
                raise TypeError(
                    "Element name should be a string of an array of string." +
                    "I receive this {0}"
                    .format(ElementNames))

    def getObservers(self):
        """
        Get the list of observer to the instance of the class.

        :return: Subscribed Obversers.
        :rtype: Array
        """
        return self.__observers

    def hasObservers(self):
        """
        Mention if the observable class has observer. 

        :return: true if it has observer, otherwise false.
        :rtype: bool
        """
        return self.getObservers().__len__() > 0

    # def isObserved(cls, fieldName):
    #     return true when exist other false

    def observeState(self, call=None):
        """
        Registers an observer to the any changes.
            The called function should have 2 parameters:
            - previousState,
            - actualState

        :param func call: The function to call.
                          When not given, decorator usage is assumed.
        :return: the function to call once state change.
        :rtype: func
        :raises TypeError: if the called function is not callable

        =================
        How to use it
        =================
        -----------------
        1. Calling the function
        -----------------
            .. code-block:: python
                instance.observeState(functionName)
                instance.observeState(functionName)

                ...
                def functionName(previousState, actualState):

        -----------------
        2. Using Decoration
        -----------------
            .. code-block:: python
                @instance.observeState()
                def functionName(previousState, actualState):

                @instance.observeState()
                def functionName(previousState, actualState):
        """
        def _observe(call):
            if not self.__isCallableFunction(call):
                raise TypeError(
                    '"call" parameter should be a callable function.')

            self.__addObserver("*", call)
            return call

        if call is not None:
            return _observe(call)
        else:
            return _observe

    def observeElement(self, what, call=None):
        """
        Registers an observer function to a specific state field or
            list of state fields.
            The function to call should have 2 parameters:
            - previousValue,
            -actualValue

        :param what: name of the state field or names of the
                     state field to observe.
        :type what: str | array
        :param func call: The function to call. When not given, 
                          decorator usage is assumed.
        :return: the function to call once state change.
        :rtype: func
        :raises TypeError: if the called function is not callable

        =================
        How to use it
        =================
        -----------------
        1. Calling the function
        -----------------
        .. code-block:: python
            instance.observeFields("FieldName", functionName)
            instance.observeFields(["FieldName1","FieldName2"], functionName)

            ...
            def functionName(previousState, actualState):

        -----------------
        2. Using Decoration
        -----------------
        .. code-block:: python
            @instance.observeFields("FieldName")
            def functionName(previousValue, actualValue):

            @instance.observeFields(["FieldName1","FieldName2"])
            def functionName(previousValue, actualValue): 
        """

        def _observe(call):
            if not self.__isCallableFunction(call):
                raise TypeError(
                    '"call" parameter must be a callable function.')

            self.__addObserver(what, call)

            return call

        if call is not None:
            return _observe(call)
        else:
            return _observe

    def observeElements(self, what, call=None):
        """
        Registers an observer function to a specific state field or
            list of state fields.
            The function to call should have 2 parameters:
            - previousValue,
            -actualValue

        :param what: name of the state field or names of the
                     state field to observe.
        :type what: str | array
        :param func call: The function to call. When not given, 
                          decorator usage is assumed.
        :return: the function to call once state change.
        :rtype: func
        :raises TypeError: if the called function is not callable

        =================
        How to use it
        =================
        -----------------
        1. Calling the function
        -----------------
        .. code-block:: python
            instance.observeFields("FieldName", functionName)
            instance.observeFields(["FieldName1","FieldName2"], functionName)

            ...
            def functionName(previousState, actualState):

        -----------------
        2. Using Decoration
        -----------------
        .. code-block:: python
            @instance.observeFields("FieldName")
            def functionName(previousValue, actualValue):

            @instance.observeFields(["FieldName1","FieldName2"])
            def functionName(previousValue, actualValue): 
        """

        def _observe(call):
            if not self.__isCallableFunction(call):
                raise TypeError(
                    '"call" parameter must be a callable function.')

            self.__addObserver(what, call)

            return call

        if call is not None:
            return _observe(call)
        else:
            return _observe

    def __addObserver(self, what, call):

        if not self.isObservableElement(what):
            msg = 'Could not find observable element named "{0}" in {1}'
            raise ValueError(msg.format(what, self.__class__))

        self.__observers.append({"fields": what, "call": call})

    def __isCallableFunction(self, function):
        return hasattr(function, "__call__")

    def unObserve(self, what, call):
        """
        unregisters an observer

        what: (string | array) state fields to observe
        call: (function) when not given, decorator usage is assumed.
            The call function should have 2 parameters:
            - previousValue,
            - actualValue

        """
        self.__observers.remove({"fields": what, "call": call})

    def diffuse(self, what, previousValue, value):
        """
        diffuse changes to the observers

        what: (string) state fields to diffuse

        """

        def _buildState(useField=None):
            state = {}
            previousState = {}

            if useField is None:
                observableElements = self.__ObservableElements
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

        for observer in self.__observers:
            if (observer['fields'] == "*"):
                _diffuse(observer['call'])

            elif (isinstance(observer['fields'], str)):
                if (what == observer['fields']):
                    _diffuse(observer['call'], observer['fields'])

            else:
                if (what in observer['fields']):
                    _diffuseManyFields(observer['call'], observer['fields'])
