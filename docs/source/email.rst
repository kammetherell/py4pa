Email
=====

The Email enables you to send emails via Python, 
including attachments, and with HTML styling.

Usage
-----
You can use this module in a few ways

1. Import the whole py4pa package::

      import py4pa

      email = py4pa.Email(
         sender = 'test@gmail.com',
         server_add = 'relay.local',
         server_port = 25
      )

      log.info('Info message')

2. Import the module directly::
   
      from py4pa import Email

      email = Email(
         sender = 'test@gmail.com',
         server_add = 'relay.local',
         server_port = 25
      )

      log.info('Info message')


Documentation
----------------------------

.. autoclass:: py4pa.Email
   :members:
   :undoc-members:
   :show-inheritance: