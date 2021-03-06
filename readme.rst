ObservablePy
================
.. image:: https://travis-ci.org/fredericklussier/ObservablePy.svg?branch=master
    :target: https://travis-ci.org/fredericklussier/ObservablePy

.. image:: https://coveralls.io/repos/github/fredericklussier/ObservablePy/badge.svg?branch=master
    :target: https://coveralls.io/github/fredericklussier/ObservablePy?branch=master

.. image:: https://api.codeclimate.com/v1/badges/809cf25fc925a3ed8ef2/maintainability
   :target: https://codeclimate.com/github/fredericklussier/ObservablePy/maintainability
   :alt: Maintainability

.. image:: https://badge.fury.io/py/observablePy.svg
    :target: https://badge.fury.io/py/observablePy

Enable observable behavior to an element, so subscribed observers will receive any changes.  

Documentation
------
https://github.com/fredericklussier/ObservablePy/wiki

Status
------
In development.

Features
--------
* Use decoration to set an observable element
* Use decoration to set an observer
* Actual value as weel as previous value
* Add and remove observable element dynamically
* Possibilty to observer multiple observable elements or all of them
* No external dependencies.
* Tested on Python 3.6.

Installation
------------

.. code-block:: batch

    pip install observablePy

If you want all, please read https://help.github.com/articles/cloning-a-repository/

Concepts
--------
* Observable: Observable implementation to a class.
* Observable Element: Is an element that diffuse changes to observers. It can be a property using @observable_property decorator or added using a function.
* State: All observable elements in the class. 
* Observer: An Observer is a function that will be called, when the specified observable element change.
* Diffusing: is the action to inform all observers of the changed observable element.

Bassically, when using property, observable will diffuse changes to subscribed observer when the property setter or deleter is executed. 

When observable is not a property, you diffuse changes when you want in your flow.

Usage
-----
Defining the observable class

.. code-block:: python

    from observablePy import Observable, observable_property

    class Battery(Observable):
    def __init__(self):
        super().__init__()
        self.__voltage = 0
        self.__level = 0.0

        self.addObservableElement("startup")

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
    
    def boot(self):
        ...
        self.diffuse("startup", false, true)

Defining an observer

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    @self.battery.observeField("voltage")
    def voltageHandle(previousValue, actualValue):
        print("voltage is {0}".format(actualValue))
    
    def levelHandle(previousValue, actualValue):
        print("Power level is {0}".format(actualValue))

    self.battery.observeField("level", levelHandle)

License
-------
Distributed under the MIT license: https://opensource.org/licenses/MIT

Copyright (c) 2017 Frédérick Lussier (www.linkedin.com/in/frederick-lussier-757b849)
