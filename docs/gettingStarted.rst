***************
Getting Started
***************

After the :ref:`installation` is done, one can use the package for the personal OpenSpecimen distribution.

Load package
============

First step is to load the package via PIP installer.

.. code:: python

    import OpenSpecimenAPIconnector as OSconn
    import OpenSpecimenAPIconnector.os_core as os_core
    import OpenSpecimenAPIconnector.os_util as os_util

Instead of ``OpenSpecimenAPIconnector.os_core as os_util`` on can use ``OSconn.os_util`` in the code. The same applies for ``os_core``.

Configure URL and Login
=======================

The next step is to define the URL of OpenSpecimen aswell as the Loginname and Password of the User, who wants to use this package.
The default password and loginname in OpenSpecimen are those which are used here:

.. code:: python

    # Set Login Example
    baseurl = 'http(s)://<OS-Instance-Name>/openspecimen/rest/ng'
    loginname = "admin"
    password = "Login@123"
    auth = (loginname, password)
    OSconn.config_manager.set_login(url = base_url, auth = auth)

Create an Institute
===================

OpenSpecimen has a hierarchy, which has to be respected when creating objects. For example if one wants to create a **site**, there has to be an **institute**.
So the highest instance is an **institute** which can be done as follows:

.. code:: python

    # initialize Institutes 
    institutes_util = os_util.institutes_util()
    
    institutes_util.create_institute(institutename = 'Demo Institute')

.. note::
    The same can be done with the function in ``os_core.institutes.create_institute``. The difference is that in the os_core functions one has to hand over a 
    JSON-formatted string. This is more general, its useable with customized OpenSpecimen versions. But it is more difficult to use.
    The code then looks like:
  
    | ``institute = os_core.institute()``
    | ``institute.create(params = '{\"institutename\":\"Demo Institute\"}')``

    The parameters which are passed to the function have all to be known, this means the *entity-name*, the *value* and the *type*. There are some parameters,
    which are itself *dicts*. The os_util functions have a defined input, with the standard values of OpenSpecimen, and the json-formatted string is generated 
    automatically.




