SFTP
====
The SFTP module simplifies much of the common activities 
needed when dealing with file on an SFTP server.

Usage
-----
You can use this module in a few ways

1. Import the whole py4pa package::

   import py4pa

   sftp = py4pa.SFTP(
      host = 'sftp.example.com',
      user = 'example_username',
      pword = 'abcd1234',
      port = 22
   )

   sftp.list_files()

2. Import the module directly::
   
   from py4pa import SFTP

   sftp = SFTP(
      host = 'sftp.example.com',
      user = 'example_username',
      pword = 'abcd1234',
      port = 22
   )

   sftp.list_files()

Documentation
----------------------------

.. automodule:: py4pa.sftp
   :members:
   :undoc-members:
   .. :show-inheritance: