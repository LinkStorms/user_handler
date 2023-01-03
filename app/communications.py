import requests

from utilities import get_data_layer_url


def login(username, password, data_layer_url=get_data_layer_url()):
    url = f"{data_layer_url}/login"
    payload = {"username": username, "password": password}
    response = requests.post(url, json=payload)
    return response.json()
