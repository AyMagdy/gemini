import pandas as pd
import numpy as np
import typing

def get_vel_df(data_dict:dict)->pd.DataFrame:
    """ Description:
            a helper funtion to iterate over the the time stamps being recieved from stream
            and converts the specified element (velocity) to a dataframe
        Args:
            :data_dict: the recieved object list after time stamped
        Returns:
            pandas DataFrame
    """
    vel = {}
    for key in data_dict.keys():
        vel.update({key:data_dict[str(key)]['velocity']})
    return pd.DataFrame(vel)


def get_pos_df(data_dict:dict)->pd.DataFrame:
    """ Description:
            a helper funtion to iterate over the the time stamps being recieved from stream
            and converts the specified element (position) to a dataframe
        Args:
            :data_dict: the recieved object list after time stamped
        Returns:
            pandas DataFrame
    """
    pos = {}
    for key in data_dict.keys():
        pos.update({key:data_dict[str(key)]['position']})
    return pd.DataFrame(pos)

def get_hed_df(data_dict:dict)->pd.DataFrame:
    """ Description:
            a helper funtion to iterate over the the time stamps being recieved from stream
            and converts the specified element (heading) to a dataframe
        Args:
            :data_dict: the recieved object list after time stamped
        Returns:
            pandas DataFrame
    """
    hed = {}
    for key in data_dict.keys():
        hed.update({key:data_dict[str(key)]['heading']})
    return pd.DataFrame(hed)

def get_dis_from_sensor(data_dict:dict)->pd.DataFrame:
    """ Description:
            a helper funtion to iterate over the the time stamps being recieved from stream
            and converts the specified element (distance from sensor) to a dataframe
        Args:
            :data_dict: the recieved object list after time stamped
        Returns:
            pandas DataFrame
    """
    dis = {}
    for key in data_dict.keys():
        dis.update({key:data_dict[str(key)]['distance_to_primary_sensor']})
    return pd.DataFrame(dis)

def get_nearest_from_sensor(dataframe:pd.DataFrame,stamp:str)->pd.Series:
    """ Description:
            this function find the nearest two objects from the senosr.
        Args:
            :dataframe: the dataframe related to the distance from the sensor.
            :stamp: the time stamp or the column in the data frame to search in it.
        Returns:
            series with the values of the distances
    """
    return dataframe[stamp].nsmallest(2)

def calc_vel_mag_diff(dataframe:pd.DataFrame,stamp:int,index1:int,index2:int)-> np.floating:
    """ Description:
            a helper function to be called to calculate the velocity norm between two objects at a specific time stamp.
        Args:
            dataframe: velocity dataframe to get the difference.
            stamp:     the required time stamp.
            index1:    the first index/row in the dataframe required.
            index2:    the second index/row in the dataframe required.
        
        Returns:
            pandas series of the calculated velocity norm between index1 and index2      
    """
    val = dict(dataframe.iloc[[index1,index2],stamp])
    vector1 = val[0]
    vector2 = val[1]
    vector1_arr = np.array(list(vector1[key] for key in vector1))
    vector2_arr = np.array(list(vector2[key] for key in vector2))
    difference = vector1_arr - vector2_arr
    norm = np.linalg.norm(difference)
    return norm

def calc_pos_mag_diff(dataframe:pd.DataFrame,stamp:int,index1:int,index2:int)-> np.floating:
    """ Description:
            a helper function to be called to calculate the position difference between two rows from the passed dataframe.
        Args:
            dataframe: positon dataframe to get the difference.
            stamp:     the required time stamp. 
            index1:    the first index/row in the dataframe required.
            index2:    the second index/row in the dataframe required.
        
        Returns:
            pandas series of the calculated position norm between index1 and index2. 
    """
    val = dict(dataframe.iloc[[index1,index2],stamp])
    vector1 = val[0]
    vector2 = val[1]
    vector1_arr = np.array(list(vector1[key] for key in vector1))
    vector2_arr = np.array(list(vector2[key] for key in vector2))
    difference = vector1_arr - vector2_arr
    norm = np.linalg.norm(difference)
    return norm   

def time_to_col(vel:np.floating,pos:np.floating)->np.floating:
    """ Description: 
            calculates the time expected for two objects to collide.  
    """
    return pos/vel