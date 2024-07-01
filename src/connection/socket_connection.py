import socket
import ssl
import logging

# define the logger to be used
logger = logging.getLogger(__name__)

HOST = socket.gethostbyname(socket.gethostname())
"""
Defines the host requiresd to connect which is local host by default.
"""
PORT_OBJECT_LIST = 3302
"""
Defines the port to listen to during receiving 3302 by default which is the object_list on tcp_server.
"""
ADDRESS = (HOST,PORT_OBJECT_LIST)
"""
tuple:
    A global  constant to show the host and port to creat socket connection to it
"""

# Fucntion used to set a socket connection and return a ssl wraped socket 
def connect_to_ssl_socket(address: tuple[str | None, int] = ADDRESS) -> ssl.SSLSocket:
    """
    Description
    ----------- 
    this function creats a socket connection and gives it a SSL wrap.
    
    Args
    ----
    address: tuple 
        the host and the port needed to connect to.
        ('local.host,3302' default).
    
    Returns
    -------
    ssl.SSLSocket
        a socket connection with SSL/TLS wrap.
    """
    try:
        
        logger.info("trying to connect")
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        logger.info("connection established")
        sock = ssl_context.wrap_socket(socket.create_connection(address))
        return sock
    except socket.error as msg:
        logger.info('connectin failed due to %s',msg)
        return False # type: ignore


if __name__ == '__main__':
    if  connect_to_ssl_socket(ADDRESS):
        print('connection established')
    else:
        print('connection failed')