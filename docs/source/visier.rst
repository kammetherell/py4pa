Visier
=====

The Visier modules enable you to interact with either the Visier API, 
or to ingest a Visier Data Connector.

Usage
-----
You can use this module in a few ways

1. Import the whole py4pa package::

      import py4pa

      api = py4pa.VisierAPI(...)
      data_api = api.query_api(...)


      data_connector = py4pa.VisierDataConnector(...)
      data_dc = data_connector.get_connector(...)

2. Import the module directly::
   
      from py4pa import VisierAPI, VisierDataConnector

      api = VisierAPI(...)
      data_api = api.query_api(...)


      data_connector = VisierDataConnector(...)
      data_dc = data_connector.get_connector(...)


Documentation
----------------------------

.. autoclass:: py4pa.VisierAPI
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: py4pa.VisierDataConnector
   :members:
   :undoc-members:
   :show-inheritance: