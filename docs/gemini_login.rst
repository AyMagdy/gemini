Login
=====

Description
-----------
The module is used to set up an authorized session for HTTPS request. 
The module uses ``HOST`` located at :doc:`connection` which is by **default** the *local host* as the base ``URL`` for the connection.
The module as well defines **the AUTHENTICATION credentials** which may be required to be changed if the user changes them after his/her first login.

.. caution::
    
    the default values for user name and password are:

    * ``USERNAME`` : ouster 
    * ``PASSWORD`` : stone-pass-fill

.. automodule:: gemini_login
   :members:
   :undoc-members:
   :show-inheritance:
