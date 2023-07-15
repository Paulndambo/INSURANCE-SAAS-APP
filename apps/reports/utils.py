import requests

# Replace these values with your Metabase server information
METABASE_URL = 'https://metabase-nda-dev.click2sure.co.za'
METABASE_USERNAME = 'paul@click2sure.co.za'
METABASE_PASSWORD = 'reN5ZJd_PYnOUn'

# API endpoints
LOGIN_ENDPOINT = '/api/session'
DATABASES_ENDPOINT = '/api/database'
CARDS_ENDPOINT = '/api/card'

def get_metabase_token():
    # Get authentication token from Metabase using username and password
    login_payload = {
        'username': METABASE_USERNAME,
        'password': METABASE_PASSWORD
    }

    response = requests.post(METABASE_URL + LOGIN_ENDPOINT, json=login_payload)

    if response.status_code == 200:
        return response.json()['id']
    else:
        raise Exception("Failed to get Metabase authentication token.")


def get_databases(token):
    # Get a list of databases using the Metabase API
    headers = {
        'Content-Type': 'application/json',
        'X-Metabase-Session': token
    }

    response = requests.get(METABASE_URL + DATABASES_ENDPOINT, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch databases from Metabase API.")


def get_all_cards(token):
    # Get all cards (questions) using the Metabase API
    headers = {
        'Content-Type': 'application/json',
        'X-Metabase-Session': token
    }

    response = requests.get(METABASE_URL + CARDS_ENDPOINT, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch cards from Metabase API.")


def get_card_data(token, card_id):
    # Get data from a specific card (question) using the Metabase API
    CARD_QUERY_ENDPOINT = f'/api/card/{card_id}/query/json'
    headers = {
        'Content-Type': 'application/json',
        'X-Metabase-Session': token
    }

    card_query_url = METABASE_URL + CARD_QUERY_ENDPOINT
    response = requests.post(card_query_url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(response.text)
