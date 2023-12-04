import json
import threading
import concurrent.futures
import json
import socket
import ssl
from typing import Callable,Literal,TypeAlias

object_key: TypeAlias = Literal['id','uuid','classification','classification_confidence',
                                'creation_ts','update_ts','dimensions','frame_count','heading',
                                'initial_position','num_points','position','position_uncertainty',
                                'velocity','velocity_uncertainty']

rootinfo_key: TypeAlias = Literal['frame_count','timestamp','objects']

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3302
#Ouster detect defined variables
ENDIAN_TYPE = "big"
FRAME_SIZE_B = 4
ADDRESS = (HOST,PORT)

def recv(socket_client: ssl.SSLContext, num_bytes: int)->bytearray: # type: ignore
    data = bytearray()
    while len(data) < num_bytes:
        remaining_bytes = num_bytes - len(data)
        try:
            packet = socket_client.recv(remaining_bytes) # type: ignore
        except(socket.timeout,ConnectionResetError):
            return bytearray()
        data.extend(packet)
        return data
    
def read_frames(socket_client: ssl.SSLContext) -> None:
    while True:
        frame_size_b = recv(socket_client, FRAME_SIZE_B)
        if len(frame_size_b) == 0:
            return
        frame_size = int.from_bytes(frame_size_b, ENDIAN_TYPE)
        data = recv(socket_client, frame_size)
        if len(data) == 0:
            return
        data = json.loads(data.decode("utf-8"))
        return data        
        #callback_function(data, *args)

def get_root_info(data: dict,key: rootinfo_key)-> str:
        return (data['object_list'][0][key])

def get_object_list_arr(data: dict,key: object_key)-> str: 
        return (data['object_list'][0]["objects"][0][key])

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
ssl_context.verify_mode = ssl.CERT_NONE
socket_client = ssl_context.wrap_socket(socket.create_connection(ADDRESS))

data = read_frames(socket_client) # type: ignore


d1 = get_root_info(data,'timestamp') # type: ignore
d2= get_object_list_arr(data,'classification') # type: ignore
print(d1,d2,sep=' ---> ')
    
socket_client.close()
