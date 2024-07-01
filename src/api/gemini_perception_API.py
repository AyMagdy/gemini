import json
import requests
import gemini_login as login
from enum import Enum

class PerceptionEndPoint(Enum):
    """

    defines the endpoints of the url for more information refer to `ouster swagger api documentation <https://127.0.0.1/perception/api/v1/swagger/ui>`_
    """
    LIST_OF_ALL_SENSORS = 'perception/api/v1/sensor/' 
    CLEAR_ALL_LIDARS = 'perception/api/v1/sensor/'
    GET_SENSOR_BY_STATUS = 'perception/api/v1/sensor/'
    ADD_SENSOR = 'perception/api/v1/sensor/'
    REMOVE_SENSOR = 'perception/api/v1/sensor/'
    LOAD_BACKGROUND ='perception/api/v1/background'
    SAVE_BACKGROUND ='perception/api/v1/background'
    SETTINGS        = 'perception/api/v1/settings/'
    UNDERLAY_MAP    = 'perception/api/v1/underlay/'
    UNDERLAY_CONFIG = 'perception/api/v1/underlay_config/'
    SET_PROFILE     = 'perception/api/v1/set_profile/'
    GET_PROFILE     = 'perception/api/v1/profile/'
    DEFAULT_PROFILE = 'perception/api/v1/profile_defaults/'
    LIST_PROFILES   = 'perception/api/v1/profiles/'
    RESTORE_PROFILE = 'perception/api/v1/restore_profile/'
    IMU_POSE = 'Perception/api/v1/imu_pose/'
    ALL_EXTRINSICS = 'perception/api/v1/extrinsics/'
    ICP_ALGORITHM = 'perception/api/v1/extrinsics/icp/'



def get_all_sensors(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    gets full list of sensors connected to perception pipeline.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get( login.URL + PerceptionEndPoint.LIST_OF_ALL_SENSORS.value)
        
def clear_all_lidars(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    removes all lice sensors from perception.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.delete( login.URL+ PerceptionEndPoint.CLEAR_ALL_LIDARS.value)

def get_sensor_by_status(session :requests.Session,status:str) -> requests.Response:
    """
    Description
    ----------- 
    gets list of sensors with the passed status query.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    status: str
        active or inactive
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get( login.URL+ PerceptionEndPoint.GET_SENSOR_BY_STATUS.value + status)

def add_senor(session : requests.Session,host_name:str) -> requests.Response:
    """
    Description
    ----------- 
    adds a new sensor to perception.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    host_name: str
        the address of the sensor to be added.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get( login.URL + PerceptionEndPoint.ADD_SENSOR.value + host_name)

def remove_sensor(session : requests.Session,sensor_id:str) -> requests.Response:
    """
    Description
    ----------- 
    removes the sensor with the passed query sensor_id.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    sensor_id: str
        required senosr serial number to be removed.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.delete( login.URL+ PerceptionEndPoint.REMOVE_SENSOR.value + sensor_id)

def load_backgrounds(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Load all current background available for all sensors.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.put( login.URL + PerceptionEndPoint.LOAD_BACKGROUND.value)

def save_backgrounds(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    Save background for all sensors.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.post( login.URL+ PerceptionEndPoint.SAVE_BACKGROUND.value)
    

def get_perception_settings(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    get all current settings.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get( login.URL+ PerceptionEndPoint.SETTINGS.value)

def set_perception_setting(session: requests.Session,body_path : str) -> requests.Response:
    """
    Description
    ----------- 
    sets all perception settings.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    body_path: str
        path to the file with the required settings in **JSON** format.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(body_path,'rt') as file:
        request_body = json.load(file)
        print(request_body)
    print(login.URL+ PerceptionEndPoint.SETTINGS.value)
    return session.post( login.URL+ PerceptionEndPoint.SETTINGS.value,json=request_body)

def get_underlay_map(session :requests.Session) -> requests.Response:
    return session.get( login.URL + PerceptionEndPoint.UNDERLAY_MAP.value)

def set_underlay_map(session : requests.Session,body_path) -> requests.Response:
    with open(body_path,'rt') as file:
        request_body = json.load(file)
    return session.post( login.URL + PerceptionEndPoint.UNDERLAY_MAP.value ,json = request_body)

def get_underlay_config(session :requests.Session) -> requests.Response:
    return session.get( login.URL + PerceptionEndPoint.UNDERLAY_CONFIG.value)

def set_underlay_config(session : requests.Session,body_path: str) -> requests.Response:
    with open(body_path,'r') as file:
        request_body = json.load(file)
    return session.post(login.URL + PerceptionEndPoint.UNDERLAY_CONFIG.value ,json=request_body)

def set_perception_current_profile(session : requests.Session,profile_name: str) -> requests.Response:
    """
    Description
    ----------- 
    sets the current prfile by name
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    profile_name: str
        the required profile name to be set.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    if isinstance(profile_name,str):
        return session.put( login.URL + PerceptionEndPoint.SET_PROFILE.value + profile_name)
    else:
        raise TypeError('profile must be string')
        
def get_perception_profile_by_name(session : requests.Session,profile_name : str) -> requests.Response:
    """
    Description
    ----------- 
    get the settings for the profile_name.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    profile_name: str
        profile name.

    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    if isinstance(profile_name,str):
        return session.get( login.URL + PerceptionEndPoint.GET_PROFILE.value + profile_name)
    else:
        raise TypeError('profile must be string')
    

def add_perception_profile(session : requests.Session,body_path : str,profile_name: str) ->requests.Response:
    """
    Description
    ----------- 
    add/update settings profile.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    body_path: str
        the path for the file with the requited settings.
    profile_name: str
        the name of the added profile.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    with open(body_path,'r') as file:
        request_body = json.load(file)
    return session.put( login.URL + PerceptionEndPoint.GET_PROFILE.value + profile_name,json=request_body)

def remove_perception_profile(session : requests.Session ,profile_name : str) -> requests.Response:
    """
    Description
    ----------- 
    delete settings profile.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    profile_name: str
        the name of the needed profile.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.delete( login.URL + PerceptionEndPoint.GET_PROFILE.value + profile_name)

def get_perception_profile_defaults(session : requests.Session , profile_name: str):
    return session.get( login.URL+ PerceptionEndPoint.DEFAULT_PROFILE.value + profile_name)

def get_perception_profile_list(session :requests.Session) -> requests.Response:
    """
    Description
    ----------- 
    get all list of profiles.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    return session.get( login.URL + PerceptionEndPoint.LIST_PROFILES.value)

def restore_to_defaults(session : requests.Session ,profile_name:str):
    """
    Description
    ----------- 
    restores the profile to default values.
    
    Args
    ----
    session: requests.Session 
        a request session for HTTP requests.
    profile_name: str
        the name of the added profile.
    
    Returns
    -------
    requests.Response
        Response object, which contains a server's response to an HTTP request.
    """
    if isinstance(profile_name,str):
        return session.put( login.URL + PerceptionEndPoint.RESTORE_PROFILE.value  + profile_name)
    else:
        raise TypeError('profile must be string')
        




if __name__ == '__main__':


    session = login.login_ouster()
    print(set_perception_setting(session,body_path='/home/aymanlinux/ouster/ousterenv/ousterrepo/perception_config.json').reason)





