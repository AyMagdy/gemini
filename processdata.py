import threading
import queue
import json
import socket
import ssl
import pandas as pd
import numpy as np
import enum
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
#Ouster detect defined variables
HOST = socket.gethostbyname(socket.gethostname())
PORT = 3302
ENDIAN_TYPE = "big"
FRAME_SIZE_B = 4
ADDRESS = (HOST,PORT)

# global variables to store data recieved from the queue

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
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context.wrap_socket(socket.create_connection(address))
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
    while True:
        frame_size_b = recv(ssl_socket_client, FRAME_SIZE_B)
        if len(frame_size_b) == 0:
            break
        frame_size = int.from_bytes(frame_size_b, byteorder=ENDIAN_TYPE)
        data = recv(ssl_socket_client, frame_size)
        if len(data) == 0:
            break
        data = json.loads(data.decode("utf-8"))
        queue.put(data)

def timestamp_from_queue(queue: queue.Queue):

    global UPDATE_TIME
    global CREATION_TIME
    global FRAME_COUNT
    global CLASSIFICATION
    global VELOCITY
    global POSITION
    global HEADING
    global TIMESTAMP
    
    temp = {}
    while True:
        if not queue.empty():
            temp = queue.get()
            timestamp = get_root_info(temp,'timestamp')
            obj_id      = get_object_list_arr(temp,'id')
            creation_time = get_object_list_arr(temp,'creation_ts')
            frame_count = get_object_list_arr(temp,'frame_count')
            classification = get_object_list_arr(temp,'classification')
            velocity = get_object_list_arr(temp,'velocity')
            position = get_object_list_arr(temp,'position')
            heading = get_object_list_arr(temp,'heading')

            TIMESTAMP.update({timestamp:[obj_id,creation_time,frame_count,velocity,position]})

            queue.task_done()
    
# post processing on the data from the global variables          
def process_from_queue(lock:threading.Lock):
    vel = []
    
    while True:
        lock.acquire()
        for key in TIMESTAMP.keys():
            vel = TIMESTAMP[key][data_order.velocity.value]
            # print(vel)
            df = pd.DataFrame.from_dict(vel).transpose()
            df["ss"] = df.apply(lambda x: x[1] - x[0] ,axis=1)
            print(df)



        lock.release()

# Function to get the root information of the streamed object_list data
def get_root_info(data: dict,key: rootinfo_key)-> str:
        return (data['object_list'][0][key])

# Function to get an individual component of the object_list 
def get_object_list_arr(data: dict,key: object_key)-> list: 
    val = []
    for i in range(len(data['object_list'][0]["objects"])):
        val.append(data['object_list'][0]["objects"][i][key])
    return val

if __name__ == '__main__':
    # creat a queue to receive from TCP stream
    data_queue = queue.Queue(maxsize=0)
    
    # Creat an ssl socket connection
    ssl_socket_client = connect_to_ssl_socket(ADDRESS)
   
    # Creat lock
    ssl_lock = threading.Lock()

    with ssl_socket_client:
        # Creat threads
        ssl_thread = threading.Thread(target=put_object_to_queue,args=(ssl_socket_client,data_queue))
        time_thread = threading.Thread(target=timestamp_from_queue,args=(data_queue,))
        process_thread = threading.Thread(target=process_from_queue,args=(ssl_lock,))
       
        # Start threads
        ssl_thread.start()
        #get_thread.start()
        time_thread.start()
        process_thread.start()
       
        # Wait for threads
        ssl_thread.join()
        #get_thread.join()
        time_thread.join()
        process_thread.join()
        # data_queue.join()
       
        print("end of program")

        
