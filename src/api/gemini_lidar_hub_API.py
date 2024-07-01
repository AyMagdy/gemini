import requests
import json
import gemini_login as login
from enum import Enum


class LidarHubEndPoint (Enum):
    """

    defines the endpoints of the url for more information refer to `ouster swagger api documentation <https://127.0.0.1/lidar-hub/api/v1/swagger/ui#/>`_
    """

    STATIC_INFO                      = 'lidar-hub/api/v1/about'     
    SYSTEM_DIAGNOSTICS               = 'lidar-hub/api/v1/diagnostics'
    SYSTEM_HEALTH                    = 'lidar-hub/api/v1/system_health'
    LIDAR_TELEMETRY                  = 'lidar-hub/api/v1/telemetry'
    LIDAR_HUB_DEFAULTS               = 'lidar-hub/api/v1/default_settings'
    LIDAR_HUB_SETTINGS               = 'lidar-hub/api/v1/settings' 
    LIDAR_HUB_WORLD                  = 'lidar-hub/api/v1/world'
    LIDAR_HUB_EVENT_ZONES            = 'lidar-hub/api/v1/event_zones'
    LIDAR_HUB_EVENT_ZONES_ACTIVE     = 'lidar-hub/api/v1/event_zones/active'
    LIDAR_HUB_EVENT_ZONES_ALERTS     = 'lidar-hub/api/v1/event_zones/alerts'
    LIDAR_HUB_EVENT_ZONES_REALTME    = 'lidar-hub/api/v1/event_zones/realtime'
    LIDAR_HUB_EVENT_ZONES_TIMESERIES = 'lidar-hub/api/v1/event_zones/timeseries'
    LIDAR_HUB_RESET                  = 'lidar-hub/api/v1/reset'
    LIDAR_HUB_ACTIVE_REC             = 'lidar-hub/api/v1/user_recording/active'
    LIDAR_HUB_START_REC              = 'lidar-hub/api/v1/user_recording/start'
    LIDAR_HUB_STOP_REC               = 'lidar-hub/api/v1/user_recording/stop'



def get_lidar_hub_info(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    gets the static information about the lidar hub.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.STATIC_INFO.value)

def get_lidar_hub_diagnostics(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    gets the diagnostics hub.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.SYSTEM_DIAGNOSTICS.value)

def get_lidar_hub_health(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    gets the system health.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.SYSTEM_HEALTH.value)

def get_lidar_hub_telemetry(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get Lidar Hub ‘telemetry’ information.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_TELEMETRY.value)

def get_lidar_hub_default_settings(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get the application default values
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_DEFAULTS.value)

def reset_lidar_hub_default_settings(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    restores the default values.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.put(login.URL + LidarHubEndPoint.LIDAR_HUB_DEFAULTS.value)

def get_lidar_hub_all_settings(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get all application settings.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_SETTINGS.value)

def set_lidar_hub_all_settings(session : requests.Session,data_file:str) -> requests.Response:
    """
    Description
    ----------- 
    setts all application to the desired settings.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    data_file: str
        the path to the settings file in **JSON** format.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(data_file,'rt') as file:
        request_body = json.load(file)
    return session.post(login.URL + LidarHubEndPoint.LIDAR_HUB_SETTINGS.value,json=request_body)

def get_lidar_hub_world_coordinates(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get the Geo-coordinates.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_WORLD.value)

def set_lidar_hub_world_coordinates(session : requests.Session,data_file:str) -> requests.Response:
    """
    Description
    ----------- 
    sets the world Geo-coordinate
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    data_file: str
        a file required to read the new settings in **JSON** format.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(data_file,'rt') as file:
        request_body = json.load(file)
    return session.put(login.URL + LidarHubEndPoint.LIDAR_HUB_WORLD.value, json=request_body)

def get_lidar_hub_event_zones(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get the evnet zones in the perception.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_EVENT_ZONES.value)

def get_lidar_hub_event_active(session : requests.Session,ids: str =str(0),classification:str=str(0),min_dwell_secs : float=0) -> requests.Response:
    """
    Description
    ----------- 
    Query Active Occupancy by ID, Classification and Dwell
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    ids: str
        even zode ID (default = 0: ALL)
    classification: str
        classification class required (default = 0: ALL)
    min_dwell_secs: float
        minimum dwell in seconds (default = 0.0)
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_EVENT_ZONES_ACTIVE.value, 
                            params={'ids':ids,'classification':classification,'min_dwell_secs':min_dwell_secs})

def get_lidar_hub_event_alerts(session : requests.Session)  -> requests.Response:
    """
    Description
    ----------- 
    Get the alerts for all evnet zones.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_EVENT_ZONES_ALERTS.value)

def get_lidar_hub_event_realtime(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get real time occupancy of all event zones.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_EVENT_ZONES_REALTME.value)

def get_lidar_hub_event_timeseries(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get time series for all event zones.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_EVENT_ZONES_TIMESERIES.value)

def reset_lidar_hub (session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    restarts the lidar hub.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.put(login.URL + LidarHubEndPoint.LIDAR_HUB_RESET.value)

def get_lidar_hub_active_rec(session : requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Get active user recordings.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_ACTIVE_REC.value)

def start_lidar_hub_rec(session : requests.Session,body_path: str) -> requests.Response:
    """
    Description
    ----------- 
    starts a user reconrding.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    body_path: str
        the path to the request body file in **json** format.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(body_path,'rt') as file:
        request_body = json.load(file)
    return session.post(login.URL + LidarHubEndPoint.LIDAR_HUB_START_REC.value,json = request_body)

def stop_lidar_hub_rec(session : requests.Session,id:str) -> requests.Response:
    """
    Description
    ----------- 
    stops a user recording.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    id: str
        query for the id for the required recording to be stopped.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get(login.URL + LidarHubEndPoint.LIDAR_HUB_STOP_REC.value,params={'id':id})


if __name__ == '__main__':
    session = login.login_ouster()

    # sensor = LidarHubEventZones(login.URL,session).get_lidar_hub_event_timeseries().text
    # print(sensor)
    # print(160*'-')
    # print(LidarHubEventZones(login.URL,session).get_lidar_hub_event_realtime().text)
    # print(160*'-')
    # print(LidarHubEventZones(login.URL,session).get_lidar_hub_event_zones().text)
    print(set_lidar_hub_all_settings(session= session,data_file='/home/aymanlinux/ouster/ousterenv/ousterrepo/lidar_hub_config.json').status_code)