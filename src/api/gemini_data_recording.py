
import requests
from bs4 import BeautifulSoup
import gemini_login
from enum import Enum



class DataEndPoint(Enum):
    """
    defines the endpoints of the url for more information refer to `ouster swagger api documentation <https://127.0.0.1/event/api/v1/swagger/ui>`_
    """
    JSON_BINARY_DATA_ENDPOINT= 'data/recordings/'
    AGGREGATION_DATA_ENDPOINT = 'data/storage/'


def json_binary_data(session: requests.Session) -> None:
    """
    Description
    -----------
    Function to get json data
    Writes saved files to data_rec_links.txt
    Open data_rec_links.txt and fetch for the required link to download.
    Write objects to data_rec_objects.json file.

    ARGs
    ----
    session: requests.Session
        an authorized HTTPS connection.
    
    Return
    ------
    None
    """
    html_response = session.get(gemini_login.URL + DataEndPoint.JSON_BINARY_DATA_ENDPOINT.value).text
    soup = BeautifulSoup(html_response.encode('utf-8'),'html.parser')
    
    # Write to a file all links saved
    with open('data_rec_links.txt','wt') as file:
        for link in soup.find_all('a'):
            data = link.get('href')
            file.write(data)
            file.write('\n')

    # Open a specifc link
    with open('data_rec_html_links.txt','rt') as file:
        text = file.readlines()
        text_index = text[1].replace('\n','')
        print(text_index)

    # Write the contents of a specific link
    with open('data_rec_objects.json','wt') as file:
        file.write(session.get(gemini_login.URL + DataEndPoint.JSON_BINARY_DATA_ENDPOINT.value+text_index).text)
    
def aggregation_data(session : requests.Session) -> None:
    """
    Description
    -----------
    Function to get aggregation data
    Fetch ‘/data/storage’
    save file to aggregation.txt.
    Download files and write it to
    ‘aggregation_total_visitors.json’
    ‘aggregation_total_visits.json


    ARGs
    ----
    session: requests.Session
        an authorized HTTPS connection.
    
    Return
    ------
    None
    """
    # Goto aggregation data storage endpoint
    data = session.get(gemini_login.URL + DataEndPoint.AGGREGATION_DATA_ENDPOINT.value)
    # Parse response HTML body request
    html_body = data.text
    soup = BeautifulSoup(html_body,'html.parser')
    # write all html links in response body to file
    with open('aggregation.txt','wt') as file:
        for link in soup.find_all('a'):
            data = link.get('href')
            file.write(data)
            file.write('\n')
    # Read the lines of links file to a python list
    with open('aggregation.txt','rt') as file:
        lines = file.readlines()
    # Creat a file with all objects in the zone
    # there should be a file with real time events
    # and the other with time seriries event.
    with open('aggregation_total_visitors.json','wt') as file:
        file.write((session.get(gemini_login.URL + DataEndPoint.AGGREGATION_DATA_ENDPOINT.value + lines[1].replace('\n','')).text))
    with open('aggregation_total_visits.json','wt') as file:
        file.write((session.get(gemini_login.URL + DataEndPoint.AGGREGATION_DATA_ENDPOINT.value + lines[2].replace('\n','')).text))


if __name__ == '__main__':
    session = gemini_login.login_ouster()
    json_binary_data(session)
