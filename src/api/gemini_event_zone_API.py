import requests
import json
import gemini_login 
from enum import Enum



class EventEndPoint(Enum):
    """
    defines the endpoints of the url for more information refer to `ouster swagger api documentation <https://127.0.0.1/event/api/v1/swagger/ui>`_
    """
    GET_ALL_EVENTS = 'event/api/v1/event_zones/'
    ADD_ZONES      = 'event/api/v1/event_zones/'
    ADD_ZONE_ID    = 'event/api/v1/event_zones/'
    REMOVE_ZONE_ID = 'event/api/v1/event_zones'
    DIAGNOSTICS    = 'event/api/v1/telemetry'
    STATIC_INFO    = '/event/api/v1/about'


# Write a file with the telemetry recieved data
def get_event_zone_telemetry(session :requests.Session,file_type: str ='txt') -> requests.Response:
    """
    Description
    ----------- 
    writes telemetry information from the server to afile.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    file_type: str
        select the required file type to write the response to .txt, .json. (default .txt)
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    response = session.get(gemini_login.URL + EventEndPoint.DIAGNOSTICS.value)
    if file_type == 'txt':
        with open('telemetry00.txt','wt') as file:
            file.write(response.text)
    else:
        with open('telemetry00.json','wt') as file:
            file.write(response.text)
    return response

# Add multiple zones
def add_event_zone_zones(session : requests.Session,data:str) -> requests.Response:
    """
    Description
    ----------- 
    Add multiple zones at once
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    data: str
        the path to the file containing information of the zones to be created.
   
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(data,'r') as file:
        body = json.load(file)
    return session.put(gemini_login.URL + EventEndPoint.ADD_ZONES.value,json=body)
'''###########################################################'''
# Get all created zones
def get_event_zone_all_zones(session : requests.Session,file_type : str='txt') -> requests.Response:
    """
    Description
    ----------- 
    gets all event zones in the perception.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    file_type: str
        select the required file type to write the response to .txt, .json. (default .txt)
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    response = session.get(gemini_login.URL + EventEndPoint.GET_ALL_EVENTS.value)
    if file_type == 'txt':
        with open('zones00.txt',mode='wt') as file:
            file.write(response.text)
    else:
        with open('zones00.json',mode='wt') as file:
            file.write(response.text)
    return response
'''#############################################################'''
# Add a zone with unique ID
def add_zone_id(session:requests.Session,zone_id:str,data:str):
    """
    Description
    ----------- 
    Adds a unique zone with an ID.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    zone_id: str
        the ID of the zone to be added
    data: str
        the file path of the information of the added zone in *json* format
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.put(f"{gemini_login.URL}{EventEndPoint.ADD_ZONE_ID.value}{zone_id}",json=data)



if __name__ == '__main__':
    
    session = gemini_login.login_ouster()
    #get_telemetry(session=s)
    #add_zones(s,'/home/aymanlinux/ouster/ousterenv/gemini/addzones.json')
    get_event_zone_telemetry(session,'json')
    #respond = add_zone_id(s,5,{"id": 5, "name": "Single New Zone", "min_height": -10.0, "max_height": 10.0, "vertices": [ { "x": -100.0, "y": -100.0 },{ "x": -100.0, "y": 100.0 }, { "x": 100.0, "y": 100.0 }, { "x": 100.0, "y": -100.0 } ] })
    #print(respond.url,respond.text,respond.status_code,sep='\n')



