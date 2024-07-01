Lidar Hub
=========

Description
-----------
The module is used to set/get the setting of the Lidar Hub . 
Lidar Hub works as the interface between the ouster detect software and the user. it integrates other features as well.
    
    #. On-device Aggregation of occupations and object lists
    #. The gathering and reporting of Diagnostics and Alerts to the Ouster Connect
    #. Down-sampling, Batching and Filtering of Perception JSON Streams used by: - TCP Relay
    #. Server(s) - MQTT Publishers
    #. On-device Data Recording of JSON Streams and Point Cloud data

The module uses ``URL`` located at :doc:`gemini_login` as the base url.

.. note::

    for more information on the module and for the information about the fields that can be altered in the
    JSON files being sent as request body please refere to the `user manual <https://static.ouster.dev/ouster-detect/lidar_hub/lidar_hub.html#>`_.

.. automodule:: gemini_lidar_hub_API
   :members:
   :undoc-members:
   :show-inheritance:
