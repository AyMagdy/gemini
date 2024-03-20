from typing import Callable,Literal,TypeAlias
import pandas as pd
import ssl, socket
import logging

logger = logging.getLogger(__name__)
# List of the componets found in the object_list

object_key: TypeAlias = Literal['id','uuid','classification','classification_confidence',
'creation_ts','update_ts','dimensions','frame_count','heading',
'initial_position','num_points','position','position_uncertainty',
'velocity','velocity_uncertainty','distance_to_primary_sensor']

""" Description:
        this is a type alias used to refere to the object to be selected or the object
        of interest from the recieved object list created by the ouster detect software.
    Usage:
        it is used as a parameters sent to the function in this module to search in
        the array of the recieved object list.

""" 
# List of the root level information returned from the ouster detect software
rootinfo_key: TypeAlias = Literal['frame_count','timestamp','objects']

""" Description:
        this is a type alias used to refere to the object to be selected or the object
        of interest from the recieved object list created by the ouster detect software.
    Usage:
        it is used as a parameters sent to the function in this module to search in
        the array of the recieved object list.

""" 




# Function to get the root information of the streamed object_list data
def get_root_info(data: dict,key: rootinfo_key)-> list:
    """ Description:
            This function is used to fetch for the root data of the recieved object.
        
        Args:
            data: which is the recieved object.
            key: which is the desired information or data (rootinfo_key: TypeAlias)
        
        Returns:
            list of the fetched data ex: frame_count, timestamp 
        
    we use the TypeAlisa (rootinfo_key: TypeAlias)
    """
    val = []
    for i in range(len(data['object_list'])):
        val.append(data['object_list'][i][key])
    return val
       

# Function to get an individual component of the object_list 
def get_object_list_arr(data: dict,stamp: int,key: object_key)-> list:
    """ Description:
            This function is used to fetch in the object data of the recieved object list.
        
        Args:
            data: which is the recieved object list.
            key: which is the desired information or data we want refere to "object_key: TypeAlias"
        
        Returns:
            list of the fetched data ex: id, velocity, position, distance_to_primary_sensor 
    """ 
    val = []
    for i in range(len(data['object_list'][stamp]["objects"])):
        val.append(data['object_list'][stamp]["objects"][i][key])
    return val


# receives data from tcp stream
def recv_stream(ssl_socket_client: ssl.SSLSocket , num_bytes: int)->bytearray:
    """
        Description:
            recieves directly form the socket listens to the server and recieve.
        Args:
            ssl_socket_client for the connection of the server
            num_byte number of bytes to be recieved
        Returns:
            bytearray

    """
    data = bytearray()
    while len(data) < num_bytes:
        remaining_bytes = num_bytes - len(data)
        try:
            packet = ssl_socket_client.recv(remaining_bytes) 
        except(socket.timeout,ConnectionResetError):
            return bytearray()
        data.extend(packet)
    return data



    




if __name__ == "__main__":
    logger.info(f"running from {__name__} as main")
    print(f"running from {__name__} as main")