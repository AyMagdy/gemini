import requests
from connection import socket_connection as connect





URL = f'https://{connect.HOST}/'
'''
It is the base url used through all the application.
'''
USERNAME = 'ouster'
PASSWORD = 'stone-pass-fill'


def login_ouster() -> requests.Session: 
    
    """
    Description
    -----------
    creates a session between host and server through HTTPS.

    ARGs
    ----
    None.
    
    Return
    ------
    requests.Session
        authorized session for HTTPS requests.
    """
    session = requests.Session()
    session.auth = (USERNAME,PASSWORD)
    session.get(URL,verify=False)
    return session



if __name__ == '__main__':

    session = login_ouster()