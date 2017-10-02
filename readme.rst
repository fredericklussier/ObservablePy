ObservablePy
================
.. image:: https://travis-ci.org/fredericklussier/ObservablePy.svg?branch=master
    :target: https://travis-ci.org/fredericklussier/ObservablePy

Enable an observable behavior to property, so subscribed observers
will receive changes.  

Status
------
In development.

Features
--------
* Use decoration to set a property observable as well as code
* use decoration to set an observer as well as code
* No external dependencies.
* Tested on Python 3.5 and 3.6.

Installation
------------
please read https://help.github.com/articles/cloning-a-repository/

.. code-block:: batch

    $ git clone https://github.com/fredericklussier/ObservablePy.git

In the future, I expect to have a setup using pip.

Working on (developping)
-------------------------
* Having an option for logging.
* When observe multiple element, knowing the element that change.
* Add more element type than properties
* Prepare a setup in pip.

Concepts
--------
* Observable: Observable implementation to a class
* Observable Element: The property of an observable class that have the 
@observable_property decorator is an observable property.
* State : All observable elements in the class. 
* Observer : An Observer is a function that will be called, 
when the specified observable element change.

Bassically, Observable will diffuse changes to subscribe 
observer when the property setter or deleter is executed

Usage
-----
Defining the observable class

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
        self.__voltage = 0

Defining an observer

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    def changeStatehandle():
        print("voltageChange")
    
    self.battery.observeFields("voltage", voltagehandle)

Detail
------

Observe one element
~~~~~~~~~~~~~~~~~~
When you observe one observable element, just named it. 
When this element change you will receive it.

* previousValue : The value before the change
* actualValue : The actual value in the instance

using the decoration:

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    @self.battery.observeElement("voltage")
    def changeVoltagehandle(previousValue, actualValue):
        print(actualValue)
    
using code

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    def changeVoltagehandle(previousValue, actualValue):
        print(actualValue)
    
    self.battery.observeElement("voltage", changeVoltagehandle)

Observe multiple elements
~~~~~~~~~~~~~~~~~~~~~~~
To observe multiple elements, just named them in an array. 
When one of them change, you will reveive a dict of 
elements and value of each of them.

* previousValue (dict(field:Value)): The values before the change
    exemple = {"voltage": 0, "level": 0.0}
* actualValue (dict(field:Value)): The actual values in the instance
    exemple = {"voltage": 3254, "level": 0.0}

using the decoration:

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    @self.battery.observeElements(["voltage", "level"])
    def changeStatushandle(previousValue, actualValue):
        print(actualValue["voltage"], actualValue["level"])
    
using code

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    def changeStatushandle(previousValue, actualValue):
        print(actualValue["voltage"], actualValue["level"])
    
    self.battery.observeElements("voltage", "level", changeStatushandle)

Observe state
~~~~~~~~~~~~~
If you all all observable elements, just call 
When one of them change, you will reveive a dict of 
elements and value of each of them.

* previousValue (dict(field:Value)): The values before the change
    exemple = {"voltage": 0, "level": 0.0, "plugged": 0}
* actualValue (dict(field:Value)): The actual values in the instance
    exemple = {"voltage": 3524, "level": 0.0, "plugged": 0}

using the decoration:

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    @self.battery.observeState()
    def changeStatehandle(previousValue, actualValue):
        print(actualValue["voltage"], actualValue["level"])
    
using code

.. code-block:: python

    from Battery import Battery

    self.battery = Battery()

    def changeStatehandle(previousValue, actualValue):
        print(actualValue["voltage"], actualValue["level"])
    
    self.battery.observeState(changeStatehandle)

License
-------
Distributed under the MIT license: https://opensource.org/licenses/MIT
Copyright (c) 2017 Frédérick Lussier (www.linkedin.com/in/frederick-lussier-757b849)
