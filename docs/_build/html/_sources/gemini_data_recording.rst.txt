Data Recording
==============

Description
-----------
used to retreive the recorded data from the ouster perception.

The Lidar Hub has an on-device `JSON Data Recorder <https://static.ouster.dev/ouster-detect/lidar_hub/lidar_hub.html#json-data-recorder>`_ module with timed-rotation, retention period, compression and purge strategies. Object Lists, Occupations,
Aggregation and Diagnostics will be recorded into a combined file. By default, recordings are saved to /opt/ouster/conf/data/recordings/.

The Lidar Hub includes an on-device `Aggregation module <https://static.ouster.dev/ouster-detect/lidar_hub/lidar_hub.html#aggregation-module>`_  that aggregates zone occupations by timeseries by object classification. A system-defined classification of “ALL” will also be aggregated for each zone representing an aggregate of all objects. 
The Aggregation module also aggregates all tracked objects by timeseries by object classification into a system-defined site-wide zone with an id of 0

The module uses ``URL`` located at :doc:`gemini_login` as the base url.

.. note::

    for more information on the module and for the information about the fields that can be altered in the
    JSON files being sent as request body please refere to the `user manual <hhttps://static.ouster.dev/ouster-detect/lidar_hub/lidar_hub.html#json-data-recorder>`_.

    refere to the module :doc:`gemini_lidar_hub_API` to know how to set the fields to start and define the desired data for recording.

.. automodule:: gemini_data_recording
   :members:
   :undoc-members:
   :show-inheritance:
