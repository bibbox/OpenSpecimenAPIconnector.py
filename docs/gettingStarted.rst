***************
Getting Started
***************

As an introduction to this package, a specimen with all its dependencies gets created.

.. note::
    The calls are done with the mandatory fields only. There are other fields which can be filled out, while creating the objects in OpenSpecimen. For further insights
    on can read  the `Documentation of OpenSpecimen <https://openspecimen.atlassian.net/wiki/spaces/CAT/overview>`_ or  the 
    :ref:`Code Documentation of the pip-package <index>`.

Before starting one has to :ref:`install <installation>` the package.
After the :ref:`installation <installation>` is done, one can use the package for the personal OpenSpecimen distribution.


Installing the Package
======================

In your console one has to run

.. code:: console

    pip install OpenSpecimenAPIConnector

or 

.. code:: console

    pip3 install OpenSpecimenAPIConnector

Importing the Package
=====================

First step is to import the modules to the python script.

.. code:: python

    import OpenSpecimenAPIconnector as OSconn
    import OpenSpecimenAPIconnector.os_core as os_core
    import OpenSpecimenAPIconnector.os_util as os_util

Instead of ``OpenSpecimenAPIconnector.os_core as os_util`` on can use ``OSconn.os_util`` in the code. The same applies for ``os_core``.


Configuring the URL and Login
=============================

The next step is to define the URL of OpenSpecimen aswell as the Loginname and Password of the User, who wants to use this package.
The default password and loginname in OpenSpecimen are those which are used here: 

.. code:: python

    # Set Login Example
    baseurl = 'http(s)://<OS-Instance-Name>/openspecimen/rest/ng'
    loginname = "admin"
    password = "Login@123"
    auth = (loginname, password)
    OSconn.config_manager.set_login(url = base_url, auth = auth)


Creating an Institute
=====================

OpenSpecimen has a hierarchy, which has to be respected when creating objects. For example if one wants to create a **site**, there has to be an **institute**.
So the highest instance is an **institute**. This can be done as follows, with the function ``create_institute``:

.. code:: python

    # initialize
    institutes_util = os_util.institutes_util()
    
    response = institutes_util.create_institute(institutename = 'Demo Institute')

.. note::
    The same can be done with the function in ``os_core.institutes.create_institute``. The difference is that in the os_core functions one has to hand over a 
    JSON-formatted string. This is more general, its useable with customized OpenSpecimen versions. But it is more difficult to use.
    The code then looks like:
  
    | ``institute = os_core.institute()``
    | ``institute.create(params = '{\"institutename\":\"Demo Institute\"}')``

    In general, the parameters which are passed to **os_core** functions have all to be known, this means the *entity-name*, the *value* and the *type*.  
    There are some parameters, which are itself *dicts*. The **os_util** functions have a *defined input*, with the *standard values* of OpenSpecimen 
    and the json-formatted string is generated automatically.


Creating a Site
===============

If there is an institute, one can create a site. This works with the method ``create_institute`` from the `os_util` class `site_util` 
as follows: 

.. code:: python

    #initialize
    site_util = os_util.site_util()

    response = site_util.create_sites(name = 'Demo Site', institutename = ' Demo Institute', type_ = 'not specified')


Creating a Collection Protocol
==============================

On a Site on can have a collection, which can be managed in OpenSpecimen. For that one can create a Collection Protocol, with the  method ``create_collection_protocol`` 
from the `os_util` class `colletion_protocol_util`:

.. code:: python

    #initialize
    colletion_protocol_util = os_util.colletion_protocol_util()

    response = colletion_protocol_util.create_collection_protocol(short_title = 'Demo CP', title = 'Demo Collection Protocol', pi_mail = 'admin', sites = ['Demo Site'])

.. note::
    The response is a dict with the details of the created collection protocol. For example the ID of the Colletion protocol can be extracted with key 'id'. 
    This will be used later and can be done as follows.

    | ``# cpId = collection protocol ID``
    | ``cpID = response['id']``


Creating a Registration
=======================

Once there is a Collection Protocol OpenSpecimen is ready to Register Participants. The method ``create_registration``, from the `os_util` class `cpr_util` does the job:

.. code:: python

    #initialize
    cpr_util = os_util.cpr_util()

    response = cpr_util.create_registration(regdate = '2021-03-17', cpid = cpID, ppid = "IntegrationTestPPID",lastname = "Sepp")
    cprID = response['id'] #is needed afterwards

Creating a Specimen together with a Visit
=========================================

In order to create a `specimen`, there has to be a visit. OpenSpecimen provides a call which created both at ones. This is the method ``add_visit_speci`` from the
`os_util` class `vis_util`. 

.. code:: python

    #initialize
    vis_util = os_util.vis_util()

    response = vis_util.add_visit_speci(name = 'Demo Visit', lineage = 'New', av_qty = 10, user = 2, init_qty = 10, spec_class ='Fluid', 
                    spec_type = 'Bile', anat_site ='Anal Canal', path='Malignant', site = 'Demo Site', speclabel = 'Demo Label' ,cpid = cpID,
                     ppid = 'Demo PPID', cprid = 'cprID, colltime = '2021-03-17' ,rectime = '2021-03-17' )

    #the user admin, which is created from OpenSpecimen when it is installed,  has the ID 2 

.. note::
    If one knows the visits before which gets collected, then one can first create an **event**, then add the visit to the event and after that collect the specimen

