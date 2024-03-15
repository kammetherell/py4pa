Quickstart Guide
================

Installation
------------

Install Python for People Analytics by running::

   pip install py4pa

Usage
-----

Simply either import the whole py4pa package::

   import py4pa

   log = py4pa.Log_File(
      directory = '/users/me/documents'
   )

   log.info('Info message')

Or import the modules you require directly::

   from py4pa import Log_File

   log = Log_File(
      directory = '/users/me/documents'
   )

   log.info('Info message')
