Log_File
====
The Log_File enables you to set up logging to a file that is 
saved for future access to persist the logs. Also enables the 
ability to output the logs to the console (STDOUT) if you desire.

Usage
-----
You can use this module in a few ways

1. Import the whole py4pa package::

      import py4pa

      log = py4pa.Log_File(
         directory = '/users/me/documents'
      )

      log.info('Info message')

2. Import the module directly::
   
      from py4pa import Log_File

      log = Log_File(
         directory = '/users/me/documents'
      )

      log.info('Info message')

Documentation
----------------------------

.. autoclass:: py4pa.Log_File
   :members:
   :undoc-members:
   :show-inheritance: