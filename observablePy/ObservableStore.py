#!/usr/bin/python3
# -*- coding: utf-8 -*-


class ObservableStore():
    def __init__(self, observables):
        self.__observables = observables

    def getObservableElements(self):
        """
        get the list of properties that have observable decoration

        :return: list of observable properties.
        :rtype: Array
        """
        return self.__observables

    def hasObservableElements(self):
        """
        Mention if class has observable element.

        :return: true if have observable element, otherwise false.
        :rtype: bool
        """
        return self.__observables.__len__() > 0

    def isObservableElement(self, elementNames):
        """
        Mention if an element is an observable element.

        :param str ElementNames: the element name to evaluate
        :ElementNames Type: (str | Array of strings)
        :return: true if is an observable element, otherwise false.
        :rtype: bool
        """
        result = False
        if (isinstance(elementNames, str)):
            result = (True if (elementNames == "*")
                      else self._evaluateString(elementNames))

        elif (hasattr(elementNames, "__len__")):
            result = self._evaluateArray(elementNames)

        else:
            raise TypeError(
                "Element name should be a string of an array of string." +
                "I receive this {0}"
                .format(elementNames))
        return result

    def _evaluateString(self, elementNames):
        result = False
        if (elementNames in self.__observables):
            result = True
        return result

    def _evaluateArray(self, elementNames):
        result = False
        if set(elementNames).issubset(self.__observables):
            result = True
        return result

    def add(self, observableElement):
        """
        add an observable element

        :param str observableElement: the name of the observable element
        :raises RuntimeError: if element name already exist in the store
        """
        if observableElement not in self.__observables:
            self.__observables.append(observableElement)
        else:
            raise RuntimeError(
                "{0} is already an observable element"
                .format(observableElement))

    def remove(self, observableElement):
        """
        remove an obsrvable element

        :param str observableElement: the name of the observable element
        """
        if observableElement in self.__observables:
            self.__observables.remove(observableElement)
