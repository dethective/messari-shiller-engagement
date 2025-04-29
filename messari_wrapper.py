
import pandas as pd
import requests
import time
from parameters import MESSARI_PREMIUM_KEY, BASE_URL



def fetch_all_users(max_users=20000, per_page=2000) -> pd.DataFrame:
    """
        Fetch all users from the Messari API. Useful to detect user tracked by the API
        and to get the list of all users.
        Args:
            max_users (int): The maximum number of users to fetch. Default is 20000.
            per_page (int): The number of users to fetch per page. Default is 2000.
        Returns:
            pd.DataFrame: A DataFrame containing all users.
    """
    
    all_users = []
    page = 1

    full_url = f'{BASE_URL}signal/v0/x-users'

    
    while len(all_users) < max_users:
        HEADERS = {
            "accept": "application/json",
            "x-messari-api-key": MESSARI_PREMIUM_KEY,
            "accountType": 'individual',
            "sort": 'followers',
            "page": f"{page}",
            "limit": f"{per_page}",
        }
        
        response = requests.get(full_url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"Error on page {page}: {response.status_code}")
            break
            
        data = response.json()
        if not data:  # If no more data is returned
            break
        
        df_user = pd.DataFrame(data['data'])
        all_users.append(df_user)
        print(f"Fetched page {page}, total users so far: {df_user.shape[0]}")
        
        page += 1
        time.sleep(1)  # Add a small delay to be respectful to the API
        
        if (page * per_page) >= max_users:
            all_users = all_users[:max_users]
            break

    # Concatenate all the dataframes into one
    all_users = pd.concat(all_users, ignore_index=True)
    
    return all_users


def fetch_user_engagement(identifier, start_date=None, end_date=None) -> pd.DataFrame:
    """
    Fetches user engagement data for a given identifier.

    :param identifier: The identifier of the user (e.g., '@Cobratate')
    :param start_date: The start date for the engagement data (format: 'YYYY-MM-DD')
    :param end_date: The end date for the engagement data (format: 'YYYY-MM-DD')
    :return: Engagement data as a JSON object
    """

    HEADERS = {
        "accept": "application/json",
        "x-messari-api-key": MESSARI_PREMIUM_KEY,
    }

    if start_date and end_date:
        HEADERS['start'] = start_date
        HEADERS['end'] = end_date

    full_url = f'{BASE_URL}signal/v0/x-users/{identifier}/time-series/engagement/1d'
    
    response = requests.get(full_url, headers=HEADERS)
    
    if response.status_code == 200:
        ts_engagement = response.json()['data']
        df = pd.DataFrame(ts_engagement['points'])
        df.columns = ['timestamp', 'engagement']
        df.timestamp = pd.to_datetime(df['timestamp'], unit='s')
        df['username'] = identifier
        df['engagement'] = df['engagement'].astype(float)
        return df
    else:
        print(f"Error fetching engagement data for {identifier}: {response.status_code}")
        return None
    
def fetch_user_mindshare(identifier, start_date=None, end_date=None):
    
    HEADERS = {
        "accept": "application/json",
        "x-messari-api-key": MESSARI_PREMIUM_KEY,
    }

    if start_date and end_date:
        HEADERS['start'] = start_date
        HEADERS['end'] = end_date

    full_url = f'{BASE_URL}signal/v0/x-users/{identifier}/time-series/mindshare/1d'

    response = requests.get(full_url, headers=HEADERS)

    if response.status_code == 200:
        ts_engagement = response.json()['data']
        df = pd.DataFrame(ts_engagement['points'])
        df.columns = ['timestamp', 'rank', 'mindshare']
        df.timestamp = pd.to_datetime(df['timestamp'], unit='s')
        df['username'] = identifier
        return df
    else:
        print(f"Error fetching engagement data for {identifier}: {response.status_code}")
        return None
    
def get_user_by_id(id):

    """
    Fetches user data by ID from the Messari API.

    :param id: The ID of the user
    :return: User data as a JSON object
    """
    
    HEADERS = {
        "accept": "application/json",
        "x-messari-api-key": MESSARI_PREMIUM_KEY,
    }

    full_url = f'{BASE_URL}signal/v0/x-users/{id}'
    
    response = requests.get(full_url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching user data for ID {id}: {response.status_code}")
        return None

