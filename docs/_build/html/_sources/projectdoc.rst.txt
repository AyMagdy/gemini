project documentation
=====================
.. toctree::
   :maxdepth: 4

introduction
------------
The whole idea of this project is to make the best use of the `Ouster Gemini <https://ouster.com/products/software/gemini>`_, A new kind of core spatial intelligence software that accurately detects, classifies, and tracks people, objects, and vehicles.
It is purpose built to address the critical need for highly accurate and dependable data, analytics, and live time tracking in the ITS, security, and crowd analytics industry. Through out this project the valubale 
data taken from the Gemini perception is received for furthur processing to make the most out of it that helps in creating more robust and convenient applications.
The project can be said to be divided into to parts first the part which can deals with the *configuration* of the ouster Gemini as a software and second that deals with the *received stream data* which will be the core of the application we want to develop.

Configuration
-------------
In this part the given APIs from Ouster are used to set the required settings, as well most of the GUI functions can be made through out scripts.
as GUI seemes to be a more convinient way to alter these settings but through the scripts it may be way to help in creating the required application,
for more explanation about each set of APIs refere to :ref:`code documentation APIs <apisection>` where the documentation and how to use information are given.

    #. Lidar_hub configuration -:doc:`gemini_lidar_hub_API`-
        deals with Sensor Management, Recording, Settings, Registration, Execution, Point Zones, Event Zones, Security, Diagnostics, Static.

    #. perception configuration -:doc:`gemini_perception_API`-
        deals with the required settings for ouster detect software that sets the work flow of the perception as detection of objects and the perception id.

    #. Event Zones -:doc:`gemini_event_zone_API`-
        deals with zones and the events ocurring in each zone.

    #. Gemini data: -:doc:`gemini_data_recording`- 
        deals with the output data of the gemini software

    #. gemini_login: -:doc:`gemini_login`-
        creates an authorized session for HTTPS requests, it is shared among the above modules to provide the base `URL` and authentication to send requests.
    
.. note::
    
    Not all APIs are implemented some APIs are still under development.
.. caution::

    The implemented APIs must be used with caution and response check is the user responsibility as all implementations returns only status code without error handling.

Recieved stream data
--------------------
Here as will be refered to as `src` or `source code` is the main starting point for making use of the Ouster detect software data since the Ouster software stack outputs 
reliable and filtered data, this data can be furthur furnished to develop a well established application. Relying on TCP servers *data will be streamed*, *saved to a queue* and 
from the queue *data will be fetched for processing*. All this will be done concurently using threads. 

the available JSON Streams.

    * object_list
    * occupations
    * clusters
    * diagnostics
    * aggregation_realtime
    * aggregation_timeseries

refere to `user manual <https://static.ouster.dev/ouster-detect/connecting_to_output/connecting-to-output.html>`_  for more specifications.

Code flow and Execution
-----------------------
After the socket connection is established, Three threads are created

    #. put_to_queue_thr:    
        This thread is responsible for **READING** data from the SSL socket connection and putting it into ``DATA_QUEUE`` . It uses the ``put_object_to_queue`` function from the ``processing.data_processing`` module.
   
    #. read_from_queue_thr: 
        This thread is responsible for **RETRIEVING** data from ``DATA_QUEUE`` and making it available for processing.It uses the ``get_from_queue`` function from the ``processing.data_processing`` module.
   
    #. process_thr:
        This thread is responsible for **PROCESSING** the data retrieved from the queue.It uses the ``processing_from_queue`` function from the ``processing.data_processing`` module.

           
 This application is an example for the future work it was made to be generic as possible by using the approch of modularity.
 in this application the time of collision is calculated following the preceeding steps.

    #. find the nearest two object to the sensor. (an information retrieved from the object list recieved from the stream)
    #. find the relative velocity magnitude between the same two objects. (the same time stamp is taken in consideratin to make sure the specific required object is found)
    #. find the relative position magnitude between the same two objects. 
    #. estimate the time of collision between the objects.

.. note::

    assumptions are made that both objects are heading towards the sensor and the written code is just a test for what may come later.

Data shape
----------
Data streamed refered to as ``object_list`` from gemini is received in JSON format which may be difficult to make furthur processing, so it was better to reorder the data depending on the timestamp
in a python dictionary with the time stamp as the key and the value will be the object it self. refere below to see what the JSON format looks like.

shape of received data from stream
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _object_example_ref:
.. code-block:: JSON

    {
      "frame_count": 226599,
      "timestamp": 1663175920089867
    "objects": [
    {
      "classification": "PERSON",
      "classification_confidence": 0,
      "creation_ts": 1663175901389312,
      "dimensions": {
        "height": 0.6693140268325806,
        "length": 0.44045835733413696,
        "width": 0.24217760562896729
      },
      "distance_to_primary_sensor": 1.8241156339645386,
      "frame_count": 188,
      "heading": 17.792495727539062,
      "id": 1094,
      "initial_position": {
        "x": 0.866864025592804,
        "y": -1.3293535709381104,
        "z": 1.1521248817443848
      },
      "num_points": 1052,
      "num_points_from_primary_sensor": 706,
      "orientation": {
        "qw": 0.9879699945449829,
        "qx": 0,
        "qy": 0,
        "qz": 0.15464559197425842
      },
      "position": {
        "x": 0.9670451879501343,
        "y": -1.5673401355743408,
        "z": 1.0692270994186401
      },
      "position_uncertainty": {
        "x": 0.00872983346207417,
        "y": 0.00872983346207417,
        "z": 0.03328978381826185
      },
      "primary_sensor": "992251000353",
      "update_ts": 1663175920076580,
      "uuid": "74b4e42e-1989-40d0-91d6-ae498b173001",
      "velocity": {
        "x": -0.03508763682949244,
        "y": 0.01674633024355329,
        "z": 0.029468615562023993
      },
      "velocity_uncertainty": {
        "x": 0.7745966692414834,
        "y": 0.7745966692414834,
        "z": 0.8143665760550121
      }
    },
    {
      "classification": "UNKNOWN",
      "classification_confidence": 0,
      "creation_ts": 1663175902884161,
      "dimensions": {
        "height": 0.5432571172714233,
        "length": 0.48804545402526855,
        "width": 0.20569449663162231
      },
      "distance_to_primary_sensor": 1.8241156339645386,
      "frame_count": 171,
      "heading": -89.16230010986328,
      "id": 1096,
      "initial_position": {
        "x": 0.9158645868301392,
        "y": -1.8394945859909058,
        "z": 0.7948745489120483
      },
      "num_points": 539,
      "num_points_from_primary_sensor": 706,
      "orientation": {
        "qw": 0.7122570276260376,
        "qx": 0,
        "qy": 0,
        "qz": -0.7019187808036804
      },
      "position": {
        "x": 0.7764403223991394,
        "y": -1.7604234218597412,
        "z": 0.9274996519088745
      },
      "position_uncertainty": {
        "x": 0.00872983346207417,
        "y": 0.00872983346207417,
        "z": 0.03328978381826185
      },
      "primary_sensor": "992251000353",
      "update_ts": 1663175920076580,
      "uuid": "b3caf8eb-8e23-47fe-a839-999f354ae4a0",
      "velocity": {
        "x": -0.10920844900324483,
        "y": 0.31853616628659553,
        "z": 0.10758132742665225
      },
      "velocity_uncertainty": {
        "x": 0.7745966692414834,
        "y": 0.7745966692414834,
        "z": 0.8143665760550121
      }
    }
    ]
    }


.. list-table:: object_list description
    :widths: 10 25 50
    :header-rows: 1

    * - Field
      - Format
      - Definition
    
    * - frame_count
      - int
      - Number of frames since perception started outputting data. This count should always be sequential.

    * - timestamp
      - int
      - Timestamp of when the last point cloud arrived which contributed to the object list. Units in microseconds since Jan. 1, 1970.
   
    * - objects
      - array
      - Array of :ref:`objects <object_array description>` visible to perception for the current frame

.. _object_array description:
.. list-table:: object_array description
    :widths: 10 25 50
    :header-rows: 1

    * - Field
      - Format
      - Definition

    * - id
      - int
      - Unique number identifying object in current running instance of perception. If perception restarts, this count will reset.

    * - uuid
      - string
      - Unique UUID for objects over all running instances. If perception restarts, objects in the new running instance will have unique UUID’s relative to all other running instances.

    * - primary_sensor
      - string
      - Serial number of the primary lidar sensor with the most points on object.
   
    * - distance_to_primary_sensor
      - float
      - Distance in meters from the primary lidar sensor.
    
    * - num_points_from_primary_sensor
      - int
      - Number of points on object from the primary lidar sensor.

    * - num_points
      - int
      - Number of points belonging to the object.
   
    * - classification
      - string
      - Classification of the object (i.e., PERSON, VEHICLE).
   
    * - classification_confidence
      - float
      - Number between 0 and 1 representing the system’s confidence in the assigned classification. 0 represents no confidence. 1 represents fully confident.

    * - initial_position
      - vector
      -  Initial XYZ location of the object in the first frame it was visible in the field of view of the lidars. This position is either in respect to the world reference frame (measured in meters), or the geo-coordinates.
   
    * - position
      - vector
      - Current XYZ location of the object in the world reference frame (measured in meters), or the geo-coordinates.
    
    * - position_uncertainty
      - vector
      - Estimated variance of the position measurement. Units in meters^2.
    
    * - velocity
      - vector
      - current rate of change in the XYZ position of the object. Velocity is in the world reference frame. Units are in m/s.
   
    * - velocity_uncertainty
      - vector 
      - Estimated variance of the velocity measurement. Units in (m/s)^2.

    * - orientation
      - orientation
      - Quaternion representing the orientation of the object with respect to the world reference frame.
   
    * - heading
      - float
      - Positive rotation about the z-axis (right-hand rule).

    * - dimension
      - dimension
      - Length, width, height of the bounding box enclosing all points on the object. Length is the extents along the x-axis, width the extents along the y-axis, height along the z-axis. Axis referenced are the axis of the object with x pointing in the direction of motion, y pointing perpendicular to the left, and z pointing up (right-hand rule). 
   
    * - frame_count
      - int
      - Number of frames an object has been visible for. This number and the creation_ts number both represent the duration the object has been in the sytem’s field of view.
   
    * - creation_ts
      - int
      - Timestamp when the object was first visible in the system’s field of view. This point in time will be before the object was tracked and classified. This number and frame_count both represent the duration the object has been in the sytem’s field of view. Units in microseconds since Jan. 1, 1970.
   
    * - update_ts
      - int
      - Timestamp the object was last updated. For objects the system has measured in the current frame, this timestamp will be the same as the timestamp at the root level. For objects the system has not measured in the current frame, this timestamp will stay at the timestamp when the object was last measured and lag behind the timestamp at the root level. An object will be considered measured when the lidars have captured a minimum number of points on the target. Units in microseconds since Jan. 1, 1970.


The previous :ref:`code snippet <object_example_ref>` shows the shape of the streamed data followed by its explanation in the tables. the code refines the data streamed and puts it in 
a python dictionary form as mentioned above. the global variable ``TIMESTAMP`` defined in ``processing.data_processing`` :ref:`module <processing_data_ref>` is the variable that will hold the refined data.
it consists of *key* as the *timestamp* and *dictionary values* where their *key* are the *name of the attribute* and the value *are lists of the data*. refere below for explanation

.. code-block::

    { 
    1701174658528965: {
    'obj_id': [11111, 22222, 33333, 44444],
    'creation_time': [1701174621516041, 1701174621516041, 1701174621516041, 1701174621516041],
    'frame_count': [343, 343, 343, 343],
    'classification': ['PERSON', 'PERSON', 'PERSON', 'PERSON'],
    'velocity': [{'x': 11, 'y': 11, 'z': 11}, {'x': 22, 'y': 22, 'z': 22}, {'x': 33, 'y': 33, 'z': 33}, {'x': 44, 'y': 44, 'z': 44}],
    'position': [{'x': 11, 'y': 11, 'z': 11}, {'x': -22, 'y': 22, 'z': 228}, {'x': -33, 'y': 33, 'z': 33}, {'x': -44, 'y': 44, 'z': 44}],
    'heading':  [11, -37.560306549072266, -37.560306549072266, -37.44]
    }
    }

.. tip::

    every object is known by its obj_id and to get the related information of that specific obj_id use indexing.
    for example in the above data shape. ``obj_id`` 11111 will have index 0 then to locate its velocity for example index ``velocity`` with index 0.
    
    .. code-block::

        print(timestamp[1701174658528965]['velocity'][0])

        >>> {'x': 11, 'y': 11, 'z': 11}

this made the data more refined and every time stamp is known what objects are captured within it with each information related to that object.

.. note::

    for calculations this data is converted to pandas DataFrame for the ease of its calculations. refere to the helper methods at :ref:`processing.utils module <processing_utils_ref>`


Data integrity
--------------
To make sure that each object has a unique ID we have to make sure that the sensors installed are all in the same perception. 
The ouster detect software stack gives each object a unique ID ``uuid`` once it is detected in the perception if the object lost from the perception and enters again 
the ouster detect will give it a new ``uuid`` so its our responsibility to make sure that our interested area is fully covered and the sensors area of coverage are well
installed to make sure that if an object never leaves our area of interest. another consideration while receiveing through the stream to make sure that we don't loose any 
data or we get an interrupted message ouster software stack sends a 32-bit unsigned integer with big endian byte order which represents the total length of the message
by checking on these 4-bytes we know the size of the expected data to receive. see ``put_object_to_queue`` method at :ref:`processing.data_processing module <processing_data_ref>`



