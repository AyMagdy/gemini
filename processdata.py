import threading
import concurrent.futures
import queue
import json
import socket
import ssl
import time
import pandas as pd
import numpy as np
import enum
import logging
from typing import Callable,Literal,TypeAlias


# List of the componets found in the object_list 
object_key: TypeAlias = Literal['id','uuid','classification','classification_confidence',
'creation_ts','update_ts','dimensions','frame_count','heading',
'initial_position','num_points','position','position_uncertainty',
'velocity','velocity_uncertainty']
# List of the root level information returned from the ouster detect software
rootinfo_key: TypeAlias = Literal['frame_count','timestamp','objects']
class data_order (enum.Enum):
    obj_id        = 0
    creation_time = 1
    frame_count   = 2
    velocity      = 3
    position      = 4
    heading       = 5
#Ouster detect defined variables
HOST = socket.gethostbyname(socket.gethostname())
PORT = 3302
ENDIAN_TYPE = "big"
FRAME_SIZE_B = 4
ADDRESS = (HOST,PORT)

# global variables to store data recieved from the queue
# shared resource between 
QUEUE_SIZE = 10
CREATION_TIME = {}
FRAME_COUNT = {}
CLASSIFICATION = {}
VELOCITY = {}
POSITION = {}
HEADING = {}
UPDATE_TIME = {}
TIMESTAMP = {}

# Fucntion used to set a socket connection and return a ssl wraped socket 
def connect_to_ssl_socket(address: tuple[str | None, int]) -> ssl.SSLSocket:
    
    try:
        logging.info("trying to connect")
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = ssl.CERT_NONE
        logging.info("connection established")
        return ssl_context.wrap_socket(socket.create_connection(address))
    except socket.error as msg:
        logging.info('connectin failed due to %s',msg)

# receives data from tcp stream
def recv(ssl_socket_client: ssl.SSLSocket, num_bytes: int)->bytearray: 
    data = bytearray()
    while len(data) < num_bytes:
        remaining_bytes = num_bytes - len(data)
        try:
            packet = ssl_socket_client.recv(remaining_bytes) 
        except(socket.timeout,ConnectionResetError):
            return bytearray()
        data.extend(packet)
    return data
# Writes the received data from the stream to a queue
def put_object_to_queue(ssl_socket_client: ssl.SSLSocket, queue: queue.Queue) -> None:
    """
        param: socket connection with ssl wrap
               queue to put received data in.
        return: None

        Description: read data from stream and put in queue for furthur processing.
    """
    logging.info("Active %s", (threading.current_thread().name))
    while True:
        logging.info("Active current thread right now: %s", (threading.current_thread().name))
        if (queue.qsize() < 10):
            logging.info("reading from tcp putting in queue queue size is %d",queue.qsize())
            frame_size_b = recv(ssl_socket_client, FRAME_SIZE_B)
            if len(frame_size_b) == 0:
                break
            frame_size = int.from_bytes(frame_size_b, byteorder=ENDIAN_TYPE)
            data = recv(ssl_socket_client, frame_size)
            if len(data) == 0:
                break
            data = json.loads(data.decode("utf-8"))
            queue.put(data)
        else:
            logging.info(f'..........queue IS FULLLLLLLLL.......{queue.qsize()}')

def read_from_queue(queue: queue.Queue,lock: threading.Lock):
    """
        param: queue to get timestamp and other data from 
               lock to lock on shared resource while writting
               
        return: NONE

        Descritpion: this function checks if the queue is not empty then
                     reads the time stamp of the received frame from queue.
                     time stamp is saved in TIMESTAMP global dictionary as the key.
                     the values are dictionaries of parameter name as key and values of 
                     the data values.
                     example: 	{1701174658528965: { 'obj_id': [11111, 22222, 33333, 44444] }
    """
    global TIMESTAMP
    
    temp = {}
    while True:
        logging.info("Active current thread right now: %s", (threading.current_thread().name))
        if not queue.empty():   # if queue is not empty pop to temp
            logging.info("reading from queue")
            temp           = queue.get(block=False)
            timestamp      = get_root_info(temp,'timestamp')    # list of all time stamps received 
            # iterate on each time stamp and save its objects' data
            for stamp in (timestamp):
                index = timestamp.index(stamp) 
                # list of the data specified by its name.
                obj_id         = get_object_list_arr(temp,index,'id')
                creation_time  = get_object_list_arr(temp,index,'creation_ts')
                frame_count    = get_object_list_arr(temp,index,'frame_count')
                classification = get_object_list_arr(temp,index,'classification') 
                velocity       = get_object_list_arr(temp,index,'velocity')
                position       = get_object_list_arr(temp,index,'position')
                heading        = get_object_list_arr(temp,index,'heading')

                obj = dict([('obj_id',obj_id),('creation_time',creation_time),
                            ('frame_count',frame_count),('classification',classification),
                            ('velocity',velocity),('position',position),('heading',heading)])
                # lock on TIMESTAMP while updating.
                with lock:
                    logging.info('read from queue has the lock')
                    TIMESTAMP.update({str(stamp):obj})
                    logging.info('size of TIMESTAMP is %s',TIMESTAMP)
                    logging.info("data shape is %s",TIMESTAMP)
            logging.info('read from queue released the lock')
            queue.task_done()
            
        else:
            logging.info('queue is empty no data to read ')
            time.sleep(1)
            

def get_velocity_diff(dataframe:pd.DataFrame,index1:int,index2:int)-> pd.Series:
    """
        param: dataframe: velocity dataframe to get the difference.
               index1: the first index/row in the dataframe required.
               index2: the second index/row in the dataframe required.
        
        return: pandas series of the calculated velocity difference between index1 and index2

        Description: a helper function to be called to find the difference between two rows
                     from the passed dataframe.

    """
    return dataframe.iloc[index1] - dataframe.iloc[index2]

def get_position_diff(dataframe:pd.DataFrame,index1:int,index2:int)-> pd.Series:
    """
        param: dataframe: position dataframe to get the difference.
               index1: the first index/row in the dataframe required.
               index2: the second index/row in the dataframe required.
        
        return: pandas series of the calculated position difference between index1 and index2

        Description: a helper function to be called to find the difference between two rows
                     from the passed dataframe.

    """
    return dataframe.iloc[index1] - dataframe.iloc[index2]

# post processing on the data from the global variables          
def processing_from_queue(lock:threading.Lock):
    """
        param: lock to protect shared resources
        
        return: None

        Description: read from TIMESTAMP and refine data 
                     creates a dictionary its key is the timestamp
                     and its values are lists of the data.
                     ex:{'1': [{'x': 11, 'y': 11, 'z': 11}, {'x': 12, 'y': 12, 'z': 12}, {'x': 13, 'y': 13, 'z': 13}, {'x': 14, 'y': 14, 'z': 14}], 
                         '2': [{'x': 21, 'y': 21, 'z': 21}, {'x': 22, 'y': 22, 'z': 22}, {'x': 23, 'y': 23, 'z': 23}, {'x': 24, 'y': 24, 'z': 24}]}
    """
    vel = {}
    pos = {}
    hed = {}
    while True:
        
        logging.info("Active current thread right now: %s", (threading.current_thread().name))
        with lock:
            if (TIMESTAMP != {}):
                logging.info('lock is acquired from%s',threading.current_thread())
                logging.info('from processing thread%s,%s,%s',ssl_thread.is_alive(),reading_thread.is_alive(),process_thread.is_alive())
                for key in TIMESTAMP.keys():
                    vel.update({key:TIMESTAMP[key]['velocity']})
                    pos.update({key:TIMESTAMP[key]['position']})
                    hed.update({key:TIMESTAMP[key]['heading']})
            else:
                logging.info('no time stamp found')
        logging.info("loock is released from processing thread")
        """
            processing of data frame begins here
            problem in implementing correct shape of dataframe 
            that depends on the timestamp to perfomr required calculations
            to predict if object is going to collide with each other
            or wether they have collided already.
        """
        veldf = pd.DataFrame.from_dict(vel)
        posdf = veldf = pd.DataFrame.from_dict(pos)
        heddf = veldf = pd.DataFrame.from_dict(pos)
        print(posdf)
        # if(get_position_diff(posdf,1,0)['x'] == 0 or get_position_diff(posdf,1,0)['y'] == 0):
        #     print('collision occured')
        # else:
        #     logging.info("x: %d, y: %d",get_position_diff(posdf,1,0)['x'] ,get_position_diff(posdf,1,0)['y'])
        #     print(get_position_diff(posdf,1,0)['x'] ,get_position_diff(posdf,1,0)['y'] ,sep='--->')

# Function to get the root information of the streamed object_list data
def get_root_info(data: dict,key: rootinfo_key)-> list:
    val = []
    for i in range(len(data['object_list'])):
        val.append(data['object_list'][i][key])
    return val
       

# Function to get an individual component of the object_list 
def get_object_list_arr(data: dict,stamp: int,key: object_key)-> list: 
    val = []
    for i in range(len(data['object_list'][stamp]["objects"])):
        val.append(data['object_list'][stamp]["objects"][i][key])
    return val




if __name__ == '__main__':

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(filename='mylogfile.log',filemode='w',format=format, level=logging.INFO,datefmt="%H:%M:%S")
    # creat a queue to receive from TCP stream
    data_queue = queue.Queue(maxsize=QUEUE_SIZE)
    
    # Creat an ssl socket connection
    ssl_socket_client = connect_to_ssl_socket(ADDRESS)
    
    # Creat lock
    ssl_lock = threading.Lock()
    with ssl_socket_client:
        # Creat threads
        ssl_thread = threading.Thread(target=put_object_to_queue,args=(ssl_socket_client,data_queue))
        reading_thread = threading.Thread(target=read_from_queue,args=(data_queue,ssl_lock))
        process_thread = threading.Thread(target=processing_from_queue,args=(ssl_lock,))
        logging.info('this is the main thread %s %s %s',ssl_thread.is_alive(),reading_thread.is_alive(),process_thread.is_alive())
        
        # Start threads
        ssl_thread.start()
        reading_thread.start()
        process_thread.start()
               
        # Wait for threads
        ssl_thread.join()
        reading_thread.join()
        process_thread.join()
        #data_queue.join()
       
        # end of main thread
        print("end of program")

        
