import socket
import ssl
import logging

logger = logging.getLogger(__name__)

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3302

ADDRESS = (HOST,PORT)
"""
    A global tuple constant to show the host and port to creat socket connection to it
"""
# Fucntion used to set a socket connection and return a ssl wraped socket 
def connect_to_ssl_socket(address: tuple[str | None, int] = ADDRESS) -> ssl.SSLSocket:
    """
        Description: 
            this function creats a socket connection and gives it a SSL wrap.
        Args: 
            address a tuple can be passed with host and port number defualt value (locla.host,3302)
        Returns:
            sslsocket 
    """
    try:
        logger.info("trying to connect")
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        ssl_context.verify_mode = ssl.CERT_NONE
        logger.info("connection established")
        return ssl_context.wrap_socket(socket.create_connection(address))
    except socket.error as msg:
        logger.info('connectin failed due to %s',msg)
        return False # type: ignore


if __name__ == '__main__':
    if not connect_to_ssl_socket(ADDRESS):
        print('connection established')
    else:
        print('connection failed')