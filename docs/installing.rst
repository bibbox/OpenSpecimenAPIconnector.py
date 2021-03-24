************
Installation
************

Install the package:

.. code:: console

    $ pip install OpenSpecimenApiConnector

In your ``sript.py`` file:

.. code:: python

    import OpenSpecimenAPIconnector as OSconn
    import OpenSpecimenAPIconnector.os_core as os_core
    import OpenSpecimenAPIconnector.os_util as os_util

    # Set Login Example
    baseurl = 'http(s)://<OS-Instance-Name>/openspecimen/rest/ng'
    loginname = "admin"
    password = "Login@123"
    auth = (loginname, password)
    OSconn.config_manager.set_login(url = base_url, auth = auth)
    # Use some Methods
        ...

.. note::
    This will produce an Error if you current instance url or authorization is invalid 

Jupyter Demos
===================

For more information and detailed demos visit:
https://github.com/bibbox/OpenSpecimenAPIconnector.py/tree/master/demo_notebooks

Integration Testing
===================

To verify your version installation is running correctly use the test.py script which can be <br>
found in the integration_test folder on GitHub
