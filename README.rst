===================================
os-adminpass-python-novaclient-ext
===================================


Admin Password extension for python-novaclient.


Install
=======

::

  pip install os_adminpass_python_novaclient_ext


Usage
=====

This extension will automatically be detected by novaclient and will provide
the --admin-password option for `boot`, `zone-boot`, `rebuild`, and `resize`
commands.


Note
====

This is the *client* extension, for admin-password to work, the Nova service must
also be using the *server-side* extension as well.
